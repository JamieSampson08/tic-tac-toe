##Jamie Sampson
September 9, 2019 - September 12, 2019

**Note**: If you wanta make this file look pretty, open with a markdown reader
Personally used: [here](https://markdownlivepreview.com/)

### Requirements
Use any language and any freely available supporting libraries you like. Clearly identify any
code that you did not write yourself. Please provide instructions to compile and run your code
and tests (including how to obtain any required dependencies or IDEs). Rules and more
information about Tic-tac-toe can be found here:

https://en.wikipedia.org/wiki/Tic-tac-toe

There is no requirement to write any GUI or AI.


## Set Up
IDE: [PyCharm](https://www.jetbrains.com/pycharm/download/#section=windows)

1. Open PyCharm -> New Project
Enviornment: `Virtualenv`
Base Interpreter: `Python 3.7`
2. Create a new folder, with a project name <name | recommended, `Jamie_Sampson`> -> Create
3. Go to location of new project, copy `src` folder inside zipped folder, paste into new project folder

### Packages
- **mock**: go to a test that uses mock, import should be red, if you hoover by it, there should be an option
        to install package, click that
- **nosetests**: follow these instructions [here](https://nose.readthedocs.io/en/latest/)
             I personally have pip installed, so I ran `pip install nose`

### Imports
**Note**: Think these all naturally come with PyCharm / Python 3.7?? (ie. I didn't have to download a package like
      I did for the mock import

- `import unittest`
- `from io import StringIO`
- `import sys`
- `from contextlib import contextmanager`

## How to Play
1. In PyCharm, click the play button beside the `if __name__ == "__main__":`
   at the bottom of the `game.py` file (things should pop up in terminal)
2. Enter grid size (ie. 3 for 3x3)(min 3, max 10)
3. Use position key map to choose move location
4. When prompted, can show position key map by entering "help" or early exit game with "exit"
5. Option to play again after win/tie, if choose yes, will show scoreboard for both players
6. Repeat #2 - #6

## How to Test
1. To run all tests that I wrote, go to the project home directory `/<whatever you named the project | Jamie_Sampson>`
2. In the terminal, run `nosetests`
3. Everything should pass (else some crazy magic is happening :o) 

## Known Bugs
1. None, which is concerning ...
2. Probs have one somewhere ...

## Optimization
1. move `add_position` to Board class
2. Tweak variable names (was having english issues when coming up descripters for board locations :D)
3. Post position key in same square space as where game occurs
 - would be more cluttered, but would remove the need for the help feature
 - would be more useful for larger sized grids (ie. the 10 x 10)
 - would take away from the readability, but add to the ease of move input
4. Exceptions
5. 100% Code Coverage


## Referances
- **unit tests**
  - How to test output: [here]( https://stackoverflow.com/questions/4219717/how-to-assert-output-with-nosetest-unittest-in-python)
 - How to test input: [here](https://dev.to/vergeev/how-to-test-input-processing-in-python-3)
