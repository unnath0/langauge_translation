from PIL import Image, ImageDraw, ImageFont
import cv2
import pytesseract
from googletrans import Translator
import textwrap
import streamlit as st
import numpy as np
import requests

# Function to preprocess the image for better OCR results
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    return gray

# Function to read text from an image with language-specific models
def read_text_from_image(image, lang='eng'):
    image = preprocess_image(image)
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
    font_path = "fonts/GoNotoCurrent-Regular.ttf"  # Update this path to your custom TTF font file
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


def home_page():
    st.markdown("<h1 style='text-align: center;'>JSSATEB</h1>", unsafe_allow_html=True)
    
    image_url = "https://github.com/unnath0/langauge_translation/blob/main/src%2Fjssateb_logo.jpeg"
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    st.image(img, use_column_width=True)
    
    st.markdown("<h2 style='text-align: center;'>Team Members</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>1. Ahijnan S (1JS21CS004)</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>2. Anand S P (1JS21CS024)</p>", unsafe_allow_html=True)
    
    st.markdown("<p style='text-align: center;'>Under the guidance of Mrs. Rashmi B N</p>", unsafe_allow_html=True)
    
def instructions():
    st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 36px;
            color: #FFFFFF;
        }
        .subtitle {
            text-align: center;
            font-size: 24px;
            color: #FFFFFF;
        }
        .content {
            text-align: justify;
            font-size: 18px;
            color: #DDDDDD;
        }
        .step {
            font-size: 20px;
            color: #AAAAAA;
        }
        .highlight {
            font-size: 20px;
            color: #FFD700;
        }
        .step-num {
            font-size: 24px;
            color: #FFD700;
            font-weight: bold;
        }
    </style>
    <div class="title">Welcome to the Image Text Detection and Translation App!</div>
    <br>
    <div class="content">
        <p>
            Our app allows you to easily extract text from images, detect the language of the text, and translate it into your preferred language. 
            Whether you're working with documents, signs, or any other text-containing images, this app makes it simple to understand and translate the content.
        </p>
        <br>
        <div class="subtitle">How It Works</div>
        <p>
            The app utilizes advanced Optical Character Recognition (OCR) technology to extract text from images. It supports multiple languages, 
            and you can specify the languages you want to detect. The detected text can then be translated into a language of your choice using powerful translation services.
        </p>
        <br>
        <div class="subtitle">How to Use the App</div>
        <br>
        <div class="step"><span class="step-num">1.</span> <span class="highlight">Upload an Image:</span></div>
        <p class="content">Use the file uploader to select an image from your device. The app supports various formats such as JPG, PNG, and JPEG.</p>
        <br>
        <div class="step"><span class="step-num">2.</span> <span class="highlight">Specify Languages for OCR:</span></div>
        <p class="content">Enter the language codes for OCR detection. For example, use 'hin' for Hindi, 'kan' for Kannada, or 'hin+kan' for both. The app will process the image and extract the text.</p>
        <br>
        <div class="step"><span class="step-num">3.</span> <span class="highlight">Translate the Text:</span></div>
        <p class="content">Select the destination language for translation from the dropdown menu. The detected text will be translated into the selected language.</p>
        <br>
        <div class="step"><span class="step-num">4.</span> <span class="highlight">View and Download:</span></div>
        <p class="content">The translated text will be displayed on a new black area below the original image. You can view the result directly in the app and download the final image with the translated text.</p>
    </div>
""", unsafe_allow_html=True)
    

def ocr_app():
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
        detected_text = read_text_from_image(opencv_image, lang=lang)
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


st.sidebar.title("Navigation")
option = st.sidebar.selectbox("Choose a chapter", ["Home", "Instructions", "App"])

if option == "Home":
    home_page()
if option == "Instructions":
    instructions()
if option == "App":
    ocr_app()
