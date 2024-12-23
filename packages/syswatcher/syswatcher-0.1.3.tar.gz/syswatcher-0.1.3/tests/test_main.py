from typer.testing import CliRunner
from src.main import app

runner = CliRunner()

def test_hi():
    result = runner.invoke(app, ["hi"])
    assert result.exit_code == 0
    assert "hi world" in result.output

def test_info():
    result = runner.invoke(app, ["info"])
    assert result.exit_code == 0
    assert "some info" in result.output

def test_mrinaal():
    result = runner.invoke(app, ["mrinaal"])
    assert result.exit_code == 0
    assert "this cli app was made by mrinaal" in result.output