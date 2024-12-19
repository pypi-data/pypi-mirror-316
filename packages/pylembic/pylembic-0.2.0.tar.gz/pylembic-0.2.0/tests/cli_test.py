from pytest import fixture
from typer.testing import CliRunner
from pylembic.cli import app

runner = CliRunner()


@fixture
def valid_migrations_path(tmp_path):
    """Creates a temporary directory for valid migrations."""
    migrations_path = tmp_path / "migrations"
    migrations_path.mkdir()
    # Simulate valid migrations setup
    (migrations_path / "env.py").write_text("env content")
    (migrations_path / "script.py.mako").write_text("script content")
    (migrations_path / "version1.py").write_text("version 1 content")
    return str(migrations_path)


@fixture
def invalid_migrations_path(tmp_path):
    """Creates a temporary directory for invalid migrations."""
    migrations_path = tmp_path / "migrations"
    migrations_path.mkdir()
    # Simulate missing or invalid migrations setup
    (migrations_path / "env.py").write_text("env content")
    return str(migrations_path)


def test_validate_valid_migrations(valid_migrations_path, mocker):
    """Test --validate with valid migrations."""
    mock_validate = mocker.patch(
        "pylembic.migrations.Validator.validate", return_value=True
    )

    result = runner.invoke(app, [valid_migrations_path, "--validate"])

    assert result.exit_code == 0
    assert "Validating migrations..." in result.output
    assert "Migrations validation passed!" in result.output
    mock_validate.assert_called_once()


def test_validate_invalid_migrations(invalid_migrations_path, mocker):
    """Test --validate with invalid migrations."""
    mock_validate = mocker.patch(
        "pylembic.migrations.Validator.validate", return_value=False
    )

    result = runner.invoke(app, [invalid_migrations_path, "--validate"])

    assert result.exit_code == 0
    assert "Validating migrations..." in result.output
    assert "Migrations validation failed!" in result.output
    mock_validate.assert_called_once()


def test_show_graph(valid_migrations_path, mocker):
    """Test --show-graph to visualize the graph."""
    mock_visualize = mocker.patch("pylembic.migrations.Validator.show_graph")

    result = runner.invoke(app, [valid_migrations_path, "--show-graph"])

    assert result.exit_code == 0
    assert "Visualizing migration graph..." in result.output
    mock_visualize.assert_called_once()


def test_no_action(valid_migrations_path):
    """Test when no action is specified."""
    result = runner.invoke(app, [valid_migrations_path])

    assert result.exit_code == 0
    assert "No action specified. Use --help for more information." in result.output


def test_invalid_path():
    """Test when an invalid migrations path is provided."""
    result = runner.invoke(app, ["/invalid/path", "--validate"])

    assert result.exit_code != 0
    assert "Processing migrations in: /invalid/path" in result.output
