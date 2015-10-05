# TyperacerBot-Python
Typeracer bot with python and selenium ChromeDriver

<b>How to Run:</b>

python3 typebotter.py

<b>What Does it Do?</b>

This bot opens up a new instance of chrome and plays as a guest.
You may specifiy the amount of races + desired WPM in the program params.

<b>Requirements:</b>

Must be somewhat technically minded (run python from cmd line, install selenium chromedriver, etc.)

Please install selenium chromedriver from [here](https://pypi.python.org/pypi/selenium) before using this bot.

<b>Currently doesn't support:</b>

WPM > 100wpm (captcha!)

Logging in.

<b>Additional Remarks:</b>

Heavily affected by lag. Beware!

If the bot fails to begin typing, and no error is shown, you can assume it's because the racing page hasn't loaded yet. Blame it on your ISP.

Lastly, one word = 5 characters. Hence the WPM is further affected by the length of the word typed, since every word is effectively typed by selenium at the same speed. 
