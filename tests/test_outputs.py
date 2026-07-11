import json
from pathlib import Path

REPORT = Path("/app/report.json")


def test_report_file_exists():
    """Criterion 1: Save the report as /app/report.json."""
    assert REPORT.exists(), "report.json not found at /app/report.json"


def test_report_is_valid_json():
    """Criterion 2: The report must be valid JSON."""
    text = REPORT.read_text()
    try:
        json.loads(text)
    except json.JSONDecodeError as e:
        raise AssertionError(f"report.json is not valid JSON: {e}")


def test_total_requests():
    """Criterion 3: total_requests equals the number of log entries (6)."""
    data = json.loads(REPORT.read_text())
    assert data.get("total_requests") == 6, (
        f"expected total_requests=6, got {data.get('total_requests')}"
    )


def test_unique_ips():
    """Criterion 4: unique_ips equals the number of distinct client IPs (3)."""
    data = json.loads(REPORT.read_text())
    assert data.get("unique_ips") == 3, (
        f"expected unique_ips=3, got {data.get('unique_ips')}"
    )


def test_top_path():
    """Criterion 5: top_path is the most frequently requested path (/index.html)."""
    data = json.loads(REPORT.read_text())
    assert data.get("top_path") == "/index.html", (
        f"expected top_path='/index.html', got {data.get('top_path')}"
    )
