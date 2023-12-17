from flask import Flask, request, url_for, render_template, jsonify, make_response
from src.models import WhisperModel, RoBERTaModel, Wav2Vec2Model
from colorama import Fore, Back, Style, just_fix_windows_console
from subprocess import run, PIPE
import os, glob
from src.utils import split_file, get_sentiments_summary

just_fix_windows_console()

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/record')
def record_audio():
    return render_template('record.html')

@app.route('/audio', methods=['POST'])
def audio():
    output_path = '/home/anurag/Documents/SIH/sentiment-analysis/web-app/tests/output/audio.wav'
    for recs in glob.glob("/home/anurag/Documents/SIH/sentiment-analysis/web-app/tests/output/recording_*.wav"):
        os.remove(recs)
        print(Fore.RED + f'removed {recs}')
    print(Style.RESET_ALL)

    with open(output_path, 'wb') as f:
        f.write(request.data)
    proc = run(['ffprobe', '-of', 'default=noprint_wrappers=1', output_path], text=True, stderr=PIPE)
    # print('proc: ', proc)

    # audio -> text
    split_audio_paths = split_file(output_path, sec_per_split=10)
    audio_to_text_transcription = WhisperModel()
    obtained_text = audio_to_text_transcription(split_audio_paths)

    # text -> sentiment
    text_to_sentiment = RoBERTaModel()
    obtained_sentiments = text_to_sentiment(obtained_text)

    sentiment_summary = get_sentiments_summary(obtained_sentiments)

    # respose = make_response(jsonify(obtained_text))
    return jsonify(
        {
            "text": obtained_text,
            "sentiments": obtained_sentiments,
            "summary_sentiment": sentiment_summary,
        }
    )

@app.route('/graphs')
def graphical_analytics():
    return render_template('graphs.html')

if __name__ == "__main__":
    just_fix_windows_console()
    app.run(port=8989, debug=True)
