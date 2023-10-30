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
        'rick_roll': ['открой 4 сезон пацанов']
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
            if do == 'youtube_search':
                print('Что будем искать?')
                rand = str(r.randint(0, 2))
                audio = AudioSegment.from_file(f"./youtube_search/youtube_search{rand}.wav", format="wav")
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


'''возможности помощника'''


def greeting():
    rand = str(r.randint(0, 4))
    file = f'./greeting/greeting{rand}.wav'
    audio = AudioSegment.from_file(file, format="wav")
    play(audio)


def open_youtube():
    wb.open('https://www.youtube.com')


def rick_roll():
    wb.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley')


def search_youtube():
    search = record_and_recognize_audio(do='youtube_search')
    search = search.split()
    search = '+'.join(search)
    url = f'https://www.youtube.com/results?search_query={search}'
    wb.open(url)


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


class Calculator(QMainWindow):
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
    ex = Calculator()
    ex.show()
    sys.exit(app.exec_())
