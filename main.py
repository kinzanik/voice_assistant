import os
import random as r
import re
import subprocess as sb
import sys
import webbrowser as wb
from time import sleep
import speech_recognition
import torch
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction, QWidget, QTableWidgetItem
from pydub import AudioSegment
from pydub.playback import play
from sound import Sound

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
names_of_func = []
urls = {}
commands_dict = {
    'commands': {

    }
}

curs = 1
for i in config[1:]:
    curs += 1
    i = i.rstrip()
    if i == '!':
        break
    i = i.split(': ')
    name_func, name, patterns = i[0], i[1], i[2]
    lst_patterns = patterns.split(', ')
    names_of_func.append(name)
    commands_dict['commands'][name_func] = lst_patterns

for i in config[curs:]:
    i = i.rstrip()
    if i == '!':
        break
    i = i.split(': ')
    name, url = i[0], i[1]
    urls[name] = url


not_banned = ['qwertyuiopasdfghjklzxcvbnmйцукенгшщзхъфывапролджэячсмитьбю1234567890 ']


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def safe_config():
    print('Сохранение изменений...')
    conf = open('config.txt', 'w', encoding='utf-8')
    conf.write(f'all_patterns: {", ".join(all_patterns)}\n')
    klv = 0
    for k, v in commands_dict['commands'].items():
        v = ', '.join(v)
        conf.write(f'{k}: {names_of_func[klv]}: {v}\n')
        klv += 1
    conf.write('!\n')
    for k, v in urls.items():
        conf.write(f'{k}: {v}\n')
    conf.write('!')
    conf.close()


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


def universal_func(func, method):
    pass


def greeting():
    play_sound('./greeting/greeting', 4)


def open_youtube():
    wb.open(urls['youtube'])


def search_youtube(vi):
    if len(vi) == 0:
        pass
    search = '+'.join(vi)
    search_url = f'https://www.youtube.com/results?search_query={search}'
    wb.open(search_url)


def open_google():
    wb.open(urls['google'])


def search_google(vi):
    if len(vi) == 0:
        pass
    search = '+'.join(vi)
    search_url = f'https://www.google.com/search?q={search}'
    wb.open(search_url)


def open_yandex_market():
    search_url = 'https://market.yandex.ru/'
    wb.open(search_url)


def search_yandex_market(vi):
    if len(vi) == 0:
        play_sound('./search_error/search_error', 3)
    search = '+'.join(vi)
    search_url = f'https://market.yandex.ru/search?text={search}'
    wb.open(search_url)


def joke():
    wb.open(urls['шуточное видео'])


def playlist():
    wb.open('https://www.youtube.com/watch?v=4W2ymUkg9Xg&list=PLmzD5x'
            'eXPBC8AHAZiTMOMhts-H2EsfAsc&ab_channel=Ren-Topic')


def open_vk():
    wb.open('https://vk.com/feed')


def run_dota():
    dota_path = r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\bin\win64\dota2.exe"
    sb.run([dota_path])


def run_telegram():
    telegram_path = r'C:\Users\turbo ishak\AppData\Roaming\Telegram Desktop\Telegram.exe'
    print(telegram_path)
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


