import os

import time
from dotenv import load_dotenv

load_dotenv("./.env")
from .args import init_args, args_client
init_args()
from .logger import init_logger, log_client
init_logger()
from .leds import set_led_white, pixels

from .mqtt import init_mqtt, publish_led_status
init_mqtt()





# Global command and LED states
# current_led_colors = [(0, 0, 0)] * NUM_LEDS
# last_status_time = time.time()

# def set_all_pixels_color(color, brightness=1.0):
#     adjusted_color = tuple(int(c * brightness) for c in color)
#     for i in range(NUM_LEDS):
#         pixels[i] = adjusted_color
#     pixels.show()

# def apply_mqtt_commands_static():
#     """Apply static mode commands and update LEDs accordingly."""
#     color = command.get("color", (255, 0, 0))
#     brightness = command.get("brightness", 1.0)
#     set_all_pixels_color(color, brightness)


def main():
    while True:
        try:
            log_client.debug("Listening for MQTT messages and processing commands.")
            set_led_white(1)
            set_led_white(5)
            log_client.debug(pixels[5])
            log_client.debug(pixels[6])
            publish_led_status()
            time.sleep(5)
        except Exception as e:
            print("[Error] An error occurred:", e)
            time.sleep(60)

if __name__ == "__main__":
    main()

# def run_static_mode():
#     """Continuously runs when mode=static, listening for MQTT updates."""
#     apply_mqtt_commands_static()
#     # Sleep briefly, then loop again to check for MQTT changes

#     # Publish LED status every 15 seconds
#     if time.time() - last_status_time >= 15:
#         publish_lifestatus()
#         last_status_time = time.time()
#     time.sleep(0.5)

# def run_api_mode():
#     global current_led_colors, last_status_time

#     # Fetch the exchange rate
#     print("[API Request] Sending request to API")
#     data = response.json()
#     print(f"[API Response] Received data: {data}")
#     exchange_rate = float(data["price"])
#     print(f"[Exchange Rate] Extracted exchange rate: {exchange_rate}")

#     # Calculate how many LEDs to light
#     difference = exchange_rate - command.get("btc_mid_value", 0.00)
#     print(f"[Calculation] Difference from {command.get('btc_mid_value')} is: {difference}")

#     num_leds_full = max(0, min(NUM_LEDS, int(difference / VALUE_PER_LED)))

#     # Prepare target LED colors
#     target_led_colors = [(0, 0, 0)] * NUM_LEDS
#     base_color = (255, 0, 0)  # Red for positive difference
#     for i in range(num_leds_full):
#         target_led_colors[i] = base_color

#     # Assign random colors to remaining LEDs
#     for i in range(NUM_LEDS):
#         if target_led_colors[i] == (0, 0, 0):
#             target_led_colors[i] = (
#                 random.randint(0, 255),
#                 random.randint(0, 255),
#                 random.randint(0, 255),
#             )

#     # Transition to new colors
#     for step in range(TRANSITION_STEPS):
#         progress = (step + 1) / TRANSITION_STEPS
#         for i in range(NUM_LEDS):
#             current_color = current_led_colors[i]
#             target_color = target_led_colors[i]
#             intermediate_color = tuple(
#                 int(current_color[j] + (target_color[j] - current_color[j]) * progress)
#                 for j in range(3)
#             )
#             pixels[i] = intermediate_color
#         pixels.show()
#         time.sleep(WAIT_TIME / TRANSITION_STEPS)

#     # Update current LED colors
#     current_led_colors = target_led_colors.copy()

#     # Publish LED status every 15 seconds
#     if time.time() - last_status_time >= 15:
#         publish_lifestatus()
#         last_status_time = time.time()
