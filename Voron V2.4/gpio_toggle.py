import requests
from gpiozero import Button, OutputDevice
from signal import pause
import logging

logging.basicConfig(filename='/home/pi/gpio_toggle.log', level=logging.INFO)

# Setup
button = Button(12, hold_time=3)  # 3-second hold time
relay = OutputDevice(16, initial_value=False)

moonraker_host = "http://***.***.***.***"  # Moonraker host (type in your IP instead of ***.***.***.***)
moonraker_port = "7125"  # Moonraker port
power_device_name = "Printer_24V"  # Power device name in Moonraker

def update_moonraker_power_state(state):
    url = f"http://***.***.***.***:7125/machine/device_power/device?device=Printer_24V&action={'on' if state else 'off'}" # (type in your IP instead of ***.***.***.***)
    data = {"action": "on" if state else "off"}
    try:
        response = requests.post(url)
        logging.info(f"Making request to {url} with data {data}")
        logging.info(f"Response: {response.status_code}, {response.text}")
    except Exception as e:
        logging.info(f"Failed to update Moonraker power state: {e}")

def toggle_relay():
    relay.toggle()
    update_moonraker_power_state(relay.value)

# Assign the function to the button press event
button.when_held = toggle_relay

pause()  # This will keep the script running
