from google_speech import Speech

# say "Hello World"
# text = "mep"
# lang = "en"
# speech = Speech(text, lang)
# speech.play()

def speech(text):
    print(text)
    lang = "en"
    speech = Speech(text, lang)
    speech.play()

