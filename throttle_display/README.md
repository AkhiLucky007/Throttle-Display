# Throttle Dashboard - Professional Embedded Systems Monitor

A premium, real-time dashboard for monitoring throttle sensor data from ESP32/Arduino embedded systems. Built with PyQt6 and designed for engineering interviews and portfolio demonstrations.

![Dashboard Preview](assets/preview.png)

## 🎯 Project Overview

This project demonstrates:
- **Real-time embedded → software integration** via Serial/WiFi
- **Signal processing** (ADC → percentage scaling)
- **State machine implementation** (DISABLED / READY / FAULT)
- **Live data visualization** with smooth plotting
- **Professional GUI design** with premium styling

## ✨ Features

- **Live throttle monitoring** with color-coded visual feedback
- **State machine logic** matching embedded system behavior
- **Multiple communication backends** (Serial, WiFi, Simulator)
- **Clean architecture** with separation of concerns
- **Premium dark theme** with smooth animations
- **Real-time plotting** with 10-second scrolling history

## 📋 System Requirements

- Python 3.10 or higher
- Windows, macOS, or Linux
- USB port (for serial communication) OR WiFi (for ESP32 wireless)

## 🚀 Installation & Setup

### Step 1: Install Python

Make sure Python 3.10+ is installed:
```bash
python --version
```

If not installed, download from: https://www.python.org/downloads/

### Step 2: Download the Project

Save the entire `throttle_dashboard` folder to your computer.

### Step 3: Install Dependencies

Open a terminal/command prompt in the project folder and run:

```bash
# On Windows
python -m pip install -r requirements.txt

# On macOS/Linux
python3 -m pip install -r requirements.txt
```

This will install:
- PyQt6 (GUI framework)
- pyqtgraph (plotting library)
- pyserial (serial communication)
- PyYAML (configuration)
- numpy (data processing)

## 🎮 Running the Dashboard

### Option 1: Run with Simulator (No Hardware Needed)

This is perfect for development and demonstrations:

```bash
# On Windows
python main.py

# On macOS/Linux
python3 main.py
```

The simulator generates realistic throttle data including:
- Smooth transitions between values
- Random state changes (DISABLED/READY/FAULT)
- Fault conditions (throttle > 70%)

### Option 2: Run with Serial Connection

1. Connect your ESP32/Arduino via USB
2. Find your serial port:
   - **Windows**: Check Device Manager → Ports (usually `COM3`, `COM4`, etc.)
   - **macOS**: Usually `/dev/cu.usbserial-XXXX`
   - **Linux**: Usually `/dev/ttyUSB0` or `/dev/ttyACM0`

3. Edit `config/app_config.yaml`:
```yaml
serial:
  port: "COM3"  # Change to your port
  baudrate: 115200
```

4. Edit `main.py` line 42-43:
```python
# Replace this:
simulator = DataSimulator()

# With this:
from comms.serial_comm import SerialComm
import yaml

with open('config/app_config.yaml', 'r') as f:
    config = yaml.safe_load(f)
    
serial_comm = SerialComm(
    port=config['serial']['port'],
    baudrate=config['serial']['baudrate']
)
```

5. Run the application:
```bash
python main.py
```

### Option 3: Run with WiFi Connection

1. Configure your ESP32 IP address in `config/app_config.yaml`:
```yaml
wifi:
  host: "192.168.1.100"  # Your ESP32 IP
  port: 8080
```

2. Edit `main.py` similarly to serial setup:
```python
from comms.wifi_comm import WiFiComm
import yaml

with open('config/app_config.yaml', 'r') as f:
    config = yaml.safe_load(f)
    
wifi_comm = WiFiComm(
    host=config['wifi']['host'],
    port=config['wifi']['port']
)
```

## 📡 Communication Protocol

The dashboard expects JSON packets (one per line):

```json
{
  "throttle_adc": 2870,
  "throttle_pct": 72.3,
  "enabled": true,
  "state": "FAULT"
}
```

### Field Descriptions

