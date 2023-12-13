from transformers import pipeline, logging

# silence the warnings. They pollute the CLI
logging.set_verbosity_error()
logging.set_verbosity_warning()

# Whisper Model
class WhisperModel:
    def __init__(self):
        self.model_name      = './models/whisper_offline/WhisperModel'
        self.model_tokenizer = './models/whisper_offline/WhisperTokenizer'
        self.task            = 'automatic-speech-recognition'
        self.audio_to_text_transcriber = pipeline (
            task=self.task,
            model=self.model_name,
            tokenizer=self.model_tokenizer
        )
    
    def __repr__(self) -> str:
        return f"WhisperModel(task: {self.task}, model: Whisper)"
    
    def __call__(self, audio_path):
        obtained_texts = self.audio_to_text_transcriber(audio_path)
        try:
            if isinstance(obtained_texts, list):
                obtained_text_list = [result['text'] for result in obtained_texts]
                return obtained_text_list
            if isinstance(obtained_texts, dict):
                obtained_text = obtained_texts['text']
                return [obtained_text]
            else:
                raise Exception('Something wrong with the input audio path')
        except:
            print('Something wrong with the input audio path')



# RoBERTa Model
class RoBERTaModel():
    def __init__(self):
        self.model_name      = './models/roBERTa_offline/RobertaModel/'
        self.model_tokenizer = './models/roBERTa_offline/RobertaTokenizer/'
        self.task            = 'text-classification'
        self.text_to_sentiment_analyser = pipeline (
            task=self.task,
            model=self.model_name,
            tokenizer=self.model_tokenizer
        )

    def __repr__(self) -> str:
        return f"RoBERTaModel(task: {self.task}, name: RoBERTa)"
    
    def __call__(self, text):
        obtained_sentiment_list = self.text_to_sentiment_analyser(text)
        try:
            obtained_sentiment_list = [(sentiment_score['label'], sentiment_score['score']) for sentiment_score in obtained_sentiment_list]
            return obtained_sentiment_list
        except:
            print("except here")
            print('Something wrong with the text input')



# Wav2Vec2 Model
class Wav2Vec2Model():
    def __init__(self):
        self.model_name = './models/wav2vec2_emotion_offline/wav2vec2-lg-xlsr-en-speech-emotion-recognition'
        self.task       = 'audio-classification'
        self.audio_sentiment_classification = pipeline (
            task=self.task,
            model=self.model_name
        )
    
    def __repr__(self):
        return f"Wav2Vec2Model(task: {self.task}, name: Wav2Vec2"
    
    def __call__(self, audio_files_path):
        audio_sentiments_list = self.audio_sentiment_classification(audio_files_path)
        try:
            if isinstance(audio_sentiments_list[0], list):
                return audio_sentiments_list
            else:
                return [audio_sentiments_list]
        except:
            if isinstance(audio_files_path, str):
                print('Something wrong with the input audio path')
            if isinstance(audio_files_path, list):
                print('Something wrong with the input audio paths list')
            else:
                print(f"Expected 'str' or 'list' but got {type(audio_files_path)}")


        