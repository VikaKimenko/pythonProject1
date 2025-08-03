from pathlib import Path

import pytest

from src.decorators import log


@pytest.fixture
def log_file(tmp_path: Path) -> Path:
    return tmp_path / "test.log"


def test_log_output(capsys: pytest.CaptureFixture[str], log_file: Path) -> None:
    # Тестируем запись в файл
    @log(filename=log_file)
    def file_logged(x: int) -> int:
        return x

    file_logged(1)
    with open(log_file, "r", encoding="utf-8") as f:
        assert f.read().strip() == "file_logged ok"

    # Тестируем вывод в консоль
    @log()
    def console_logged(x: int) -> int:
        return x

    console_logged(2)
    captured = capsys.readouterr()
    assert captured.out.strip() == "console_logged ok"


def test_error_handling(capsys: pytest.CaptureFixture[str]) -> None:
    @log()
    def error_func() -> None:
        raise ValueError("Test")

    with pytest.raises(ValueError):
        error_func()
    captured = capsys.readouterr()
    assert "error_func error: ValueError. Inputs: (), {}" in captured.out


def test_arguments(capsys: pytest.CaptureFixture[str]) -> None:
    @log()
    def args_func(a: int, b: int = 2) -> int:
        return a + b

    args_func(1, b=3)
    captured = capsys.readouterr()
    assert captured.out.strip() == "args_func ok"
