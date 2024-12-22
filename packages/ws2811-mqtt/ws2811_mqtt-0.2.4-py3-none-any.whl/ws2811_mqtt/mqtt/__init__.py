import os
import json
import paho.mqtt.client as mqtt
import yaml
import pprint
import logging
from logger import log_client
from leds import leds, set_led, NUM_LEDS
from utils import colr_str_to_tuple, colr_tuple_to_st


mqtt_client = None
device_config = None  # Declare a global variable for the device configuration

# MQTT settings
MQTT_BROKER = os.getenv("MQTT_BROKER") or "CHANGE_THIS_TO_MQTTBROKER"
MQTT_PORT = int(os.getenv("MQTT_PORT")) or 12345
MQTT_USER = os.getenv("MQTT_USER") or "CHANGE_THIS_TO_MQTTUSER"
MQTT_PASS = os.getenv("MQTT_PASS") or "CHANGE_THIS_TO_MQTTPASSWORD"
MQTT_UID = os.getenv("MQTT_UID") or "ws2811-mqtt"
MQTT_TOPIC_STATUS = os.getenv("MQTT_TOPIC_STATUS") or f"homeassistant/device/{MQTT_UID}/config"


def publish_all_led(all_led_state):
    try:
        led_status = all_led_state["state"]
        topic = device_config.get("cmps").get(f"all_leds").get("state_topic")
        rgb_topic = device_config.get("cmps").get(f"all_leds").get("rgb_stat_t")
        mqtt_client.publish(f"{topic}", led_status.encode('utf-8'), retain=True)
        if "color" in all_led_state:
            led_status = colr_tuple_to_st(all_led_state["color"])
            mqtt_client.publish(f"{rgb_topic}", led_status.encode('utf-8'), retain=True)
            log_client.debug(f"[MQTT][%15s] Status: {all_led_state}", "publish_all_led")
        else:
            log_client.debug(f"[MQTT][%15s] Status: {all_led_state['state']}", "publish_all_led")
    except Exception as e:
        log_client.error(f"[MQTT][%15s] Error publishing LED status: {e}", "publish_all_led")


def publish_led(led_index):
    try:
        led = leds[led_index]
        led_status = leds[led_index]["state"]
        topic = device_config.get("cmps").get(f"led_{led_index + 1}").get("state_topic")
        rgb_topic = device_config.get("cmps").get(f"led_{led_index + 1}").get("rgb_stat_t")
        mqtt_client.publish(f"{topic}", led_status.encode('utf-8'), retain=True)
        led_status = colr_tuple_to_st(led["color"])
        mqtt_client.publish(f"{rgb_topic}", led_status.encode('utf-8'), retain=True)
        log_client.debug(f"[MQTT][%15s] Published LED status : Led #{led_index + 1} == {led['color']}", "publish_led")
    except Exception as e:
        log_client.error(f"[MQTT][%15s] Error publishing LED status: {e}", "publish_led")

def on_connect(client, userdata, flags, rc):
    log_client.info(f"[MQTT][%15s] Connected to broker", "on_connect")
    # Loop through LEDs and subscribe to their command topics
    for _, led_config in device_config['cmps'].items():
        command_topic = led_config['command_topic']
        client.subscribe(command_topic)
        log_client.info(f"[MQTT][%15s] Subscribed to {command_topic}", "on_connect")
        if (led_config.get("rgb_cmd_t")):
            rgb_command_topic = led_config['rgb_cmd_t']
            client.subscribe(rgb_command_topic)
            log_client.info(f"[MQTT][%15s] Subscribed to {rgb_command_topic}", "on_connect")

    # Publish initial status
    client.publish(MQTT_TOPIC_STATUS, json.dumps(device_config), retain=True)


