from pathlib import Path


class FileReader:    
    def __init__(self, file_path: str = "file.db"):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
    
    def read(self, offset: int, size: int) -> bytes:
        with open(self.file_path, 'rb') as f:
            f.seek(offset)
            return f.read(size)