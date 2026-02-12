import pytest
import tempfile
import os
from main import process_csv_files


@pytest.fixture
def test_csv_file():
    """Создаёт реальный CSV файл"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        f.write('Country,Year,GDP\n')
        f.write('USA,2024,25000\n')
        f.write('USA,2025,26000\n')
        f.write('Russia,2024,1800\n')
        path = f.name
    yield path
    os.unlink(path)


def test_process_csv_files_single_file(test_csv_file):
    """Тест одного файла"""
    result, header = process_csv_files([test_csv_file])

    assert isinstance(result, dict)
    assert len(result) >= 2  # Минимум 2 страны
    assert 'USA' in result
    assert result['USA'] == pytest.approx(25500.0, abs=1)


def test_process_csv_files_no_files():
    """Тест без файлов"""
    result, _ = process_csv_files([])
    assert result == {}


def test_process_csv_files_auto_find(tmp_path):
    """Тест автоопределения"""
    # Создаём пустую папку (нет CSV)
    os.chdir(tmp_path)
    result, _ = process_csv_files()
    assert result == {}
