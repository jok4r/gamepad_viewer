import json
import os


mappings_path = 'buttons_mapping.json'
if os.path.isfile(mappings_path):
    with open(mappings_path, encoding='utf-8') as f:
        buttons_mapping = json.load(f)
else:
    print(f'{mappings_path} not found, using standard mappings. To remap buttons, use "./test_buttons.py write"')
    buttons_mapping = {
        0: 'DPAD_UP',
        1: 'DPAD_DOWN',
        2: 'DPAD_LEFT',
        3: 'DPAD_RIGHT',
        4: 'START',
        5: 'BACK',
        6: 'LEFT_THUMB',
        7: 'RIGHT_THUMB',
        8: 'LEFT_SHOULDER',
        9: 'RIGHT_SHOULDER',
        12: 'A',
        13: 'B',
        14: 'X',
        15: 'Y'
    }


def get_pressed_buttons(buttons_value):
    pressed_buttons = []
    for bit_position, button_name in buttons_mapping.items():
        if buttons_value & (1 << int(bit_position)):
            pressed_buttons.append(button_name)
    return pressed_buttons
