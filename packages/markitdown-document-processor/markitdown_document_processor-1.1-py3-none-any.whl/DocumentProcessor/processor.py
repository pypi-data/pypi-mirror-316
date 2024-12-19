import os
from markitdown import MarkItDown

class DocumentProcessor:
    def __init__(self, doc_folder='docs', output_folder='processed_files'):
        self.doc_folder = doc_folder
        self.output_folder = output_folder
        self.markitdown = MarkItDown()
        self.create_output_folder()

    def create_output_folder(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def process_documents(self):
        for filename in os.listdir(self.doc_folder):
            file_path = os.path.join(self.doc_folder, filename)
            if os.path.isfile(file_path):  # Check if it's a file, not a subfolder
                result = self.markitdown.convert(file_path)
                markdown_filename = os.path.splitext(filename)[0] + '.md'
                markdown_file_path = os.path.join(self.output_folder, markdown_filename)
                with open(markdown_file_path, 'w', encoding='utf-8') as f:
                    f.write(result.text_content)
                print(f"Converted {filename} to {markdown_filename}")

if __name__ == '__main__':
    processor = DocumentProcessor()
    processor.process_documents()