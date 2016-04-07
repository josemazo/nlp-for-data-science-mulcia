import signal
import sys

from checker import Checker


def process_input(sentence):
    sentence = checker.words(sentence)
    length = len(sentence)

    for index, word in enumerate(sentence):
        if index == 0:
            pre = ''
        else:
            pre = sentence[index - 1]

        if index == length - 1:
            post = ''
        else:
            post = sentence[index + 1]

        proposals = checker.correct(pre, word, post)
        print('{0}: {1}'.format(word, proposals))


def signal_handler(signal_handled, frame):
    exiting()


def exiting(initial_jump=True):
    bye_bye = 'Bye bye!'
    if initial_jump:
        bye_bye = '\n{0}'.format(bye_bye)
    print(bye_bye)
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    print('Welcome to a simple spell checker.\n'
          'You can finish it with \'Ctrl+c\'.\n'
          'Please wait while the program is loading...')

    checker = Checker()

    while True:
        user_input = input('Type a sentence to check: ')
        if user_input == 'exit':
            exiting(False)

        else:
            process_input(user_input)
