import time
from flask import Flask, jsonify, render_template
import threading
import logging
import XInput
import os
import sys
from buttons import get_pressed_buttons, buttons_mapping

abs_pth = os.path.abspath(sys.argv[0])
this_dir = os.path.dirname(abs_pth)
template_dir = os.path.abspath(os.path.join(this_dir, 'templates'))
static_dir = os.path.abspath(os.path.join(this_dir, 'static'))
# print(f'{template_dir=}')
app = Flask(__name__, root_path=this_dir, template_folder=template_dir, static_folder=static_dir)
# os.chdir(this_dir)
# print(f'{this_dir=}')
# app = Flask(__name__)

# lt_percentage = 0
# rt_percentage = 0
g_data = {}

# Отключение логирования запросов Flask
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


# Функция для получения данных с геймпада
def get_gamepad_data():
    global g_data
    # gamepad = XInput.get_connected()[0]  # Получаем первый подключенный геймпад
    state = XInput.get_state(0)

    lt = state.Gamepad.bLeftTrigger / 255.0  # Преобразуем значение в диапазон от 0 до 1
    rt = state.Gamepad.bRightTrigger / 255.0  # Преобразуем значение в диапазон от 0 до 1

    # ABXY Buttons
    pressed_buttons = get_pressed_buttons(state.Gamepad.wButtons)
    # print(f'Buttons: {state.Gamepad.wButtons}')
    # print(f'buttons: {pressed_buttons}')

    # Thumbs (max 32768)
    lx = int(state.Gamepad.sThumbLX / 32768 * 100)
    ly = int(state.Gamepad.sThumbLY / 32768 * 100)
    rx = int(state.Gamepad.sThumbRX / 32768 * 100)
    ry = int(state.Gamepad.sThumbRY / 32768 * 100)
    # print(f'sThumbLX: {state.Gamepad.sThumbLX}')
    # print(f'sThumbLY: {state.Gamepad.sThumbLY}')
    # print(f'sThumbRX: {state.Gamepad.sThumbRX}')
    # print(f'sThumbRY: {state.Gamepad.sThumbRY}')

    g_data = {
        'lt': int(lt * 100),
        'rt': int(rt * 100),
        'lx': lx,
        'ly': ly,
        'rx': rx,
        'ry': ry,
    }

    for button in buttons_mapping.values():
        g_data[button] = button in pressed_buttons

    # print(g_data)

    return g_data


# Запуск функции получения данных в отдельном потоке
def update_gamepad_data():
    # global lt_percentage, rt_percentage
    global g_data
    while True:
        g_data = get_gamepad_data()
        # lt_percentage = g_data['lt_percentage']
        # rt_percentage = g_data['rt_percentage']
        time.sleep(0.1)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data')
def data():
    # return jsonify({'lt': lt_percentage, 'rt': rt_percentage})
    return jsonify(g_data)


if __name__ == "__main__":
    threading.Thread(target=update_gamepad_data, daemon=True).start()
    if len(sys.argv) > 2:
        app.run(host=sys.argv[1], port=int(sys.argv[2]))
    else:
        app.run()
