import random
from numpy.random import choice


def prepare_training(all_trials, elements_per_group):
    training_trials = []
    for with_equal in [True, False]:
        chosen_trials = [trial for trial in all_trials if trial["with_equal"] == with_equal]
        for answer_type in ["identical", "reversed", "two_pairs"]:
            chosen_trials_2 = [trial for trial in chosen_trials if trial["answer_type"] == answer_type]
            training_trials += list(choice(chosen_trials_2, elements_per_group))
    random.shuffle(training_trials)
    return training_trials
