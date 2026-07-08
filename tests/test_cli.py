import subprocess
import sys

from app import cli


def test_cli_mock_analyze_prints_summary(capsys):
    exit_code = cli.main(
        [
            "analyze",
            "examples/sample_contract.txt",
            "--analysis-type",
            "Contract Review",
            "--mock",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Legal Agent Analysis" in captured.out
    assert "Mock analysis generated without external API calls." in captured.out
    assert "Questions for a Qualified Legal Professional" in captured.out


def test_cli_mock_analyze_accepts_custom_query(capsys):
    exit_code = cli.main(
        [
            "analyze",
            "examples/sample_contract.txt",
            "--analysis-type",
            "Custom Query",
            "--custom-query",
            "Find termination language.",
            "--mock",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Analysis type: Custom Query" in captured.out


def test_cli_subprocess_module_invocation_runs_in_mock_mode():
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "app.cli",
            "analyze",
            "examples/sample_contract.txt",
            "--mock",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert "Legal Agent Analysis" in completed.stdout
    assert "without external API calls" in completed.stdout
