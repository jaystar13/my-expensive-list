import os
from pathlib import Path
from typing import List

class FileUtils:
    """파일 및 디렉토리 관련 유틸리티 클래스"""

    @staticmethod
    def list_files(directory: str, full_path: bool = False) -> List[str]:
        """
        지정된 디렉토리의 파일 목록을 반환

        :param directory: 파일 목록을 조회할 디렉토리 경로
        :param full_path: True면 절대 경로, False면 파일명만 반환
        :return: 파일명 또는 절대 경로 목록
        """
        path = Path(directory)
        if not path.is_dir():
            raise ValueError(f"유효한 디렉토리가 아닙니다: {directory}")

        files = [f for f in os.listdir(directory) if (path / f).is_file()]
        return [str(path / f) if full_path else f for f in files]
