import subprocess
import logging

class ProximitySensorManager:
    CMD_FILE = "/sys/class/sec/tsp/cmd"

    @staticmethod
    def set_proximity_sensor(state: bool):
        try:
            command = f"ear_detect_enable,{1 if state else 0}"
            with open(ProximitySensorManager.CMD_FILE, "w") as f:
                f.write(command)
            logging.info(f"Proximity sensor {'enabled' if state else 'disabled'}. Command: {command}")
        except Exception as e:
            logging.error(f"Failed to change proximity sensor state: {e}")


def monitor_proximity_events():
    logging.info("Monitoring proximity sensor events...")

    try:
        process = subprocess.Popen(
            ["journalctl", "-f", "-n", "0"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        screen_on = None
        unlocked = False

        for line in iter(process.stdout.readline, ""):
            if not line:
                continue

            if "hfd-service" in line:
                if "LedsDummy on" in line and screen_on is not False:
		    logging.info("Disabling proximity sensor.")
                    screen_on = False
                    unlocked = False
                    ProximitySensorManager.set_proximity_sensor(False)
                elif "LedsDummy off" in line and screen_on is not True:
		    logging.info("Enabling proximity sensor.")
                    screen_on = True
                    ProximitySensorManager.set_proximity_sensor(True)

            if "lomiri" in line and "gkr-pam: unlocked login keyring" in line and not unlocked:
		logging.info("Device unlocked. Disabling proximity sensor.")
                unlocked = True
                ProximitySensorManager.set_proximity_sensor(False)

    except KeyboardInterrupt:
        logging.info("Monitoring stopped by user.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    monitor_proximity_events()
