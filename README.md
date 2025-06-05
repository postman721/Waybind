# 🧭 Waybind – Global Keybind Launcher for Linux

**Waybind** is a lightweight global keyboard shortcut daemon written in Python.  
It lets you define custom keybindings that launch commands.
Works on both **X11** and **Wayland**, depending on permissions and compositor behavior.

---

###### Note. Tested on Wayland - LabWc

## ✅ Features

- Global keybinding support using low-level input events
- Supports combinations like `CTRL+ALT+T`, `SUPER+W`, etc.
- Lightweight and daemonized – runs quietly in the background
- No `systemd` or desktop environment integration forced/required (but recommended).
- Minimal dependencies (Python only)

---

## 📦 Dependencies (Debian/Ubuntu)

Install the required packages:

```bash
sudo apt update
sudo apt install python3 python3-evdev python3-yaml
```

## 🔒 Permissions Required

Waybind listens to raw input devices under /dev/input/.
You must give your user permission to access them.
Add your user to the input group:

```bash
sudo usermod -aG input $USER
newgrp input
groups
```
Alternatively, you can run the waybind with sudo, but this is not recommended in long term.

## ⚙️ Configuration

Create a configuration file in your home directory named config.yaml. See my provided example from this repository.

## Notes:

    Key names must be uppercase and joined with +

    Commands must be shell-executable.


## 📂 Running

Make the script executable:
```bash
chmod +x waybind.py
```

Then run it as a background process.

```bash
./waybind.py &
```

🔁 Updating Keybindings

To update your shortcuts:

    Edit ~/config.yaml

    Restart the script manually:

```bash
pkill -f waybind.py

./waybind.py &
```

##### Note. Do not stay focused on the initial terminal that started waybind, applies to non-systemd and systemd ways. By completely staying in the initial terminal, the focus somehow breaks. After moving to another program/window/location the issue is gone.

### For Systemd

See Systemd.md for integration. Remember to adjust the script path to your own preference, or just use the same as I do, /opt.

#### Notice: systemd.sh in its current form is Wayland specific, but could of course be changed to X11 specific as well.









