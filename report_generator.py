# File: report_generator.py
import json
import time
from datetime import datetime
from enum import Enum

class ReportType(Enum):
    CASEVAC = 1    # Medical evacuation
    SPOTREP = 2    # Spot report  
    SITREP = 3     # Situation report
    THREAT = 4     # Threat alert

class BattlefieldReporter:
    def __init__(self):
        self.doctrine_templates = {
            ReportType.CASEVAC: self._casevac_template,
            ReportType.SPOTREP: self._spotrep_template,
            ReportType.THREAT: self._threat_template
        }
    
    def generate_report(self, report_type, incident_data, mesh_nodes=None):
        """Generate structured battlefield report"""
        template = self.doctrine_templates.get(report_type)
        if not template:
            return None
            
        report = template(incident_data)
        
        # Add mesh intelligence if available
        if mesh_nodes:
            report['sources'] = list(mesh_nodes.keys())
            report['confidence'] = self._calculate_confidence(mesh_nodes)
            
        return self._compress_report(report)
    
    def _casevac_template(self, data):
        """CASEVAC - Medical Evacuation Report"""
        return {
            'type': 'CASEVAC',
            'time': int(time.time()),
            'loc': data.get('grid', 'UNKNOWN'),
            'patients': data.get('casualties', 1),
            'injuries': data.get('injuries', 'UNKNOWN'),
            'security': data.get('security', 'ENEMY_CONTACT'),
            'marking': data.get('marking', 'SMOKE'),
            'urgent': data.get('urgent', True)
        }
    
    def _spotrep_template(self, data):
        """SPOTREP - Spot Report"""
        return {
            'type': 'SPOTREP', 
            'time': int(time.time()),
            'loc': data.get('grid', 'UNKNOWN'),
            'unit': data.get('unit', 'FRIENDLY'),
            'activity': data.get('activity', 'MOVEMENT'),
            'size': data.get('size', 'UNKNOWN'),
            'equipment': data.get('equipment', 'UNKNOWN')
        }
    
    def _threat_template(self, data):
        """THREAT - Immediate Threat Alert"""
        return {
            'type': 'THREAT',
            'time': int(time.time()),
            'loc': data.get('grid', 'UNKNOWN'), 
            'threat': data.get('threat_type', 'UNKNOWN'),
            'direction': data.get('direction', 'UNKNOWN'),
            'distance': data.get('distance', 'UNKNOWN'),
            'movement': data.get('movement', 'UNKNOWN')
        }
    
    def _calculate_confidence(self, mesh_nodes):
        """Calculate confidence based on mesh consensus"""
        if not mesh_nodes:
            return 0.5
            
        node_count = len(mesh_nodes)
        if node_count >= 3:
            return 0.9
        elif node_count == 2:
            return 0.7
        else:
            return 0.5
    
    def _compress_report(self, report):
        """Ultra compression for low-bandwidth transmission"""
        
        # Strategy 1: Extreme field shortening
        field_map = {
            'type': 't',
            'time': 'tm', 
            'location': 'l',
            'patients': 'p',
            'injuries': 'i',
            'security': 's',
            'marking': 'm',
            'urgent': 'u',
            'unit': 'un',
            'activity': 'a',
            'size': 'sz',
            'equipment': 'e',
            'threat': 'th',
            'direction': 'd',
            'distance': 'dst',
            'movement': 'mv',
            'sources': 'src',
            'confidence': 'c'
        }
        
        compressed = {}
        for key, value in report.items():
            short_key = field_map.get(key, key)
            compressed[short_key] = value
        
        # Strategy 2: Value encoding for common terms
        value_codes = {
            'ENEMY_CONTACT': 'EC',
            'MOVEMENT': 'MOV',
            'VEHICLE': 'VHC',
            'INFANTRY': 'INF',
            'SMOKE': 'SMK',
            'IR_STROBE': 'IRS'
        }
        
        for key, value in compressed.items():
            if isinstance(value, str) and value in value_codes:
                compressed[key] = value_codes[value]
        
        return compressed

# Integrated with your mesh system
class AegisReporter:
    def __init__(self, mesh_network):
        self.mesh = mesh_network
        self.reporter = BattlefieldReporter()
        
    def on_threat_detected(self, threat_data):
        """Automatically generate report when threat detected"""
        report = self.reporter.generate_report(
            ReportType.THREAT, 
            threat_data,
            self.mesh.nodes
        )
        
        if report:
            compressed = self._to_transmission_format(report)
            self.mesh.broadcast('ai_report', compressed)
            return compressed
        return None
    
    def on_voice_command(self, command, data):
        """Generate report from voice command"""
        report_type = self._command_to_report_type(command)
        if report_type:
            report = self.reporter.generate_report(
                report_type,
                data, 
                self.mesh.nodes
            )
            compressed = self._to_transmission_format(report)
            self.mesh.broadcast('ai_report', compressed)
            return compressed
        return None
    
    def _command_to_report_type(self, command):
        """Map voice commands to report types"""
        command_map = {
            'request casevac': ReportType.CASEVAC,
            'spot report': ReportType.SPOTREP,
            'situation report': ReportType.SITREP,
            'enemy spotted': ReportType.THREAT
        }
        return command_map.get(command.lower())
    
    def _to_transmission_format(self, report):
        """Convert to ultra-compact string for transmission"""
        # Even more compact than JSON for LoRa
        parts = []
        for key, value in report.items():
            if isinstance(value, bool):
                value = '1' if value else '0'
            parts.append(f"{key}:{value}")
        
        return "|".join(parts)  # "t:THREAT|tm:12345|l:E5|th:VHC"

    def parse_received_report(self, report_string):
        """Parse received compressed report"""
        try:
            # Handle both JSON and compressed format
            if report_string.startswith('{'):
                return json.loads(report_string)
            else:
                # Parse compressed format "t:THREAT|tm:12345|l:E5"
                report = {}
                pairs = report_string.split('|')
                for pair in pairs:
                    if ':' in pair:
                        key, value = pair.split(':', 1)
                        # Convert back boolean and numeric values
                        if value == '1': value = True
                        elif value == '0': value = False
                        elif value.isdigit(): value = int(value)
                        report[key] = value
                return report
        except:
            return {'raw': report_string}