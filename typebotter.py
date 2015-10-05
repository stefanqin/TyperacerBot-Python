#!/usr/bin/env python
# coding=utf-8

"""Typeracer bot v1.0

Races as a guest in the web game play.typeracer.com.

Author: Stefan Qin
Version: 1.0
See README.md
Link: https://github.com/stefanqin/TyperacerBot-Python
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import sys

#variable parameters -> YOU CAN CHANGE THESE
approx_WPM = 90
num_of_races = 5

load_delay = 15
type_URL = 'http://play.typeracer.com'

#num_or_races/speeds tracker
race_num = 0
speeds = []

#available error messages
err_msgs = {
    "default": "Nothing wrong here!",
    "ERR_ONE": "Failed to open start screen. Errno: 1",
    "ERR_TWO": "Failed to enter race. Errno: 2",
    "ERR_THREE": "Race failed to finish. Errno: 3",
    "ERR_FOUR": "Pop-up didn't load. Errno: 4",
    "ERR_FIVE": "Captcha tester didn't load. Errno: 5",
    "ERR_SIX": "Text couldn't be found. Errno: 6",
    "ERR_SEVEN": "WPM couldn't be found. Errno: 7"
}
curr_err_msg = err_msgs["default"]

def main():
    global race_num
    global approx_WPM
    global num_of_races
    global curr_err_msg
    global err_msgs

    try:
        bot_one = typeBot(num_of_races,approx_WPM)
        bot_one.initPage()
        bot_one.enterRace()

        while race_num < bot_one.num_races:
            try:
                full_text = bot_one.waitForCount()
                bot_one.startTyping(full_text)

                if race_num < bot_one.num_races:
                    bot_one.getSpeed()
                    bot_one.raceAgain()

                    #check if "sign me up!" pop-up appears.
                    if race_num == 2:
                        bot_one.dontSignUp()
            except TimeoutException:
                raise TimeoutException(curr_err_msg)
                exit()

        print("Your average speed over",num_of_races,"races was",
            str(sum(speeds)/num_of_races) + ".")

    except TimeoutException:
        raise TimeoutException(curr_err_msg)
        exit()

class typeBot():
    def __init__(self,num_races,WPM_chosen):
        self.driver = webdriver.Chrome()

        #seconds per word
        self.SPW = 60/WPM_chosen
        self.num_races = num_races

        self.driver.maximize_window()

    def loginToAcc(self):
        """Login to specified account"""

        self.driver = driver

    def initPage(self):
        """Open the initial page

        Raises:
            TimeoutException: If start screen fails to load on time.
        """

        driver = self.driver

        #access initial startup screen. JS elems take a while to load.
        driver.get(type_URL)
        try:
            init_loaded = WebDriverWait(driver,load_delay).until(
            EC.presence_of_element_located((By.CLASS_NAME, "gwt-Anchor"))
            )
        except TimeoutException:
            curr_err_msg = err_msgs["ERR_ONE"]

    def enterRace(self):
        """Enters race from start screen.

        Raises:
            TimeoutException: Failed to enter race.
        """

        driver = self.driver

        #ctrl+Alt+I = start race keyboard shortcut
        driver.find_element_by_tag_name("body").send_keys(
            Keys.CONTROL+Keys.ALT+'i')

        #enter race
        try:
            race_entered = WebDriverWait(driver,load_delay).until(
                EC.visibility_of_element_located((By.CLASS_NAME,"gameStatusLabel"))
            )
        except TimeoutException:
            curr_err_msg = err_msgs["ERR_TWO"]

    def waitForCount(self):
        """Wait for the countdown timer."""

        global race_num
        driver = self.driver

        #Get text to type
        full_text = self.getText()
        while not full_text[0]:
            time.sleep(0.5)
            full_text = self.getText()

        #wait until countdown timer ends
        race_started = driver.find_element_by_class_name("gameStatusLabel")

        while (("The race is on!" not in race_started.text)
                and ("Go!" not in race_started.text)):
            race_started = driver.find_element_by_class_name("gameStatusLabel")
            time.sleep(0.5)

        race_num += 1

        return full_text

    def getText(self):
        """Function to return a list of the text.

        Raises:
            TimeoutException: If typing paragraph doesn't appear.
        """

        driver = self.driver

        try:
            text = WebDriverWait(driver,load_delay).until(
                EC.visibility_of_element_located(
                    (By.CLASS_NAME,"nonHideableWords")
                    )
                ).text
            arrText = text.split(' ')
        except TimeoutException:
            curr_err_msg = err_msgs["ERR_SIX"]

        return arrText


    def startTyping(self,full_text):
        """Start typing

        todo:
            implement minimum WPM checker
            implement range of WPM with seed generator
            implement accuracy generator
        """

        driver = self.driver

        #focus the input box
        input_box = driver.find_element_by_class_name("txtInput")
        input_box.send_keys('')

        #start typing!
        print("Typing Progress:")
        for word in full_text:
            print(word,end=' '),
            time.sleep(self.SPW)
            input_box.send_keys(word)
            if input_box.is_displayed():
                input_box.send_keys(' ')
        print("\n")

    def getSpeed(self):
        """Gets the actual WPM of the race.

        Raises:
            TimeoutException: Failed to grab speed.
        """

        driver = self.driver

        #get speed
        try:
            actual_speed = WebDriverWait(driver,load_delay).until(
                EC.visibility_of_element_located(
                    (By.CLASS_NAME,"rankPanelWpm")
                )
            ).text
            print("Bot WPM:",actual_speed,"\n")

            #store int(WPM) in speeds
            speeds.append(int(''.join(x for x in actual_speed if x.isdigit())))
        except TimeoutException:
            curr_err_msg = err_msgs["ERR_SEVEN"]

    def raceAgain(self):
        """Click race again.

        Raises:
            TimeoutException: Race fails to finish.
        """

        driver = self.driver

        try:
            race_again_href = WebDriverWait(driver,load_delay).until(
                EC.element_to_be_clickable((By.CLASS_NAME,"raceAgainLink"))
            )
            driver.execute_script("arguments[0].click()",race_again_href)
        except TimeoutException:
            curr_err_msg = err_msgs["ERR_THREE"]

    def dontSignUp(self):
        """Click "no thanks :(" on the 'Sign me up!' pop-up.

        Raises:
            TimeoutException: Popup doesn't appear.
        """

        driver = self.driver

        try:
            WebDriverWait(driver,load_delay).until(
                EC.element_to_be_clickable(
                    (By.XPATH,"//a[text()='No thanks :(']")
                    )
                ).click()
        except TimeoutException:
            curr_err_msg = err_msgs["ERR_FOUR"]

    def takeCaptcha(self):
        """Completes the captcha test to max speed.

        Raises:
            TimeoutException: Captcha pop-up doesn't appear.

        todo:
            Test whether WPM is > 100wpm.
            check wheter it's >= 100wpm or >100wpm
            NOTE: THIS DOESN"T WORK YET!!
        """

        driver = self.driver

        #begin captcha
        try:
            WebDriverWait(driver,load_delay).until(
                EC.element_to_be_clickable(
                    (By.XPATH,"//button[text()='Begin Test']")
                )
            ).click()
        except TimeoutException:
            curr_err_msg = err_msgs["ERR_FIVE"]

if __name__=="__main__":
    main()
