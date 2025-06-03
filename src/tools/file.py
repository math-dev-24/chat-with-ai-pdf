import os
from pathlib import Path

def get_pdf_files(base_path: Path, extensions : list[str]) -> list[Path]:
    """
    :param base_path: Path de base
    :param extensions: les extensions à prendre en charge
    :return: list de path des fichiers
    """
    print(f"🔍 Search in {base_path}")

    result_files: list[Path] = []

    for root, _, files in os.walk(base_path):
        root_path = Path(root)

        for file in files:
            file_extension = file.lower().split('.')[-1]
            if file_extension in extensions:
                file_path = root_path / file
                result_files.append(file_path)

    print(f"🗃️ Found {len(result_files)} files")

    return result_files
