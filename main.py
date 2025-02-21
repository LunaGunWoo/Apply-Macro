import pyautogui
import keyboard
from models import Dict, Point

positions: Dict[str, Point] = {}
is_set_mode: bool = True


def add_position(key: str):
    positions[key] = pyautogui.position()
    print(key + " Key was set position.")


def click_given_position(key: str):
    pyautogui.click(x=positions[key].x, y=positions[key].y)


def change_set_mode(to_be: bool):
    global is_set_mode
    is_set_mode = to_be
    print(f"Set Mode Is " + ("Activated." if is_set_mode else "Deactivated."))


change_set_mode(True)


def handle_key_press(event):
    key: str = event.name
    if key == "s":
        change_set_mode(True)
    elif key == "S":
        change_set_mode(False)
    elif is_set_mode:
        add_position(key)
    else:
        try:
            click_given_position(key)
        except KeyError:
            print("설정부터 해주세요")


keyboard.on_press(handle_key_press)
keyboard.wait()
