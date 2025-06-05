
## Systemd integration - systemd.sh is Wayland specific.

Remember: Script is pointing to /opt/waybind.sh by default. Unless you edit systemd.sh.

    chmod +x systemd.sh

    sudo cp waybind.py /opt

    ./systemd.sh


✅ After Installation

    The service will automatically run on login.

    To check status:   systemctl --user status waybind.service

## Make sure it runs on system start, this should be done by default with systemd.sh:

        systemctl --user enable waybind.service

To stop it(and relaunch if you make keybinding changes):

    systemctl --user restart waybind.service
