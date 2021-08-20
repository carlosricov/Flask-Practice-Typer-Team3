import unittest
from pt_client import NamedEntityClient


class TestPtClient(unittest.TestCase):
    def test_get_ents_returns_dictionary_given_empty_string(self):
        ner = NamedEntityClient()
        ents = ner.get_ents("")
        self.assertIsInstance(ents, dict)

    def test_get_ents_returns_dictionary_given_empty_string(self):
        ner = NamedEntityClient()
        ents = ner.get_ents("Dictionary")
        self.assertIsInstance(ents, dict)
