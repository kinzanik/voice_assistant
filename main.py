import speech_recognition
import sys
import random as r
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction, QPushButton
import os
import torch
from pydub import AudioSegment
from pydub.playback import play
import webbrowser as wb
import subprocess as sb
from time import sleep
from sound import Sound
import re

device = torch.device('cpu')

local_file = 'model.pt'
if not os.path.isfile(local_file):
    print('Производится загрузка необходимых файлов...')
    torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/v4_ru.pt',
                                   local_file)
model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
model.to(device)


config = open('config.txt', 'r', encoding='utf-8').readlines()

all_patterns = config[0].rstrip().split(': ')[1].split(', ')

commands_dict = {
    'commands': {

    }
}

for i in config[1:]:
    if i == '!':
        break
    i = i.rstrip().split(': ')
    name_func, patterns = i[0], i[1]
    lst_patterns = patterns.split(', ')
    all_patterns.extend(lst_patterns)
    commands_dict['commands'][name_func] = lst_patterns


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def play_sound(path: str, klv):
    file = path
    if klv is None:
        file += '.wav'
        return
    klv = int(klv)
    if klv == 0:
        file += '0' + '.wav'
    else:
        rand = str(r.randint(0, klv - 1))
        file += rand + '.wav'
    audio = AudioSegment.from_file(file, format="wav")
    play(audio)


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
                play_sound('./wating/wating', 0)
            elif do == 'youtube_search':
                print('Что будем искать?')
                play_sound('./youtube_search/youtube_search', 3)
            elif do == 'w_todo':
                print('Что запишем в список дел?')
                play_sound('./todo_list/todo_wait', 2)
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


'''основные возможности помощника'''


def greeting():
    play_sound('./greeting/greeting', 4)


def open_youtube():
    wb.open('https://www.youtube.com')


def search_youtube(vi):
    if len(vi) == 0:
        pass
    search = '+'.join(vi)
    url = f'https://www.youtube.com/results?search_query={search}'
    wb.open(url)


def open_google():
    wb.open('https://www.google.com')


def search_google(vi):
    if len(vi) == 0:
        pass
    search = '+'.join(vi)
    url = f'https://www.google.com/search?q={search}'
    wb.open(url)


def search_yandex_market(vi):
    if len(vi) == 0:
        pass
    search = '+'.join(vi)
    url = f'https://market.yandex.ru/search?text={search}'
    wb.open(url)


def rick_roll():
    wb.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley')


def playlist():
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
    print('Добавлено!')


def r_todo():
    a = open('todo.txt', 'r', encoding='utf-8').readlines()
    if len(a) == 0:
        sleep(2)
        play_sound('./todo_list/todo_error', 3)
        return
    a = '. '.join(a) + '.'
    speaker = Speaker()
    speaker.text_to_spreach(a)
    play_sound('test.wav', None)


def clear_todo():
    todo = open('todo.txt', 'w', encoding='utf-8')
    todo.close()


def vol_set(vi):
    match = re.search(r'\d+', vi)
    sound = Sound()
    if match:
        vol = int(match.group())  # Преобразование найденного числа в int
        vol = 100 if vol > 100 else vol
        sound.volume_set(vol)
        print(f'Громкость поставлена на {vol}')
    else:
        print("Число не найдено в строке.")


def vol_off():
    sound = Sound()
    sound.mute()


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle("Всплывающее меню")

        # Создаем кнопку, на которую можно будет щелкнуть для открытия меню
        button = QPushButton("Показать Меню", self)
        button.move(50, 50)

        # Создаем всплывающее меню
        menu = QMenu(self)

        # Создаем действия (пункты меню)
        action1 = QAction("Действие 1", self)
        action2 = QAction("Действие 2", self)
        action3 = QAction("Действие 3", self)

        # Добавляем действия в меню
        menu.addAction(action1)
        menu.addAction(action2)
        menu.addSeparator()  # Разделитель
        menu.addAction(action3)

        # Связываем меню с кнопкой
        button.setMenu(menu)


class Nika(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('beta.ui', self)
        self.ListenBTN.clicked.connect(self.listen)
        menu = QMenu(self)
        act1 = QAction('Промпты', self)
        act2 = QAction('Ссылки', self)
        act1.triggered.connect(self.prompt)
        menu.addAction(act1)
        menu.addSeparator()
        menu.addAction(act2)
        menu.setStyleSheet("QMenu { background-color: #8388a4; }")
        self.MenuBTN.setMenu(menu)

        self.speaker = Speaker()

    def closeEvent(self, event):
        print('Сохранение...')
        conf = open('config.txt', 'w', encoding='utf-8')
        conf.write(f'all_patterns: {", ".join(all_patterns)}\n')
        for k, v in commands_dict['commands'].items():
            v = ', '.join(v)
            conf.write(f'{k}: {v}\n')
        conf.write('!')
        conf.close()

    def listen(self):
        f = True
        voice_input = record_and_recognize_audio()
        if voice_input is None:
            return
        print(f'Вы сказали: {voice_input}')
        for i in commands_dict['commands']['vol_up']:
            lsti = i.split(' ')
            if lsti == voice_input.split(' ')[:len(lsti)]:
                vol_set(voice_input)
                play_sound('./successful/successful', 3)
                return
        for i in commands_dict['commands']['search_youtube']:
            lsti = i.split(' ')
            if lsti == voice_input.split(' ')[:len(lsti)]:
                seached = voice_input.split(' ')[len(lsti):]
                search_youtube(seached)
                play_sound('./successful/successful', 3)
                return
        for i in commands_dict['commands']['search_google']:
            lsti = i.split(' ')
            if lsti == voice_input.split(' ')[:len(lsti)]:
                seached = voice_input.split(' ')[len(lsti):]
                search_google(seached)
                play_sound('./successful/successful', 3)
                return
        for i in commands_dict['commands']['search_yandex_market']:
            lsti = i.split(' ')
            if lsti == voice_input.split(' ')[:len(lsti)]:
                seached = voice_input.split(' ')[len(lsti):]
                search_yandex_market(seached)
                play_sound('./successful/successful', 3)
                return
        for k, v in commands_dict['commands'].items():
            if voice_input in v:
                f = False
                play_sound('./successful/successful', 3)
                globals()[k]()
        if f:
            play_sound('./error/error', 3)

    def prompt(self):
        other_window = MyWindow()
        other_window.setParent(self)  # Устанавливаем текущее окно в качестве родителя
        other_window.show()
        print('dinahu')


if __name__ == "__main__":
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()
    app = QApplication(sys.argv)
    ex = Nika()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
