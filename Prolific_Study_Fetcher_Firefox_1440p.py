import keyboard
import time
import requests
import pyperclip
import pyautogui, sys
import os
import webbrowser
import re
import cv2
import mss
from PIL import Image
import numpy as np
import pytesseract


# pyautogui parameters 

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False


# various variables needed for the script to function properly

starting_page = "https://example.com/"
prolific_dashboard = "https://app.prolific.com/studies"
prolific_submissions = "https://app.prolific.com/submissions"
prolific_404 = "https://app.prolific.com/404"
error = "callback"
error_2 = "login"
confirmation_check = "remaining"
confirmation_check_2 = "reserved"
study_full_check = "this study is now full"
firefox_failsafe = 0
urls_firefox = []
found_midpoint_firefox = False
browser = "firefox"

# path to and firefox .exes
pth_firefox = r""


# variables for notifications using Telegram and Discord

bot_token = "" # Bot token for Telegram
chat_id = ""  # chat id for the telegram channel the notifications get send to 
url = "https://api.telegram.org/bot%s/sendMessage?chat_id=%s" % (bot_token, chat_id)
webhook_url = "" # webhook for discord



# text recognition for joining studies from the dashboard

# path to the pytesseract.exe
pytesseract.pytesseract.tesseract_cmd = r""

# keywords to look for
target_text_1 = "take"
target_text_2 = "part"




# pyautogui coordinates for a 1080 main monitor

firefox_random = (2289, 1284)      # random coordinate in the bottom right corner of the firefox browser
firefox_extension = (2188, 80)    # location for the firefox prolific assistant extension
firefox_open_study = (1788, 257)   # opens the study inside of the extension
firefox_automatic = (2049, 953)    # first location for the joining study button in firefox
firefox_not_automatic = (1976, 767) # second location for the joining study button in firefox
firefox_ai = (1892, 1070)        # third location for the joining study button in firefox



# opens the study inside of the prolific assistant extension

def extension_click():
    time.sleep(0.1)
    pyautogui.click(*firefox_extension)
    time.sleep(1)
    pyautogui.click(*firefox_open_study) 

# saves the url of a website to a variable

def get_url():
        time.sleep(0.1)
        keyboard.press_and_release("ctrl + l")
        time.sleep(0.1) 
        keyboard.press_and_release("ctrl + c") 
        time.sleep(0.1) 
        site_url = pyperclip.paste()
        return site_url


# saves the content of a website to a variable

def get_content():
        time.sleep(0.1)
        keyboard.press_and_release("ctrl + a")
        time.sleep(0.1) 
        keyboard.press_and_release("ctrl + c")
        time.sleep(0.1) 
        site_content = pyperclip.paste()
        return site_content


# clicks on study joining buttons in one browser

def join_buttons_browser(loops, browser):
        if browser == "firefox":
            for i in range(loops):
                pyautogui.click(*firefox_automatic) 
                pyautogui.click(*firefox_not_automatic)  
                pyautogui.click(*firefox_ai) 
                time.sleep(1)

def reload_browser(browser):
    time.sleep(0.2)
    if browser == "firefox":
        pyautogui.click(*firefox_random) 
    time.sleep(0.1)
    keyboard.press_and_release("F5")  
    time.sleep(4)

# compares urls, sends notification with study url via telegram/discord and tries to join

def join_study():

    join_buttons_browser(4, browser)

    time.sleep(0.4) 
    pyautogui.click(*firefox_random) 
    firefox_url = get_url()
    study_url = firefox_url

    if len(study_url) < 300:
        requests.post(url, json={'text': study_url}, timeout=10)
        requests.post(webhook_url, json={"content": study_url}, timeout=10)
        time.sleep(0.1)
        join_buttons_browser(1, browser)

    return study_url


# uses the text recognition software tesseract ocr to search for keywords on the screen to join studies showing up on the prolific dashboard

