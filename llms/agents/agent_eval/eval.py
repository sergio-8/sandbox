
import os

from dotenv import load_dotenv
import vertexai
import random
import string

from IPython.display import HTML, Markdown, display

# Build agent
from google.cloud import aiplatform
import pandas as pd
import plotly.graph_objects as go
from vertexai import agent_engines

# Evaluate agent
from vertexai.preview.evaluation import EvalTask
from vertexai.preview.evaluation.metrics import (
    PointwiseMetric,
    PointwiseMetricPromptTemplate,
    TrajectorySingleToolUse,
)
from vertexai.preview.reasoning_engines import LangchainAgent





load_dotenv()
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
BUCKET_NAME = os.getenv("BUCKET_NAME")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")
BUCKET_URI = f"gs://{BUCKET_NAME}"


"""

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=os.getenv("GOOGLE_CLOUD_LOCATION"))


if __name__ == "__main__":
    try:
        print(f"Vertex AI project: {PROJECT_ID}")
        print(f"Vertex AI location: {os.getenv('GOOGLE_CLOUD_LOCATION')}")
        print(f"Bucket URI: {BUCKET_URI}")
    except Exception as e:
        print(f"Error during initialization: {e}")

"""

EXPERIMENT_NAME = "evaluate-re-agent"  # @param {type:"string"}

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=BUCKET_URI,
    experiment=EXPERIMENT_NAME,
)



def get_id(length: int = 8) -> str:
    """Generate a uuid of a specified length (default=8)."""
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def display_eval_report(eval_result: pd.DataFrame) -> None:
    """Display the evaluation results."""
    metrics_df = pd.DataFrame.from_dict(eval_result.summary_metrics, orient="index").T
    display(Markdown("### Summary Metrics"))
    display(metrics_df)

    display(Markdown(f"### Row-wise Metrics"))
    display(eval_result.metrics_table)


def display_drilldown(row: pd.Series) -> None:
    """Displays a drill-down view for trajectory data within a row."""

    style = "white-space: pre-wrap; width: 800px; overflow-x: auto;"

    if not (
        isinstance(row["predicted_trajectory"], list)
        and isinstance(row["reference_trajectory"], list)
    ):
        return

    for predicted_trajectory, reference_trajectory in zip(
        row["predicted_trajectory"], row["reference_trajectory"]
    ):
        display(
            HTML(
                f"Tool Names:{predicted_trajectory['tool_name'], reference_trajectory['tool_name']}"
            )
        )

        if not (
            isinstance(predicted_trajectory.get("tool_input"), dict)
            and isinstance(reference_trajectory.get("tool_input"), dict)
        ):
            continue

        for tool_input_key in predicted_trajectory["tool_input"]:
            print("Tool Input Key: ", tool_input_key)

            if tool_input_key in reference_trajectory["tool_input"]:
                print(
                    "Tool Values: ",
                    predicted_trajectory["tool_input"][tool_input_key],
                    reference_trajectory["tool_input"][tool_input_key],
                )
            else:
                print(
                    "Tool Values: ",
                    predicted_trajectory["tool_input"][tool_input_key],
                    "N/A",
                )
        print("\n")
    display(HTML(""))


def display_dataframe_rows(
    df: pd.DataFrame,
    columns: list[str] | None = None,
    num_rows: int = 3,
    display_drilldown: bool = False,
) -> None:
    """Displays a subset of rows from a DataFrame, optionally including a drill-down view."""

    if columns:
        df = df[columns]

    base_style = "font-family: monospace; font-size: 14px; white-space: pre-wrap; width: auto; overflow-x: auto;"
    header_style = base_style + "font-weight: bold;"

    for _, row in df.head(num_rows).iterrows():
        for column in df.columns:
            display(
                HTML(
                    f"{column.replace('_', ' ').title()}: "
                )
            )
            display(HTML(f"{row[column]}"))

        display(HTML(""))

        if (
            display_drilldown
            and "predicted_trajectory" in df.columns
            and "reference_trajectory" in df.columns
        ):
            display_drilldown(row)


def plot_bar_plot(
    eval_result: pd.DataFrame, title: str, metrics: list[str] = None
) -> None:
    fig = go.Figure()
    data = []

    summary_metrics = eval_result.summary_metrics
    if metrics:
        summary_metrics = {
            k: summary_metrics[k]
            for k, v in summary_metrics.items()
            if any(selected_metric in k for selected_metric in metrics)
        }

    data.append(
        go.Bar(
            x=list(summary_metrics.keys()),
            y=list(summary_metrics.values()),
            name=title,
        )
    )

    fig = go.Figure(data=data)

    # Change the bar mode
    fig.update_layout(barmode="group")
    fig.show()


