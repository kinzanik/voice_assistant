import speech_recognition
import sys
import random as r
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import os
import torch
from pydub import AudioSegment
from pydub.playback import play
import webbrowser as wb
import subprocess as sb
from time import sleep

device = torch.device('cpu')
local_file = 'model.pt'
model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
model.to(device)
if not os.path.isfile(local_file):
    torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/v4_ru.pt',
                                   local_file)

commands_dict = {
    'commands': {
        'greeting': ['привет', 'ку', 'здарова', 'добрый день'],
        'open_youtube': ['открой ютуб', 'ютуб', 'открой youtube', 'youtube'],
        'search_youtube': ['найди в ютуб', 'найди в youtube', 'найди в ютубе', 'найди в ютуби', 'поиск ютуб',
                           'ютуб поиск', 'youtube поиск', 'поиск youtube'],
        'open_google': ['открой гугл', 'гугл', 'google', 'открой google', 'включи google'],
        'rick_roll': ['открой 4 сезон пацанов'],
        'playlist_youtube': ['включи мой плейлист', 'плейлист ютуб', 'включи музыку'],
        'open_vk': ['открой вк', 'открой вконтакте', 'вк'],
        'run_dota': ['запусти доту', 'открой доту', 'открой dota', 'открой доту'],
        'run_telegram': ['запусти телеграм', 'открой телеграм', 'открой telegram', 'запусти telegram'],
        'run_minecraft': ['запусти minecraft', 'открой minecraft', 'включи майн', 'открой майн'],
        'w_todo': ['напиши в список дел', 'напиши список дел', 'добавь в список дел', 'добавь список дел',
                   'запиши в список дел', 'запиши список дел', 'пополни список дел', 'пополнить список дел',
                   'дополни список дел'],
        'r_todo': ['прочти список дел', 'сделай'],
        'clear_todo': ['очисти список дел', 'очистить список дел']
    }
}


def record_and_recognize_audio(*args: tuple, do='default'):
    """
    Запись и распознавание аудио
    """
    with microphone:
        recognized_data = ""

        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        try:
            if do == 'default':
                print('Слушаю...')
                audio = AudioSegment.from_file(f"./wating/wating1.wav", format="wav")
            elif do == 'youtube_search':
                print('Что будем искать?')
                rand = str(r.randint(0, 2))
                audio = AudioSegment.from_file(f"./youtube_search/youtube_search{rand}.wav", format="wav")
            elif do == 'w_todo':
                print('Что запишем в список дел?')
                rand = str(r.randint(0, 1))
                audio = AudioSegment.from_file(f'./todo_list/todo_wait{rand}.wav')
            play(audio)
            audio = recognizer.listen(microphone, 3, 5)

        except speech_recognition.WaitTimeoutError:
            print("Уверен что микрофон подключен?")
            return

        try:
            print("Распознаю...")
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()

        except speech_recognition.UnknownValueError:
            pass

        except speech_recognition.RequestError:
            print("Инета нет, чо делать?")

        return recognized_data


class Speaker:
    def __init__(self):
        torch.set_num_threads(4)
        self.sample_rate = 48000
        self.speaker = 'baya'

    def get_speaker(self):
        return self.speaker

    def set_speaker(self, new_speaker):
        self.speaker = new_speaker

    def text_to_spreach(self, example_text):
        audio_paths = model.save_wav(text=example_text,
                                     speaker=self.speaker,
                                     sample_rate=self.sample_rate)


'''возможности помощника'''


def greeting():
    rand = str(r.randint(0, 4))
    file = f'./greeting/greeting{rand}.wav'
    audio = AudioSegment.from_file(file, format="wav")
    play(audio)


def open_youtube():
    wb.open('https://www.youtube.com')


def search_youtube():
    search = record_and_recognize_audio(do='youtube_search')
    search = search.split()
    if len(search) == 0:
        pass
    search = '+'.join(search)
    url = f'https://www.youtube.com/results?search_query={search}'
    wb.open(url)


def open_google():
    wb.open('https://www.google.com')


def rick_roll():
    wb.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley')


def playlist_youtube():
    wb.open('https://www.youtube.com/watch?v=4W2ymUkg9Xg&list=PLmzD5x'
            'eXPBC8AHAZiTMOMhts-H2EsfAsc&ab_channel=Ren-Topic')


def open_vk():
    wb.open('https://vk.com/feed')


def run_dota():
    dota_path = "C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\\bin\win64\dota2.exe"
    sb.run([dota_path])


def run_telegram():
    telegram_path = 'C:\\Users\\turbo ishak\AppData\Roaming\Telegram Desktop\Telegram.exe'
    sb.run([telegram_path])


def run_minecraft():
    minecraft_path = 'C:\XboxGames\Minecraft Launcher\Content\Minecraft.exe'
    sb.run([minecraft_path])


def w_todo():
    a = open('todo.txt', 'a', encoding='utf-8')
    w_str = record_and_recognize_audio(do='w_todo')
    a.write(w_str + '\n')
    a.close()



def r_todo():
    a = open('todo.txt', 'r', encoding='utf-8').readlines()
    if len(a) == 0:
        sleep(2)
        rand = str(r.randint(0, 2))
        file = f'./todo_list/todo_error{rand}.wav'
        audio = AudioSegment.from_file(file, format="wav")
        play(audio)
        return
    a = '. '.join(a)
    speaker = Speaker()
    speaker.text_to_spreach(a)
    file = f'test.wav'
    audio = AudioSegment.from_file(file, format="wav")
    play(audio)


def clear_todo():
    todo = open('todo.txt', 'w', encoding='utf-8')
    todo.close()


class Nika(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('beta.ui', self)
        self.ListenBTN.clicked.connect(self.listen)
        self.speaker = Speaker()

    def listen(self):
        f = True
        voice_input = record_and_recognize_audio()
        print(voice_input)
        for k, v in commands_dict['commands'].items():
            if voice_input in v:
                f = False
                rand = str(r.randint(0, 2))
                file = f'./successful/successful{rand}.wav'
                audio = AudioSegment.from_file(file, format="wav")
                play(audio)
                globals()[k]()
        if f:
            rand = str(r.randint(0, 2))
            file = f'./error/error{rand}.wav'
            audio = AudioSegment.from_file(file, format="wav")
            play(audio)


if __name__ == "__main__":
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()
    app = QApplication(sys.argv)
    ex = Nika()
    ex.show()
    sys.exit(app.exec_())
