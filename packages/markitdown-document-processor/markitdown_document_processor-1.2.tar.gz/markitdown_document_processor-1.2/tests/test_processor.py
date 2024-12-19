import unittest
from document_processor.processor import DocumentProcessor

class TestDocumentProcessor(unittest.TestCase):
    def test_process_documents(self):
        processor = DocumentProcessor()
        documents = processor.process_documents()
        self.assertGreater(len(documents), 0)

if __name__ == '__main__':
    unittest.main()