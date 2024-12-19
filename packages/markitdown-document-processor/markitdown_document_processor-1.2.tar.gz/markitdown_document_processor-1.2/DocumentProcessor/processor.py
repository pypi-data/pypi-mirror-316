import pathlib
import os
import argparse
from markitdown import MarkItDown

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Document processor")
    parser.add_argument("-i", "--input_folder", help="Path to the input folder", required=True)
    parser.add_argument("-o", "--output_folder", help="Path to the output folder", required=True)
    return parser.parse_args()

class DocumentProcessor:
    def __init__(self, input_folder: str, output_folder: str):
        self.input_folder = pathlib.Path(input_folder)
        self.output_folder = pathlib.Path(output_folder)
        self.markitdown = MarkItDown()
        self.create_output_folder()

    def create_output_folder(self) -> None:
        self.output_folder.mkdir(parents=True, exist_ok=True)

    def process_documents(self) -> None:
        for file_path in self.input_folder.glob('*'):
            if file_path.is_file():
                result = self.markitdown.convert(str(file_path))
                markdown_filename = f"{file_path.stem}.md"
                markdown_file_path = self.output_folder / markdown_filename
                with open(markdown_file_path, 'w', encoding='utf-8') as f:
                    f.write(result.text_content)
                print(f"Converted {file_path.name} to {markdown_filename}")

def main() -> None:
    args = parse_args()
    processor = DocumentProcessor(args.input_folder, args.output_folder)
    processor.process_documents()

if __name__ == '__main__':
    main()