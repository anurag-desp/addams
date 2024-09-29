from flask import Flask, request, url_for, render_template, jsonify, make_response, redirect
from src.models import WhisperModel, RoBERTaModel, Wav2Vec2Model
from colorama import Fore, Back, Style, just_fix_windows_console
from subprocess import run, PIPE
import os, glob
from src.utils import split_file, save_pie_chart, get_sentiments_count
from src.call_bot import CallBot, save_response_audio


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
    output_path = './tests/output/audio.wav'
    for recs in glob.glob("./tests/output/recording_*.wav"):
        os.remove(recs)
        print(Fore.RED + f'removed {recs}')
    print(Style.RESET_ALL)

    with open(output_path, 'wb') as f:
        f.write(request.data)
    proc = run(['ffprobe', '-of', 'default=noprint_wrappers=1', output_path], text=True, stderr=PIPE)
    # print('proc: ', proc)

    # audio -> text
    split_audio_paths = split_file(output_path, sec_per_split=7)
    audio_to_text_transcription = WhisperModel()
    obtained_text = audio_to_text_transcription(split_audio_paths)

    # text -> sentiment
    text_to_sentiment = RoBERTaModel()
    obtained_sentiments = text_to_sentiment(obtained_text)

    sentiments = []
    for sentiment, score in obtained_sentiments:
        sentiments.append(sentiment)
    
    sentiments_count = get_sentiments_count(sentiments=sentiments)
    print(sentiments_count)

    unique_sentiments = []
    unique_sentiments_count = []
    for sentiment in sentiments_count.keys():
        unique_sentiments.append(sentiment)
        unique_sentiments_count.append(sentiments_count[sentiment])
    

    save_pie_chart(unique_sentiments, unique_sentiments_count)
    print(unique_sentiments, unique_sentiments_count)

    
    # respose = make_response(jsonify(obtained_text))
    return jsonify(
        {
            "text": obtained_text,
            "sentiments": obtained_sentiments,
        }
    )



@app.route('/graphs')
def graphical_analytics():
    return render_template('graphs.html')

@app.route('/navbar')
def navigation_bar():
    return render_template('navbar.html')

@app.route('/customize')
def customize_model():
    return render_template('customize.html')





@app.route('/saveaudio', methods=['POST'])
def save_audio():
    output_path = './tests/output/talk.wav'

    with open(output_path, 'wb') as f:
        f.write(request.data)
    proc = run(['ffprobe', '-of', 'default=noprint_wrappers=1', output_path], text=True, stderr=PIPE)

    return jsonify({
        'status': 'saved audio successfully!',
    })







def create_call_bot():
    call_bot = CallBot()
    return call_bot

call_bot = None
@app.route('/init_prompt', methods=['POST'])
def init_conv_with_call_bot():
    initial_prompt = request.json['init_prompt']
    print(initial_prompt)
    
    global call_bot
    call_bot = create_call_bot()
    result = call_bot.chat(initial_prompt)
    print(Fore.GREEN + result)
    print(Style.RESET_ALL)

    chat_infos = call_bot.chatInfo()

    return jsonify({
        'chat_id': chat_infos['chat_id']
    })




@app.route('/callbot')
def init_conv():
    return render_template('callbot_init_prompt.html')

@app.route('/callbot/<chat_id>')
def converse_with_call_bot(chat_id):
    global call_bot
    if call_bot is None:
        print('call_bot was None')
        call_bot = CallBot()


    print(f'chat_id: {chat_id}')
    
    try:
        output_path = '/home/anurag/Documents/SIH/sentiment-analysis/web-app/tests/output/talk.wav'
        audio_to_text_transcription = WhisperModel()
        obtained_text = audio_to_text_transcription(output_path)
        print(obtained_text)
        bot_response = call_bot.chat(obtained_text[0])
        save_response_audio(bot_response)
    except FileNotFoundError:
        print('exception thrown')
        return render_template('callbot.html')

    for recs in glob.glob("/home/anurag/Documents/SIH/sentiment-analysis/web-app/tests/output/recording_*.wav"):
        os.remove(recs)
        print(Fore.RED + f'removed {recs}')
    print(Style.RESET_ALL)


    return render_template('callbot.html')


    
    
    

if __name__ == "__main__":
    just_fix_windows_console()
    app.run(port=8989, debug=True)
