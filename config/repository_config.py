from dataclasses import dataclass
from typing import Optional


@dataclass
class RepositoryConfig:
    storage_type: str
    directory_path: Optional[str] = None
    file_name: Optional[str] = None
    sheet_id: Optional[str] = None
    credentials_path: Optional[str] = None
    db_url: Optional[str] = None
