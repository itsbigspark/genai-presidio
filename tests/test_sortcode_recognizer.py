import unittest
from presidio_analyzer import PatternRecognizer, Pattern
from presidio_analyzer.recognizer_registry import RecognizerRegistry
from presidio_analyzer.context_aware_enhancers import LemmaContextAwareEnhancer
from presidio_analyzer import AnalyzerEngine


class TestSortCodeRecognizer(unittest.TestCase):

    def setUp(self):

        # Define sort code patterns
        self.sortcode_pattern_full = Pattern(name="Sort Code Perfect", regex=r"\b\d{2}[-\s]\d{2}[-\s]\d{2}\b",
                                             score=1.0)
        self.sortcode_pattern = Pattern(name="Sort Code (weak)", regex=r"\b\d{6}\b", score=0.001)

        # Define recognizer
        self.sortcode_recognizer = PatternRecognizer(supported_entity="SORTCODE",
                                                     patterns=[self.sortcode_pattern, self.sortcode_pattern_full],
                                                     context=["sortcode", "sort"])

        # Setup registry and analyzer
        self.registry = RecognizerRegistry()
        self.registry.load_predefined_recognizers()
        self.registry.add_recognizer(self.sortcode_recognizer)

        self.context_aware_enhancer = LemmaContextAwareEnhancer(context_similarity_factor=0.75,
                                                                min_score_with_context_similarity=0.4)
        self.analyzer = AnalyzerEngine(registry=self.registry, context_aware_enhancer=self.context_aware_enhancer)

    def test_perfect_sort_code(self):
        text = "My sort code is 12-34-56."
        results = self.analyzer.analyze(text=text, language="en")

        self.assertTrue(len(results) >= 1)
        self.assertEqual(results[0].entity_type, "SORTCODE")
        self.assertEqual(results[0].start, 16)
        self.assertEqual(results[0].end, 24)
        self.assertEqual(results[0].score, 1.0)

    def test_weak_sort_code_with_context(self):
        text = "My sort code is 123456."
        results = self.analyzer.analyze(text=text, language="en")

        self.assertTrue(len(results) >= 2)
        self.assertEqual(results[0].entity_type, "SORTCODE")
        self.assertEqual(results[0].start, 16)
        self.assertEqual(results[0].end, 22)
        self.assertTrue(results[0].score > 0.01)

    def test_weak_sort_code_without_context(self):
        text = "Here is a number: 123456."
        results = self.analyzer.analyze(text=text, language="en")

        self.assertTrue(len(results) > 1)
        self.assertEqual(results[1].entity_type, "SORTCODE")
        self.assertEqual(results[1].score, 0.001)

    def test_no_sort_code(self):
        text = "This text does not contain any sort codes or personal information."
        results = self.analyzer.analyze(text=text, language="en")

        self.assertEqual(len(results), 0)

    def test_multiple_sort_codes(self):
        text = "First sort code: 12-34-56. Second sort code: 123456."
        results = self.analyzer.analyze(text=text, language="en")

        self.assertTrue(len(results) >= 2)
        self.assertEqual(results[0].entity_type, "SORTCODE")
        self.assertEqual(results[0].start, 17)
        self.assertEqual(results[0].end, 25)
        self.assertEqual(results[0].score, 1.0)

        self.assertEqual(results[1].entity_type, "SORTCODE")
        self.assertEqual(results[1].start, 45)
        self.assertEqual(results[1].end, 51)
        self.assertTrue(results[1].score > 0.01)

    def test_sort_code_with_noise(self):
        text = "Sort code: 12-34-56, and some more text."
        results = self.analyzer.analyze(text=text, language="en")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].entity_type, "SORTCODE")
        self.assertEqual(results[0].start, 11)
        self.assertEqual(results[0].end, 19)
        self.assertEqual(results[0].score, 1.0)


if __name__ == '__main__':
    unittest.main()
