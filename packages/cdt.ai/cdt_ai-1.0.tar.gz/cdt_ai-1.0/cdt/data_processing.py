# cdt/data_processing.py
from cdt.text_processing import summarize_text, analyze_sentiment, text_preprocessing, vectorize_text, train_sentiment_classifier
from cdt.image_processing import extract_text_from_image, extract_image_caption
from cdt.audio_processing import transcribe_audio, extract_audio_features
from cdt.document_processing import extract_text_from_pdf, extract_text_from_pdf_plumber, extract_text_from_docx, extract_text_from_mupdf

def process_data(input_data, data_type):
    if data_type == 'text':
        # Preprocess and analyze text
        processed_text = text_preprocessing(input_data)
        summary = summarize_text(processed_text)
        sentiment = analyze_sentiment(processed_text)
        return {"summary": summary, "sentiment": sentiment}
    elif data_type == 'image':
        # Extract text from image using OCR
        text = extract_text_from_image(input_data)
        caption = extract_image_caption(input_data)
        return {"text": text, "caption": caption}
    elif data_type == 'audio':
        # Transcribe and extract features from audio
        transcription = transcribe_audio(input_data)
        audio_features = extract_audio_features(input_data)
        return {"transcription": transcription, "audio_features": audio_features.tolist()}
    elif data_type == 'pdf':
        # Extract text from PDF using different methods
        text = extract_text_from_pdf(input_data)
        return {"text": text}
    elif data_type == 'pdf_plumber':
        # Use pdfplumber for better quality text extraction
        text = extract_text_from_pdf_plumber(input_data)
        return {"text": text}
    elif data_type == 'docx':
        # Extract text from DOCX file
        text = extract_text_from_docx(input_data)
        return {"text": text}
    elif data_type == 'mupdf':
        # Extract text using PyMuPDF
        text = extract_text_from_mupdf(input_data)
        return {"text": text}
    else:
        return {"error": "Unsupported data type"}
