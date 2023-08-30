import os

from click.testing import CliRunner

from tbt.cli import main, prep, run


def fixture_project_dir():
    return os.path.join(os.path.dirname(__file__), "fixture_project")


def test_main():
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0, result.output
    assert "Usage:" in result.output


def test_prep():
    runner = CliRunner()
    result = runner.invoke(prep, ["--dir", fixture_project_dir()])
    assert result.exit_code == 0, result.output


def test_run():
    runner = CliRunner()
    result = runner.invoke(run, ["--dir", fixture_project_dir()])
    assert result.exit_code == 0, result.output
