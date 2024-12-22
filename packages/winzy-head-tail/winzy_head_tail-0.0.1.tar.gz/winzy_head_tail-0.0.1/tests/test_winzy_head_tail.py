import pytest
import winzy_head_tail as w

import subprocess
import sys
from io import StringIO

from winzy_head_tail.head import head, head_command
from winzy_head_tail.tail import tail, tail_command

from argparse import ArgumentParser


def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser_head(subparser)

    assert parser is not None

    result = parser.parse_args(["hello"])
    assert result.files == ["hello"]


def test_plugin(capsys):
    w.head_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``winzy`` plugin." in captured.out


@pytest.fixture
def test_files(tmp_path):
    """Fixture to create temporary test files."""
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"

    file1.write_text("line1\nline2\nline3\nline4\nline5\n")
    file2.write_text("alpha\nbeta\ngamma\ndelta\nepsilon\n")

    return file1, file2


def test_head_function(test_files):
    file1, _ = test_files

    # Test head function
    output = StringIO()
    sys.stdout = output
    head(filename=str(file1), n=3)
    sys.stdout = sys.__stdout__
    assert output.getvalue() == "line1\nline2\nline3\n"


def test_tail_function(test_files):
    file1, _ = test_files

    # Test tail function
    output = StringIO()
    sys.stdout = output
    tail(filename=str(file1), n=3)
    sys.stdout = sys.__stdout__
    assert output.getvalue() == "line3\nline4\nline5\n"


def test_head_command(test_files):
    file1, file2 = test_files

    # Test multiple files with head_command
    output = StringIO()
    sys.stdout = output
    head_command(filenames=[str(file1), str(file2)], n=2)
    sys.stdout = sys.__stdout__

    assert f"==> {file1} <==\nline1\nline2\n\n" in output.getvalue()
    assert f"==> {file2} <==\nalpha\nbeta\n\n" in output.getvalue()


def test_tail_command(test_files):
    file1, file2 = test_files

    # Test multiple files with tail_command
    output = StringIO()
    sys.stdout = output
    tail_command(filenames=[str(file1), str(file2)], n=2)
    sys.stdout = sys.__stdout__

    assert f"==> {file1} <==\nline4\nline5\n\n" in output.getvalue()
    assert f"==> {file2} <==\ndelta\nepsilon\n\n" in output.getvalue()


@pytest.mark.xfail
def test_head_with_piped_input():
    input_data = "line1\nline2\nline3\nline4\nline5\n"
    expected_output = "line1\nline2\nline3\n"

    # Run head.py with piped input
    result = subprocess.run(
        [sys.executable, "head.py", "-n", "3"],
        input=input_data,
        text=True,
        capture_output=True,
    )
    assert result.stdout == expected_output


@pytest.mark.xfail
def test_tail_with_piped_input():
    input_data = "line1\nline2\nline3\nline4\nline5\n"
    expected_output = "line3\nline4\nline5\n"

    # Run tail.py with piped input
    result = subprocess.run(
        [sys.executable, "tail.py", "-n", "3"],
        input=input_data,
        text=True,
        capture_output=True,
    )
    assert result.stdout == expected_output
