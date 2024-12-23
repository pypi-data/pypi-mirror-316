# battery_notifier

Sends desktop notifications for low and critical battery warnings, and optionally when charging/discharging state changes

## Installation

battery_notifier has the following dependencies available on PyPI:

- `pydbus`
- `PyGObject`

The package can be installed using [pipx](https://pipx.pypa.io/stable/installation/), e.g.:

```bash
pipx install battery_notifier
```

## Configuration

battery_notifier can be configured with a file located at `~/.config/battery_notifier/config.ini`, e.g.

```ini
# Enable/disable the notifications for discharging and charging
enable_discharging_notification = true
enable_charging_notification = true

# Notification timeouts in ms
low_notification_expire_timeout = 0
critical_notification_expire_timeout = 0
discharging_notification_expire_timeout = 0
charging_notification_expire_timeout = 5000
```

## Starting with systemd

A systemd service file is included in this repository which can be enabled and started like so:

```bash
# Copy the service file
cp battery_notifier.service ~/.local/share/systemd/user/

# Enable the service
systemctl --user enable battery_notifier

# Start the service
systemctl --user start battery_notifier
```
