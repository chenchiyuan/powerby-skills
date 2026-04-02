from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import powerby.cli.acceptance_map as acceptance_map_cli
from tests.acceptance_map.helpers import make_ohlcv_payload


def test_cli_outputs_analysis_json(tmp_path: Path, capsys) -> None:
    payload = make_ohlcv_payload(500)
    input_file = tmp_path / "btcusdt-4h.json"
    input_file.write_text(json.dumps(payload), encoding="utf-8")

    exit_code = acceptance_map_cli.main(["--input-file", str(input_file)])

    captured = capsys.readouterr()
    body = json.loads(captured.out)

    assert exit_code == 0
    assert body["input_summary"]["symbol"] == "BTCUSDT"
    assert body["params"]["partition_mode"] == "equal_width"
    assert "regions" in body


def test_cli_omits_heatmap_and_diagnostics_when_flags_are_disabled(
    tmp_path: Path,
    capsys,
) -> None:
    payload = make_ohlcv_payload(500)
    input_file = tmp_path / "btcusdt-4h.json"
    input_file.write_text(json.dumps(payload), encoding="utf-8")

    exit_code = acceptance_map_cli.main(
        ["--input-file", str(input_file), "--no-heatmap", "--no-diagnostics"]
    )

    captured = capsys.readouterr()
    body = json.loads(captured.out)

    assert exit_code == 0
    assert "heatmap" not in body
    assert body["params"]["include_heatmap"] is False
    assert body["params"]["include_diagnostics"] is False
    assert "coverage_count" not in body["regions"][0]
    assert "weighted_volume_contribution" not in body["regions"][0]


def test_cli_returns_error_for_missing_file(capsys) -> None:
    exit_code = acceptance_map_cli.main(["--input-file", "/tmp/does-not-exist.json"])

    captured = capsys.readouterr()
    body = json.loads(captured.err)

    assert exit_code == 1
    assert body["error"]["code"] == "INPUT_FILE_NOT_FOUND"


def test_cli_returns_json_error_for_unsupported_partition_mode(
    tmp_path: Path,
    capsys,
) -> None:
    payload = make_ohlcv_payload(500)
    input_file = tmp_path / "btcusdt-4h.json"
    input_file.write_text(json.dumps(payload), encoding="utf-8")

    exit_code = acceptance_map_cli.main(["--input-file", str(input_file), "--partition-mode", "unknown"])

    captured = capsys.readouterr()
    body = json.loads(captured.err)

    assert exit_code == 1
    assert body["error"]["code"] == "UNSUPPORTED_PARTITION_MODE"


def test_cli_returns_input_parse_error_for_non_object_json_root(
    tmp_path: Path,
    capsys,
) -> None:
    input_file = tmp_path / "invalid-root.json"
    input_file.write_text(json.dumps([1, 2, 3]), encoding="utf-8")

    exit_code = acceptance_map_cli.main(["--input-file", str(input_file)])

    captured = capsys.readouterr()
    body = json.loads(captured.err)

    assert exit_code == 1
    assert body["error"]["code"] == "INPUT_PARSE_ERROR"


def test_cli_returns_input_parse_error_for_directory_path(
    tmp_path: Path,
    capsys,
) -> None:
    exit_code = acceptance_map_cli.main(["--input-file", str(tmp_path)])

    captured = capsys.readouterr()
    body = json.loads(captured.err)

    assert exit_code == 1
    assert body["error"]["code"] == "INPUT_PARSE_ERROR"


def test_cli_returns_input_parse_error_for_invalid_utf8_file(
    tmp_path: Path,
    capsys,
) -> None:
    input_file = tmp_path / "invalid-encoding.json"
    input_file.write_bytes(b"\xff\xfe\x00\x00")

    exit_code = acceptance_map_cli.main(["--input-file", str(input_file)])

    captured = capsys.readouterr()
    body = json.loads(captured.err)

    assert exit_code == 1
    assert body["error"]["code"] == "INPUT_PARSE_ERROR"


def test_cli_unexpected_error_does_not_expose_raw_exception_text(
    tmp_path: Path,
    capsys,
    monkeypatch,
) -> None:
    payload = make_ohlcv_payload(500)
    input_file = tmp_path / "btcusdt-4h.json"
    input_file.write_text(json.dumps(payload), encoding="utf-8")

    def _raise_unexpected(*_args, **_kwargs):
        raise RuntimeError("secret path /tmp/private-token.txt")

    monkeypatch.setattr(acceptance_map_cli, "analyze_acceptance_map", _raise_unexpected)

    exit_code = acceptance_map_cli.main(["--input-file", str(input_file)])

    captured = capsys.readouterr()
    body = json.loads(captured.err)

    assert exit_code == 1
    assert body["error"]["code"] == "ANALYSIS_FAILED"
    assert body["error"]["context"]["exception_type"] == "RuntimeError"
    assert "secret path" not in captured.err


def test_package_cli_subcommand_outputs_analysis_json(tmp_path: Path) -> None:
    payload = make_ohlcv_payload(500)
    input_file = tmp_path / "btcusdt-4h.json"
    input_file.write_text(json.dumps(payload), encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "powerby.cli",
            "acceptance-map",
            "--input-file",
            str(input_file),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    body = json.loads(completed.stdout)

    assert body["input_summary"]["symbol"] == "BTCUSDT"
    assert body["params"]["partition_mode"] == "equal_width"


def test_package_cli_subcommand_help_lists_acceptance_map_options() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "powerby.cli", "acceptance-map", "--help"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "--input-file" in completed.stdout
    assert "--partition-mode" in completed.stdout
    assert "--no-heatmap" in completed.stdout


def test_package_manifest_includes_acceptance_map_runtime_artifacts() -> None:
    package_manifest = json.loads(Path("package.json").read_text(encoding="utf-8"))

    assert "powerby/" in package_manifest["files"]
    assert "web/" in package_manifest["files"]
