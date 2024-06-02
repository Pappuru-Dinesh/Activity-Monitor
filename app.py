import gradio as gr
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
from io import StringIO

# Load the trained model
model = load_model('activity_cnn_lstm_model.h5')

# Define the sensor columns
sensor_columns = ['alx', 'aly', 'alz', 'glx', 'gly', 'glz', 'arx', 'ary', 'arz', 'grx', 'gry', 'grz']

def predict_activity(csv_input):
    # Read the CSV input into a DataFrame
    df = pd.read_csv(StringIO(csv_input), header=None, names=sensor_columns)
    
    # Convert the DataFrame to the correct data type
    df = df.astype(float)
    
    # Ensure the input shape matches the model's expected input shape
    if df.shape[0] != 100 or df.shape[1] != len(sensor_columns):
        return "Error: The input CSV must have 100 rows and the correct number of columns."
    
    inputs_array = df.values.reshape(1, 100, len(sensor_columns))
    
    # Make predictions
    prediction = model.predict(inputs_array)
    activity = np.argmax(prediction, axis=1)[0]
    return f'Predicted Activity: {activity}'

# Define the Gradio interface
interface = gr.Interface(
    fn=predict_activity,
    inputs=gr.Textbox(lines=20, placeholder="Paste your CSV content here..."),
    outputs=gr.Textbox(),
    title='Activity Prediction',
    description='Predict the activity based on sensor data using CNN-LSTM model. Ensure your CSV has 100 rows and the correct number of columns.'
)

# Launch the interface
interface.launch()
