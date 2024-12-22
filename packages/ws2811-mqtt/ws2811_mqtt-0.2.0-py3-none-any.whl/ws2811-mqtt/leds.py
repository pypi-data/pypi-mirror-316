# import board
# import neopixel
import os
from .logger import log_client


NUM_LEDS = int(os.getenv("NUM_LEDS") or 50) # Number

# Initialize the NeoPixel strip
# pixels = neopixel.NeoPixel(board.D18, NUM_LEDS, brightness=1, auto_write=False)
pixels = [(0, 0, 0) for _ in range(NUM_LEDS)]


# Function to set a LED's color to white (255, 255, 255)
def set_led_white(led_index):
    try:
        pixels[led_index] = (255, 255, 255)
        log_client.info(f"[LED] LED {led_index} color set to white.")
    except Exception as e:
        log_client.error(f"[LED] Error setting LED color: {e}")