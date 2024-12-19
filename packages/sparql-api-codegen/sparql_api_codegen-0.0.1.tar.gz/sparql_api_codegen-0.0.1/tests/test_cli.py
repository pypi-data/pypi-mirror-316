from typer.testing import CliRunner

from sparql_api_codegen.__main__ import cli

runner = CliRunner()


def test_cli():
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
