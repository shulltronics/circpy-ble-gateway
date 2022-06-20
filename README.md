## A BLE to MQTT gateway written in CircuitPython

Use this code to create a BLE gateway that logs messages to an MQTT broker.
Use on a desktop computer with BLE,
Or on an embedded system such as:
* Feather RP2040 with CircuitPython
* Particle Ethernet Featherwing
* Airlift Featherwing with ESP32 co-processor

## How to use
* Copy this code to a CircuitPython compatible device with BLE and internet connectivity.
* Create a `secrets.py` file that contains the MQTT server information.
* Name and publish the MQTT topic and associated with the data recieved over BLE.
