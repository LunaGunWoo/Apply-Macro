import re
import time
import win32api
import win32con
from pywinauto import Application, Desktop, keyboard, findwindows

# --- 설정 ---
parent_process_name = "MDmain.exe"
# 1. 인증번호 팝업창 제목
auth_popup_title = "대학 수강신청(과부하방지)"
# 2. 일반 경고 팝업창 제목 (메인 창과 이름이 같음)
warning_popup_title = "수강신청"
# 감시 간격 (초) - 값을 줄일수록 반응이 빨라지지만 CPU 사용량이 소폭 증가합니다.
search_interval = 0.05
# ------------


def combined_popup_handler():
    """
    두 종류의 팝업창을 동시에 감시하고 자동으로 처리합니다.
    """
    print("🚀 팝업 처리 통합 스크립트를 시작합니다...")
    print(f"   - '{auth_popup_title}' (인증번호)")
    print(f"   - '{warning_popup_title}' (일반 경고)")
    print("스크립트를 완전히 종료하려면 터미널에서 Ctrl+C를 누르세요. ⌨️")

    try:
        app = Application(backend="win32").connect(path=parent_process_name, timeout=10)
        print("✅ 부모 프로세스에 성공적으로 연결했습니다. 감시를 시작합니다.")

        while True:
            # --- 1. 인증번호 팝업(과부하방지) 처리 로직 ---
            try:
                auth_windows = findwindows.find_windows(title=auth_popup_title)
                if auth_windows:
                    print(f"\n✅ '{auth_popup_title}' 팝업 발견!")
                    popup_window = Desktop(backend="win32").window(
                        handle=auth_windows[0]
                    )
                    popup_window.set_focus()

                    auth_label = popup_window.child_window(auto_id="Label")
                    match = re.search(r"\[(\d+)\]", auth_label.window_text())

                    if match:
                        auth_code = match.group(1)
                        print(f"   - 인증번호 [{auth_code}] 추출 완료.")
                        edit_box = popup_window.child_window(auto_id="TextBox")
                        ok_button = popup_window.child_window(
                            title="OK", auto_id="OKButton"
                        )

                        print("   - 인증번호 입력 및 'OK' 클릭...")
                        edit_box.type_keys(auth_code, with_spaces=False)
                        time.sleep(0.05)  # 아주 짧은 딜레이
                        ok_button.click()
                        print("   - 처리 완료!")
                        time.sleep(0.05)  # 창 닫히는 시간 대기
            except Exception as e:
                print(f"\n... 인증번호 팝업 처리 중 오류: {e}")
                time.sleep(0.05)

            # --- 2. 일반 경고 팝업 처리 로직 ---
            try:
                warning_windows = app.windows(title=warning_popup_title)
                if len(warning_windows) >= 2:
                    print(f"\n⚠️  '{warning_popup_title}' 경고 팝업 감지!")
                    popup_handle = warning_windows[-1].handle

                    print("   - [1단계] 전역 Enter 키 입력을 시도합니다...")
                    keyboard.send_keys("{LEFT}")
                    keyboard.send_keys("{ENTER}")
                    time.sleep(0.05)

                    if len(app.windows(title=warning_popup_title)) < 2:
                        print("   - Enter 키로 팝업이 닫혔습니다.")
                        continue

                    print("   - [2단계] WM_CLOSE 메시지를 직접 보냅니다...")
                    win32api.PostMessage(popup_handle, win32con.WM_CLOSE, 0, 0)
                    time.sleep(0.05)
            except Exception as e:
                print(f"\n... 일반 경고 팝업 처리 중 오류: {e}")
                time.sleep(0.05)

            # --- 루프 대기 ---
            time.sleep(search_interval)

    except KeyboardInterrupt:
        print("\n사용자에 의해 프로그램이 종료되었습니다.")
    except Exception as e:
        print(f"\n❌ 최상위 오류 발생: {e}")


if __name__ == "__main__":
    combined_popup_handler()
