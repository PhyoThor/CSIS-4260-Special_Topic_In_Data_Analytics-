I used the following steps for project creation..
however, I would like to test by using conda prompt instead of pip
____________________________________________________________________
To check which are allowed by the website.
www.abcsd.com/robots.text
--------------------------------------------------------------------

https://www.reddit.com/prefs/apps to create apps
Click "Create App" (at the bottom)
    1. App Type: Choose Script
    2. Name: Anything (e.g., "RedditScraper")
    3. Redirect URI: http://localhost
Click Create App
Copy Client ID & Client Secret
--------------------------------------------------------------------

how to create Virtual Environment on VScode for python.
For Window
    - python -m venv venv
    - venv\scripts\activate
For Mac
    - python3 -m venv venv
    - source venv/bin/activate
--------------------------------------------------------------------
**Install Required Libraries
pip install praw pandas textblob sumy
pip install vaderSentiment ---> advance analysis compare to textblob
---------------------------------------------------------------------
Open VS Code
Press Ctrl + Shift + P (or Cmd + Shift + P on Mac) → Type "Python: Select Interpreter"
Choose the virtual environment interpreter (venv).
Now, your VS Code terminal should show (venv).

to run python scripts
python reddit_scraper.py
---------------------------------------------------------------------

FOR USING Anaconda
open "Anaconda Prompt"
    conda create --name reddit_scrapper python=3.9
    conda activate reddit_scrapper
    conda install pandas
    pip install praw textblob sumy (these libraries are not included in conda)
    python -c "import praw; print('Reddit API is ready!')" _____ Test if api is ready or not


To make sure VS Code uses your Conda environment:

1️⃣ Open VS Code
2️⃣ Press Ctrl + Shift + P (or Cmd + Shift + P on Mac)
3️⃣ Type "Python: Select Interpreter"
4️⃣ Choose "Conda (reddit_scraper)"
5️⃣ Now, run your Python script in VS Code!

deepseek api key= sk-521420a4212741a692939cbbf87e8651
openai api key=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
