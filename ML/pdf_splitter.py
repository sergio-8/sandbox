from google.cloud.documentai_toolbox import document

# TODO(developer): Uncomment these variables before running the sample.
# Given a local document.json or sharded document.json from a splitter/classifier in path
document_path: str = "/Users/sergiovillani/code/sandbox/ML/document.json"
pdf_path = "/Users/XXXXXXXX/Downloads/1010733_BPO_REDACTED.pdf"

output_path = "/Users/XXXXXX/code/sandbox/ML/docai_ouput/"


def split_pdf_sample(document_path: str, pdf_path: str, output_path: str) -> None:
    wrapped_document = document.Document.from_document_path(document_path=document_path)

    output_files = wrapped_document.split_pdf(
        pdf_path=pdf_path, output_path=output_path
    )

    print("Document Successfully Split")
    for output_file in output_files:
        print(output_file)



split_pdf_sample(document_path=document_path, pdf_path=pdf_path, output_path=output_path)