- `throttle_adc`: Raw ADC value (0-4095 for 12-bit ADC)
- `throttle_pct`: Calculated percentage (0.0-100.0)
- `enabled`: System enable flag (true/false)
- `state`: One of "DISABLED", "READY", or "FAULT"

### ESP32 Example Code

```cpp
void sendData() {
  StaticJsonDocument<200> doc;
  
  doc["throttle_adc"] = analogRead(THROTTLE_PIN);
  doc["throttle_pct"] = map(throttle_adc, 0, 4095, 0, 100);
  doc["enabled"] = digitalRead(ENABLE_PIN);
  
  // State logic
  if (!doc["enabled"]) {
    doc["state"] = "DISABLED";
  } else if (doc["throttle_pct"] > 70) {
    doc["state"] = "FAULT";
  } else {
    doc["state"] = "READY";
  }
  
  serializeJson(doc, Serial);
  Serial.println();  // Important: newline separator
}
```

## 🏗️ Project Structure

```
throttle_dashboard/
│
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── README.md                  # This file
│
├── config/
│   └── app_config.yaml       # Configuration settings
│
├── comms/                    # Communication layer
│   ├── serial_comm.py        # USB serial handler
│   ├── wifi_comm.py          # WiFi/TCP handler
│   └── data_simulator.py     # Testing simulator
│
├── core/                     # Business logic
│   ├── data_model.py         # Data structures
│   ├── state_machine.py      # State management
│   └── throttle_processor.py # ADC scaling
│
├── ui/                       # User interface
│   ├── main_window.py        # Main application window
│   ├── dashboard_layout.py   # Layout composition
│   ├── status_widgets.py     # Custom widgets
│   └── plot_widget.py        # Real-time plot
│
├── assets/
│   ├── theme.qss             # Dark theme stylesheet
│   └── icons/                # UI icons (optional)
│
└── logs/
    └── app.log               # Application logs
```

## 🎨 UI Features

### State Color Coding

- 🟢 **READY** (Green): System enabled, throttle ≤ 70%
- 🔴 **FAULT** (Red): System enabled, throttle > 70%
- ⚪ **DISABLED** (Gray): System disabled

### Real-Time Plot

- 10-second scrolling window
- Color-coded threshold lines
- Warning zone highlighting (60-70%)
- Smooth 20 Hz updates

## 🔧 Customization

### Change Fault Threshold

Edit `config/app_config.yaml`:
```yaml
throttle:
  fault_threshold: 80.0  # Change from 70% to 80%
```

### Adjust Update Rate

Edit `config/app_config.yaml`:
```yaml
ui:
  update_rate_ms: 100  # Slower updates (10 Hz instead of 20 Hz)
```

### Change Theme Colors

Edit `assets/theme.qss` to customize colors.

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'PyQt6'"

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### Serial port not found

**Solution**:
1. Check your USB connection
2. Verify the port name in Device Manager (Windows) or `ls /dev/tty*` (Linux/macOS)
3. Update `config/app_config.yaml` with correct port

### Plot not updating

**Solution**:
1. Check logs in `logs/app.log`
2. Verify data packets are being received (check terminal output)
3. Ensure JSON format is correct (use a validator)

### Permission denied on Linux

**Solution**:
```bash
sudo usermod -a -G dialout $USER
# Then logout and login again
```

## 📊 State Machine Logic

```
DISABLED ←→ READY ←→ FAULT
    ↑         ↓         ↓
    └─────────┴─────────┘

Rules:
1. enabled = False  → DISABLED
2. enabled = True AND throttle ≤ 70%  → READY
3. enabled = True AND throttle > 70%  → FAULT
```

## 🎓 Interview Talking Points

- **Architecture**: Clean separation between communication, logic, and UI layers
- **Threading**: Non-blocking serial/WiFi communication using QThread
- **Real-time**: Efficient data buffering with deque for O(1) operations
- **Scalability**: Abstract communication layer allows easy hardware swapping
- **Professional**: Production-ready code with logging, error handling, and documentation

## 📝 License

This project is created for educational and portfolio purposes.

## 👨‍💻 Author

Created as a demonstration project for embedded systems engineering interviews.

---

**Questions?** Check the logs in `logs/app.log` or review the inline code documentation.
