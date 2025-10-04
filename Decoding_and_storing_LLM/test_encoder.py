import unittest
from military_text_encoder import MilitaryTextEncoder, ReportType
from pathlib import Path

class TestMilitaryTextEncoder(unittest.TestCase):
    def setUp(self):
        self.encoder = MilitaryTextEncoder()
        
    def test_messy_text_processing(self):
        # Test messy input text
        messy_text = """
        !!URGENT!! Squad Alpha-2 & Bravo-3 must move ASAP!!!!
        Location coords: ((45.2134, -122.5789))
        Time frame: 1300Z TODAY
        PRIORITY STATUS: HIGHEST/URGENT!!!
        Multiple @#$% special ch@racters scattered && around...
        """
        
        # Process the text
        result = self.encoder.process_text(messy_text)
        
        # Check if processing succeeded
        self.assertNotIn("error", result)
        
        # Validate structure
        self.assertIn("action", result)
        self.assertIn("target_units", result)
        self.assertIn("coordinates", result)
        self.assertIn("timeframe", result)
        self.assertIn("priority", result)
        
        # Test coordinate format
        self.assertIn("x", result["coordinates"])
        self.assertIn("y", result["coordinates"])
        
    def test_report_formatting(self):
        test_text = """
        Delta team requires immediate support at (34.5678, 98.7654)
        Charlie team providing assistance
        Complete by 2200Z tonight
        HIGH PRIORITY
        """
        
        # Test EOINCREP format
        eoincrep_content, eoincrep_path = self.encoder.process_and_format(
            test_text, 
            ReportType.EOINCREP
        )
        self.assertTrue(len(eoincrep_content) > 0)
        
        # Test CASEVAC format
        casevac_content, casevac_path = self.encoder.process_and_format(
            test_text,
            ReportType.CASEVAC
        )
        self.assertTrue(len(casevac_content) > 0)
        
    def test_text_cleaning(self):
        dirty_text = "Test@#$%^&* with (123.45, -67.89) <<special>> ch@racters!"
        cleaned = self.encoder.clean_text(dirty_text)
        self.assertNotIn("@", cleaned)
        self.assertNotIn("#", cleaned)
        self.assertIn("(", cleaned)
        self.assertIn(")", cleaned)
        
if __name__ == '__main__':
    unittest.main()