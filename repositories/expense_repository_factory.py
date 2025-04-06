from config.repository_config import RepositoryConfig
from repositories.db_expense_repository import (
    BaseExpenseRepository,
    DbExpenseRepository,
)
from repositories.expense_repository import ExpenseRepository
from repositories.google_sheets_expense_repository import GoogleSheetsExpenseRepository


class ExpenseRepositoryFactory:
    @staticmethod
    def create(config: RepositoryConfig) -> BaseExpenseRepository:
        if config.storage_type == "json":
            return ExpenseRepository(config.directory_path, config.file_name)
        elif config.storage_type == "sheets":
            return GoogleSheetsExpenseRepository(
                config.sheet_id, config.credentials_path
            )
        elif config.storage_type == "db":
            return DbExpenseRepository(config.db_url)
        else:
            raise ValueError(f"지원하지 않는 저장 방식: {config.storage_type}")
