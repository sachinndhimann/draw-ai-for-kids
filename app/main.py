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

# Generate a random number
random_number = np.random.randint(0, 10)

# Display the random number
st.write(f"Draw the number: {random_number}")


# Track if the user has submitted their drawing and if the prediction is correct
submitted = False
correct_prediction = False

submit_flag=st.button("Submit")

while not correct_prediction:
    # Perform prediction on the drawn image
    if submit_flag:
        if canvas.image_data is not None and not submitted:
            # Preprocess the image
            image = Image.fromarray(np.uint8(canvas.image_data))
            image = image.convert("L")
            image = image.resize((28, 28))
            image = np.expand_dims(image, axis=0)
            image = np.array(image) / 255.0

            # Make a prediction
            prediction = np.argmax(model.predict(image), axis=-1)[0]

            # Check if the prediction matches the current number
            if prediction == current_number:
                st.write("Congratulations! You drew the correct number.")
                correct_prediction = True
            else:
                st.write("Sorry, the number you drew is incorrect.")

            # Mark the drawing as submitted
            submitted = True

        if correct_prediction:
            # Move on to the next random number
            current_number = next_number
            next_number = np.random.randint(0, 10)
            st.write(f"Draw the next number: {current_number}")
        else:
            st.write("Please draw the current number correctly before submitting.")