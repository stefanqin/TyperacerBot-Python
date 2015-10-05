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
approx_WPM = 100
num_of_races = 20

load_delay = 15
type_URL = 'http://play.typeracer.com'

#num_or_races/num_error_messages tracker
race_num = 0
num_errors = 6

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
            print("Failed to open start screen Errno:",1,file=sys.stderr)

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
            print("Failed to enter race. Errno:",2,file=sys.stderr)

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
            #driver.find_element_by_class_name("nonHideableWords").text
            text = WebDriverWait(driver,load_delay).until(
                EC.visibility_of_element_located(
                    (By.CLASS_NAME,"nonHideableWords")
                    )
                ).text
            arrText = text.split(' ')
        except TimeoutException:
            print("Text couldn't be found. Errno:",6,file=sys.stderr)
        return arrText


    def startTyping(self,full_text): #input speed params here
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
        print('\n')

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
            print("Race failed to finish. Errno:",3,file=sys.stderr)

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
            print("Pop-up didn't load. Errno:",4,file=sys.stderr)

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
            print("Captcha tester didn't load. Errno:",5,file=sys.stderr)

def main():
    global race_num
    global approx_WPM
    global num_of_races

    try:
        #change name of bot_one to something like typebot
        bot_one = typeBot(num_of_races,approx_WPM)
        bot_one.initPage()
        bot_one.enterRace()

        while race_num < bot_one.num_races:
            full_text = bot_one.waitForCount()
            bot_one.startTyping(full_text)

            if race_num < bot_one.num_races:
                bot_one.raceAgain()

                #check if "sign me up!" pop-up appears.
                if race_num == 2:
                    bot_one.dontSignUp()
    except:
        raise

if __name__=="__main__":
    main()
