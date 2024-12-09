import subprocess
import logging
import os


# Setup logging to output via journalctl
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%b %d %H:%M:%S')


class InputManager:
    INPUT_FILE = "/sys/class/sec/tsp/input/enabled"

    @staticmethod
    def set_input_state(state: bool):
        try:
            with open(InputManager.INPUT_FILE, "w") as f:
                f.write("1" if state else "0")
            logging.info(f"Input {'enabled' if state else 'disabled'}.")
        except Exception as e:
            logging.error(f"Failed to change input state: {e}")


def monitor_system_events():
    logging.info("Monitoring system events...")

    try:
        # Monitor journalctl logs for key presses and LedsDummy status
        process = subprocess.Popen(
            ["journalctl", "-f", "-n", "0"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        screen_on = None

        for line in iter(process.stdout.readline, ""):
            if not line:
                continue

            # Detect power key event
            if "Power key pressed" in line:
                logging.info("Power key detected.")

            # Detect LedsDummy status
            if "hfd-service" in line:
                if "LedsDummy on" in line and screen_on is not False:
                    logging.info("Screen off detected.")
                    screen_on = False
                    InputManager.set_input_state(False)

                elif "LedsDummy off" in line and screen_on is not True:
                    logging.info("Screen on detected.")
                    screen_on = True
                    InputManager.set_input_state(True)

    except KeyboardInterrupt:
        logging.info("Monitoring stopped by user.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    monitor_system_events()
