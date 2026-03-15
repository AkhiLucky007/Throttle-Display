# Step-by-Step Tutorial: Running Your First Dashboard

This tutorial assumes you know NOTHING about programming or Python. Let's get you up and running!

## 🎯 What We're Going to Do

By the end of this tutorial, you'll see a cool dashboard on your screen showing:
- A number changing in real-time (throttle percentage)
- A live scrolling graph
- Color-coded status indicators

No hardware needed for now - we'll use a simulator!

---

## Part 1: Installing Python (15 minutes)

### Windows Users

**Step 1:** Open your web browser (Chrome, Edge, Firefox, etc.)

**Step 2:** Go to: `https://www.python.org/downloads/`

**Step 3:** You'll see a big yellow button that says "Download Python 3.XX.X" - Click it!

**Step 4:** Wait for the download to finish (check your Downloads folder)

**Step 5:** Double-click the downloaded file (it's called something like `python-3.11.x.exe`)

**Step 6:** ⚠️ **VERY IMPORTANT** - You'll see a checkbox at the bottom that says:
```
☐ Add Python to PATH
```
**CLICK THIS CHECKBOX!** It's crucial!

**Step 7:** Click "Install Now"

**Step 8:** Wait for installation (might take 2-3 minutes)

**Step 9:** Click "Close" when it's done

**Step 10:** Let's verify it worked:
1. Press the Windows key (⊞) + R
2. Type: `cmd`
3. Press Enter
4. A black window opens (Command Prompt)
5. Type: `python --version`
6. Press Enter
7. You should see: `Python 3.11.x` or similar

✅ **If you see the Python version - SUCCESS! Move to Part 2.**

❌ **If you see "python is not recognized":**
- You forgot to check "Add to PATH"
- Uninstall Python (Control Panel → Programs)
- Re-install and CHECK THE BOX

### macOS Users

**Step 1:** Open "Terminal" 
- Press Cmd + Space
- Type "Terminal"
- Press Enter

**Step 2:** Copy and paste this command (then press Enter):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
(This installs "Homebrew" - a tool for installing other tools)

**Step 3:** It will ask for your password - type it and press Enter
(You won't see the password as you type - that's normal!)

**Step 4:** Wait... this takes 5-10 minutes. Be patient!

**Step 5:** Once finished, run:
```bash
brew install python@3.11
```

**Step 6:** Verify:
```bash
python3 --version
```
You should see: `Python 3.11.x`

✅ **Success! Move to Part 2.**

---

## Part 2: Getting the Project Files (5 minutes)

**Step 1:** You should have received a folder called `throttle_dashboard`

**Step 2:** Copy this folder to an easy-to-find location:
- **Windows:** `C:\Users\YourName\Documents\throttle_dashboard`
- **macOS:** Drag it to your Documents folder

**Step 3:** Remember where you put it! You'll need this location soon.

---

## Part 3: Installing Required Libraries (10 minutes)

Think of this like installing apps on your phone - Python needs some extra tools to run this dashboard.

### Windows Users

**Step 1:** Press Windows key (⊞) + R

**Step 2:** Type: `cmd` and press Enter

**Step 3:** You need to navigate to your project folder. Type this (replace YourName with YOUR username):
```
cd C:\Users\YourName\Documents\throttle_dashboard
```
Press Enter

**Step 4:** Verify you're in the right place. Type:
```
dir
```
Press Enter

You should see a list of files including `main.py` and `requirements.txt`

**Step 5:** Now install the libraries. Type:
```
python -m pip install -r requirements.txt
```
Press Enter

**Step 6:** Watch the magic happen! 🎭
- You'll see lots of text scrolling
- Don't worry, it's installing things
- This takes 2-5 minutes
- Wait for it to finish (you'll see the cursor blinking again when done)

✅ **When you see the blinking cursor again - you're done!**

### macOS Users

**Step 1:** Open Terminal (Cmd + Space, type "Terminal")

**Step 2:** Navigate to project folder:
```bash
cd ~/Documents/throttle_dashboard
```
Press Enter

**Step 3:** Verify location:
```bash
ls
```
You should see files listed including `main.py`

**Step 4:** Install libraries:
```bash
python3 -m pip install -r requirements.txt
```
Press Enter

**Step 5:** Wait for installation to complete (2-5 minutes)

✅ **Done when you see the cursor blinking again!**

---

## Part 4: Running the Dashboard! (2 minutes)

This is the exciting part! 🚀

### Windows

**Step 1:** Make sure you're still in the Command Prompt from Part 3
(If you closed it, repeat Part 3 steps 1-4)

**Step 2:** Type:
```
python main.py
```

**Step 3:** Press Enter

**Step 4:** Wait 2-3 seconds...

**Step 5:** 🎉 **A window should open!**

### macOS

**Step 1:** In Terminal (should still be in project folder):
```bash
python3 main.py
```

**Step 2:** Press Enter

**Step 3:** 🎉 **A window should open!**

---

## Part 5: Understanding What You See

### What's on the Dashboard?

```
┌─────────────────────────────────────────────┐
│        THROTTLE DASHBOARD                   │
├─────────────────────┬───────────────────────┤
│  THROTTLE POSITION  │   SYSTEM STATE        │
│                     │                       │
│      72.3 %         │      FAULT            │
│                     │     (in red)          │
├─────────────────────┴───────────────────────┤
│                                             │
│        LIVE THROTTLE SIGNAL                 │
│    (A graph showing a line going up/down)   │
│                                             │
├─────────────────────────────────────────────┤
│ System Enabled: YES  │  Connection: Active  │
└─────────────────────────────────────────────┘
```

### What's Happening?

1. **Top Left (Throttle Position):**
   - Shows a percentage (0-100%)
   - The number changes in real-time
   - Color changes:
     - Blue = Normal (0-60%)
     - Orange = Warning (60-70%)
     - Red = Too high (>70%)

2. **Top Right (System State):**
   - **DISABLED** (Gray) = System is off
   - **READY** (Green) = System is on and safe
   - **FAULT** (Red) = Throttle is too high (>70%)

3. **Middle (Live Graph):**
   - Shows throttle over time (last 10 seconds)
   - Line scrolls from right to left
   - Yellow zone = Warning area
   - Red dashed line = Danger threshold

4. **Bottom (Status Bar):**
   - Left: Shows if system is enabled
   - Right: Shows connection status
   - Should say "Simulator Active" (means it's working!)

### Watch It Work!

Just leave it running for a minute and watch:
- The percentage changes randomly
- The graph scrolls
- Sometimes it says FAULT (when throttle > 70%)
- Sometimes it says READY (when throttle is safe)
- Sometimes it says DISABLED (system off)

**This is the SIMULATOR** - it's creating fake data so you can see how it works!

---

## Part 6: Stopping the Dashboard

**Easy!** Just close the window (click the X button)

Or, in the Command Prompt/Terminal, press `Ctrl + C`

---

## Troubleshooting: "It didn't work!"

### Problem: "python is not recognized"
**Fix:** Python isn't installed correctly
- Go back to Part 1
- Make sure you checked "Add to PATH"
- Try: `py --version` instead of `python --version`

### Problem: "No module named PyQt6"
**Fix:** Libraries aren't installed
- Go back to Part 3
- Make sure you see "Successfully installed" messages
- Try running the install command again

### Problem: Window opens and closes immediately
**Fix:** There's an error we need to see
- DON'T double-click `main.py`
- ALWAYS run from Command Prompt/Terminal
- Look for red error text
- Copy the error and Google it

### Problem: "Cannot find file main.py"
**Fix:** You're in the wrong folder
- Use `dir` (Windows) or `ls` (macOS) to see files
- Make sure you see `main.py` listed
- If not, use `cd` to navigate to correct folder

### Problem: Nothing displays on the graph
**Fix:** Check the bottom status bar
- Should say "Simulator Active"
- If it says "Disconnected" - close and restart
- Check `logs/app.log` for error messages

---

## Next Steps

### Want to Customize It?

**Change the fault threshold:**
1. Open `config` folder
2. Open `app_config.yaml` with Notepad
3. Find the line: `fault_threshold: 70.0`
4. Change 70.0 to something else (like 80.0)
5. Save the file
6. Run the dashboard again

**Change colors:**
1. Open `assets` folder
2. Open `theme.qss` with Notepad
3. Look for color codes like `#22c55e` (green)
4. Change them to other colors
5. Save and run again

### Want to Learn More?

1. Read `README.md` for full documentation
2. Read `QUICK_REFERENCE.md` for quick tips
3. Look at the code files - they have comments explaining everything!
4. Try editing small things and see what happens

### Ready for Real Hardware?

When your friend finishes the ESP32 part:
1. Read `SETUP_GUIDE.md`
2. Follow "Step 7: Running with Real Hardware"
3. You'll connect via USB instead of using the simulator

---

## Congratulations! 🎉

You've successfully:
- ✅ Installed Python
- ✅ Set up the project
- ✅ Installed libraries
- ✅ Ran a professional embedded systems dashboard

This is the SAME kind of software used in real engineering companies!

**What makes this impressive:**
- Real-time data visualization
- Professional UI design
- Clean code architecture
- Industry-standard tools

Perfect for showing in interviews! 💼

---

## Quick Command Reference

**Run the dashboard:**
```bash
# Windows
python main.py

# macOS/Linux
python3 main.py
```

**Check Python version:**
```bash
python --version
```

**Navigate to project:**
```bash
# Windows
cd C:\Users\YourName\Documents\throttle_dashboard

# macOS
cd ~/Documents/throttle_dashboard
```

**See current folder files:**
```bash
# Windows
dir

# macOS/Linux
ls
```

---

Remember: The Command Prompt/Terminal is your friend! Don't be scared of it. It's just another way to talk to your computer. 😊
