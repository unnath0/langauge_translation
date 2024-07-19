import cv2
import pytesseract
from googletrans import Translator
import textwrap
import streamlit as st
from PIL import Image
import numpy as np

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


def display_translated_text(image, translated_text):
    h, w, _ = image.shape

    # Set the text properties
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    color = (0, 255, 0)
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

    return image


# Streamlit interface
st.title("Image Text Detection and Translation")

# Step 1: Upload an image
uploaded_file = st.file_uploader(
    "Choose an image...", type=["jpg", "png", "jpeg"])
if uploaded_file is not None:
    # Convert the file to an opencv image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)

    # Display the uploaded image
    st.image(opencv_image, channels="BGR")

    # Step 2: Detect the language of the text
    lang = st.text_input(
        "Enter language code(s) for OCR (e.g., 'hin' for Hindi, 'kan' for Kannada, 'hin+kan' for both)", 'eng')
    detected_text = read_text_from_image(uploaded_file.name, lang=lang)
    st.write(f"Detected text: {detected_text}")

    # Step 3: Translate the text
    dest_lang = st.text_input(
        "Enter destination language code for translation", 'en')
    translated_text = translate_text(
        detected_text, src_lang='auto', dest_lang=dest_lang)
    st.write(f"Translated text: {translated_text}")

    # Step 4: Display the translated text on the image
    result_image = display_translated_text(opencv_image, translated_text)

    # Convert the image to RGB format for Streamlit
    result_image_rgb = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)
    st.image(result_image_rgb)
