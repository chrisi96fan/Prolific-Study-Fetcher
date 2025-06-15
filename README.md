# Prolific Study Fetcher
   
Script to automatically open study notification for prolific.com and join them.

This script uses the official Prolific Assistant and Prolific Studies Notifier by spin311. 
For a Firefox-compatible version of this extension, please see my fork: [chrisi96fan/ProlificAutomaticStudies](https://github.com/chrisi96fan/ProlificAutomaticStudies)

You can find installation instructions and releases there.

Note: This is intended as a personal project. Some parameters like screen coordinates used with pyautogui are customized to my specific setup and most likely won't work for other setups, at least for the main file Prolific_Study_Catcher.py which I am using myself.

# Requirements: 

The required Python libraries are listed in the requirements.txt file. You can install them with:

pip install -r requirements.txt

# Tesseract OCR:

This script uses the text recognition software tesseract ocr to join studies on the prolific dashboard.

You can download it under [tesseract ocr](https://github.com/tesseract-ocr/tesseract)


# How it works:

1. Detects notifications from Chrome/Firefox using Windows events.

2. Opens study with the prolific assistant extensions and tries to join them.

3. For studies appearing on the prolific dashboard, it uses the text recognition software tesseract ocr to locate the join button.

4. Sends a notification via Telegram and Discord Webhook.


# Setup:
1. Choose the file based on your browser and screen resolution.

   Screen coordinates like chrome_random and firefox_random define where PyAutoGUI clicks on your screen.  
   Only the PyAutoGUI parameters in Prolific_Study_Fetcher.py, Prolific_Study_Fetcher_Chrome_1440p.py and Prolific_Study_Fetcher_Firefox_1080p.py have been tested. The parameters in the other files are roughly calculated but should generally work.
   You still need to adjust the value for firefox_extension manually.
   Use the Pyautogui-coordinates_locator.py script to find the x and y values by hovering over the Prolific Assistant extension icon after pinning it in Firefox.
   To compile the locator script, run the following command in the folder where you cloned the repository:

   pyinstaller Pyautogui-coordinates_locator.py

   Hover over the extension icon and record the x and y values.
   Replace the firefox_extension values in the Prolific_Study_Fetcher_Firefox file with the ones you recorded.

   For Chrome, you need to configure a shortcut for the Prolific Assistant extension.

   Go to: chrome://extensions/shortcuts

   Find the Prolific Assistant extension.

   Set the shortcut to: Alt + Shift + O

2. Manually set up parameters such as the full paths to your Chrome and Firefox browser executables, and to the tesseract.exe 
   on your system. Adjust these paths directly in the script before running.

3. To set up notifications, adjust the webhook URLs (Discord webhook, Telegram bot token, and chat ID) directly in the script 
   before running.
   Make sure to replace the placeholders with your actual values.

3. To compile the script, run the following command in the folder where you cloned the repository. 
   Replace the filename with the specific version you're using (e.g., Prolific_Study_Fetcher_Chrome_1440p.py, Prolific_Study_Fetcher_Firefox_1080p.py, etc.) like:

   pyinstaller Prolific_Study_Fetcher_Chrome_1440p.py --noconsole


# Automation Setup (Windows)

This script is triggered via a scheduled task in Windows Task Scheduler:

1. Create a New Task named prolific.
   
2. Under the Trigger tab:

   Begin the task: On an event

   Log: Microsoft-Windows-PushNotifications-Platform/Operational

   Source: PushNotifications-Platform

   Event ID: 3052

3. Under the Actions tab:

   Action: Start a program

   Program/script: Select the compiled Prolific_study_Fetcher.exe file

   Make sure that notifications for other apps/programs are disabled, except for Chrome and Firefox. This ensures that only browser-based notifications trigger the script.


# Extended Setup

By default, the script triggers on every browser notification even if you're actively using the PC.
With this setup, the script will only run when the monitor is powered off, preventing unwanted triggers.

1. Install [powereventprovider](https://github.com/hirschmann/powereventprovider)

2. Create two batch files and save them in a permanent directory

   enable_prolific.bat:
   
   @Echo Off
   schtasks /Change /TN \prolific /Enable
   exit
   
   and
   
   disable_prolific.bat:
   
   
   @Echo Off
   schtasks /Change /TN \prolific /Disable
   exit

3.  In Windows Task Scheduler, create two new tasks:
      Enable Prolific Task:
      
      Begin the task: On an event
      
      Log: Application
      
      Source: PowerEventProvider
      
      Event ID: 5000 (Monitor OFF)
      
      Action: Start a program → Select enable_prolific.bat
      
      Run with highest privileges
      
      Disable Prolific Task:
      
      Begin the task: On an event
      
      Log: Application
      
      Source: PowerEventProvider
      
      Event ID: 5001 (Monitor ON)
      
      Action: Start a program → Select disable_prolific.bat
      
      Run with highest privileges
      

