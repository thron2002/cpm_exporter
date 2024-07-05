#!/usr/bin/env python3

import sys
import time
import serial
from prometheus_client import Gauge, start_http_server
import logging

# Prometheus metrics setup
# This Gauge will store and expose the CPM metric for our program.
cpm_gauge = Gauge('geiger_cpm', 'Counts per minute from Geiger counter')

# Add logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
SERIAL_PORT = '/dev/cpm'
SERIAL_BAUDRATE = 57600
SERIAL_TIMEOUT = 3
DEFAULT_SLEEP_INTERVAL = 60  # Default 1 minute

def get_cpm(geiger_device):
    """Retrieve the Counts Per Minute (CPM) from the Geiger counter device.

    Args:
        geiger_device (serial.Serial): The serial device representing the Geiger counter.

    Returns:
        int: The current CPM value.
    """
    try:
        geiger_device.write(b'<GETCPM>>')
        data = geiger_device.read(2)
        if len(data) != 2:
            raise ValueError("Insufficient data received")
        return (data[0] << 8) | data[1]
    except (serial.SerialException, IndexError, ValueError) as e:
        logging.error("Error getting CPM: {}".format(e))
        return None

def main():
    """
    Main function to handle the process flow.
    
    This function initializes the Prometheus server, establishes a connection
    with the Geiger counter, and continuously retrieves and logs CPM data
    at specified intervals.

    Command-line Arguments:
        An optional float value can be provided to set the sleep interval
        between data retrievals (in seconds). If not provided, it defaults
        to DEFAULT_SLEEP_INTERVAL.

    The function runs indefinitely until interrupted by a KeyboardInterrupt.
    """
    try:
        sleep_interval = float(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SLEEP_INTERVAL
        if sleep_interval <= 0:
            raise ValueError("Sleep interval must be positive")
    except ValueError as e:
        logging.error("Invalid interval provided: {}".format(e))
        sys.exit(1)

    # Start Prometheus server to expose metrics on port 8000
    try:
        start_http_server(8000)
    except OSError as e:
        logging.error("Failed to start Prometheus server: {}".format(e))
        sys.exit(1)

    # Try to establish a serial connection and retrieve data continuously
    try:
        with serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=SERIAL_TIMEOUT) as geiger_device:
            logging.info("Connected to Geiger counter. Starting data collection.")
            while True:
                current_cpm = get_cpm(geiger_device)

                if current_cpm is not None:
                    # Update Prometheus metric
                    cpm_gauge.set(current_cpm)
                    logging.info("CPM: {}".format(current_cpm))
                else:
                    logging.warning("Failed to retrieve valid data from the Geiger counter")

                # Sleep for the defined interval before the next data retrieval
                time.sleep(sleep_interval)
    except serial.SerialException as e:
        logging.error("Error: Unable to establish connection to the Geiger counter. {}".format(e))
    except KeyboardInterrupt:
        logging.info("Exiting gracefully.")
    except Exception as e:
        logging.error("Unexpected error: {}".format(e))

if __name__ == "__main__":
    main()
