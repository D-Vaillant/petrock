import sys
from PIL import Image
sys.path.append('../')
from petrock.models import describe_image, get_moondream
from petrock.llms import summon_moondream

def test_image_descriptions():
    images = [
        "../images/cat.jpg",
        "../images/dog.jpg",
        "../images/person_black_hat.jpg",
        "../images/person_hand_over_face.jpg",
        "../images/person_white_hat.jpg"
    ]

    moondream = summon_moondream()  # Make sure this method returns the Moondream model

    for image_path in images:
        img = Image.open(image_path)
        description = describe_image(moondream, image_path)
        print(f"Description for {image_path}: {description}")

if __name__ == "__main__":
    test_image_descriptions()
