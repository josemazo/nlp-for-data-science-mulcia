# Task 01: Create a spell checker.

This task will use as basis the Peter Norvig's essay *[How to Write a Spelling Corrector](http://norvig.com/spell-correct.html)* Also, I added control of *bi-grams* and of the position of the keys in the keyboard.

## How to use it
1. Download a corpus for traning the spell checker. In my case I used [this](https://dumps.wikimedia.org/eswiki/20160305/eswiki-20160305-pages-meta-current.xml.bz2) Spanish's Wikipedia dump.
2. Extract the corpus as plain text. You can use [this modified version](https://github.com/josemazo/wikiextractor) of WikiExtractor. The original one has been developed by [Giuseppe Attardi](https://github.com/attardi).
3. Put some of the plain text files in a folder called `data_files`.
4. You'll need **Python 3** for running the code. Also, its only dependice is [dill](https://pypi.python.org/pypi/dill). For running the spell checker:

```
python run.py
```

## Improvements
* Peter Norvig's and other future work.
* A better training data.
* And of course, the usage of evaluation methods, which we'll see in the course.
