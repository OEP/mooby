import mooby
import sys

brain = mooby.Brain(order=1)

for corpus in sys.argv[1:]:
    brain.learn(open(corpus).read())
for _ in range(5):
    print(brain.speak())