class PromptChange(QWidget):
    def __init__(self, name_of_func, func, prompts_list):
        self.name_of_func = name_of_func
        self.func = func
        self.prompts_list = prompts_list
        self.selected_item = None
        self.new_prompt = ''
        super().__init__()
        uic.loadUi('new_prompt.ui', self)
        self.nameLabel.setText(name_of_func)
        self.funcLabel.setText(func)
        self.addBTN.clicked.connect(self.add)
        self.deleteBTN.clicked.connect(self.delete)
        for i in prompts_list:
            self.promptsList.addItem(i)

    def closeEvent(self, event):
        pass

    def add(self):
        self.new_prompt = self.newPrompt.text().lower()
        if self.new_prompt == '':
            self.infoLabel.setStyleSheet("color: rgb(255, 79, 79);")
            self.infoLabel.setText('Вы ничего не ввели')
            return

        if self.new_prompt in all_patterns:
            self.infoLabel.setStyleSheet("color: rgb(255, 79, 79);")
            self.infoLabel.setText('Такой промпт уже существует.')
            return

        for i in self.new_prompt:
            if i not in not_banned[0]:
                self.infoLabel.setStyleSheet("color: rgb(255, 79, 79);")
                self.infoLabel.setText(f'Недопустимый символ: {i}')
                return
        self.promptsList.addItem(self.new_prompt)
        commands_dict['commands'][self.name_of_func].append(self.new_prompt)
        all_patterns.append(self.new_prompt)
        self.infoLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.infoLabel.setText('Добавлено!')
        self.new_prompt = ''
        self.newPrompt.setText('')

        safe_config()

    def delete(self):
        selected_item = self.promptsList.currentItem()
        if selected_item is None:
            self.infoLabel.setStyleSheet("color: rgb(255, 255, 255);")
            self.infoLabel.setText('Вы не выбрали элемент')
        else:
            self.promptsList.takeItem(self.promptsList.row(selected_item))
            commands_dict['commands'][self.name_of_func].remove(selected_item.text())
            all_patterns.remove(selected_item.text())
            self.infoLabel.setStyleSheet("color: rgb(255, 255, 255);")
            self.infoLabel.setText('Удалено!')


class PromptsSettings(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('prompts.ui', self)
        row = 0
        for i in commands_dict['commands'].keys():
            self.allPromptsList.addItem(f'{i} - {names_of_func[row]}')
            row += 1

        self.changeBTN.clicked.connect(self.change)

    def change(self):
        selected_item = self.allPromptsList.currentItem().text()
        lst_selected = selected_item.split(' - ')
        func_name = lst_selected[0]
        func = lst_selected[1]
        prompts = commands_dict['commands'][func_name]
        self.new_wind = PromptChange(func_name, func, prompts)
        self.new_wind.show()


class UrlsPaths(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('urls_paths.ui', self)
        self.urlpathTable.setRowCount(len(urls.keys()))
        self.urlpathTable.setColumnCount(2)
        self.urlpathTable.setColumnWidth(0, 150)
        self.urlpathTable.setColumnWidth(1, 316)
        self.urlpathTable.setHorizontalHeaderLabels(['Название', 'Ссылка/путь'])

        row = 0
        for key, value in urls.items():
            key_item = QTableWidgetItem(str(key))
            url_item = QTableWidgetItem(str(value))
            self.urlpathTable.setItem(row, 0, key_item)
            self.urlpathTable.setItem(row, 1, url_item)
            row += 1

        self.safeBTN.clicked.connect(self.safe)

    def safe(self):
        for row in range(len(urls.keys())):
            key = self.urlpathTable.item(row, 0).text()
            value = self.urlpathTable.item(row, 1).text()
            if value == '':
                value = 'None'
            urls[key] = value
        self.infoLabel.setText('Успешно!')
        safe_config()


class Nika(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('beta.ui', self)
        self.ListenBTN.clicked.connect(self.listen)
        menu = QMenu(self)
        act1 = QAction('Промпты', self)
        act2 = QAction('Ссылки', self)
        act1.triggered.connect(self.prompt)
        act2.triggered.connect(self.urls_pats)
        menu.addAction(act1)
        menu.addSeparator()
        menu.addAction(act2)
        menu.setStyleSheet("QMenu { background-color: #8388a4; }")
        self.MenuBTN.setMenu(menu)

        self.speaker = Speaker()

    def closeEvent(self, event):
        safe_config()

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
        self.other_window = PromptsSettings()
        self.other_window.show()

    def urls_pats(self):
        self.other_window = UrlsPaths()
        self.other_window.show()


if __name__ == "__main__":
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()
    app = QApplication(sys.argv)
    ex = Nika()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
