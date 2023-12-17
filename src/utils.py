# convert wav tot flac file
from pydub import AudioSegment
import math
import os
from natsort import natsorted


def get_duration(audio):
    return audio.duration_seconds



def single_split(audio, from_sec, to_sec, split_filename):
    folder = '/home/anurag/Documents/SIH/sentiment-analysis/web-app/tests/output'
    t1 = from_sec * 1000
    t2 = to_sec   * 1000
    split_audio = audio[t1:t2]
    split_audio.export(folder + '/' + split_filename, format="wav")
    


def multiple_split(filepath, sec_per_split):
    audio = AudioSegment.from_wav(filepath)
    total_secs = math.ceil(get_duration(audio))

    for i in range(0, total_secs, sec_per_split):
        split_fname = 'recording_' + str(i) + '.wav'
        single_split(audio, i, i+sec_per_split, split_fname)

        print('recording_' + str(i) + '.wav' + ' Done')
        if i == total_secs - sec_per_split:
            print('All splited successfully')



def split_file(file_path, sec_per_split):
    multiple_split(filepath=file_path, sec_per_split=sec_per_split)
    folder = '/'.join(file_path.split('/')[:-1])
    split_files = get_split_files(folder)

    return split_files


def get_split_files(folder):
    filename = folder.split('/')[-1]
    split_files = os.listdir(folder)
    split_files = natsorted(split_files)
    split_files_path = [folder + '/' + f for f in split_files if f != filename]
    return split_files_path

def filter_sentiments(sentiments):
    filtered_sentiments = []
    for i in sentiments:
        filtered_sentiments.append(i[0])
    
    return filtered_sentiments

def get_sentiments_summary(sentiments):
    if len(sentiments[0]) == 2:
        sentiments = filter_sentiments(sentiments=sentiments)
    text_sentiments = [
    "love",
    "joy",
    "gratitude",
    "caring",
    "admiration",
    "pride",
    "excitement",
    "curiosity",
    "amusement",
    "optimism",
    "surprise",
    "desire",
    "realization",
    "approval",
    "relief",
    "neutral",
    "confusion",
    "anger",
    "fear",
    "disgust",
    "remorse",
    "grief",
    "annoyance",
    "nervousness",
    "embarrassment ",
    "disappointment",
    "disapproval",
    "sadness"
    ]
        
    very_positive_sentiments = [
        "love",
        "joy",
        "gratitude",
        "caring",
        "admiration",
        "pride",
        "excitement",
        "curiosity",
        "amusement",
        "optimism",
        "surprise",
    ]

    positive_sentiments = [
        "desire",
        "realization",
        "approval",
        "relief",
    ]

    neutral_sentiments = [
        "neutral",
    ]

    negative_sentiments = [
        "confusion",
        "anger",
        "fear",
        "disgust",
    ]

    very_negative_sentiments = [
        "remorse",
        "grief",
        "annoyance",
        "nervousness",
        "embarrassment ",
        "disappointment",
        "disapproval",
        "sadness"
    ]

    very_positive_score = 0
    positive_score = 0
    neutral_score = 0
    negative_score = 0
    very_negative_score = 0

    for i in sentiments:
        if i in very_positive_sentiments:
            very_negative_score += 5
        elif i in positive_sentiments:
            positive_score += 2
        elif i in neutral_sentiments:
            neutral_score += 1
        elif i in negative_sentiments:
            negative_score -= 2
        else:
            very_negative_score -= 5

    
    total_score = very_positive_score + positive_score + negative_score + negative_score + very_negative_score
    if total_score >=5 :
        summary_sentiment = 'very positive'
    elif total_score >= 2 and total_score <= 4:
        summary_sentiment = 'positive'
    elif total_score <= 1 and total_score > -2:
        summary_sentiment = 'neutral'
    elif total_score >= -2 and total_score <= -4:
        summary_sentiment = 'negative'
    else:
        summary_sentiment = 'very negative'
    

    return summary_sentiment