def locate_join_button():
    with mss.mss() as sct:
        monitors = sct.monitors

        left = min(monitor['left'] for monitor in monitors)
        top = min(monitor['top'] for monitor in monitors)
        right = max(monitor['left'] + monitor['width'] for monitor in monitors)
        bottom = max(monitor['top'] + monitor['height'] for monitor in monitors)

        bbox = (left, top, right, bottom)

        screenshot = sct.grab(bbox)
        screenshot = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')

    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)

    coords = None

    for i in range(len(data['text'])):
        if data['text'][i].lower() == "take":
            take_coords = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            if i + 1 < len(data['text']) and data['text'][i + 1].lower() == "part":
                part_coords = (data['left'][i + 1], data['top'][i + 1], data['width'][i + 1], data['height'][i + 1])
                
                left_x = min(take_coords[0], part_coords[0])
                top_y = min(take_coords[1], part_coords[1])
                right_x = max(take_coords[0] + take_coords[2], part_coords[0] + part_coords[2])
                bottom_y = max(take_coords[1] + take_coords[3], part_coords[1] + part_coords[3])

                midpoint = ((left_x + right_x) // 2, (top_y + bottom_y) // 2)

                return midpoint
    return None


# initializes firefox browser  
def open_browser():

    webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(pth_firefox))
    firefox = webbrowser.get('firefox')
    firefox.open_new_tab(starting_page)
    
    return firefox

# checks a browser page for certain keywords

def check_content(content):
    if confirmation_check in content or confirmation_check_2 in content:
        return "joined", None
    elif study_full_check in content:
        return "full", None
    else:
        pattern = r"([1-9][0-9]{0,3})\splaces?"
        match = re.search(pattern, content)

        if match:
            places = match.group(0) 
            return "places", places
        else:
            return None, None

# sends notifications via telegram and discord

def send_notification(result,places = None):
    if result == "joined":
        requests.post(url, json={"text": "joined study"}, timeout=10)
        requests.post(webhook_url, json={"content": "joined study"}, timeout=10)

    elif result == "full":
        requests.post(url, json={"text": "study is full"}, timeout=10)  
        requests.post(webhook_url, json={"content": "study is full"}, timeout=10)
    elif result ==  "places":
        requests.post(url, json={"text": places}, timeout=10)
        requests.post(webhook_url, json={"content": places}, timeout=10)
    else:
        pass








# main script starts here

# # opens an empty page to focus both browsers and for url comparison
firefox = open_browser()

# opens the study inside of the prolific assistant extension
time.sleep(0.5) 
extension_click()

time.sleep(2)
study_url = join_study() # compares urls, sends notification with study url via telegram/discord and tries to join them by clicking on the join buttons
if len(study_url) > len(prolific_404):
    join_buttons_browser(2, browser)
    

    # spots possible errors in the study url and repeats the whole process 
    if error in study_url or error_2 in study_url or len(study_url) > 300:
        extension_click()
        time.sleep(2)
        study_url = join_study()
        if len(study_url) > len(starting_page):
            join_buttons_browser(4, browser)
        else: # opens the topmost notification in the windows notification center
            time.sleep(1)
            os.system("start ms-actioncenter:")
            time.sleep(0.5)
            pyautogui.click(x = 2365, y = 153)
            pyautogui.click(*firefox_random)
            time.sleep(2.5)

            join_buttons_browser(2, browser)
            

    time.sleep(0.1)
    pyautogui.click(*firefox_random) 
    content = get_content()
    result, places = check_content(content)
    if result:
        send_notification(result, places)
    if result == "places":
        join_buttons_browser(6, browser)
        
        reload_browser(browser)
        time.sleep(4)
        content = get_content()
        result,places = check_content(content)
        if result == "joined":
            send_notification(result, places)




 # this part is for joining studies that show up on the prolific dashboard page
