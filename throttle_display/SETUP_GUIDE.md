# 🚀 Complete Setup Guide for Beginners

This guide will walk you through every step needed to run the Throttle Dashboard, even if you're new to Python and development.

## Step 1: Install Python

### Windows
1. Go to https://www.python.org/downloads/
2. Download Python 3.11 or 3.12 (latest stable version)
3. **IMPORTANT**: During installation, CHECK the box "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
   - Press `Win + R`, type `cmd`, press Enter
   - Type: `python --version`
   - You should see something like: `Python 3.11.x`

### macOS
1. Open Terminal (Cmd + Space, type "Terminal")
2. Install Homebrew (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Install Python:
   ```bash
   brew install python@3.11
   ```
4. Verify: `python3 --version`

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.11 python3-pip
python3 --version
```

## Step 2: Get the Project Files

### Option A: If you have the folder already
Just extract/copy the `throttle_dashboard` folder to a location like:
- Windows: `C:\Users\YourName\Documents\throttle_dashboard`
- macOS/Linux: `~/Documents/throttle_dashboard`

### Option B: If downloading
1. Download the project ZIP file
2. Extract to a convenient location
3. Remember this location!

## Step 3: Open Terminal/Command Prompt in Project Folder

### Windows
1. Open File Explorer
2. Navigate to the `throttle_dashboard` folder
3. Click in the address bar, type `cmd`, press Enter
4. You should see: `C:\...\throttle_dashboard>`

### macOS/Linux
1. Open Terminal
2. Navigate to project folder:
   ```bash
   cd ~/Documents/throttle_dashboard
   ```
3. Verify you're in the right place:
   ```bash
   ls
   ```
   You should see files like `main.py`, `requirements.txt`, etc.

## Step 4: Install Required Libraries

In your terminal/command prompt (inside the project folder):

### Windows
```bash
python -m pip install -r requirements.txt
```

### macOS/Linux
```bash
python3 -m pip install -r requirements.txt
```

**Wait for it to finish!** You'll see several packages being downloaded and installed:
- PyQt6
- pyqtgraph
- pyserial
- PyYAML
- numpy

This might take 2-5 minutes depending on your internet speed.

## Step 5: Run the Dashboard!

### First Time (Testing with Simulator)

The easiest way to see if everything works:

**Windows:**
```bash
python main.py
```

**macOS/Linux:**
```bash
python3 main.py
```

**What you should see:**
1. A window opens with a dark theme
2. You see a throttle percentage changing
3. A live graph scrolling
4. State indicator changing between READY/FAULT/DISABLED
5. Bottom status bar showing "Simulator Active"

**If this works - CONGRATULATIONS! 🎉 Your setup is complete!**

## Step 6: Understanding the Display

### Top Section
- **Left Card**: Shows current throttle percentage (0-100%)
  - Blue = Normal (0-60%)
  - Orange = Warning (60-70%)
  - Red = Fault (>70%)
  
- **Right Card**: Shows system state
  - DISABLED (Gray): System is off
  - READY (Green): System is on and safe
  - FAULT (Red): Throttle exceeded 70%

### Middle Section
- **Live Plot**: Shows throttle over last 10 seconds
  - Yellow shaded area = Warning zone
  - Red dashed line = Fault threshold

### Bottom Section
- **System Enabled**: Green when enabled, gray when disabled
- **Connection**: Shows if data source is active

## Step 7: Running with Real Hardware (Later)

When your friend completes the ESP32 part:

### For Serial (USB) Connection

1. **Connect ESP32 to USB**

2. **Find your port:**
   - **Windows**: 
     - Open Device Manager
     - Look under "Ports (COM & LPT)"
     - Note the COM number (e.g., COM3, COM4)
   
   - **macOS**: 
     ```bash
     ls /dev/cu.*
     ```
     Look for something like `/dev/cu.usbserial-XXX`
   
   - **Linux**: 
     ```bash
     ls /dev/ttyUSB*
     ```
     Usually `/dev/ttyUSB0`

3. **Edit config file:**
   - Open `config/app_config.yaml` with Notepad (Windows) or TextEdit (Mac)
   - Change the port line:
     ```yaml
     serial:
       port: "COM3"  # Use your actual port here!
     ```
   - Save the file

4. **Edit main.py:**
   - Open `main.py` with Notepad/TextEdit
   - Find lines 42-43 (around there)
   - Replace:
     ```python
     simulator = DataSimulator()
     window.set_data_source(simulator)
     ```
   - With:
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
   - Save the file

5. **Run:**
   ```bash
   python main.py
   ```

## Common Issues & Solutions

### Issue: "python is not recognized"
**Solution**: Python not in PATH
- Reinstall Python and CHECK "Add to PATH" box
- OR use full path: `C:\Python311\python.exe main.py`

### Issue: "No module named PyQt6"
**Solution**: Dependencies not installed
```bash
pip install -r requirements.txt
```

### Issue: Window opens then immediately closes
**Solution**: Check for errors
- Run from terminal/command prompt (not by double-clicking)
- Look at error messages
- Check `logs/app.log` file

### Issue: "Permission denied" on Linux/Mac
**Solution**: Add yourself to dialout group
```bash
sudo usermod -a -G dialout $USER
```
Then logout and login again.

### Issue: Serial port not found
**Solution**: 
1. Verify ESP32 is connected
2. Check port in Device Manager (Windows)
3. Try a different USB cable
4. Update port in `config/app_config.yaml`

### Issue: Nothing displays on graph
**Solution**:
1. Check bottom status bar shows "Connected"
2. Verify ESP32 is sending data
3. Check `logs/app.log` for errors
4. Ensure JSON format is correct

## Useful Commands

### Check if Python is installed
```bash
python --version
```

### Check installed packages
```bash
pip list
```

### Update pip (if needed)
```bash
python -m pip install --upgrade pip
```

### Run tests (to verify code works)
```bash
python -m pytest tests/
```

### Clear log file
**Windows:**
```bash
del logs\app.log
```

**macOS/Linux:**
```bash
rm logs/app.log
```

## File Organization Tips

Keep your project folder organized:

```
throttle_dashboard/
├── main.py                 ← The file you run
├── requirements.txt        ← List of needed libraries
├── config/
│   └── app_config.yaml    ← Settings (port, threshold, etc.)
├── logs/
│   └── app.log            ← Check this for errors
└── ... (other folders)
```

**Important files to know:**
- `main.py` - Start here, this is what you run
- `config/app_config.yaml` - Change settings here
- `logs/app.log` - Check for error messages
- `README.md` - Full documentation

## Next Steps

1. ✅ **Test with simulator** - Make sure it runs
2. ✅ **Read the code** - Understand how it works
3. ⏳ **Wait for hardware** - Your friend builds ESP32 part
4. ⏳ **Connect real hardware** - Follow Step 7
5. ⏳ **Demonstrate** - Show it working in interviews!

## Getting Help

If you get stuck:
1. Check the error message in terminal
2. Look at `logs/app.log`
3. Google the error message
4. Check that all files are in the right folders
5. Verify Python version is 3.10+

Good luck! 🚀
