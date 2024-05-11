import unittest
import logging

from petrock.llms import summon_llm
from petrock.entities import Petrock, Personality



class TestPetrockChat(unittest.TestCase):
    model = 'llama3'

    def setUp(self):
        self.llm = summon_llm(self.model)
        self.rocky = Petrock(('boring', 'answering questions simply and plainly'))

    def test_basic_response(self):
        lt = self.llm + self.rocky.chat("What's being a rock like?")
        logging.info(f"Rock response: {lt['response']}")
        self.assertNotEqual(lt['response'], '')