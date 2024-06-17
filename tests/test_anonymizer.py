import unittest
from anonymizer.anonymizer import InstanceCounterAnonymizer, InstanceCounterDeanonymizer


class TestInstanceCounterAnonymizer(unittest.TestCase):

    def setUp(self):
        self.anonymizer = InstanceCounterAnonymizer()
        self.deanonymizer = InstanceCounterDeanonymizer()
        self.entity_mapping = {}

    def test_anonymize_single_entity(self):
        params = {"entity_type": "TEST", "entity_mapping": self.entity_mapping}
        result = self.anonymizer.operate("12345", params)
        self.assertEqual(result, "<TEST_0>")
        self.assertIn("TEST", self.entity_mapping)
        self.assertEqual(self.entity_mapping["TEST"]["12345"], "<TEST_0>")

    def test_anonymize_multiple_entities(self):
        params = {"entity_type": "TEST", "entity_mapping": self.entity_mapping}
        self.anonymizer.operate("12345", params)
        result = self.anonymizer.operate("67890", params)
        self.assertEqual(result, "<TEST_1>")
        self.assertEqual(self.entity_mapping["TEST"]["67890"], "<TEST_1>")

    def test_anonymize_duplicate_entity(self):
        params = {"entity_type": "TEST", "entity_mapping": self.entity_mapping}
        self.anonymizer.operate("12345", params)
        result = self.anonymizer.operate("12345", params)
        self.assertEqual(result, "<TEST_0>")
        self.assertEqual(self.entity_mapping["TEST"]["12345"], "<TEST_0>")

    def test_deanonymize_single_entity(self):
        params = {"entity_type": "TEST", "entity_mapping": self.entity_mapping}
        self.anonymizer.operate("12345", params)
        result = self.deanonymizer.operate("<TEST_0>", params)
        self.assertEqual(result, "12345")

    def test_deanonymize_nonexistent_entity(self):
        params = {"entity_type": "TEST", "entity_mapping": self.entity_mapping}
        with self.assertRaises(ValueError) as context:
            self.deanonymizer.operate("<TEST_1>", params)
        self.assertTrue("Text <TEST_1> not found in entity mapping for entity type TEST" in str(context.exception))

    def test_validate_missing_entity_mapping(self):
        params = {"entity_type": "TEST"}
        with self.assertRaises(ValueError) as context:
            self.anonymizer.validate(params)
        self.assertTrue("An input Dict called `entity_mapping` is required." in str(context.exception))

    def test_validate_missing_entity_type(self):
        params = {"entity_mapping": self.entity_mapping}
        with self.assertRaises(ValueError) as context:
            self.anonymizer.validate(params)
        self.assertTrue("An entity_type param is required." in str(context.exception))


if __name__ == '__main__':
    unittest.main()

    # python -m unittest discover -s tests
