DevCup 2016 App (backend)
=====

Introduction
-----
Backend API to handle the generation of quiz from article.


##### Approach
We used serveral references for the analyzer. 

First we need to get the summary of a certain article. We use the `newspaper.Article` library to be able to get and extract meaningful stuff that could represent an article in a web page.

Next is we need to summarize the article. Getting question from the whole article sentences is prone to error and will lead to A LOT of false questions. We need something to get the gist of the article so we use [textteaser](https://github.com/DataTeaser/textteaser). We feed the article to text teaser after we extract it from the web page.

Then we need to get the relevant sentences and extract the trivia questions we want. There are several guidelines and demo code that we use here: https://github.com/atbaker/wikipedia-question-generator. The implementation is sound but there are still so many false positives so we need to improve on this.

Lastly is generating the other 3 choices (since this is a multiple choice type of question). This prove to be really difficult since we do not want to give away too many context clues if we just generate random words. So what we did is that we get all the relevant nouns and noun phrases in the sumamrized text. We get the choices from there based on their position on the article (1st question, we will get in the first part of the summary for the choices) so that the terms and ideas is probably related.

#### Running the app
- Runs on Python 3.4+
- Install Python3 and pip3
- Install dependencies `pip3 install -r requirements.txt`
- Start the server `python3 run.py`

#### Project Structure
```
    +-- app/
    |   +-- api/
    |   |   +-- module/
    |   |   |   +-- __init__.py
    |   |   |   +-- dispatch.py
    |   |   |   +-- model.py
    |   +-- conf/
    |   |   +-- env/
    |   |   |   +-- __init__.py
    |   |   |   +-- development.py
    |   |   |   +-- staging.py
    |   |   |   +-- production.py
    |   |   +-- __init__.py
    |   |   +-- config.py
    |   |   +-- constants.py
    |   +-- lib/
    |   |   +-- __init__.py
    |   |   +-- database.py
    |   |   +-- decorators.py
    |   |   +-- error_handler.py
    |   |   +-- response.py
    |   +-- util/
    |   |   +-- __init__.py
    |   |   +-- utils.py
    |   +-- www/
    |   |   +-- assets/
    |   |   +-- pages/
    |   +-- app.py
    |   +-- __init__.py
    +-- data/
    |   +-- schema.sql
    |   +-- seed.sql
    +-- README.md
    +-- requirements.txt
    +-- run.py
    +-- setup.py
```