def display_radar_plot(eval_results, title: str, metrics=None):
    """Plot the radar plot."""
    fig = go.Figure()
    summary_metrics = eval_results.summary_metrics
    if metrics:
        summary_metrics = {
            k: summary_metrics[k]
            for k, v in summary_metrics.items()
            if any(selected_metric in k for selected_metric in metrics)
        }

    min_val = min(summary_metrics.values())
    max_val = max(summary_metrics.values())

    fig.add_trace(
        go.Scatterpolar(
            r=list(summary_metrics.values()),
            theta=list(summary_metrics.keys()),
            fill="toself",
            name=title,
        )
    )
    fig.update_layout(
        title=title,
        polar=dict(radialaxis=dict(visible=True, range=[min_val, max_val])),
        showlegend=True,
    )
    fig.show()

    def get_product_details(product_name: str):
        """Gathers basic details about a product."""
        details = {
            "smartphone": "A cutting-edge smartphone with advanced camera features and lightning-fast processing.",
            "usb charger": "A super fast and light usb charger",
            "shoes": "High-performance running shoes designed for comfort, support, and speed.",
            "headphones": "Wireless headphones with advanced noise cancellation technology for immersive audio.",
            "speaker": "A voice-controlled smart speaker that plays music, sets alarms, and controls smart home devices.",
        }
        return details.get(product_name, "Product details not found.")

    def get_product_price(product_name: str):
        """Gathers price about a product."""
        details = {
            "smartphone": 500,
            "usb charger": 10,
            "shoes": 100,
            "headphones": 50,
            "speaker": 80,
        }
        return details.get(product_name, "Product price not found.")

    model = "gemini-2.0-flash"

    local_1p_agent = LangchainAgent(
        model=model,
        tools=[get_product_details, get_product_price],
        agent_executor_kwargs={"return_intermediate_steps": True},
    )

    response = local_1p_agent.query(input="Get product details for shoes")
    display(Markdown(response["output"]))

    response = local_1p_agent.query(input="Get product price for shoes")
    display(Markdown(response["output"]))

    remote_1p_agent = agent_engines.create(
        local_1p_agent,
        requirements=[
            "google-cloud-aiplatform[agent_engines,langchain]",
            "langchain_google_vertexai",
            "cloudpickle==3.0.0",
            "pydantic>=2.10",
            "requests",
        ],
    )

    response = remote_1p_agent.query(input="Get product details for shoes")
    print(response["output"])

    eval_data = {
        "prompt": [
            "Get price for smartphone",
            "Get product details and price for headphones",
            "Get details for usb charger",
            "Get product details and price for shoes",
            "Get product details for speaker?",
        ],
        "reference_trajectory": [
            [
                {
                    "tool_name": "get_product_price",
                    "tool_input": {"product_name": "smartphone"},
                }
            ],
            [
                {
                    "tool_name": "get_product_details",
                    "tool_input": {"product_name": "headphones"},
                },
                {
                    "tool_name": "get_product_price",
                    "tool_input": {"product_name": "headphones"},
                },
            ],
            [
                {
                    "tool_name": "get_product_details",
                    "tool_input": {"product_name": "usb charger"},
                }
            ],
            [
                {
                    "tool_name": "get_product_details",
                    "tool_input": {"product_name": "shoes"},
                },
                {"tool_name": "get_product_price", "tool_input": {"product_name": "shoes"}},
            ],
            [
                {
                    "tool_name": "get_product_details",
                    "tool_input": {"product_name": "speaker"},
                }
            ],
        ],
    }

    eval_sample_dataset = pd.DataFrame(eval_data)

    display_dataframe_rows(eval_sample_dataset, num_rows=3)

    single_tool_usage_metrics = [TrajectorySingleToolUse(tool_name="get_product_price")]

    EXPERIMENT_RUN = f"single-metric-eval-{get_id()}"

    single_tool_call_eval_task = EvalTask(
        dataset=eval_sample_dataset,
        metrics=single_tool_usage_metrics,
        experiment=EXPERIMENT_NAME,
    )

    single_tool_call_eval_result = single_tool_call_eval_task.evaluate(
        runnable=remote_1p_agent, experiment_run_name=EXPERIMENT_RUN
    )

    display_eval_report(single_tool_call_eval_result)

    display_dataframe_rows(single_tool_call_eval_result.metrics_table, num_rows=3)