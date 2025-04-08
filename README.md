# AI-Powered Plant Disease Detection

This application uses Google's Gemini API and machine learning to detect plant diseases from images and provide treatment recommendations.

## Features

- Upload plant images for disease detection
- Get instant disease identification
- Receive severity assessment
- Get treatment recommendations
- View preventive measures

## Setup

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in a `.env` file:
```
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=your-location
GEMINI_ENDPOINT=your-gemini-endpoint
```

3. Make sure you have Google Cloud credentials set up properly.

## Running the Application

Run the Streamlit app:
```bash
streamlit run app.py
```

## Usage

1. Open the application in your web browser
2. Upload a plant image using the file uploader
3. Click "Analyze Plant" to get the results
4. View the detailed analysis including:
   - Disease detection
   - Severity level
   - Treatment recommendations
   - Preventive measures

## Requirements

- Python 3.7+
- Google Cloud account with Gemini API access
- Required Python packages (see requirements.txt) 