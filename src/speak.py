from google_speech import Speech

text = "幹你娘"
lang = "zh"
speech = Speech(text, lang)
speech.play()