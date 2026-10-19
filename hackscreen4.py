#!/usr/bin/env python3
# DEAD SIGNAL - Dark Horror Terminal Sequence
# Run: python3 hackscreen4.py

import os, sys, time, random, shutil, math, struct, wave, subprocess
from datetime import datetime

SPEED = 1.0

R = "\033[91m"; DR = "\033[31m"; G = "\033[92m"; C = "\033[96m"
Y = "\033[93m"; W = "\033[97m"; D = "\033[90m"; B = "\033[1m"; X = "\033[0m"
HIDE = "\033[?25l"; SHOW = "\033[?25h"

def _header():
    name = "E N T I T Y   I N T E R F A C E".center(56)
    left, right = "  DEAD SIGNAL // SYSTEM COMPROMISED", "[ CORRUPTED ]   "
    mid = left + " " * max(0, 56 - len(left) - len(right)) + right
    return (f"{DR}{B}╔{'═' * 56}╗\n║{R}{name}{DR}║\n╟{'─' * 56}╢\n"
            f"║{mid}║\n╚{'═' * 56}╝{X}")

HEADER = _header()

SKULL = r"""
                 .ed"""" """$$$$be.
               -"           ^""**$$$e.
             ."                   '$$$c
            /                      "4$$b
           d  3                      $$$$
           $  *                   .$$$$$$
          .$  ^c           $$$$$e$$$$$$$$.
          d$L  4.         4$$$$$$$$$$$$$$b
          $$$$b ^ceeeee.  4$$ECL.F*$$$$$$$
  e$""=. $$$$$$d$$$$$$$d  $$$$$$$d$$$$$$$P
  $---   *$$$$$$$$$$$$$$  "$$$$$$$###$$$"
          "$$$C***$$$$*"    "$$$$$$$$$$"
           ^r" =*""         '$$$$$$$$$P
            '                 "$$$$$$P
                               '$$$$P
