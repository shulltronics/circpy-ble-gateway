import time
import socket
import ssl
import adafruit_minimqtt.adafruit_minimqtt as MQTT

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

# Bluetooth radio variables
ble = BLERadio()
uart_connection = None

# Add a secrets.py to your filesystem that has a dictionary called secrets with the following keys:
# "username", "password", "broker", and "port"
try:
    from secrets import secrets
except ImportError:
    print("Secrets file not found!")
    raise

# MQTT Topic
# Use this topic if you'd like to connect to a standard MQTT broker
mqtt_topic = "clue/temp"

### Code ###
# Define callback methods which are called when events occur
# pylint: disable=unused-argument, redefined-outer-name
def connect(mqtt_client, userdata, flags, rc):
    # This function will be called when the mqtt_client is connected
    # successfully to the broker.
    print("Connected to MQTT Broker!")
    print("Flags: {0}\n RC: {1}".format(flags, rc))


def disconnect(mqtt_client, userdata, rc):
    # This method is called when the mqtt_client disconnects
    # from the broker.
    print("Disconnected from MQTT Broker!")


def subscribe(mqtt_client, userdata, topic, granted_qos):
    # This method is called when the mqtt_client subscribes to a new feed.
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))


def unsubscribe(mqtt_client, userdata, topic, pid):
    # This method is called when the mqtt_client unsubscribes from a feed.
    print("Unsubscribed from {0} with PID {1}".format(topic, pid))


def publish(mqtt_client, userdata, topic, pid):
    # This method is called when the mqtt_client publishes data to a feed.
    print("Published to {0} with PID {1}".format(topic, pid))


def message(client, topic, message):
    # Method called when a client's subscribed feed has a new value.
    print("[{2}]: New message on topic {0}: {1}".format(topic, message, time.strftime("%I:%M:%S %p")))


# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(
    broker=secrets["broker"],
    port=secrets["port"],
    username=secrets["username"],
    password=secrets["password"],
    socket_pool=socket,
    ssl_context=ssl.create_default_context(),
)

# Connect callback handlers to mqtt_client
mqtt_client.on_connect = connect
mqtt_client.on_disconnect = disconnect
mqtt_client.on_subscribe = subscribe
mqtt_client.on_unsubscribe = unsubscribe
mqtt_client.on_publish = publish
mqtt_client.on_message = message

print("Attempting to connect to %s" % mqtt_client.broker)
try:
    mqtt_client.connect()
except Exception as e:
    print("error connecting to MQTT broker: {}".format(e))
    raise e

print("Subscribing to %s" % mqtt_topic)
mqtt_client.subscribe(mqtt_topic)

#print("Publishing to %s" % mqtt_topic)
#mqtt_client.publish(mqtt_topic, "Hello Broker!")

#print("Unsubscribing from %s" % mqtt_topic)
#mqtt_client.unsubscribe(mqtt_topic)

#print("Disconnecting from %s" % mqtt_client.broker)
#mqtt_client.disconnect()

# Connect to BLE device (TODO: Make this more robust)
if not uart_connection:
    print("Trying to connect to BLE...")
    for adv in ble.start_scan(ProvideServicesAdvertisement):
        if UARTService in adv.services:
            uart_connection = ble.connect(adv)
            print("Connected")
            break
    ble.stop_scan()

while True:
    # read the buffers and do the callbacks
    mqtt_client.loop()
    
    # Get the bluetooth data
    if uart_connection and uart_connection.connected:
        uart_service = uart_connection[UARTService]
        while uart_connection.connected:
            data = uart_service.readline().decode("utf-8")
            print(data)
            timed_data = "{0}: {1}".format(time.strftime("%I:%M:%S %p"), data)
            mqtt_client.publish(mqtt_topic, timed_data)

    #time.sleep(0.5)

