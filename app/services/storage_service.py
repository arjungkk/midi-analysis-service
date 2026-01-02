import os
from uuid import uuid4


class StorageService:

    def __init__(self, base_path="data/uploads"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def save_file(self, filename: str, content: bytes) -> str:
        unique_name = f"{uuid4()}_{filename}"
        file_path = os.path.join(self.base_path, unique_name)

        with open(file_path, "wb") as f:
            f.write(content)

        return file_path