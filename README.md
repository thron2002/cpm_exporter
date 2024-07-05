# CPM Exporter

CPM Exporter is a Python script that reads Counts Per Minute (CPM) data from a Geiger counter device and exposes it as a Prometheus metric. This tool is useful for monitoring radiation levels and integrating the data with Prometheus-based monitoring systems.

In this case, this script is used with the following device:
GQ GME-300E Plus

## Features

- Reads CPM data from a Geiger counter device via serial communication
- Exposes CPM data as a Prometheus metric
- Configurable sleep interval between data retrievals
- Logging for easy troubleshooting

## Requirements

- Python 3.x
- pyserial
- prometheus_client

## Installation

1. Clone this repository or download the `cpm_metrics.py` script.
2. Install the required Python packages:

```
pip install pyserial prometheus_client
```

## Usage

Run the script with:

```
python cpm_metrics.py [sleep_interval]
```

- `sleep_interval` (optional): Time in seconds between data retrievals. Defaults to 60 seconds if not specified.

## Configuration

The script uses the following constants, which can be modified in the code if needed:

- `SERIAL_PORT`: The serial port for the Geiger counter device (default: '/dev/cpm')
- `SERIAL_BAUDRATE`: The baud rate for serial communication (default: 57600)
- `SERIAL_TIMEOUT`: Timeout for serial operations in seconds (default: 3)
- `DEFAULT_SLEEP_INTERVAL`: Default sleep interval between data retrievals in seconds (default: 60)

## Prometheus Integration

The script starts a Prometheus HTTP server on port 8000. The CPM data is exposed as a Gauge metric named `geiger_cpm` with the description "Counts per minute from Geiger counter".

To scrape this metric with Prometheus, add the following job to your Prometheus configuration:

```yaml
scrape_configs:
  - job_name: 'cpm_exporter'
    static_configs:
      - targets: ['localhost:8000']
```

## Logging

The script logs information, warnings, and errors to the console. The log format includes timestamps and log levels for easy debugging.

## Error Handling

The script includes error handling for various scenarios, including:

- Invalid sleep interval input
- Failure to start the Prometheus server
- Serial communication errors
- Unexpected errors during execution

In case of critical errors, the script will log the error and exit with a non-zero status code.

## License

This project is licensed under the GNU General Public License v3.0. See the LICENSE file for details.
