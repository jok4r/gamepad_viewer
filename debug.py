import pygame
import time

# Инициализация Pygame и джойстиков
pygame.init()
pygame.joystick.init()

# Проверка наличия подключенного геймпада
if pygame.joystick.get_count() == 0:
    raise Exception("No gamepad detected!")

# Получение первого подключенного геймпада
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Функция для получения данных всех осей
def get_all_axes():
    pygame.event.pump()
    axes = {}
    num_axes = joystick.get_numaxes()
    for i in range(num_axes):
        axis_value = joystick.get_axis(i)
        axis_percentage = int((axis_value + 1) / 2 * 100)
        axes[f'Axis {i}'] = axis_percentage
    return axes

if __name__ == "__main__":
    try:
        while True:
            axes_data = get_all_axes()
            for axis, percentage in axes_data.items():
                print(f"{axis}: {percentage}%")
            print("=" * 30)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Отладка завершена.")
    finally:
        pygame.quit()
