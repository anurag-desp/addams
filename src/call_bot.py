from hugchat import hugchat
from hugchat.login import Login
from gtts import gTTS
# from io import BytesIO
import os
import playsound

def signInAndChatHug(user: str, passwd: str, query: str) -> str:
    cookie_path_dir = "./cookies_snapshot"
    # if already logged in: loadCookiesFromDir else: get Cookies and save to Dir
    sign = Login(user, passwd)
    try:
        cookies = sign.loadCookiesFromDir(cookie_path_dir)
    except:
        cookies = sign.login()
        sign.saveCookiesToDir(cookie_path_dir)

    # create chatbot
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    
    # new conversation (for switching)
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)

    # switch models
    chatbot.switch_llm(1)

    # send query + retrieve result
    result = chatbot.query(query, stream=True)
    result = str(result)

    chatbot.delete_all_conversations()
    return result

def speakResult(text: str):
    tts = gTTS(text=text, lang='en')

    au_filename = "out.mp3"
    tts.save(au_filename)
    playsound.playsound(au_filename)
    os.remove('./' + au_filename)

query = input()
result = signInAndChatHug(user="hugnatester", passwd="hugonthefaceP3N", query=query)
speakResult(result)




