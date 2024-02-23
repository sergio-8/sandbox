
from google.api_core.client_options import ClientOptions
from google.cloud import documentai  # type: ignore
print('this worked! 1')

# TODO(developer): Uncomment these variables before running the sample.
# project_id = "YOUR_PROJECT_ID"
# location = "YOUR_PROCESSOR_LOCATION"  # Format is "us" or "eu"
# file_path = "/path/to/local/pdf"
# processor_display_name = "YOUR_PROCESSOR_DISPLAY_NAME" # Must be unique per project, e.g.: "My Processor"
project_id = "412996116194"
location = "us"  # Format is "us" or "eu"
processor_id = "66ecef3533517e2f" # Create processor before running sample
#file_path = "/Users/sergiovillani/Downloads/1010733_BPO_REDACTED.puppa"
file_path = "/Users/sergiovillani/Desktop/cacioppo.png"

processor_display_name = "auction_test" # Must be unique per project, e.g.: "My Processor"
print('this worked! 2')

#mime_type = "pdf" # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
#field_mask = "text,entities,pages.pageNumber"  # Optional. The fields to return in the Document object.
print('this worked!3')
def quickstart(
    project_id: str,
    location: str,
    file_path: str,

    processor_display_name: str = "My Processor",
):
    # You must set the `api_endpoint`if you use a location other than "us".
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    print('this worked!4'),
    # The full resource name of the location, e.g.:
    # `projects/{project_id}/locations/{location}`
    parent = client.common_location_path(project_id, location)
    print('this worked!5')


    # Create a Processor
    processor = client.create_processor(
        parent=parent,
        processor=documentai.Processor(
            type_="OCR_PROCESSOR",  # Refer to https://cloud.google.com/document-ai/docs/create-processor for how to get available processor types
            display_name=processor_display_name,
        ),
    )


    # Print the processor information
    print(f"Processor Name: {processor.name}")
    print ('this worked!')

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load binary data
    raw_document = documentai.RawDocument(
        content=image_content,
        mime_type="application/pdf",  # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
    )

    # Configure the process request
    # `processor.name` is the full resource name of the processor, e.g.:
    # `projects/{project_id}/locations/{location}/processors/{processor_id}`
    request = documentai.ProcessRequest(name=processor.name, raw_document=raw_document)

    result = client.process_document(request=request)

    # For a full list of `Document` object attributes, reference this page:
    # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
    document = result.document

    # Read the text recognition output from the processor
    print("The document contains the following text:")
    print(document.text, "cippalippa")



quickstart(project_id,location,file_path)