from PIL import Image, ImageDraw, ImageFont
import cv2
import pytesseract
from googletrans import Translator
import textwrap
import streamlit as st
import numpy as np
import os

# Function to preprocess the image for better OCR results
def preprocess_image(image_path):
    abs_path = os.path.abspath(image_path)
    image = cv2.imread(abs_path)
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

# Function to display the translated text on a new black area below the image
def display_translated_text(image, translated_text):
    h, w, _ = image.shape
    black_area_height = 100  # Adjust this value based on the amount of text

    # Create a new image with an additional black area at the bottom
    result_image = np.zeros((h + black_area_height, w, 3), dtype=np.uint8)
    result_image[:h, :w] = image

    # Convert the OpenCV image to a PIL image
    pil_image = Image.fromarray(result_image)

    # Load a font
    font_path = "GoNotoCurrent-Regular.ttf"  # Update this path to your custom TTF font file
    font = ImageFont.truetype(font_path, 20)

    # Create a drawing context
    draw = ImageDraw.Draw(pil_image)

    # Wrap text to fit the image width
    wrapped_text = textwrap.wrap(translated_text, width=60)

    # Position the text in the black area
    y = h + 20
    for line in wrapped_text:
        draw.text((10, y), line, font=font, fill=(0, 255, 0))
        y += 30

    # Convert the PIL image back to an OpenCV image
    result_image = np.array(pil_image)

    return result_image

# Streamlit interface
st.title("Image Text Detection and Translation")

# Step 1: Upload an image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
if uploaded_file is not None:
    # Convert the file to an opencv image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)

    # Display the uploaded image
    st.image(opencv_image, channels="BGR")

    # Step 2: Detect the language of the text
    lang = st.text_input("Enter language code(s) for OCR (e.g., 'hin' for Hindi, 'kan' for Kannada, 'hin+kan' for both)", 'hin+kan+en')
    detected_text = read_text_from_image(uploaded_file.name, lang=lang)
    st.write(f"Detected text: {detected_text}")

    # Step 3: Translate the text
    dest_lang = st.selectbox("Select destination language for translation", ['en', 'hindi', 'kannada'])
    translated_text = translate_text(detected_text, src_lang='auto', dest_lang=dest_lang)
    st.write(f"Translated text: {translated_text}")

    # Step 4: Display the translated text on the image
    result_image = display_translated_text(opencv_image, translated_text)

    # Convert the image to RGB format for Streamlit
    result_image_rgb = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)
    st.image(result_image_rgb)

    # Step 5: Allow user to download the final image
    # Encode the RGB image for download
    _, buffer = cv2.imencode('.png', result_image)
    byte_im = buffer.tobytes()

    st.download_button(
        label="Download image",
        data=byte_im,
        file_name="translated_image.png",
        mime="image/png"
    )
