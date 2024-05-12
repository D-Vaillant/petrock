# test_classification.py
# Simply asks if a picture is a dog or a cat.
# from petrock.models import prompt_image
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO)

# TODO: Add in some code to see how long this takes.
# TODO: Refactor to use some testing framework. Pytest or Unittest, I guess.
def test_classifier():
    classes = ['cat', 'dog']
    for animal in classes:
        logging.info(f"Classifying {animal}.")
        img = Image.open(f'images/{animal}.jpg')
        answer = prompt_image(img, "What animal is this? Answer in one word.").lower()
        if answer == animal:
            logging.info(f"{animal} successfully classified.")
        else:
            logging.warning(f"Expected {animal}, got {answer}.")


if __name__ == "__main__":
    test_classifier()
