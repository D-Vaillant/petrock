from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image

model_id = "vikhyatk/moondream2"
revision = "2024-04-02"
model = AutoModelForCausalLM.from_pretrained(
    model_id, trust_remote_code=True, revision=revision
)

tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)

# def prompt_model
def prompt_image(image: Image,
                 prompt: str='Describe this image.') -> str:
    enc_image = model.encode_image(image)
    return model.answer_question(enc_image, prompt, tokenizer)


if __name__ == "__main__":
    lm += "What color is made by mixing red and blue? "
    print(lm)
    # image = Image.open('images/dog.jpg')
    # print(prompt_image(image))