def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        log_client.info(f"[MQTT][%15s] topic  : \"{msg.topic}\"", "on_message")
        log_client.info(f"[MQTT][%15s] payload: \"{msg.payload}\"", "on_message")
        if msg.topic == f"cmnd/{MQTT_UID}/all_leds/blink":
            publish_state(f"stat/{MQTT_UID}/all_leds/blink")
        if msg.topic == f"cmnd/{MQTT_UID}/all_leds/rgb":
            for led_index in range(len(leds)):
                leds[led_index] = {"state": "ON", "color": colr_str_to_tuple(payload) }
                set_led(led_index)
                publish_led(led_index)
                publish_all_led({"state": "ON", "color": colr_str_to_tuple(payload) })
        elif msg.topic == f"cmnd/{MQTT_UID}/all_leds":
            for led_index in range(len(leds)):
                leds[led_index]["state"] = payload
                set_led(led_index)
                publish_led(led_index)
                publish_all_led({"state": payload })
        elif msg.topic in [led_config.get('command_topic') for led_config in device_config['cmps'].values()]:
            led_index = int(msg.topic.split('_')[-1]) -1
            leds[led_index]["state"] = payload
            set_led(led_index)
        elif msg.topic in [led_config.get('rgb_cmd_t') for led_config in device_config['cmps'].values()]:
            led_index = int(msg.topic.split(MQTT_UID)[-1].split('/')[1].split('_')[-1]) -1
            leds[led_index] = {"state": "ON", "color": colr_str_to_tuple(payload) }
            set_led(led_index)
        publish_led(led_index)
    except Exception as e:
        log_client.error(f"[MQTT][%15s] Error processing message: {e}", "on_message")
        log_client.debug(f"[MQTT][%15s] Message payload : {msg.payload}", "on_message")
        log_client.debug(f"[MQTT][%15s] Message topic : {msg.topic}", "on_message")

def gen_leds_conf():
    led_config = {}
    for i in range(1, NUM_LEDS + 1):
        led_id = f"led_{i}"
        led_number = f"{i:02}"  # Format as two digits
        led_config[led_id] = {
            "p": "light",
            "clrm": "rgb",
            "ret": True,
            "unique_id": f"ws2811_led_{led_number}",
            "rgb_stat_t": f"stat/{MQTT_UID}/led_{led_number}/rgb",
            "rgb_cmd_t": f"cmnd/{MQTT_UID}/led_{led_number}/rgb",
            "name": f"Led {led_number}",
            "command_topic": f"cmnd/{MQTT_UID}/led_{led_number}",
            "state_topic": f"stat/{MQTT_UID}/led_{led_number}"
        }
    device_config["cmps"].update(led_config)
    device_config["cmps"]["all_leds"]["state_topic"] = device_config["cmps"]["all_leds"]["state_topic"].replace("MQTT_UID", MQTT_UID)
    device_config["cmps"]["all_leds"]["rgb_stat_t"] = device_config["cmps"]["all_leds"]["rgb_stat_t"].replace("MQTT_UID", MQTT_UID)
    device_config["cmps"]["all_leds"]["command_topic"] = device_config["cmps"]["all_leds"]["command_topic"].replace("MQTT_UID", MQTT_UID)
    device_config["cmps"]["all_leds"]["rgb_cmd_t"] = device_config["cmps"]["all_leds"]["rgb_cmd_t"].replace("MQTT_UID", MQTT_UID)
    device_config["cmps"].update(led_config)
    log_client.info("[MQTT][%15s] `LED configuration generated` :", "gen_leds_conf")
    if log_client.getEffectiveLevel() == logging.INFO:
        pprint.pprint(device_config, indent=2)


def init_mqtt():
    global mqtt_client, device_config  # Declare global to modify the external variables

    # Load device configuration once during initialization
    with open('ws2811_mqtt/device_config.yaml', 'r') as file:
        device_config = yaml.safe_load(file)
        gen_leds_conf()
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(username=MQTT_USER, password=MQTT_PASS)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()
    for i in range(NUM_LEDS):
        publish_led(i)