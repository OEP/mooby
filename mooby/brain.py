from . import tokenize, phrasify
import random
import pickle


class Brain(object):

    def __init__(self, order=1):
        self.order = order
        self._graph = {}
        self._back_graph = {}
        self._jump = {}
        self._rng = random.Random()

    @classmethod
    def load(cls, fp):
        d = pickle.load(fp)
        return cls.from_dict(d)

    @classmethod
    def from_dict(cls, d):
        order = d.pop('order')
        graph = d.pop('graph')
        if d:
            raise ValueError('Extra keys: %s' % ' '.join(d.keys()))
        brain = cls(order=order)
        brain._graph = graph
        return brain

    def learn_phrase(self, phrase):
        tokens = tokenize(phrase)
        if not tokens:
            return
        for j in range(self.order):
            i = j
            if i == 0:
                t0 = None
            else:
                t0 = tuple(tokens[0:i])
                self._associate(None, t0)
            while i < len(tokens):
                t1 = tuple(tokens[i:i+self.order])
                self._associate(t0, t1)
                t0 = t1
                i += self.order
            self._associate(t1, None)

    def learn(self, corpus):
        for phrase in phrasify(corpus):
            self.learn_phrase(phrase)

    def utter(self, jump=None):
        if not self._graph:
            return []
        if jump is not None:
            try:
                token = self._rng.choice(self._jump[jump])
            except KeyError:
                pass
            else:
                return self._bidirectional_utter(token)
        return self._forward_utter()

    def _forward_utter(self):
        utterance = []
        tokens = self._next(None)
        while tokens is not None:
            utterance.extend(tokens)
            tokens = self._next(tokens)
        return utterance

    def _bidirectional_utter(self, token):
        utterance = []
        t0 = token
        while t0 is not None:
            utterance.extend(t0)
            t0 = self._next(t0)
        utterance = list(reversed(utterance))
        t0 = self._prev(token)
        while t0 is not None:
            utterance.extend(reversed(t0))
            t0 = self._prev(t0)
        return list(reversed(utterance))

    def speak(self, **kw):
        utterance = self.utter(**kw)
        return ' '.join(utterance)

    def to_dict(self):
        return {'order': self.order, 'graph': self._graph}

    def save(self, fp):
        pickle.dump(self.to_dict(), fp, pickle.HIGHEST_PROTOCOL)

    def _next(self, token):
        t = self._graph[token]
        if t is None:
            return t
        return self._rng.choice(t)

    def _prev(self, token):
        t = self._back_graph[token]
        if t is None:
            return t
        return self._rng.choice(t)

    def _associate(self, t1, t2):
        self._learnjump(t1)
        self._learnjump(t2)
        bag = self._graph.setdefault(t1, [])
        bag.append(t2)
        bag = self._back_graph.setdefault(t2, [])
        bag.append(t1)

    def _learnjump(self, token):
        if token is None:
            return
        for t in token:
            l = self._jump.setdefault(t, [])
            l.append(token)
