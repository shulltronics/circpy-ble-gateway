## A BLE to MQTT gateway written in CircuitPython

Use this code to create a BLE gateway that logs messages to an MQTT broker.
Use on a desktop computer with BLE,
Or on an embedded system such as:
* Feather RP2040 with CircuitPython
* Particle Ethernet Featherwing
* Airlift Featherwing with ESP32 co-processor

## How to use
* Copy this code to a CircuitPython compatible device with BLE and internet connectivity
* Create a `secrets.py` file that contains the MQTT server information
* If on a desktop, create and activate a Python virtualenv, then install the dependencies with `pip install -r requirements.txt`
* If on a circuitpython board, make sure the appropriate libraries are in the `lib` folder
* Publish the MQTT topic and associated with the data recieved over BLE (TODO)
* Run the script by saving it to the circuitpython board, or by running `python code.py` from within the venv on your desktop.
