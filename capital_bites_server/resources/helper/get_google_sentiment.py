from google.cloud import language_v1
from google.cloud.language_v1 import enums
from google.oauth2 import service_account
import os
import json
credentials_raw = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

# Generate credentials
service_account_info = json.loads(credentials_raw)
credentials = service_account.Credentials.from_service_account_info(
    service_account_info)

client = language_v1.LanguageServiceClient(credentials=credentials) 

type_ = enums.Document.Type.PLAIN_TEXT
language = "en"



# Define a client, in this case Google's text to speech
# client = texttospeech.TextToSpeechClient(credentials=credentials)

def analyze_text_sentiment(text_sent):
    """
    Language Analysis 
    text_sent = text or paragraph passed
    """ #authenticate the client
    document = {"content": text_sent, "type": type_, "language":language}

    encoding_type = enums.EncodingType.UTF8

    analyzed_sentiment = client.analyze_sentiment(document, encoding_type=encoding_type)  #analyze the sentiment

    return analyzed_sentiment.document_sentiment.score