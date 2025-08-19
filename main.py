from tkinter import *
from typing import Dict
import pyautogui
import keyboard

Point = pyautogui.Point

# 설정 모드 및 마우스 위치 변수
is_set_mode: bool = True
positions: Dict[str, Point] = {}

# Window 구성 파라메터
window = Tk()
window.title("Apply Macro")
window.geometry("800x400")
window.resizable(False, False)

default_font = ("Helvetica", 14, "bold")
default_color: Dict[bool, str] = {True: "skyblue", False: "pink"}

# 체크박스의 상태를 저장할 Tkinter 전용 변수
is_click_zero_after = BooleanVar()
is_click_zero_after.set(False)


# 메인 함수
def change_set_mode():
    global is_set_mode
    is_set_mode = not is_set_mode
    mode_label.config(
        bg=default_color[is_set_mode],
        text="설정 모드 " + ("켜짐" if is_set_mode else "꺼짐"),
    )
    mode_button.config(
        text="끄기" if is_set_mode else "켜기",
    )


def update_mouse_position():
    try:
        x, y = pyautogui.position()
        mouse_label.config(text=f"마우스 위치: ({x}, {y})")
        window.after(100, update_mouse_position)
    except pyautogui.FailSafeException:
        print("Fail-safe triggered. Exiting.")
        window.quit()


def add_position(key: str):
    positions[key] = pyautogui.position()
    position_labels[int(key)].config(
        bg=default_color[True],
        text=f"위치{key} ({positions[key].x}, {positions[key].y})로 할당됨",
    )


def click_given_position(key: str):
    pyautogui.click(x=positions[key].x, y=positions[key].y)


# --- 수정된 부분 ---
def handle_key_press(event):
    global is_set_mode
    key: str = event.name
    if not ("0" <= key <= "9"):
        return

    if is_set_mode:
        add_position(key)
    else:
        if is_click_zero_after.get() and "1" <= key <= "9":
            try:
                click_given_position(key)
                click_given_position("0")
                print(f"{key}번 위치 클릭 후 0번 위치 클릭 완료")
            except KeyError as e:
                print(f"클릭 실패: 위치 {e.args[0]}이(가) 할당되지 않았습니다.")
        else:
            try:
                click_given_position(key)
            except KeyError:
                print(f"클릭 실패: 위치 {key}이(가) 할당되지 않았습니다.")


# GUI
option_frame = Frame(window)
option_frame.pack(side="top", anchor="w", padx=10, pady=10)

mode_label = Label(
    option_frame,
    text="설정 모드 " + ("켜짐" if is_set_mode else "꺼짐"),
    bg=default_color[is_set_mode],
    font=default_font,
)
mode_label.grid(row=0, column=0)

mode_button = Button(
    option_frame,
    text="끄기" if is_set_mode else "켜기",
    font=default_font,
    command=change_set_mode,
)
mode_button.grid(row=0, column=1, padx=5)

mouse_label = Label(
    option_frame,
    text="(0,0)",
    font=default_font,
)
mouse_label.grid(row=0, column=2, padx=5)

click_zero_checkbox = Checkbutton(
    option_frame,
    text="1~9 클릭 후 0번 위치 클릭",
    font=default_font,
    variable=is_click_zero_after,
)
click_zero_checkbox.grid(row=0, column=3, padx=10)


position_frame = Frame(window)
position_frame.pack(side="left", anchor="n", padx=10)

position_labels: list[Label] = []
for i in range(10):
    is_assign = str(i) in positions
    position_label_text = f"위치{i} " + (
        f"({positions[str(i)].x}, {positions[str(i)].y})로 할당됨"
        if is_assign
        else "할당 되지 않음"
    )

    position_label = Label(
        position_frame,
        text=position_label_text,
        bg=default_color[is_assign],
        font=default_font,
        width=40,
        anchor="w",
    )
    position_label.pack(anchor="w", pady=2)
    position_labels.append(position_label)

update_mouse_position()
keyboard.on_press(handle_key_press)

window.mainloop()
