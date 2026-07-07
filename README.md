# Throttle Dashboard

A desktop dashboard for monitoring throttle sensor data from an ESP32 or Arduino. The application is built with PyQt6 and provides live visualization of sensor values, system state, and communication status. It can connect over Serial, WiFi, or run with a built-in simulator when hardware isn't available.

## Overview

The project demonstrates:

- Communication between embedded hardware and a desktop application
- ADC scaling from raw values to throttle percentage
- Simple state machine implementation (DISABLED, READY, FAULT)
- Live plotting of incoming sensor data
- A modular application structure separating communication, processing, and UI

## Features

- Live throttle percentage display
- State indicator with color-coded status
- Serial, WiFi, and simulator backends
- Rolling history graph with a 10-second window
- Configurable thresholds and update rates
- Dark theme with responsive UI

## Requirements

- Python 3.10+
- Windows, macOS, or Linux
- USB connection (Serial) or WiFi if connecting to hardware

## Installation

Verify Python is installed:

    python --version

Install the required packages:

    # Windows
    python -m pip install -r requirements.txt

    # macOS / Linux
    python3 -m pip install -r requirements.txt

Dependencies include:

- PyQt6
- pyqtgraph
- pyserial
- PyYAML
- numpy

## Running the Application

### Simulator

The simulator is enabled by default and generates realistic throttle values along with state transitions.

    python main.py

### Serial Communication

1. Connect the ESP32 or Arduino.
2. Update the serial settings in config/app_config.yaml:

    serial:
      port: "COM3"
      baudrate: 115200

3. Replace the simulator in main.py with the serial communication class.
4. Start the application:

    python main.py

### WiFi Communication

Configure the device address in config/app_config.yaml:

    wifi:
      host: "192.168.1.100"
      port: 8080

Replace the simulator with the WiFi communication backend and run the application.

## Communication Format

The application expects one JSON object per line:

{
  "throttle_adc": 2870,
  "throttle_pct": 72.3,
  "enabled": true,
  "state": "FAULT"
}

### Fields

- throttle_adc: Raw ADC reading
- throttle_pct: Throttle position (0–100%)
- enabled: System enable status
- state: DISABLED, READY, or FAULT

## Project Structure

throttle_dashboard/

├── main.py
├── requirements.txt
├── README.md
├── config/
├── comms/
├── core/
├── ui/
├── assets/
└── logs/

Project layout:

- Communication – Serial, WiFi, and simulator interfaces
- Core – Data processing and state logic
- UI – Dashboard widgets, layout, and plotting

## State Logic

- enabled == false → DISABLED
- enabled == true and throttle ≤ 70% → READY
- enabled == true and throttle > 70% → FAULT

## Configuration

Most application settings can be changed in config/app_config.yaml, including:

- Fault threshold
- Update interval
- Communication settings
- Theme colors

## Troubleshooting

Missing PyQt6:

    pip install -r requirements.txt

Serial port unavailable:

- Confirm the board is connected.
- Verify the selected COM/TTY port.
- Update the configuration file if necessary.

No incoming data:

- Check logs/app.log.
- Verify the JSON format.
- Confirm the device is transmitting newline-separated packets.

## Design Notes

The application separates communication, processing, and presentation into independent modules. This makes it easier to switch communication methods, test with simulated data, or extend the dashboard without modifying unrelated parts of the project.

Incoming data is buffered efficiently for plotting, while communication runs independently of the UI to keep the interface responsive.

## License

This project is intended for educational use and as part of an embedded systems portfolio.
