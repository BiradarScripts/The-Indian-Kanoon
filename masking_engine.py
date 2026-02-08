from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

class SmartMasker:
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
        
        # Keywords that indicate a person is a victim or family member
        self.sensitive_context_words = [
            "victim", "deceased", "prosecutrix", "minor", "child", "survivor",
            "wife of", "son of", "daughter of", "husband of", "mother of", "father of",
            "complainant", "informant", "pw-", "p.w." # Prosecution Witnesses
        ]

    def _is_sensitive_context(self, text, start, end, window=60):
        """
        Checks if any sensitive keyword exists near the detected entity.
        """
        snippet_start = max(0, start - window)
        snippet_end = min(len(text), end + window)
        snippet = text[snippet_start:snippet_end].lower()

        for word in self.sensitive_context_words:
            if word in snippet:
                return True
        return False

    def mask_victims_and_family(self, text):
        if not text:
            return ""

        # 1. Analyze: Find ALL entities (People, Phones, etc.)
        results = self.analyzer.analyze(
            text=text,
            entities=["PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS", "LOCATION", "IN_PAN"],
            language='en'
        )

        # 2. Identification Phase: Find names that appear near sensitive words
        identified_victim_names = set()
        
        for res in results:
            if res.entity_type == "PERSON":
                # Check if this specific instance has "victim/wife/etc" nearby
                if self._is_sensitive_context(text, res.start, res.end):
                    # Get the actual text of the name (e.g., "Sita")
                    name = text[res.start:res.end]
                    identified_victim_names.add(name)

        # 3. Filtering Phase: Decide what to mask
        final_results_to_mask = []
        
        for res in results:
            # Rule A: Always mask contact info
            if res.entity_type in ["PHONE_NUMBER", "EMAIL_ADDRESS", "LOCATION", "IN_PAN"]:
                final_results_to_mask.append(res)
                continue
            
            # Rule B: Mask Person if they are in our "identified_victim_names" list
            if res.entity_type == "PERSON":
                name_in_text = text[res.start:res.end]
                
                # If this name was flagged as a victim ANYWHERE in the doc, mask it HERE too.
                if name_in_text in identified_victim_names:
                    final_results_to_mask.append(res)
                else:
                    # It's likely a Judge/Lawyer who never appeared near "victim" words
                    pass

        # 4. Anonymize
        anonymized_result = self.anonymizer.anonymize(
            text=text,
            analyzer_results=final_results_to_mask,
            operators={
                "PERSON": OperatorConfig("replace", {"new_value": "[VICTIM/FAMILY]"}),
                "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "[PHONE]"}),
                "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "[EMAIL]"}),
                "LOCATION": OperatorConfig("replace", {"new_value": "[LOC]"}),
                "IN_PAN": OperatorConfig("replace", {"new_value": "[PAN]"}),
            }
        )

        return anonymized_result.text