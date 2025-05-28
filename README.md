# Prolific Study Fetcher

Note: This is intended as a personal project. Some parameters like screen coordinates used with pyautogui are customized to my specific setup and most likely won't work for other setups.

# Requirements: 

The required Python libraries are listed in the requirements.txt file. You can install them with:

pip install -r requirements.txt

# Tesseract OCR:

This script uses the text recognition software tesseract ocr to join studies on the prolific dashboard.

You can download it under [tesseract ocr](https://github.com/tesseract-ocr/tesseract)

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


This script uses the official Prolific Assistant and Prolific Studies Notifier by spin311. 
For a Firefox-compatible version of this extension, please see my fork: [chrisi96fan/ProlificAutomaticStudies](https://github.com/chrisi96fan/ProlificAutomaticStudies)

You can find installation instructions and releases there.


# How it works:

1. Detects notifications from Chrome/Firefox using Windows events.

2. Opens study with the prolific assistant extensions and tries to join them.

3. For studies appearing on the prolific dashboard, it uses the text recognition software tesseract ocr to locate the join button.

4. Sends a notification via Telegram and Discord Webhook.


# Setup:
1. Screen coordinates like (chrome_random, firefox_random) define where pyautogui clicks on your screen  
   Most likely you will need to adjust these for your own screen resolution and browser window positions.
   
   I’ve added a helper script to determine screen coordinates used by pyautogui.
   To compile it, run this command in the folder where you cloned this repository:

   pyinstaller Pyautogui-coordinates_locator.py

2. To set up notifications, adjust the webhook URLs (Discord webhook, Telegram bot token, and chat ID) directly in the script 
   before running.
   Make sure to replace the placeholders with your actual values.

3. To compile the script, run this command in the folder where you cloned this repository: 

   pyinstaller Prolific_Study_Fetcher.py--noconsole