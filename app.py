import streamlit as st
import numpy as np
import pickle
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.preprocessing.sequence import pad_sequences
import gdown
import os

# Load MobileNetV2 model
mobilenet_model = MobileNetV2(weights="imagenet")
mobilenet_model = Model(inputs=mobilenet_model.inputs, outputs=mobilenet_model.layers[-2].output)

# Download model if not already present
if not os.path.exists("model6.h5"):
    # url = "https://drive.google.com/file/d/10T13MDfL08RsTYM2x4Eka8Yotjp-_tEW/view?usp=drive_link"  
    url = "https://drive.google.com/uc?id=10T13MDfL08RsTYM2x4Eka8Yotjp-_tEW"
    gdown.download(url, "model6.h5", quiet=False)



#adding extra for loading the model from the drive
#---------------------------------------------------------------------------------------
if os.path.exists("model6.h5"):
    print("Model file exists")
else:
    print("Model file does not exist")


try:
    model = tf.keras.models.load_model('model6.h5')
    print("Model loaded successfully")
except Exception as e:
    print("Error loading model:", e)


#------------------------------------------------------------------------------------
#original
# model = tf.keras.models.load_model('model6.h5')

# Load the tokenizer
with open('tokenizer.pkl', 'rb') as tokenizer_file:
    tokenizer = pickle.load(tokenizer_file)


#real code
# -----------------------------------------------------
# # Set custom web page title
# st.set_page_config(page_title="Caption Generator App", page_icon="📷")

# # Streamlit app
# st.title("Image Caption Generator")
# st.markdown(
#     "Upload an image, and this app will generate a caption for it using a trained LSTM model."
# )

# # Upload image
# uploaded_image = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

# # Process uploaded image
# if uploaded_image is not None:
#     st.subheader("Uploaded Image")
#     st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

#     st.subheader("Generated Caption")
#     # Display loading spinner while processing
#     with st.spinner("Generating caption..."):
#         # Load image
#         image = load_img(uploaded_image, target_size=(224, 224))
#         image = img_to_array(image)
#         image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
#         image = preprocess_input(image)

#         # Extract features using VGG16
#         image_features = mobilenet_model.predict(image, verbose=0)

#         # Max caption length
#         max_caption_length = 34
        
#         # Define function to get word from index
#         def get_word_from_index(index, tokenizer):
#             return next(
#                 (word for word, idx in tokenizer.word_index.items() if idx == index), None
#         )

#         # Generate caption using the model
#         def predict_caption(model, image_features, tokenizer, max_caption_length):
#             caption = "startseq"
#             for _ in range(max_caption_length):
#                 sequence = tokenizer.texts_to_sequences([caption])[0]
#                 sequence = pad_sequences([sequence], maxlen=max_caption_length)
#                 yhat = model.predict([image_features, sequence], verbose=0)
#                 predicted_index = np.argmax(yhat)
#                 predicted_word = get_word_from_index(predicted_index, tokenizer)
#                 caption += " " + predicted_word
#                 if predicted_word is None or predicted_word == "endseq":
#                     break
#             return caption

#         # Generate caption
#         generated_caption = predict_caption(model, image_features, tokenizer, max_caption_length)

#         # Remove startseq and endseq
#         generated_caption = generated_caption.replace("startseq", "").replace("endseq", "")

#     # Display the generated caption with custom styling
#     st.markdown(
#         f'<div style="border-left: 6px solid #ccc; padding: 5px 20px; margin-top: 20px;">'
#         f'<p style="font-style: italic;">“{generated_caption}”</p>'
#         f'</div>',
#         unsafe_allow_html=True
#     )
# ------------------------------------------------------


#code from chatGPT
# Function to get word from index
def get_word_from_index(index, tokenizer):
    return next(
        (word for word, idx in tokenizer.word_index.items() if idx == index), None
    )

# Function to predict caption
def predict_caption(model, image_features, tokenizer, max_caption_length):
    caption = "startseq"
    for _ in range(max_caption_length):
        sequence = tokenizer.texts_to_sequences([caption])[0]
        sequence = pad_sequences([sequence], maxlen=max_caption_length)
        yhat = model.predict([image_features, sequence], verbose=0)
        predicted_index = np.argmax(yhat)
        predicted_word = get_word_from_index(predicted_index, tokenizer)
        if predicted_word is None or predicted_word == "endseq":
            break
        caption += " " + predicted_word
    return caption

# Streamlit app
st.title("Image Caption Generator")
uploaded_image = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    try:
        # Process uploaded image
        image = load_img(uploaded_image, target_size=(224, 224))
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image = preprocess_input(image)

        # Extract image features
        image_features = mobilenet_model.predict(image, verbose=0)

        # Generate caption
        max_caption_length = 34
        generated_caption = predict_caption(model, image_features, tokenizer, max_caption_length)

        # Clean and display caption
        generated_caption = generated_caption.replace("startseq", "").replace("endseq", "").strip()
        st.markdown(f"**Generated Caption:** {generated_caption}")
    except Exception as e:
        st.error(f"An error occurred: {e}")


