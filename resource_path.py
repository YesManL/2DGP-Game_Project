import os
import sys

def resource_path(relative_path):
    """PyInstaller로 빌드된 실행 파일에서 리소스 파일 경로를 올바르게 찾아줍니다."""
    try:
        # PyInstaller가 생성한 임시 폴더
        base_path = sys._MEIPASS
    except Exception:
        # 일반 Python 실행 환경
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

