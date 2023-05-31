import numpy as np
from PIL import Image


def preprocess_image(canvas):
    # Convert the RGBA image to grayscale
    image = canvas.astype(np.uint8)[:, :, :3]
    image = Image.fromarray(image).convert("L")

    # Resize the image to 28x28 and normalize pixel values
    image = image.resize((28, 28))
    image = np.array(image) / 255.0

    # Invert the image (black background, white digit)
    image = 1.0 - image

    # Reshape the image to match the model input shape (1, 28, 28, 1)
    image = image.reshape((1, 28, 28, 1))

    return image


def predict_number(image, model):
    # Make predictions using the model
    prediction = model.predict(image)
    number = np.argmax(prediction)

    return number
