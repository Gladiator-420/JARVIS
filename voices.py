import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

speech_key = "Your-Azure-Speech-API-Key"
service_region = "Your-Region"

speech_config = SpeechConfig(subscription=speech_key, region=service_region)
speech_synthesizer = SpeechSynthesizer(speech_config=speech_config)

def speak(text):
    speech_synthesizer.speak_text_async(text).get()

speak("Hello, this is your AI assistant with a custom voice.")
