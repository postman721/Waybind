#!/bin/bash

# Waybind systemd user service installer

SCRIPT_PATH="/opt/waybind.py"
SERVICE_DIR="$HOME/.config/systemd/user"
SERVICE_FILE="$SERVICE_DIR/waybind.service"

# Ensure waybind.py exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ waybind.py not found in $SCRIPT_PATH"
    exit 1
fi

# Create systemd user service directory
mkdir -p "$SERVICE_DIR"

# Write the service file
cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=Waybind - Global Keybind Launcher
After=graphical-session.target
Wants=graphical-session.target

[Service]
Type=simple
Environment=DISPLAY=:0
Environment=WAYLAND_DISPLAY=wayland-0
ExecStart=/bin/bash -c 'sleep 5 && exec /usr/bin/env python3 $SCRIPT_PATH'
Restart=always
RestartSec=2

[Install]
WantedBy=default.target
EOF

echo "✅ Created systemd user service at $SERVICE_FILE"

# Reload systemd, enable and start the service
systemctl --user daemon-reload
systemctl --user enable --now waybind.service

echo "✅ waybind.service enabled and started"

# Enable linger so the service runs at boot even if not logged into GUI
if loginctl enable-linger "$USER"; then
    echo "✅ Linger enabled for user $USER"
else
    echo "⚠️ Failed to enable linger (may require root or systemd-logind support)"
fi
