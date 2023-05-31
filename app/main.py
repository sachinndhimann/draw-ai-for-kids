import streamlit as st
from tensorflow import keras
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# Load the MNIST model
model = keras.models.load_model("data/mnist/mnist_model.h5")

# Set up the canvas
st.title("Number Drawing App")
canvas = st_canvas(
    fill_color="#000000",
    stroke_width=10,
    stroke_color="#FFFFFF",
    background_color="#000000",
    height=300,
    width=300,
    drawing_mode="freedraw",
    key="canvas",
)

# Track the current number and the next number to be drawn
#if st.button("Generate Number"):
current_number = st.session_state.current_number if "current_number" in st.session_state else None
next_number = st.session_state.next_number if "next_number" in st.session_state else np.random.randint(0, 10)

if current_number is None:
    current_number = next_number

    # Display the current number
st.write(f"Draw the number: {current_number}")

# Track if the user has submitted their drawing and if the prediction is correct
submitted = st.session_state.submitted if "submitted" in st.session_state else False
correct_prediction = st.session_state.correct_prediction if "correct_prediction" in st.session_state else False


# Perform prediction on the drawn image
if st.button("Submit"):
    print("invoked...")
    #print(canvas.image_data)
    #print(submitted)
    if canvas.image_data is not None:
        # Preprocess the image
        image = Image.fromarray(np.uint8(canvas.image_data))
        image = image.convert("L")
        image = image.resize((28, 28))
        image = np.expand_dims(image, axis=0)
        image = np.array(image) / 255.0

        # Make a prediction
        prediction = np.argmax(model.predict(image), axis=-1)[0]

        # Check if the prediction matches the current number
        print(prediction,current_number)
        if prediction == current_number:
            st.write("Congratulations! You drew the correct number.")
            correct_prediction = True
        else:
            st.write("Sorry, the number you drew is incorrect.")

        # Mark the drawing as submitted
        submitted = True

# Update the app state
st.session_state.correct_prediction = correct_prediction
st.session_state.submitted = submitted

if correct_prediction:
    # Move on to the next random number if the user has submitted their drawing
    if submitted:
        current_number = next_number
        next_number = np.random.randint(0, 10)
        #st.write(f"Draw the next number: {current_number}")
        
        # Reset the submission flag and clear the canvas
        submitted = False
        canvas.data = []
    else:
        st.write("Please submit your drawing.")
else:
    # Reset the current number and canvas if the user has not submitted their drawing
    if submitted:
        current_number = next_number
        #st.write(f"Draw the number: {current_number}")
        submitted = False
        canvas.data = []

# Update the app state with the current and next numbers
st.session_state.current_number = current_number
st.session_state.next_number = next_number