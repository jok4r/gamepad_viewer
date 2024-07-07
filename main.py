import time
from flask import Flask, jsonify, render_template
import threading
import logging
import XInput
import os
import sys

abs_pth = os.path.abspath(sys.argv[0])
this_dir = os.path.dirname(abs_pth)
template_dir = os.path.abspath(os.path.join(this_dir, 'templates'))
# print(f'{template_dir=}')
app = Flask(__name__, root_path=this_dir, template_folder=template_dir)
# os.chdir(this_dir)
# print(f'{this_dir=}')
# app = Flask(__name__)

lt_percentage = 0
rt_percentage = 0

# Отключение логирования запросов Flask
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Функция для получения данных с геймпада
def get_gamepad_data():
    # gamepad = XInput.get_connected()[0]  # Получаем первый подключенный геймпад
    state = XInput.get_state(0)

    lt = state.Gamepad.bLeftTrigger / 255.0  # Преобразуем значение в диапазон от 0 до 1
    rt = state.Gamepad.bRightTrigger / 255.0  # Преобразуем значение в диапазон от 0 до 1

    lt_percentage = int(lt * 100)
    rt_percentage = int(rt * 100)

    return lt_percentage, rt_percentage

# Запуск функции получения данных в отдельном потоке
def update_gamepad_data():
    global lt_percentage, rt_percentage
    while True:
        lt, rt = get_gamepad_data()
        lt_percentage = lt
        rt_percentage = rt
        time.sleep(0.1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    return jsonify({'lt': lt_percentage, 'rt': rt_percentage})

if __name__ == "__main__":
    threading.Thread(target=update_gamepad_data, daemon=True).start()
    app.run()
