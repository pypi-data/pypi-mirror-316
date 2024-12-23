import os
import configparser

enable_discharging_notification = True
enable_charging_notification = True

low_notification_expire_timeout = 0
critical_notification_expire_timeout = 0
discharging_notification_expire_timeout = 0
charging_notification_expire_timeout = 5000


def load():
    config_file_path = os.path.expanduser('~/.config/battery_notifier/config.ini')

    # Retrun if there's no user config file
    if not os.path.exists(config_file_path):
        return

    # Load config file
    _config = configparser.ConfigParser(allow_unnamed_section=True)
    _config.read(config_file_path)

    global enable_discharging_notification
    enable_discharging_notification = _config.getboolean("UNNAMED_SECTION", "enable_discharging_notification",
                                                         fallback=enable_discharging_notification)

    global enable_charging_notification
    enable_charging_notification = _config.getboolean("UNNAMED_SECTION", "enable_charging_notification",
                                                      fallback=enable_charging_notification)

    global low_notification_expire_timeout
    low_notification_expire_timeout = _config.getint("UNNAMED_SECTION", "low_notification_expire_timeout",
                                                     fallback=low_notification_expire_timeout)

    global critical_notification_expire_timeout
    critical_notification_expire_timeout = _config.getint("UNNAMED_SECTION", "critical_notification_expire_timeout",
                                                          fallback=critical_notification_expire_timeout)

    global discharging_notification_expire_timeout
    discharging_notification_expire_timeout = _config.getint("UNNAMED_SECTION",
                                                             "discharging_notification_expire_timeout",
                                                             fallback=discharging_notification_expire_timeout)

    global charging_notification_expire_timeout
    charging_notification_expire_timeout = _config.getint("UNNAMED_SECTION", "charging_notification_expire_timeout",
                                                          fallback=charging_notification_expire_timeout)
