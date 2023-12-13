from flask import Flask, request, url_for, render_template
from src.models import WhisperModel, RoBERTaModel, Wav2Vec2Model
from colorama import Fore, Back, Style, just_fix_windows_console
just_fix_windows_console()

import os

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/')
def get_home_page():
    return render_template('index.html')


@app.route('/audio_input', methods=['POST'])
def get_audio_data():
    print(request.get_json()['name'])
    print(request.get_json()['path'])
    os.system(f"open {request.get_json()['path']}")
    return {'status': 'received'}

@app.route('/whisper', methods=['GET'])
def get_transcribed_text():
    audio_path = request.get_json()['path']
    print(audio_path)
    print(Fore.GREEN + 'loading model...')
    print(Style.RESET_ALL)

    text_transcriber = WhisperModel()
    obtained_text = text_transcriber(audio_path)
    return {'text': obtained_text}

@app.route('/roberta', methods=['GET'])
def get_text_to_sentiment():
    texts = request.get_json()['text']
    print(texts)

    print(Fore.GREEN + 'loading model...')
    print(Style.RESET_ALL)

    text_to_sentiment = RoBERTaModel()
    sentiments = text_to_sentiment(texts)

    return {"sentiments": sentiments}

@app.route('/wav2vec', methods=['GET'])
def get_audio_to_sentiment():
    audio_paths = request.get_json()['path']
    print(audio_paths)

    print(Fore.GREEN + 'loading model...')
    print(Style.RESET_ALL)
    audio_to_sentiment = Wav2Vec2Model()
    sentiments = audio_to_sentiment(audio_paths)

    return {"sentiments": sentiments}


if __name__ == "__main__":
    just_fix_windows_console()
    app.run(debug=True)