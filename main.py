import os
import requests
from azure.identity import DefaultAzureCredential
from azure.ai.translation.document import DocumentTranslationClient

# Settings
AZURE_TRANSLATOR_RESOURCE_GROUP = "SeuResourceGroup"
AZURE_TRANSLATOR_RESOURCE_NAME = "SeuNomeDoTradutor"
AZURE_TRANSLATOR_LOCATION = "sua-localizacao"  # Ex: 'eastus'
AZURE_TRANSLATOR_API_KEY = "SuaChaveDeAPI"  # Se necessário

# Function to create an Azure Translator instance
def create_translator_instance():
    os.system(f"az group create --name {AZURE_TRANSLATOR_RESOURCE_GROUP} --location {AZURE_TRANSLATOR_LOCATION}")
    os.system(f"az cognitiveservices account create --name {AZURE_TRANSLATOR_RESOURCE_NAME} "
              f"--resource-group {AZURE_TRANSLATOR_RESOURCE_GROUP} --kind Translator --sku S0 "
              f"--location {AZURE_TRANSLATOR_LOCATION}")

# Function to translate a text
def translate_text(text, target_language="pt"):
    endpoint = f"https://{AZURE_TRANSLATOR_RESOURCE_NAME}.cognitiveservices.azure.com/"
    path = '/translate?api-version=3.0'
    params = f"&to={target_language}"

    # Header configuration
    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_TRANSLATOR_API_KEY,
        'Content-Type': 'application/json'
    }

    body = [{
        'text': text
    }]
    
    # Makes the call to the API
    response = requests.post(endpoint + path + params, headers=headers, json=body)
    response.raise_for_status()  # Levanta um erro se a resposta for um erro
    translation = response.json()
    
    # Returns the translated text
    return translation[0]['translations'][0]['text']

# Application testing
if __name__ == "__main__":
    # Create the translator instance
    create_translator_instance()

    # Example text for translation
    text_to_translate = "This is a technical article about Azure AI services."
    translated_text = translate_text(text_to_translate, target_language="pt")
    
    print("Original Text: ", text_to_translate)
    print("Translated Text: ", translated_text)
