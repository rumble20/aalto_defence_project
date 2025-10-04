"""
Improved military report formatter
================================

This module refactors the original ``MilitaryReportFormatter`` into a cleaner, more maintainable design.  The goal of the class is
to accept a structured dictionary describing a military event and emit a formatted report. 

The improvements include:
* The formatting functions in the original code simply dumped the raw
  ``MilitaryPacket`` fields into a plain text block.  They did not follow
  widely used reporting conventions such as the nine‑line MEDEVAC/CASEVAC
  format or the DA Form 3265 explosive ordnance incident report.  The new
  implementation adds domain‑specific formatting:  a CASEVAC report is
  rendered as a nine‑line request (location, radio frequency, number of
  patients, etc.), and an EOD/EOINCREP report contains the key pieces of
  information described in FM 9‑15, appendix E (initial information, actions
  taken and disposition, and authentication details)【308824397195432†L90-L120】.
* Error handling has been strengthened.  Invalid input now results in a
  ``ValueError`` with a clear explanation instead of silently swallowing
  exceptions.  Optional fields can be left unspecified and sensible defaults
  will be used.

Users can instantiate either report class directly from a Python dictionary and
then call ``to_text()`` to obtain a formatted report.  The ``save_to_file``
function writes the report to a text file with a timestamped filename.

Example::

    from improved_military_report_formatter import CasevacReport, save_to_file

    packet = {
        "pickup_location": "FS123456",
        "frequency": "36.500 MHz",
        "patients_by_precedence": "1 urgent, 2 routine",
        "special_equipment": "none",
        "number_of_patients": "3 litter",
        "security": "N",  # no enemy in area
        "marking_method": "smoke, green",
        "patient_nationality": "A",  # US forces
        "nbc_contamination": "none"
    }
    report = CasevacReport(**packet)
    print(report.to_text())

"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

__all__ = [
    "EOIncidentReport",
    "CasevacReport",
    "save_to_file",
]


def _timestamp() -> str:
    """Return a file‑safe current timestamp."""
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")


@dataclass
class EOIncidentReport:
    """Explosive Ordnance/EO Incident report (similar to DA Form 3265).

    This dataclass represents the key elements of an explosive ordnance
    incident report as described in FM 9‑15 Appendix E【308824397195432†L90-L120】.  Fields correspond to
    sections on the form: initial information, action by EOD, and
    authentication.  Many of the fields are optional because not every
    incident will have all information immediately available.
    """

    # Heading information
    unit_number: Optional[str] = None
    control_number: Optional[str] = None
    category: Optional[str] = None  # "unusual" or "routine"

    # Section A: initial information
    date_time_reported: Optional[str] = None  # e.g. "20241004T1230Z"
    reported_by: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    incident_location: Optional[str] = None
    point_of_contact: Optional[str] = None
    items_reported: Optional[str] = None

    # Section B: action by EOD
    personnel_dispatched: Optional[str] = None
    departure_time: Optional[str] = None
    arrival_time: Optional[str] = None
    completion_time: Optional[str] = None
    travel_air_time: Optional[str] = None
    travel_vehicle_mileage: Optional[str] = None
    work_hours: Optional[str] = None
    confirmed_identification: Optional[str] = None
    disposition: Optional[str] = None
    narrative: Optional[str] = None

    # Section C: authentication
    commander_name: Optional[str] = None
    commander_phone: Optional[str] = None
    authentication_date: Optional[str] = None  # YYYYMMDD

    def to_text(self) -> str:
        """Render the report into a human‑readable multi‑section string.

        Fields that are not provided are omitted from the output.  This method
        follows the order and headings described in FM 9‑15 Appendix E【308824397195432†L90-L120】.
        """
        lines: list[str] = []
        lines.append("EXPLOSIVE ORDNANCE INCIDENT REPORT (EOINCREP)")
        # Heading information
        if any([self.unit_number, self.control_number, self.category]):
            lines.append("Heading Information:")
            if self.unit_number:
                lines.append(f"  Unit Number: {self.unit_number}")
            if self.control_number:
                lines.append(f"  Control Number: {self.control_number}")
            if self.category:
                lines.append(f"  Incident Category: {self.category}")
            lines.append("")
        # Section A
        if any([
            self.date_time_reported,
            self.reported_by,
            self.phone_number,
            self.address,
            self.incident_location,
            self.point_of_contact,
            self.items_reported,
        ]):
            lines.append("Section A – Initial Information:")
            if self.date_time_reported:
                lines.append(f"  Date/Time Reported: {self.date_time_reported}")
            if self.reported_by:
                lines.append(f"  Reported by: {self.reported_by}")
            if self.phone_number:
                lines.append(f"  Phone Number: {self.phone_number}")
            if self.address:
                lines.append(f"  Address: {self.address}")
            if self.incident_location:
                lines.append(f"  Incident Location: {self.incident_location}")
            if self.point_of_contact:
                lines.append(f"  Point of Contact: {self.point_of_contact}")
            if self.items_reported:
                lines.append(f"  Item(s) Reported: {self.items_reported}")
            lines.append("")
        # Section B
        if any([
            self.personnel_dispatched,
            self.departure_time,
            self.arrival_time,
            self.completion_time,
            self.travel_air_time,
            self.travel_vehicle_mileage,
            self.work_hours,
            self.confirmed_identification,
            self.disposition,
            self.narrative,
        ]):
            lines.append("Section B – Action by EOD:")
            if self.personnel_dispatched:
                lines.append(f"  Personnel Dispatched: {self.personnel_dispatched}")
            if any([self.departure_time, self.arrival_time, self.completion_time]):
                sub = []
                if self.departure_time:
                    sub.append(f"Departure: {self.departure_time}")
                if self.arrival_time:
                    sub.append(f"Arrival: {self.arrival_time}")
                if self.completion_time:
                    sub.append(f"Completion: {self.completion_time}")
                lines.append("  Date/Time (Departure/Arrival/Completion): " + "; ".join(sub))
            if any([self.travel_air_time, self.travel_vehicle_mileage]):
                sub = []
                if self.travel_air_time:
                    sub.append(f"Air travel time: {self.travel_air_time}")
                if self.travel_vehicle_mileage:
                    sub.append(f"Vehicle mileage: {self.travel_vehicle_mileage}")
                lines.append("  Travel Data: " + "; ".join(sub))
            if self.work_hours:
                lines.append(f"  Work Hours: {self.work_hours}")
            if self.confirmed_identification:
                lines.append(f"  Confirmed Identification: {self.confirmed_identification}")
            if self.disposition:
                lines.append(f"  Disposition: {self.disposition}")
            if self.narrative:
                lines.append(f"  Incident Narrative: {self.narrative}")
            lines.append("")
        # Section C
        if any([self.commander_name, self.commander_phone, self.authentication_date]):
            lines.append("Section C – Authentication:")
            if self.commander_name:
                lines.append(f"  Commander Name/Grade: {self.commander_name}")
            if self.commander_phone:
                lines.append(f"  Commander Phone: {self.commander_phone}")
            if self.authentication_date:
                lines.append(f"  Date: {self.authentication_date}")
        return "\n".join(lines)


@dataclass
class CasevacReport:
    """Casualty evacuation (CASEVAC) request following a nine‑line format.

    The nine lines used here are adapted from public explanations of the
    U.S. military's medical evacuation request procedures【467337062681845†L144-L156】.  Each field
    corresponds to a line in the request.  For example, ``pickup_location`` is
    line 1 and ``frequency`` is line 2.  All fields are strings to allow the
    caller to combine multiple pieces of information, e.g. "2 litter, 1
    ambulatory" for ``number_of_patients``.
    """

    pickup_location: str
    frequency: str
    patients_by_precedence: str
    special_equipment: str
    number_of_patients: str
    security: str
    marking_method: str
    patient_nationality: str
    nbc_contamination: str = field(default="none")

    def __post_init__(self) -> None:
        # Basic validation – ensure no field is empty
        required_fields = [
            ("pickup_location", self.pickup_location),
            ("frequency", self.frequency),
            ("patients_by_precedence", self.patients_by_precedence),
            ("special_equipment", self.special_equipment),
            ("number_of_patients", self.number_of_patients),
            ("security", self.security),
            ("marking_method", self.marking_method),
            ("patient_nationality", self.patient_nationality),
            ("nbc_contamination", self.nbc_contamination),
        ]
        for name, value in required_fields:
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Field '{name}' must be a non‑empty string.")

    def to_text(self) -> str:
        """Render the CASEVAC request into the standard nine‑line format.

        The ordering and descriptions are based on the description from
        OperationMilitaryKids【467337062681845†L144-L156】.  Each line is prefaced with the line number
        and a short description to aid clarity.
        """
        lines: list[str] = []
        lines.append("CASEVAC REQUEST (Nine‑Line)")
        lines.append(f"1. Location of pick‑up site: {self.pickup_location}")
        lines.append(f"2. Radio frequency / call sign: {self.frequency}")
        lines.append(f"3. Number of patients by precedence: {self.patients_by_precedence}")
        lines.append(f"4. Special equipment required: {self.special_equipment}")
        lines.append(f"5. Number of patients: {self.number_of_patients}")
        lines.append(f"6. Security at pick‑up site: {self.security}")
        lines.append(f"7. Method of marking pick‑up site: {self.marking_method}")
        lines.append(f"8. Patient nationality and status: {self.patient_nationality}")
        lines.append(f"9. NBC contamination (if any): {self.nbc_contamination}")
        return "\n".join(lines)


def save_to_file(report_text: str, report_type: str, output_dir: str = "./reports") -> str:
    """Save a report string to a timestamped text file and return its path.

    ``report_type`` should be a short identifier such as ``EOINCREP`` or
    ``CASEVAC``.  The output directory is created if it does not exist.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    filename = f"{report_type}_{_timestamp()}.txt"
    path = Path(output_dir) / filename
    with path.open("w", encoding="utf‑8") as fh:
        fh.write(report_text)
    return str(path)