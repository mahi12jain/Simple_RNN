# Step 1: Import Libraries and Load the Model
import numpy as np
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam
import streamlit as st


# Load the IMDB dataset word index
word_index = imdb.get_word_index()
reverse_word_index = {value: key for key, value in word_index.items()}


# Load the pre-trained model
model = load_model('simple_rnn_imdb.h5')

# Recompile the model
model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])


# Step 2: Helper Functions
# Function to decode reviews
def decode_review(encoded_review):
    return ' '.join([reverse_word_index.get(i - 3, '?') for i in encoded_review])


def preprocess_text(text):
    # Handle empty input
    if not text.strip():
        return np.array([])  # Return an empty array if input is empty

    # Split and encode the review
    words = text.lower().split()
    encoded_review = [word_index.get(word, 2) + 3 for word in words]
    
    # If encoded_review is empty, return an empty array
    if len(encoded_review) == 0:
        return np.array([])

    # Pad the sequence to a fixed length
    padded_review = sequence.pad_sequences([encoded_review], maxlen=500)
    return padded_review


# Streamlit app
st.title('IMDB Movie Review Sentiment Analysis')
st.write('Enter a movie review to classify it as positive or negative.')

# User input
user_input = st.text_area('Movie Review')

if st.button('Classify'):
    preprocessed_input = preprocess_text(user_input)
    
    # Check for empty input after preprocessing
    if preprocessed_input.size == 0:
        st.write("Error: Input is empty or invalid.")
    else:
        prediction = model.predict(preprocessed_input)
        sentiment = 'Positive' if prediction[0][0] > 0.5 else 'Negative'
        st.write(f'Sentiment: {sentiment}')
        st.write(f'Prediction Score: {prediction[0][0]}')

else:
    st.write('Please enter a movie review.')


