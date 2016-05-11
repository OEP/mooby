from .brain import Brain
import argparse
import readline  # noqa
import shlex
import random
import tempfile


def aside(msg):
    print('({})'.format(msg))


def learn(args, brain):
    for path in args:
        try:
            brain.learn(open(path).read())
        except IOError as e:
            aside('could not open `{}`: {}'.format(path, e))
            return


def learnlines(args, brain):
    for path in args:
        try:
            with open(path) as fp:
                for line in fp:
                    brain.learn_phrase(line)
        except IOError as e:
            aside('could not open `{}`: {}'.format(path, e))
            return


def command(command, brain):
    command = shlex.split(command)
    args = command[1:]
    command = command[0]
    if command == 'learn':
        learn(args, brain)
    elif command == 'learnlines':
        learnlines(args, brain)
    else:
        aside('unknown command: {}'.format(command))


def chat(brain):
    while True:
        phrase = input('mooby> ')
        phrase = phrase.strip()
        words = phrase.split()
        if words:
            jump = random.choice(words)
        else:
            jump = None
        if phrase.startswith('!'):
            command(phrase[1:], brain)
        else:
            print(brain.speak(jump=jump))
            brain.learn_phrase(phrase)


def main():
    parser = _get_parser()
    args = parser.parse_args()
    show_brain = False

    if args.brain is None:
        args.brain = tempfile.mktemp(prefix='mooby')
        show_brain = True

    try:
        with open(args.brain, 'rb') as fp:
            brain = Brain.load(fp)
    except IOError:
        brain = Brain(order=args.order)

    try:
        chat(brain)
    except (EOFError, KeyboardInterrupt):
        print()
    finally:
        with open(args.brain, 'wb') as fp:
            brain.save(fp)
    if show_brain:
        print("Saved session to `{}'".format(args.brain))


def _get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('brain', nargs='?')
    parser.add_argument('-k', '--order', type=int, default=1)
    return parser

if __name__ == '__main__':
    main()