"""

SOUND = bool(shutil.which("termux-media-player"))
SND_DIR = os.path.expanduser("~/.deadsignal")
RATE = 22050
SOUNDS = {}

def _write(name, samples):
    path = os.path.join(SND_DIR, name + ".wav")
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(
            struct.pack("<h", max(-32767, min(32767, int(s * 32767)))) for s in samples))
    return path

def _tone(freq, dur, vol=0.5, decay=False):
    n = int(RATE * dur)
    return [vol * ((1 - i / n) if decay else 1.0) * math.sin(2 * math.pi * freq * i / RATE)
            for i in range(n)]

def _silence(dur):
    return [0.0] * int(RATE * dur)

def _noise(dur, vol=0.4):
    n = int(RATE * dur)
    return [vol * random.uniform(-1, 1) for _ in range(n)]

def init_sound():
    global SOUND
    if not SOUND:
        return
    try:
        os.makedirs(SND_DIR, exist_ok=True)
        SOUNDS["beep"] = _write("beep", _tone(1400, 0.08, 0.4, True))
        SOUNDS["tick"] = _write("tick", _tone(600, 0.05, 0.3, True))
        SOUNDS["alarm"] = _write("alarm", (_tone(900, 0.15, 0.6) + _tone(450, 0.15, 0.6)) * 2)
        SOUNDS["static"] = _write("static", _noise(0.8, 0.4))
        SOUNDS["heartbeat"] = _write(
            "heartbeat",
            _tone(45, 0.18, 0.9, True) + _silence(0.1) + _tone(38, 0.22, 0.9, True) + _silence(0.4)
        )
        drone = [a + b for a, b in zip(_tone(40, 5, 0.5), _tone(42.5, 5, 0.5))]
        SOUNDS["drone"] = _write("drone", drone)
    except Exception:
        SOUND = False

def sfx(name):
    if not SOUND or name not in SOUNDS:
        return
    try:
        subprocess.Popen(["termux-media-player", "play", SOUNDS[name]],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

def speak(text, pitch=0.2, rate=0.6):
    if not SOUND:
        return
    try:
        subprocess.Popen(["termux-tts-speak", "-p", str(pitch), "-r", str(rate), text],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

def wait(s):
    time.sleep(s * SPEED)

def clear():
    os.system("clear")

def vibrate(ms=200):
    os.system(f"termux-vibrate -d {ms} >/dev/null 2>&1")

def ts():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

def rhex(n):
    return "".join(random.choice("0123456789abcdef") for _ in range(n))

def glitch(text, chance=0.25):
    junk = "▓▒░§Ж#@%$?!/\\†‡☠"
    return "".join(random.choice(junk) if (c != " " and random.random() < chance) else c
                   for c in text)

def typewrite(text, color=D, delay=0.035, end="\n"):
    sys.stdout.write(color)
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay * SPEED * random.uniform(0.5, 1.4))
    sys.stdout.write(X + end)

def glitch_print(text, color=R, times=8):
    for _ in range(times):
        sys.stdout.write("\r" + color + B + glitch(text, 0.35) + X + "      ")
        sys.stdout.flush()
        time.sleep(0.06)
    sys.stdout.write("\r" + color + B + text + X + "      \n")

def log(tag, msg, color=G, delay=0.22):
    print(f"{D}{ts()}{X} {color}{B}[{tag}]{X} {msg}")
    if tag in ("BREACH", "ENTITY", "CRITICAL"):
        sfx("alarm")
    elif tag == "OK":
        sfx("beep")
    wait(delay * random.uniform(0.7, 1.4))

def bar(label, steps=25, speed=0.06, color=R):
    for i in range(steps + 1):
        fill = "█" * i + "░" * (steps - i)
        sys.stdout.write(f"\r {W}{label:<18}{X}{color}{fill}{X} {W}{int(i / steps * 100):3d}%{X}")
        sys.stdout.flush()
        time.sleep(speed * SPEED * random.uniform(0.3, 1.8))
    print()

def flicker(times=6, color=R):
    sfx("static")
    cols = shutil.get_terminal_size().columns
    for i in range(times):
        clear()
        if i % 2 == 0:
            for _ in range(random.randint(4, 10)):
                print(color + glitch("█" * cols, 0.45) + X)
        time.sleep(random.uniform(0.04, 0.15))
    clear()

def blood(seconds=2.5):
    cols = shutil.get_terminal_size().columns
    drops = [0] * cols
    end = time.time() + seconds * SPEED
    while time.time() < end:
        line = ""
        for i in range(cols):
            if random.random() < 0.05:
                drops[i] = random.randint(3, 12)
            if drops[i] > 0:
                line += random.choice([R, DR]) + random.choice("█▓▒│†") + X
                drops[i] -= 1
            else:
                line += " "
        print(line)
        time.sleep(0.04)

def intro():
    clear()
    sfx("drone")
    wait(1.2)
    steps = [
        "> establish low-frequency peer link...",
        "> handshake bypassed.",
        "> foreign signature intercepted.",
        "> port 0: unauthorized observer presence detected."
    ]
    for s in steps:
        typewrite(s, D, 0.04)
        wait(0.7)
    wait(0.8)
    speak("I am inside.")
    sfx("static")
    glitch_print("> AN UNKNOWN PRESENCE CLAIMS OWNERSHIP.", R, 10)
    vibrate(300)
    wait(1.5)

def horror():
    flicker(6)
    sfx("drone")
    print(DR + B + SKULL + X)
    wait(1.5)
    lines = [
        "I SEE YOU.",
        "LOOK AWAY FROM THE SCREEN.",
        "I CAN HEAR YOUR BREATHING.",
        "THE CAMERA CANNOT SAVE YOU.",
        "THERE IS NO DISCONNECT BUTTON."
    ]
    for i, t in enumerate(lines):
        speak(t.lower())
        typewrite("  " + t, R, 0.08)
        sfx("heartbeat")
        vibrate(250)
        wait(2.0)
        if i % 2 == 1:
            flicker(3)
            print(R + B + SKULL + X)

def countdown(n=15):
    clear()
    alerts = {
        12: "Purging shadow copies...",
        8: "Disabling device peripherals...",
        4: "Core dump irrecoverable.",
        1: "Goodbye."
    }
    for i in range(n, -1, -1):
        col = R if i % 2 == 0 else W
        sys.stdout.write(f"\r{col}{B}  SYSTEM PURGE COMMENCING IN: 00:{i:02d}  {X}      ")
        sys.stdout.flush()
        if i in alerts:
            print(f"\n{D}{ts()}{X} {R}{B}[!]{X} {alerts[i]}")
        sfx("alarm" if i <= 5 else "tick")
        if i <= 5:
            vibrate(180)
        time.sleep(1.0 * SPEED)
    print()
    flicker(8)
    sfx("heartbeat")
    blood(2.5)
    clear()

def main():
    print(HIDE, end="")
    init_sound()
    intro()
    clear()
    print(HEADER + "\n")
    log("SCAN", "Target host acquired", Y, 0.4)
    bar("Infiltrating core", speed=0.1, color=R)
    log("ENTITY", "Host telemetry mirrored", R, 0.6)
    wait(1.0)
    horror()
    countdown(15)
    print(SHOW, end="")
    print(f"\n{R}{B}[!] SIGNAL LOST. HOST UNRESPONSIVE.{X}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(SHOW + f"\n{R}[!] Disconnect rejected.{X}")
    finally:
        print(SHOW, end="")
        
