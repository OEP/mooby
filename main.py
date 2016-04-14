import mooby
import argparse


def main():
    parser = _get_parser()
    args = parser.parse_args()
    brain = mooby.Brain(order=args.order)

    for corpus in args.corpus:
        brain.learn(open(corpus).read())

    for _ in range(args.count):
        print(brain.speak())


def _get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('corpus', nargs='+')
    parser.add_argument('-k', '--order', type=int, default=1)
    parser.add_argument('-n', '--count', type=int, default=1)
    return parser

if __name__ == '__main__':
    main()
