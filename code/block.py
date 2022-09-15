import numpy as np
from code.trial import Trial

class Block:
    def __init__(self, elements, stimulus):
        self.trials_list = []
        last_stimulus = []
        for i in range(elements):
            allow_stimulus = [elem for elem in stimulus if elem not in last_stimulus]
            a, b, c = np.random.choice(allow_stimulus, 3, replace=False)
            last_stimulus = [a, b, c]
            trial = Trial(with_equal, memory=False, elements=[a, b, c],
                          answer_type=None, symbols=None)