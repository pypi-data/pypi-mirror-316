A document processor that converts documents to Markdown using Microsoft markitdown package

Install the package
`pip install markitdown-document-processor`

Then, in your application code, you can import and use the DocumentProcessor class:

`from document_processor import DocumentProcessor
processor = DocumentProcessor()
documents = processor.process_documents()
print(documents)`

Make sure to create a docs directory in the same directory as your application code, and place your documents to be processed in this directory.
You should now see the Markdown files being created in the processed_documents folder
