from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_analyzer.recognizer_registry import RecognizerRegistry
from presidio_analyzer.context_aware_enhancers import LemmaContextAwareEnhancer
from presidio_anonymizer import AnonymizerEngine, DeanonymizeEngine
from presidio_anonymizer.operators import Operator, OperatorType
from typing import Dict


class InstanceCounterAnonymizer(Operator):
    """
    Anonymizer which replaces the entity value with an instance counter per entity type.
    """

    REPLACING_FORMAT = "<{entity_type}_{index}>"

    def operate(self, text: str, params: Dict = None) -> str:
        """
        Anonymize the input text by replacing entity values with a counter.

        Args:
            text (str): The input text to be anonymized.
            params (Dict): Parameters containing 'entity_type' and 'entity_mapping'.

        Returns:
            str: Anonymized text.
        """
        entity_type: str = params["entity_type"]
        entity_mapping: Dict[Dict: str] = params["entity_mapping"]
        entity_mapping_for_type = entity_mapping.get(entity_type)

        if not entity_mapping_for_type:
            new_text = self.REPLACING_FORMAT.format(entity_type=entity_type, index=0)
            entity_mapping[entity_type] = {}
        else:
            if text in entity_mapping_for_type:
                return entity_mapping_for_type[text]

            previous_index = self._get_last_index(entity_mapping_for_type)
            new_text = self.REPLACING_FORMAT.format(entity_type=entity_type, index=previous_index + 1)

        entity_mapping[entity_type][text] = new_text
        return new_text

    @staticmethod
    def _get_last_index(entity_mapping_for_type: Dict) -> int:
        """
        Get the last index for a given entity type.

        Args:
            entity_mapping_for_type (Dict): The entity mapping for a specific type.

        Returns:
            int: The last index used.
        """
        def get_index(value: str) -> int:
            return int(value.split("_")[-1][:-1])

        indices = [get_index(v) for v in entity_mapping_for_type.values()]
        return max(indices)

    def validate(self, params: Dict = None) -> None:
        """
        Validate operator parameters.

        Args:
            params (Dict): Parameters to be validated.

        Raises:
            ValueError: If required parameters are missing.
        """
        if "entity_mapping" not in params:
            raise ValueError("An input Dict called `entity_mapping` is required.")
        if "entity_type" not in params:
            raise ValueError("An entity_type param is required.")

    def operator_name(self) -> str:
        """
        Get the name of the operator.

        Returns:
            str: The operator name.
        """
        return "entity_counter"

    def operator_type(self) -> OperatorType:
        """
        Get the type of the operator.

        Returns:
            OperatorType: The type of the operator.
        """
        return OperatorType.Anonymize


class InstanceCounterDeanonymizer(Operator):
    """
    Deanonymizer which replaces the unique identifier with the original text.
    """

    def operate(self, text: str, params: Dict = None) -> str:
        """
        Deanonymize the input text by replacing counters with original entity values.

        Args:
            text (str): The anonymized text to be deanonymized.
            params (Dict): Parameters containing 'entity_type' and 'entity_mapping'.

        Returns:
            str: Deanonymized text.

        Raises:
            ValueError: If entity type or text is not found in the mapping.
        """
        entity_type: str = params["entity_type"]
        entity_mapping: Dict[Dict: str] = params["entity_mapping"]

        if entity_type not in entity_mapping:
            raise ValueError(f"Entity type {entity_type} not found in entity mapping!")
        if text not in entity_mapping[entity_type].values():
            raise ValueError(f"Text {text} not found in entity mapping for entity type {entity_type}!")

        return self._find_key_by_value(entity_mapping[entity_type], text)

    @staticmethod
    def _find_key_by_value(entity_mapping, value):
        """
        Find the original key (entity value) by its anonymized value.

        Args:
            entity_mapping (Dict): The entity mapping for a specific type.
            value (str): The anonymized value to be found.

        Returns:
            str: The original entity value.
        """
        for key, val in entity_mapping.items():
            if val == value:
                return key
        return None

    def validate(self, params: Dict = None) -> None:
        """
        Validate operator parameters.

        Args:
            params (Dict): Parameters to be validated.

        Raises:
            ValueError: If required parameters are missing.
        """
        if "entity_mapping" not in params:
            raise ValueError("An input Dict called `entity_mapping` is required.")
        if "entity_type" not in params:
            raise ValueError("An entity_type param is required.")

    def operator_name(self) -> str:
        """
        Get the name of the operator.

        Returns:
            str: The operator name.
        """
        return "entity_counter_deanonymizer"

    def operator_type(self) -> OperatorType:
        """
        Get the type of the operator.

        Returns:
            OperatorType: The type of the operator.
        """
        return OperatorType.Deanonymize


def setup_presidio():
    """
    Function to define the custom recognizers, add them to presidio's analyzer engine, instantiate the anonymizer
    and deanonymizer engines, and define the entity_mapping dictionary.

    Returns:
        analyzer: Presidio Analyzer Engine object w/ custom recognizers.
        anonymizer_engine: Presidio Anonymizer Engine object.
        deanonymizer_engine: Presidio Deanonymizer Engine object.
        entity_mapping: dict for pii entity mappings (pii type to value).
    """

    # DEFINING CUSTOMER RECOGNIZERS

    # SORT CODE
    # Regex expressions for perfect and non-trivial sort code matches
    sortcode_pattern_full = Pattern(name="Sort Code (perfect)", regex=r"\b\d{2}[-\s]\d{2}[-\s]\d{2}\b", score=1.0)
    sortcode_pattern = Pattern(name="Sort Code (weak)", regex=r"\b\d{6}\b", score=0.001)

    # Define Sortcode Recognizer
    sortcode_recognizer = PatternRecognizer(
        supported_entity="SORTCODE",
        patterns=[sortcode_pattern, sortcode_pattern_full],
        context=["sortcode", "sort"]
    )

    # Add to recognizer registry along with default recognizers
    registry = RecognizerRegistry()
    registry.load_predefined_recognizers()
    registry.add_recognizer(sortcode_recognizer)

    # Define context aware enhancer to increase match score if sort code is mentioned before a potential sort code
    context_aware_enhancer = LemmaContextAwareEnhancer(
        context_similarity_factor=0.75,
        min_score_with_context_similarity=0.4
    )

    # Instantiate an analyzer and add the new registry and context aware enhancer
    analyzer = AnalyzerEngine(registry=registry, context_aware_enhancer=context_aware_enhancer)

    # Instantiate the anonymizer engine and configure it to use the instance counter anonymizer class
    anonymizer_engine = AnonymizerEngine()
    anonymizer_engine.add_anonymizer(InstanceCounterAnonymizer)

    # Instantiate the deanonymizer engine and configure it to use the instance counter deanonymizer class
    deanonymizer_engine = DeanonymizeEngine()
    deanonymizer_engine.add_deanonymizer(InstanceCounterDeanonymizer)

    # Create an empty dict to use for entity mapping
    entity_mapping = dict()

    return analyzer, anonymizer_engine, deanonymizer_engine, entity_mapping
