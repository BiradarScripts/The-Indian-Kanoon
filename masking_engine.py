from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

class PIIMasker:
    def __init__(self):
        # Initialize the NLP analyzer (using Spacy underneath)
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()

    def mask_text(self, text):
        """
        Analyzes text for PII and masks it.
        """
        if not text:
            return ""

        # 1. Analyze: Find the PII entities
        # We look for Person, Phone, Email, Location, etc.
        results = self.analyzer.analyze(
            text=text,
            entities=["PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS", "LOCATION", "IN_PAN"],
            language='en'
        )

        # 2. Anonymize: Replace the found entities
        # We replace them with hash-like placeholders e.g., <PERSON>
        anonymized_result = self.anonymizer.anonymize(
            text=text,
            analyzer_results=results,
            operators={
                "PERSON": OperatorConfig("replace", {"new_value": "[REDACTED_NAME]"}),
                "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "[REDACTED_PHONE]"}),
                "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "[REDACTED_EMAIL]"}),
                "LOCATION": OperatorConfig("replace", {"new_value": "[REDACTED_LOC]"}),
                "IN_PAN": OperatorConfig("replace", {"new_value": "[REDACTED_PAN]"}),
            }
        )

        return anonymized_result.text