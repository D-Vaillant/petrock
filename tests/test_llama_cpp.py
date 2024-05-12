from petrock.models import get_model_zoo
from guidance import models, gen, select, user, assistant, system

import logging
import random
import unittest

logging.basicConfig(level=logging.INFO)


@unittest.skip('Part of model intelligence testing.')
class ModelTester(unittest.TestCase):
    def setUp(self):
        model_zoo = get_model_zoo()
        mn = random.choice(list(model_zoo.keys()))
        self.lm = models.LlamaCppChat(f"{model_zoo[mn]['model']}",
                                      n_ctx=2048,
                                      echo=False)
        with system():
            self.lm += "Finish sentences accurately."

    def test_chat(self):
        question = "What letter comes after Q?"
        answer = 'R'
        logging.info("Testing: {question}")
        with user():
            lm = self.lm + question
        with assistant():
            lm += gen(stop='.', name='answer', max_tokens=50)
        logging.debug(f"Text state: {lm}")
        self.assertEqual(lm['answer'].upper(), answer)



if __name__ == "__main__":
    unittest.main()
