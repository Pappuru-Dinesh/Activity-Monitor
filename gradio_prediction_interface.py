import gradio as gr
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd

# Load the trained model
model = load_model('cnn_lstm_model_4_activities.h5')

# Define the sensor columns
sensor_columns = ['alx', 'aly', 'alz', 'glx', 'gly', 'glz', 'arx', 'ary', 'arz', 'grx', 'gry', 'grz']

# Activity names
activity_names = {0: 'Walking', 1: 'Climbing', 2: 'Cycling', 3: 'Running'}

def predict_activity(file_path):
    # Read the uploaded CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Restrincting to only 100 rows
    df = df[:100]

    # Ensure the input shape matches the model's expected input shape
    if df.shape[0] != 100 or df.shape[1] != len(sensor_columns):
        return f"Error: The input CSV must have 100 rows and the correct number of columns. {df.shape}"
    
    inputs_array = df.values.reshape(1, 100, len(sensor_columns))
    
    # Make predictions
    prediction = model.predict(inputs_array)
    activity = np.argmax(prediction, axis=1)[0]
    return f'Predicted Activity: {activity_names[activity]}'

# Define the Gradio interface
interface = gr.Interface(
    fn=predict_activity,
    inputs=gr.File(type="filepath", label="Upload your CSV file"),
    outputs=gr.Textbox(),
    title='Activity Prediction',
    description='Predict the activity based on sensor data using CNN-LSTM model. Ensure your CSV has 100 rows and the correct number of columns.'
)

# Launch the interface
interface.launch()
