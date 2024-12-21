# cdt/main.py
from cdt.text_processing import summarize_text  # Importing the summarize_text function

def process_input_data(input_data, data_type):
    result = summarize_text(input_data)  # Use summarize_text function
    return result
