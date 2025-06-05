#!/usr/bin/env python3
# <Waybind> Copyright (C) 2025 JJ Posti (techtimejourney.net)
# GPL Version 2 License
import os
import sys
import yaml
import time
import threading
import subprocess
import getpass
from evdev import InputDevice, categorize, ecodes, list_devices

CONFIG_PATH = f"/home/{getpass.getuser()}/config.yaml"

MODIFIER_KEYS = {
    ecodes.KEY_LEFTCTRL, ecodes.KEY_RIGHTCTRL,
    ecodes.KEY_LEFTALT, ecodes.KEY_RIGHTALT,
    ecodes.KEY_LEFTMETA, ecodes.KEY_RIGHTMETA
}

MODIFIER_NAMES = {
    ecodes.KEY_LEFTCTRL: "CTRL", ecodes.KEY_RIGHTCTRL: "CTRL",
    ecodes.KEY_LEFTALT: "ALT", ecodes.KEY_RIGHTALT: "ALT",
    ecodes.KEY_LEFTMETA: "SUPER", ecodes.KEY_RIGHTMETA: "SUPER"
}


def load_bindings():
    if not os.path.exists(CONFIG_PATH):
        return {}
    try:
        with open(CONFIG_PATH, "r") as f:
            data = yaml.safe_load(f) or {}
            return {
                tuple(sorted(combo.upper().split("+"))): cmd
                for combo, cmd in data.get("bindings", {}).items()
            }
    except Exception as e:
        print(f"Error loading config: {e}")
        return {}


def is_keyboard_device(dev):
    try:
        if "keyboard" in dev.name.lower():
            return True
        keys = dev.capabilities().get(ecodes.EV_KEY, [])
        return ecodes.KEY_A in keys and ecodes.KEY_ENTER in keys
    except Exception:
        return False


def find_keyboard_devices():
    devices = []
    for path in list_devices():
        try:
            dev = InputDevice(path)
            if is_keyboard_device(dev):
                devices.append(path)
        except Exception:
            continue
    return devices


def keycode_to_name(code):
    if code in MODIFIER_NAMES:
        return MODIFIER_NAMES[code]
    try:
        return ecodes.KEY[code].replace("KEY_", "").upper()
    except KeyError:
        return None


def read_keyboard_events(bindings, path):
    try:
        dev = InputDevice(path)
    except Exception as e:
        print(f"Failed to open device {path}: {e}")
        return

    pressed = set()
    for event in dev.read_loop():
        if event.type != ecodes.EV_KEY:
            continue

        e = categorize(event)
        if e.keystate == e.key_down:
            pressed.add(e.scancode)
        elif e.keystate == e.key_up:
            pressed.discard(e.scancode)

        names = [keycode_to_name(c) for c in pressed]
        combo = tuple(sorted(filter(None, names)))

        if e.keystate == e.key_down and combo in bindings:
            cmd = bindings[combo]
            try:
                subprocess.Popen(cmd, shell=True)
            except Exception as e:
                print(f"Failed to execute {cmd}: {e}")


def run_service():
    bindings = load_bindings()
    if not bindings:
        print("No bindings loaded.")
        return

    devices = find_keyboard_devices()
    if not devices:
        print("No keyboard devices found. Ensure you have permission to access /dev/input.")
        return

    for path in devices:
        threading.Thread(
            target=read_keyboard_events,
            args=(bindings, path),
            daemon=True
        ).start()

    # Do not block the terminal — just keep running quietly
    print("Waybind started.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Waybind stopped.")


if __name__ == "__main__":
    run_service()
