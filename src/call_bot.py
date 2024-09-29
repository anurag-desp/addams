from hugchat import hugchat
from hugchat.login import Login
from gtts import gTTS
from pydub import AudioSegment
import os


class CallBot:

    def __init__(self) -> None:
        self.user = "hugnatester"
        self.passwd = "hugonthefaceP3N"
        self.cookie_dir_path = './cookies_snapshot'

        self.sign = Login(self.user, self.passwd)
        try:
            self.cookies = self.sign.loadCookiesFromDir(self.cookie_dir_path)
        except:
            self.cookies = self.sign.login()
            self.sign.saveCookiesToDir(self.cookie_dir_path)
        
        self.chatbot = hugchat.ChatBot(cookies=self.cookies.get_dict())

        id = self.chatbot.new_conversation()
        self.chatbot.change_conversation(id)

        self.chatbot.switch_llm(1)

    def chat(self, query: str) -> str:
        result = self.chatbot.query(query, stream=False)
        result = str(result)
        return result
    
    def chatInfo(self) -> str:
        self.info = self.chatbot.get_conversation_info()
        return {
            "chat_id": self.info.id,
            "chat_title": self.info.title,
            "model": self.info.model,
            "system_prompt": self.info.system_prompt,
            "history": self.info.history,
            }
    
    def delChat(self):
        print("Chat deleted\n")
        self.chatbot.delete_all_conversations()

def save_response_audio(text: str):
    tts = gTTS(text=text, lang='en')

    au_filename = "/home/anurag/Documents/SIH/sentiment-analysis/web-app/tests/output/call_bot_response.mp3"
    tts.save(au_filename)

    sound = AudioSegment.from_mp3(au_filename)
    sound.export("/home/anurag/Documents/SIH/sentiment-analysis/web-app/tests/output/call_bot_response.wav", format="wav")
    os.remove(au_filename)