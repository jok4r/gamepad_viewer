import XInput
import time
import json
import sys

# Словарь соответствий битов и кнопок
std_buttons_mapping = {
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


def wait_button():
    while True:
        state = XInput.get_state(0)
        if buttons_value := state.Gamepad.wButtons:
            break
    return buttons_value


def get_pressed_buttons(buttons_value):
    pressed_buttons = []
    for bit_position, button_name in std_buttons_mapping.items():
        if buttons_value & (1 << bit_position):
            pressed_buttons.append(button_name)
    return pressed_buttons


# Функция для тестирования всех кнопок
def test_all_buttons():
    # state = XInput.get_state(0)
    # buttons_value = state.Gamepad.wButtons
    print(f'Press any button')
    buttons_value = wait_button()
    print(f'Buttons value: {buttons_value}')
    pressed_buttons = get_pressed_buttons(buttons_value)
    print("Pressed buttons:", pressed_buttons)


# Последовательное тестирование кнопок
def sequential_button_test():
    button_states = {}
    for button_name in std_buttons_mapping.values():
        # input(f"Press and hold {button_name}, then press Enter...")
        print(f'Press {button_name}')
        buttons_value = wait_button()
        buttons_value = len(bin(buttons_value)[2:])-1
        # button_states[button_name] = buttons_value
        button_states[int(buttons_value)] = button_name
        print(f"Button {button_name} has value {buttons_value}")
        time.sleep(1)

    return button_states


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage script.py [test|write]')
        sys.exit(1)
    if sys.argv[1] == 'test':
        test_all_buttons()
    elif sys.argv[1] == 'write':
        button_states = sequential_button_test()
        print("Button states:", button_states)
        with open('buttons_mapping.json', 'w') as f:
            json.dump(button_states, f, indent=4)
    else:
        raise RuntimeError(f'Unknown option: {sys.argv[1]}')