elif study_url == starting_page:
    # changes the browser tab to the prolific dashboard in firefox, failsafe to not get stuck in a inifite loop

    firefox_url = ""
    pyautogui.click(*firefox_random)
    time.sleep(0.2)
    while firefox_url != prolific_dashboard and firefox_failsafe < 20:
        firefox_url = get_url()
        urls_firefox.append(firefox_url)
        firefox_failsafe += 1
        if firefox_url != prolific_dashboard:
            keyboard.press_and_release("ctrl + shift + tab")
        
        time.sleep(0.5)
        pyautogui.click(*firefox_random)
        time.sleep(0.1)
        keyboard.press_and_release("page down")
        time.sleep(0.1)
        keyboard.press_and_release("page down")
        time.sleep(0.2)
        
        midpoint_firefox = locate_join_button()
        
        if midpoint_firefox:
            time.sleep(0.2)
            for i in range(7):
                pyautogui.click(*midpoint_firefox)
                time.sleep(1.5)
            found_midpoint_firefox = True


    # if a button was found, checks page if joining was succesfull and sends notification     
    if found_midpoint_firefox :
        time.sleep(1)
        firefox.open_new_tab(prolific_submissions)
        time.sleep(10)
        pyautogui.click(*firefox_random)
        content = get_content()
        result, places = check_content(content)
        if result == "joined":
            send_notification(result, places)
            time.sleep(0.2)
            pyautogui.click(*firefox_random)
            firefox_tesseract_url = get_url()
            requests.post(url, json={'text': firefox_tesseract_url}, timeout=10)
            requests.post(webhook_url, json={"content": firefox_tesseract_url}, timeout=10)
        elif result is None:
            requests.post(url, json={'text': "could not join study"}, timeout=10) 
            requests.post(webhook_url, json={"content": "could not join study"}, timeout=10)
        
        time.sleep(1) 
        for i in range(2):
            time.sleep(0.3) 
            pyautogui.click(*firefox_random)
            time.sleep(0.1) 
            keyboard.press_and_release("ctrl + w")  
    else:
        requests.post(url, json={'text': "no midpoint"}, timeout=10)
        for i in range(2):
            time.sleep(0.3) 
            pyautogui.click(*firefox_random)
            time.sleep(0.1) 
            keyboard.press_and_release("ctrl + w")     
    
    # if no dashboard page was found, opens a new one in the browser
    if prolific_dashboard not in urls_firefox:
        firefox.open_new_tab(prolific_dashboard)

    


 # due to a bug in the prolfic assistant extension for a short peroid of time every opened study lead to a faulty 404 error page
 # this part deals with this rare case, as studies show up on a newly opened dashboard page instead
elif study_url == prolific_404:

    firefox.open_new_tab(prolific_dashboard)
    time.sleep(3)
    pyautogui.click(*firefox_random)
    time.sleep(0.1)
    keyboard.press_and_release("page down")
    time.sleep(0.1)
    keyboard.press_and_release("page down")
    
    # calls the text recognition fucntion
    midpoint_firefox = locate_join_button()
    
    if midpoint_firefox:
        time.sleep(0.2)
        pyautogui.click(*midpoint_firefox)
        for i in range(6):
            pyautogui.click(*midpoint_firefox)
            time.sleep(1.5)
        found_midpoint_firefox = True
        
    else:
        requests.post(url, json={'text': "no firefox midpoint"}, timeout=10) 
        time.sleep(0.3) 
        pyautogui.click(*firefox_random)
        time.sleep(0.1) 
        keyboard.press_and_release("ctrl + w")    

    if found_midpoint_firefox:
        time.sleep(1)
        firefox.open_new_tab(prolific_submissions)
        time.sleep(10)
        pyautogui.click(*firefox_random)
        content = get_content()
        result, places = check_content(content)
        if result == "joined":
            send_notification(result, places)
            time.sleep(0.2)
            pyautogui.click(*firefox_random)
            firefox_tesseract_url = get_url()
            requests.post(url, json={'text': firefox_tesseract_url}, timeout=10)
            requests.post(webhook_url, json={"content": firefox_tesseract_url}, timeout=10)
        elif result is None:
            requests.post(url, json={'text': "could not join study"}, timeout=10) 
            requests.post(webhook_url, json={"content": "could not join study"}, timeout=10)
        
        time.sleep(1) 
        for i in range(2):
            time.sleep(0.3) 
            pyautogui.click(*firefox_random)
            time.sleep(0.1) 
            keyboard.press_and_release("ctrl + w")    

