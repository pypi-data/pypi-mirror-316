import os
import json
import paho.mqtt.client as mqtt
import yaml
from .logger import log_client
from .leds import pixels, set_led_white


mqtt_client = None
device_config = None  # Declare a global variable for the device configuration

# MQTT settings
MQTT_BROKER = os.getenv("MQTT_BROKER") or "CHANGE_THIS_TO_MQTTBROKER"
MQTT_PORT = int(os.getenv("MQTT_PORT")) or 12345
MQTT_USER = os.getenv("MQTT_USER") or "CHANGE_THIS_TO_MQTTUSER"
MQTT_PASS = os.getenv("MQTT_PASS") or "CHANGE_THIS_TO_MQTTPASSWORD"
MQTT_TOPIC_COMMAND = "cmnd/ws2811/command/#"
MQTT_TOPIC_STATUS = "stat/ws2811/status"
MQTT_UID = os.getenv("MQTT_UID") or "ws2811-mqtt"
MQTT_TOPIC_STATUS = os.getenv("MQTT_TOPIC_STATUS") or f"homeassistant/device/{MQTT_UID}/config"


def publish_led_status():
    try:
        for index in range(len(pixels)):
            led = pixels[index]
            led_status = "ON" if any(int(a) != 0 for a in led) else "OFF"
            topic = device_config.get("cmps").get(f"led_{index + 1}").get("state_topic")
            mqtt_client.publish(f"{topic}", led_status.encode('utf-8'), retain=True)
        log_client.debug(f"[MQTT] Published LED status : {led}")
    except Exception as e:
        log_client.error(f"[MQTT] Error publishing LED status: {e}")

def on_connect(client, userdata, flags, rc):
    log_client.info("[MQTT] Connected to broker")
    # Loop through LEDs and subscribe to their command topics
    for _, led_config in device_config['cmps'].items():
        command_topic = led_config['command_topic']
        client.subscribe(command_topic)
        log_client.debug(f"Subscribed to {command_topic}")

    # Publish initial status
    client.publish(MQTT_TOPIC_STATUS, json.dumps(device_config), retain=True)


def on_message(client, userdata, msg):
    try:
        log_client.info(msg.topic)

        if msg.topic in [led_config['command_topic'] for led_config in device_config['cmps'].values()]:
            log_client.info(f"[MQTT] Received message: {msg.payload}")
            payload = msg.payload.decode('utf-8')
            log_client.info(f"[MQTT] Updated command: {payload}")
            led_index = int(msg.topic.split('_')[-1]) -1
            set_led_white(led_index)
            publish_led_status()
        else:
            log_client.info(f"[MQTT] Unknown command topic: {msg.topic}")
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
    publish_led_status()
    mqtt_client.loop_start()
    return mqtt_client
