from PIL import Image
import pytesseract


def visual(path: str = '') -> str:
    image = Image.open(path)
    text: str = pytesseract.image_to_string(image, lang='por')

    return text
