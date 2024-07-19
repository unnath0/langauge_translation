import cv2
import pytesseract
from googletrans import Translator
import textwrap

# Function to preprocess the image for better OCR results


def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    return gray

# Function to read text from an image with language-specific models


def read_text_from_image(image_path, lang='eng'):
    image = preprocess_image(image_path)
    text = pytesseract.image_to_string(image, lang=lang)
    return text

# Function to translate text


def translate_text(text, src_lang='auto', dest_lang='en'):
    translator = Translator()
    translation = translator.translate(text, src=src_lang, dest=dest_lang)
    return translation.text

# Function to display the translated text on the image


def display_translated_text(image_path, translated_text):
    image = cv2.imread(image_path)
    h, w, _ = image.shape

    # Set the text properties
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    color = (0, 0, 0)
    thickness = 1
    margin = 10

    # Wrap text to fit the image width
    wrapped_text = textwrap.wrap(translated_text, width=60)

    # Position the text at the bottom of the image
    y0, dy = h - margin - 20 * len(wrapped_text), 20
    for i, line in enumerate(wrapped_text):
        y = y0 + i * dy
        cv2.putText(image, line, (margin, y), font, font_scale,
                    color, thickness, lineType=cv2.LINE_AA)

    # Display the image with the translated text
    cv2.imshow('Translated Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    # Step 1: Load an image from a local file
    image_path = '9.png'  # Replace with your image path

    # Step 2: Detect the language of the text (optional, improve as needed)
    lang = 'hin+kan'  # Example: use 'hin' for Hindi, 'kan' for Kannada, 'hin+kan' for both
    detected_text = read_text_from_image(image_path, lang=lang)
    print(f"Detected text: {detected_text}")

    # Step 3: Translate the text
    translated_text = translate_text(detected_text)
    print(f"Translated text: {translated_text}")

    # Step 4: Display the translated text on the image
    display_translated_text(image_path, translated_text)


if __name__ == "__main__":
    main()
