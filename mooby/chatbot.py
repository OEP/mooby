from .brain import Brain
import argparse
import readline  # noqa
import shlex


def aside(msg):
    print('({})'.format(msg))


def learn(args, brain):
    for path in args:
        try:
            brain.learn(open(path).read())
        except IOError as e:
            aside('could not open `{}`: {}'.format(path, e))
            return


def command(command, brain):
    command = shlex.split(command)
    args = command[1:]
    command = command[0]
    if command == 'learn':
        learn(args, brain)
    else:
        aside('unknown command: {}'.format(command))


def chat(brain):
    while True:
        phrase = input('mooby> ')
        phrase = phrase.strip()
        if phrase.startswith('!'):
            command(phrase[1:], brain)
        else:
            brain.learn_phrase(phrase)
            print(brain.speak())


def main():
    parser = _get_parser()
    args = parser.parse_args()

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


def _get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('brain')
    parser.add_argument('-k', '--order', type=int, default=1)
    return parser

if __name__ == '__main__':
    main()
