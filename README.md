# Prolific Study Fetcher

Note: This is intended as a personal project. Some parameters like screen coordinates used with pyautogui are customized to my specific setup and most likely won't work for other setups.

# Requirements: 

The required Python libraries are listed in the requirements.txt file. You can install them with:

pip install -r requirements.txt

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

