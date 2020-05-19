import random


class Gesture:
    model = 3
    def __init__(self):
        self.value = -1

    def __sub__(self, other):
        if (self.value + 1) % self.model == other.value:
            return 1
        elif self.value == other.value:
            return 0
        elif (self.value - 1) % self.model == other.value:
            return -1


class Rock(Gesture):
    def __init__(self):
        super().__init__()
        self.value = 0


class Scissor(Gesture):
    def __init__(self):
        super().__init__()
        self.value = 1


class Paper(Gesture):
    def __init__(self):
        super().__init__()
        self.value = 2


class Env:
    """
    Rock: 0
    Scissor: 1
    Paper: 2
    """
    def __init__(self):
        self.state = 0
        self.options = [Rock(), Scissor(), Paper()]
        self._gen()

    def _gen(self):
        self._hand = random.choice(self.options)

    def reward(self, action):
        return action - self._hand

    def step(self, action):
        self.state = 0
        reward = self.reward(action)
        self._gen()
        done = False
        return self.state, reward, done, None

    def observe(self):
        return self.state

    def reset(self):
        self._gen()
        return self.state


class DiscreteDistribution:
    def __init__(self, options, dist=None):
        self.options = options
        self.count = len(self.options)
        if dist is None:
            self.dist = {k:(ind + 1)/self.count for ind, k in enumerate(self.options)}
        else:
            self.dist = dict(zip(self.options, dist))

    def random(self):
        num = random.random()
        for k, v in self.dist.items():
            if num < v:
                return k
            else:
                continue

    def value_dist(self):
        return list(self.dist.values())

    @property
    def prob(self):
        prob = {}
        values = self.value_dist()
        for ind, k in enumerate(self.options):
            if ind == 0:
                prob[k] = values[ind]/1
            else:
                prob[k] = (values[ind] - values[ind - 1])/1
        return prob

    def change_dists(self, dist):
        self.dist = dict(zip(self.options, dist))
        self._check()

    def change_dist(self, option, num):
        self.dist[option] = num
        self._check_values()
        
    def _check_values(self):
        value_dist = self.value_dist()
        assert value_dist[0] >= 0
        for i in range(1, self.count - 1):
            assert value_dist[i - 1] < value_dist[i] < value_dist[i + 1]
        assert value_dist[-1] == 1

    def _check_dist(self):
        assert sum(self.prob) == 1 


class Agent:
    def __init__(self):
        self.options = [Rock(), Scissor(), Paper()]
        self.distribution = DiscreteDistribution(self.options)
        self._gen()

    def _gen(self):
        #self._hand = self.options[0]#random.choice(self.options)
        self._hand = self.distribution.random()

    def policy(self, state):
        self._gen()
        return self._hand

    def learn(self):
        self.distribution.change_dist(self.options[0], 0)


if __name__ == '__main__':
    #r = Rock()
    #s = Scissor()
    #p = Paper()
    env = Env()
    agent = Agent()
    agent.learn()
    state = env.reset()
    r = 0
    reward_seq = []
    rnd = 1000
    for i in range(rnd):
        state = env.observe()
        action = agent.policy(state)
        state, reward, done, info = env.step(action)
        r += reward
        reward_seq.append(reward)
    print(r)
    #print(f"r - p = {r - p}")
    #print(f"p - r = {p - r}")
    #print(f"s - r = {s - r}")
    #print(f"r - s = {r - s}")
    #print(f"p - s = {p - s}")
    #print(f"s - p = {s - p}")
    #print(f"p - p = {p - p}")
    #print(f"s - s = {s - s}")
    #print(f"r - r = {r - r}")


