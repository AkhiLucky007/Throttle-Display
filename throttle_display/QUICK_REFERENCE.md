# Quick Reference - Throttle Dashboard

## 🏃‍♂️ Quick Start (1 Minute)

```bash
# 1. Navigate to project folder
cd throttle_dashboard

# 2. Install dependencies (first time only)
pip install -r requirements.txt

# 3. Run the dashboard
python main.py
```

## 📁 Project Structure at a Glance

```
throttle_dashboard/
├── main.py              ← RUN THIS
├── requirements.txt     ← Dependencies list
├── config/
│   └── app_config.yaml ← Edit settings here
├── comms/              ← Communication layer
├── core/               ← Business logic
├── ui/                 ← Visual components
├── assets/             ← Theme & icons
└── logs/               ← Error logs
```

## ⚙️ Configuration (config/app_config.yaml)

```yaml
serial:
  port: "COM3"           # ← Change your port here
  baudrate: 115200

throttle:
  fault_threshold: 70.0  # ← Adjust fault limit here

ui:
  update_rate_ms: 50     # ← Change refresh rate here
```

## 🔌 Switching Between Data Sources

Edit `main.py` around line 42:

### Simulator (Default - No Hardware)
```python
from comms.data_simulator import DataSimulator
simulator = DataSimulator()
window.set_data_source(simulator)
```

### Serial (USB Connection)
```python
import yaml
from comms.serial_comm import SerialComm

with open('config/app_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

serial = SerialComm(
    port=config['serial']['port'],
    baudrate=config['serial']['baudrate']
)
window.set_data_source(serial)
```

### WiFi (ESP32 Wireless)
```python
import yaml
from comms.wifi_comm import WiFiComm

with open('config/app_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

wifi = WiFiComm(
    host=config['wifi']['host'],
    port=config['wifi']['port']
)
window.set_data_source(wifi)
```

## 📡 Expected Data Format (JSON)

Your ESP32 should send this format (one line per packet):

```json
{"throttle_adc": 2048, "throttle_pct": 50.0, "enabled": true, "state": "READY"}
```

**Fields:**
- `throttle_adc`: Integer (0-4095)
- `throttle_pct`: Float (0.0-100.0)
- `enabled`: Boolean (true/false)
- `state`: String ("DISABLED", "READY", or "FAULT")

## 🎨 State Color Codes

| State | Color | Condition |
|-------|-------|-----------|
| DISABLED | Gray | enabled = false |
| READY | Green | enabled = true AND throttle ≤ 70% |
| FAULT | Red | enabled = true AND throttle > 70% |

## 🔍 Finding Your Serial Port

**Windows:**
1. Device Manager → Ports (COM & LPT)
2. Look for "USB Serial Port (COMX)"
3. Use that COM number

**macOS:**
```bash
ls /dev/cu.*
# Look for: /dev/cu.usbserial-XXXX
```

**Linux:**
```bash
ls /dev/ttyUSB*
# Usually: /dev/ttyUSB0
```

## 🐛 Troubleshooting Checklist

**Dashboard won't start:**
- [ ] Python installed? Run: `python --version`
- [ ] Dependencies installed? Run: `pip install -r requirements.txt`
- [ ] In correct folder? Run: `ls` (should see main.py)

**Serial connection fails:**
- [ ] ESP32 plugged in via USB?
- [ ] Correct port in config/app_config.yaml?
- [ ] On Linux: Added to dialout group?

**No data showing:**
- [ ] Bottom status bar shows "Connected"?
- [ ] Check logs/app.log for errors
- [ ] ESP32 sending correct JSON format?
- [ ] Baudrate matches (115200)?

## 📊 File Roles Summary

| File | Purpose | Edit? |
|------|---------|-------|
| main.py | Entry point, run this | Sometimes (change data source) |
| requirements.txt | Python packages needed | No |
| config/app_config.yaml | Settings (port, threshold) | Yes |
| comms/serial_comm.py | Serial communication | No |
| comms/wifi_comm.py | WiFi communication | No |
| comms/data_simulator.py | Test data generator | No |
| core/state_machine.py | State logic | No |
| ui/main_window.py | Main window | No |
| ui/dashboard_layout.py | UI layout | No |
| assets/theme.qss | Visual styling | Yes (if customizing) |
| logs/app.log | Error messages | Read only |

## 💡 Customization Quick Edits

### Change Fault Threshold (e.g., to 80%)
Edit `config/app_config.yaml`:
```yaml
throttle:
  fault_threshold: 80.0
```

### Change Update Speed
Edit `config/app_config.yaml`:
```yaml
ui:
  update_rate_ms: 100  # Slower (was 50)
```

### Change Plot History Length
Edit `ui/plot_widget.py` line 20:
```python
def __init__(self, history_seconds=20, ...):  # Was 10
```

### Change Window Size
Edit `ui/main_window.py` line 24:
```python
self.setMinimumSize(1200, 800)  # Bigger
self.resize(1400, 900)
```

## 🧪 Testing Without Hardware

The simulator automatically cycles through different scenarios:
- Low throttle (~20%)
- Medium throttle (~50%)
- Near limit (~65%)
- Fault condition (~75-85%)
- Enable/disable toggles

Perfect for:
- Development
- Demonstrations
- Screenshots/videos
- Testing UI changes

## 📝 Important Commands

```bash
# Run application
python main.py

# Run tests
python -m unittest tests/test_state_machine.py

# Check logs
cat logs/app.log           # macOS/Linux
type logs\app.log         # Windows

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python packages
pip list

# Freeze your environment
pip freeze > requirements.txt
```

## 🎯 Interview Highlights

When discussing this project:

1. **Architecture**: "Separated concerns - comms, core logic, and UI are independent"
2. **Real-time**: "Non-blocking communication using QThread for responsiveness"
3. **Scalability**: "Abstract data source interface - swap Serial/WiFi/Simulator without changing UI"
4. **State Management**: "Implemented proper state machine with clear transition rules"
5. **Professional**: "Logging, error handling, configuration files, and documentation"

## 📖 Further Reading

- Full documentation: `README.md`
- Setup guide: `SETUP_GUIDE.md`
- Code comments: Read inline documentation in each .py file
- PyQt6 docs: https://doc.qt.io/qtforpython-6/
- PyQtGraph: https://pyqtgraph.readthedocs.io/

---
**Remember**: Check `logs/app.log` first when something doesn't work!
