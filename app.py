import streamlit as st
import os
from PIL import Image
import io
import json
import requests
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()

# Get API key from environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
# Updated to use gemini-1.5-flash model
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

def encode_image(image):
    """Convert PIL Image to base64"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str

def analyze_plant_image(image):
    """Analyze plant image using Gemini API"""
    try:
        # Convert image to base64
        base64_image = encode_image(image)
        
        # Prepare the prompt
        prompt = """
        Analyze this plant image and provide the following information:
        1. Identify if there are any visible diseases
        2. If disease is detected, provide:
           - Disease name
           - Severity level (Low/Medium/High)
           - Treatment recommendations
           - Preventive measures
        3. General plant health assessment
        
        Format the response in JSON format.
        """

        # Updated payload structure for Gemini 1.5 Flash
        payload = {
            "contents": [{
                "parts":[{
                    "text": prompt
                }, {
                    "inlineData": {
                        "mimeType": "image/png",
                        "data": base64_image
                    }
                }]
            }],
            "generationConfig": {
                "temperature": 0.4,
                "topK": 32,
                "topP": 1,
                "maxOutputTokens": 2048,
            }
        }

        # Make the API request with updated headers
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY
        }
        
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            # Extract the text from the response
            if 'candidates' in result:
                text_response = result['candidates'][0]['content']['parts'][0]['text']
                try:
                    # Try to parse as JSON
                    return json.loads(text_response)
                except json.JSONDecodeError:
                    return {"raw_response": text_response}
            else:
                return {"error": "No response from API"}
        else:
            return {"error": f"API Error: {response.status_code}", "details": response.text}
            
    except Exception as e:
        st.error(f"Error analyzing image: {str(e)}")
        return None

def main():
    st.set_page_config(
        page_title="Plant Disease Detection",
        page_icon="🌿",
        layout="wide"
    )
    
    st.title("AI-Powered Plant Disease Detection 🌿")
    st.write("Upload a plant image to detect diseases and get treatment recommendations")

    # Check if API key is configured
    if not GEMINI_API_KEY:
        st.error("Please configure your Gemini API key in the .env file")
        return

    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Create columns for layout
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

        with col2:
            # Analyze button
            if st.button("Analyze Plant"):
                with st.spinner("Analyzing image..."):
                    result = analyze_plant_image(image)
                    
                    if result:
                        # Display results in a nice format
                        st.success("Analysis Complete!")
                        
                        if "error" in result:
                            st.error(result["error"])
                            if "details" in result:
                                st.code(result["details"])
                        elif "raw_response" in result:
                            st.write(result["raw_response"])
                        else:
                            # Display formatted results
                            if "disease_detected" in result:
                                st.subheader("Disease Information")
                                st.write(f"Disease: {result.get('disease_name', 'N/A')}")
                                st.write(f"Severity: {result.get('severity_level', 'N/A')}")
                                
                                st.subheader("Treatment Recommendations")
                                st.write(result.get('treatment_recommendations', 'N/A'))
                                
                                st.subheader("Preventive Measures")
                                st.write(result.get('preventive_measures', 'N/A'))
                            
                            st.subheader("Plant Health Assessment")
                            st.write(result.get('health_assessment', 'N/A'))
                    else:
                        st.error("Failed to analyze image. Please try again.")

if __name__ == "__main__":
    main() 