# Importing the required libraries
import requests
import os
import uuid
import json
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, render_template
  
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    
    # Formdaki değerleri okunur
    original_text = request.form['text']
    target_language = request.form['language']
  
    key = os.environ['KEY']
    endpoint = 'https://api.cognitive.microsofttranslator.com/'
    location = 'global'
    path = '/translate?api-version=3.0'
      
    # Hedef dil parametresini ekleme
    target_language_parameter = '&to=' + target_language
      
    # URL'yi oluşturma
    constructed_url = endpoint + path + target_language_parameter
  
    # Header bilgilerini ayarlama
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
  
    # Çevrilecek metni alma
    body = [{'text': original_text}]
  
    # POST yapma
    translator_request = requests.post(
        constructed_url, headers=headers, json=body)
      
    # Retrieve the JSON response
    translator_response = translator_request.json()
      
    # Retrieve the translation
    translated_text = translator_response[0]['translations'][0]['text']
  
    # Call render template, passing the translated text,
    # original text, and target language to the template
    return render_template(
        'index.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )