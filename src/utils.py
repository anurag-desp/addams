# convert wav tot flac file
from pydub import AudioSegment
import wave
import math
import os
import io
from settings import *
from natsort import natsorted
import pandas as pd

class PlayWithWavAudio():
    def __init__(self, folder, filename=''):
        self.folder = folder
        self.folder_wav = self.folder + '/wav_files/'
        self.folder_flac = self.folder + '/flac_files/'

        self.filename = filename
        if self.filename[-4:] == '.wav':
            self.filename = self.filename[0:-4]
            
        self.filename_wav  = self.filename + '.wav'
        self.filename_flac = self.filename + '.flac'


        self.filepath_wav  = self.folder_wav + self.filename_wav
        self.filepath_flac = self.folder_flac + self.filename_flac 
        
        if filename != '':
            self.audio = AudioSegment.from_wav(self.filepath_wav)

    def __call__(self, filename='recording.wav'):
        if filename == '':
            raise Exception("File name can't be empty")
        if filename[-4:] == '.wav':
            self.filename = filename[0:-4]
        else:
            self.filename = filename
        self.filename_wav  = self.filename + '.wav'
        self.filename_flac = self.filename + '.flac'
        
        self.filepath_wav  = self.folder_wav + self.filename_wav
        self.audio = AudioSegment.from_wav(self.filepath_wav)

    def get_duration(self):
        return self.audio.duration_seconds
    
    def single_split(self, from_sec, to_sec, split_filename):
        t1 = from_sec * 1000
        t2 = to_sec   * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export(self.folder_wav + '/' + split_filename, format="wav")
        
    def multiple_split(self, sec_per_split):
        total_secs = math.ceil(self.get_duration())
        for i in range(0, total_secs, sec_per_split):
            split_fn = self.filename + '_' + str(i) + '.wav'
            self.single_split(i, i+sec_per_split, split_fn)
            print(str(i) + ' Done')
            if i == total_secs - sec_per_split:
                print('All splited successfully')
    
    def single_wav2flac(self, flac_file_name='', wav_path=''):
        if wav_path == '':
            wav_path = self.filepath_wav
        
        if flac_file_name == '':
            wav_path_reversed = wav_path[::-1]
            i = 0
            while wav_path_reversed[i] != '/':
                flac_file_name = wav_path_reversed[i] + flac_file_name
                i += 1
            if flac_file_name[-4:] == '.wav':
                flac_file_name = flac_file_name[0:-4] + '.flac'
            else:
                flac_file_name += '.flac'

        if (len(flac_file_name) < 6) or (flac_file_name[-5:] != '.flac'):
            print('here')
            flac_file_name += '.flac'

        flac_path = self.folder_flac + flac_file_name
        print(flac_path)
        song = AudioSegment.from_wav(wav_path)
        song.export(flac_path, format = "flac")
    
    def multiple_wav2flac(self, flac_name_list=[], wav_path_list=[]):
        if wav_path_list == []:
            wav_name_list = os.listdir(self.folder_wav)
            wav_path_list = [self.folder_wav + f for f in wav_name_list]
        
        print(wav_path_list)

        if flac_name_list == []:
            flac_name_list = [''] * len(wav_path_list)
 
        if len(flac_name_list) < len(wav_path_list):
            temp = [''] * (len(flac_name_list) - len(wav_path_list))
            flac_name_list += temp
        

        for flac_name, wav_path in zip(flac_name_list, wav_path_list):
            self.single_wav2flac(flac_name, wav_path)

    def get_split_files(self):
        split_files = os.listdir(self.folder_wav)
        split_files = natsorted(split_files)
        split_files_path = [self.folder_wav + f for f in split_files if f != self.filename_wav]
        

        return split_files_path





def save_audio(recording, file_path):
    s = io.BytesIO(recording)
    sample_width = 2
    audio = AudioSegment.from_raw(s, sample_width=2, frame_rate=RATE, channels=CHANNELS).export(file_path, format='wav')



def get_problem_statement():
    labels = [
        "Problem Number",
        "Problem Statement ID",  	
        "Problem Statement Title", 	
        "Description", 	            
        "Organization", 	            
        "Category", 	                
        "Domain Bucket", 	        
        "Youtube Link", 	            
        "Dataset Link"] 	            

    data = [
        "79",
        "1356",
        "Sentiment Analysis of Incoming calls on helpdesk",
        "The problem at hand involves developing a sentiment analysis solution specifically tailored for analyzing the sentiment of incoming calls in helpdesks, call centers, and customer services. With the ever-increasing volume of customer interactions in these domains, it is crucial for businesses to gain insights into the sentiments expressed by their customers during phone conversations. Sentiment analysis refers to the process of automatically determining the sentiment or emotional tone conveyed by a text or speech. In the context of incoming calls, sentiment analysis can provide valuable information about customer satisfaction, identify potential issues, and highlight areas for improvement in customer service delivery.",
        "Ministry of Commerce and Industries",
        "Software",
        "Miscellaneous",
        "NA",
        "NA"]

    label_data_dict = {
        "label" : labels,
        "data"  : data 
    }

    table = pd.DataFrame.from_dict(label_data_dict)

    return table

def get_mentor_details():
    labels = [
        "Name",
        "Department",
        "Category",
        "Expertise",
        "Domain Experience"
    ]

    data = [
        "Dr. Tusar Kanti Dash",
        "Electronics and Communications Engineering",
        "Academic",
        "Speech Processing, Health Informatics, AI & ML",
        "18 Years"
    ]

    label_data_dict = {
        "label" : labels,
        "data"  : data 
    }

    table = pd.DataFrame.from_dict(label_data_dict)
    return table
