from checker import Checker


def process_input(sentence):
    sentence = checker.words(sentence)
    length = len(user_input)

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

if __name__ == '__main__':
    print('Welcome to a simply spell checker.\n'
          'Please wait while the program is loading...')

    checker = Checker('files/wiki_articles_test', 'model_01.pkl')
    user_input = input('Type a sentence to check: ')
    process_input(user_input)
