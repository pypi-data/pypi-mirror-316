import os
import json
import paho.mqtt.client as mqtt
import yaml
from .logger import log_client
from .leds import leds, set_led_on, set_led_off, led_is_on


mqtt_client = None
device_config = None  # Declare a global variable for the device configuration

# MQTT settings
MQTT_BROKER = os.getenv("MQTT_BROKER") or "CHANGE_THIS_TO_MQTTBROKER"
MQTT_PORT = int(os.getenv("MQTT_PORT")) or 12345
MQTT_USER = os.getenv("MQTT_USER") or "CHANGE_THIS_TO_MQTTUSER"
MQTT_PASS = os.getenv("MQTT_PASS") or "CHANGE_THIS_TO_MQTTPASSWORD"
MQTT_UID = os.getenv("MQTT_UID") or "ws2811-mqtt"
MQTT_TOPIC_STATUS = os.getenv("MQTT_TOPIC_STATUS") or f"homeassistant/device/{MQTT_UID}/config"

def color_tuple_to_string(color_tuple):
    try:
        # Check if the color tuple has exactly 3 components
        if len(color_tuple) != 3:
            raise ValueError("Color tuple must have three components")

        # Swap the first two elements back
        original_color = (color_tuple[1], color_tuple[0], color_tuple[2])

        # Convert the tuple into a comma-separated string
        color_string = ','.join(map(str, original_color))
        return color_string
    except Exception as e:
        log_client.error(f"[CREATE] Error creating color string from {color_tuple}: {e}")
        return None


def color_string_to_tuple(color_string):
    try:
        # Parse the color string into a tuple of integers
        color = tuple(map(int, color_string.split(',')))

        # Check if the color tuple has exactly 3 components
        if len(color) != 3:
            raise ValueError("Color string must have three components")

        # Swap the first two elements
        swapped_color = (color[1], color[0], color[2])
        return swapped_color
    except Exception as e:
        log_client.error(f"[PARSE] Error parsing color string {color_string}: {e}")
        return None

def publish_led_status(led_index):
    try:
        led = leds[led_index]
        led_status = leds[led_index]["state"]
        topic = device_config.get("cmps").get(f"led_{led_index + 1}").get("state_topic")
        rgb_topic = device_config.get("cmps").get(f"led_{led_index + 1}").get("rgb_stat_t")
        mqtt_client.publish(f"{topic}", led_status.encode('utf-8'), retain=True)
        led_status = color_tuple_to_string(led["color"])
        mqtt_client.publish(f"{rgb_topic}", led_status.encode('utf-8'), retain=True)
        log_client.debug(f"[MQTT] Published LED status : Led #{led_index + 1} == {led['color']}")
    except Exception as e:
        log_client.error(f"[MQTT] Error publishing LED status: {e}")

def on_connect(client, userdata, flags, rc):
    log_client.info("[MQTT] Connected to broker")
    # Loop through LEDs and subscribe to their command topics
    for _, led_config in device_config['cmps'].items():
        command_topic = led_config['command_topic']
        rgb_command_topic = led_config['rgb_cmd_t']
        client.subscribe(command_topic)
        client.subscribe(rgb_command_topic)
        log_client.info(f"Subscribed to {command_topic}")
        log_client.info(f"Subscribed to {rgb_command_topic}")

    # Publish initial status
    client.publish(MQTT_TOPIC_STATUS, json.dumps(device_config), retain=True)


def on_message(client, userdata, msg):
    try:
        log_client.info(msg.topic)

        if msg.topic in [led_config['command_topic'] for led_config in device_config['cmps'].values()]:
            payload = msg.payload.decode('utf-8')
            log_client.info(f"[MQTT] Received message: {payload}")
            led_index = int(msg.topic.split('_')[-1]) -1
            set_led_on(led_index) if payload == "ON" else set_led_off(led_index)
        elif msg.topic in [led_config['rgb_cmd_t'] for led_config in device_config['cmps'].values()]:
            payload = msg.payload.decode('utf-8')
            log_client.info(f"[MQTT] Received message: {payload}")
            led_index = int(msg.topic.split(MQTT_UID)[-1].split('/')[1].split('_')[-1]) -1
            set_led_on(led_index, color_string_to_tuple(payload))

        publish_led_status(led_index)
    except Exception as e:
        log_client.error(f"[MQTT] Error processing message: {e}")
        log_client.debug(f"[MQTT] Message payload : {msg.payload}")
        log_client.debug(f"[MQTT] Message topic : {msg.topic}")

def init_mqtt():
    global mqtt_client, device_config  # Declare global to modify the external variables

    # Load device configuration once during initialization
    with open('ws2811_mqtt/device_config.yaml', 'r') as file:
        device_config = yaml.safe_load(file)
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(username=MQTT_USER, password=MQTT_PASS)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()
    return mqtt_client
