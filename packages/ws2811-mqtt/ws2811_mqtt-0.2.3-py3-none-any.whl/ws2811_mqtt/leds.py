import board
import neopixel
import os
from .logger import log_client


NUM_LEDS = int(os.getenv("NUM_LEDS") or 50) # Number

# Initialize the NeoPixel strip
pixels = neopixel.NeoPixel(board.D18, NUM_LEDS, brightness=1, auto_write=True)
leds = [{"state": "OFF", "color": (255,255,255)} for _ in range(len(pixels))]
# pixels = [(0, 0, 0) for _ in range(NUM_LEDS)]

# Function to apply changes from the leds array to the pixels array
def set_led_state(led_index):
    try:
        if leds[led_index]["state"] == "OFF":
            pixels[led_index] = (0, 0, 0)
        else:
            pixels[led_index] = leds[led_index]["color"]
            log_client.info("[apply_led_changes] LED states applied to pixels array.")
    except Exception as e:
        log_client.error(f"[apply_led_changes] Error applying LED changes: {e}")


# Function to check if an LED is on by verifying its color is not black (0, 0, 0)
def led_is_on(led_index):
    log_client.debug(f"[LED led_is_on] LED index {led_index}")
    log_client.debug(f"[LED led_is_on] LED value {pixels[led_index]}")
    led_on = leds[led_index]["state"] == "ON"
    return led_on

# Function to set a LED's color to black (0, 0, 0), effectively turning it off
def set_led_off(led_index):
    try:
        log_client.debug(f"[LED set_led_off] LED value before {pixels[led_index]}")
        pixels[led_index] = (0, 0, 0)
        log_client.debug(f"[LED set_led_off] LED {led_index} color set to black.")
        log_client.debug(f"[LED set_led_off] LED value after  {pixels[led_index]}")
    except Exception as e:
        log_client.error(f"[LED set_led_off] Error setting LED color: {e}")

# Function to set a LED's color to a specified value, defaulting to white (255, 255, 255)
def set_led_on(led_index, color=None):
    try:
        leds[led_index].update({"state": "ON", "color": color or leds[led_index]["color"]})
        set_led_state(led_index)
        log_client.info(f"[LED set_led_on] LED {led_index} color set to {color}.")
    except Exception as e:
        log_client.error(f"[LED set_led_on] Error setting LED color: {e}")
