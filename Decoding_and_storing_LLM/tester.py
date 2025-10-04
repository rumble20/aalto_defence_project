import pytest
from llm_processor import (
    MilitaryReportFormatter,
    MilitaryPacket,
    Coordinates,
    Priority,
    ReportType
)
import os
from pathlib import Path

@pytest.fixture
def military_formatter():
    return MilitaryReportFormatter()

@pytest.fixture
def valid_packet():
    return MilitaryPacket(
        action="Move",
        target_units=["Alpha", "Bravo"],
        coordinates=Coordinates(x=123.45, y=678.90),
        timeframe="1200Z",
        priority=Priority.HIGH
    )

@pytest.fixture
def packet_without_units():
    return MilitaryPacket(
        action="Observe",
        target_units=[],
        coordinates=Coordinates(x=123.45, y=678.90),
        timeframe="1200Z",
        priority=Priority.LOW
    )

def test_format_eoincrep_valid_packet(military_formatter, valid_packet):
    expected_output = (
        "EOINCREP REPORT\n"
        "Action: Move\n"
        "Units Involved: Alpha, Bravo\n"
        "Coordinates: X=123.45, Y=678.9\n"
        "Timeframe: 1200Z\n"
        "Priority: HIGH\n"
    )
    result = military_formatter.format_eoincrep(valid_packet)
    assert result == expected_output

def test_format_eoincrep_empty_units(military_formatter, packet_without_units):
    expected_output = (
        "EOINCREP REPORT\n"
        "Action: Observe\n"
        "Units Involved: N/A\n"
        "Coordinates: X=123.45, Y=678.9\n"
        "Timeframe: 1200Z\n"
        "Priority: LOW\n"
    )
    result = military_formatter.format_eoincrep(packet_without_units)
    assert result == expected_output

def test_format_eoincrep_structure(military_formatter, valid_packet):
    result = military_formatter.format_eoincrep(valid_packet)
    assert result.startswith("EOINCREP REPORT\n")
    assert "Action:" in result
    assert "Units Involved:" in result
    assert "Coordinates:" in result
    assert "Timeframe:" in result
    assert "Priority:" in result

def test_format_casevac_valid_packet(military_formatter, valid_packet):
    expected_output = (
        "CASEVAC REPORT\n"
        "Evacuation Action: Move\n"
        "Units to Evacuate: Alpha, Bravo\n"
        "Evacuation Coordinates: X=123.45, Y=678.9\n"
        "Required Timeframe: 1200Z\n"
        "Evacuation Priority: HIGH\n"
    )
    result = military_formatter.format_casevac(valid_packet)
    assert result == expected_output

def test_format_and_save_report(military_formatter, valid_packet, tmp_path):
    military_formatter.output_dir = tmp_path
    report_content, filepath = military_formatter.format_and_save_report(
        valid_packet.dict(),
        ReportType.EOINCREP
    )
    
    assert report_content.startswith("EOINCREP REPORT\n")
    assert os.path.exists(filepath)
    with open(filepath, 'r') as f:
        saved_content = f.read()
    assert saved_content == report_content