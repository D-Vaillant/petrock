from petrock.models import model_zoo, ggufs
from guidance import models, gen, select, user, assistant, system

import logging
import random
import unittest

logging.basicConfig(level=logging.DEBUG)


class ModelTester(unittest.TestCase):
    def setUp(self):
        mn = random.choice(list(model_zoo.keys()))
        self.lm = models.LlamaCppChat(f"models/{model_zoo[mn]}",
                                      n_ctx=2048,
                                      echo=False)
        with system():
            self.lm += "Finish sentences accurately."

    def test_chat(self):
        with user():
            lm = self.lm + "What letter comes after Q?"
        with assistant():
            lm += gen(stop='.', name='answer', max_tokens=50)
        logging.debug(f"Text state: {lm}")
        self.assertEqual(lm['answer'].upper(), 'R')



if __name__ == "__main__":
    unittest.main()
