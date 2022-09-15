import random
import yaml
from os.path import join
import numpy as np


def replace_stimulus_in_pair(pair, new_stimulus):
    new_pair = []
    for elem in pair:
        if elem in new_stimulus.keys():
            new_pair.append(new_stimulus[elem])
        else:
            new_pair.append(elem)
    return new_pair


def replace_stimulus(trial, allowed_stimulus):
    a, b, c = np.random.choice(allowed_stimulus, 3, replace=False)
    new_stimulus = {"A": a, "B": b, "C": c}
    trial["stimulus"] = [replace_stimulus_in_pair(pair, new_stimulus) for pair in trial["stimulus"]]
    trial["pairs"] = [replace_stimulus_in_pair(pair, new_stimulus) for pair in trial["pairs"]]
    trial["answer"] = replace_stimulus_in_pair(trial["answer"], new_stimulus)
    trial["order"] = [new_stimulus[elem] for elem in trial["order"]]
    return trial, [a, b, c]


def save_trials(trials, part_id):
    with open(join("trials", f"{part_id}.yaml"), "w") as file:
        yaml.safe_dump(trials, file)


def load_trials(part_id):
    with open(join("trials", f"{part_id}.yaml"), "r") as file:
        return yaml.safe_load(file)


def reverse_pair(pair):
    if pair[1] == "/":
        return f"{pair[2]}\\{pair[0]}"
    elif pair[1] == "\\":
        return f"{pair[2]}/{pair[0]}"
    else:
        return pair[::-1]


def all_possible_trials():
    all_trials = []

    with_equal = False
    stimulus = [{"stim": ["A/B", r"C\B"], "order": "ABC"},
                {"stim": ["A/B", r"A\C"], "order": "CAB"},
                {"stim": [r"A\B", "C/B"], "order": "CBA"},
                {"stim": [r"A\B", "A/C"], "order": "BAC"}]
    for i, elem in enumerate(stimulus):
        stim = elem["stim"]
        order = elem["order"]
        for answer_type in ["identical", "reversed", "two_pairs"]:
            for correct_pair in stim:
                if answer_type == "identical":
                    answer = correct_pair
                elif answer_type == "reversed":
                    answer = reverse_pair(correct_pair)
                elif answer_type == "two_pairs" and i == 0:
                    answer = f"{order[0]}/{order[2]}"
                else:
                    answer = f"{order[2]}\\{order[0]}"
                for incorrect_far in [f"{order[0]}\\{order[2]}", f"{order[2]}/{order[0]}"]:
                    for incorrect_pair in [f"{order[0]}\\{order[1]}", f"{order[1]}\\{order[2]}",
                                           f"{order[1]}/{order[0]}", f"{order[2]}/{order[1]}"]:
                        pairs = [answer, incorrect_pair, incorrect_far]
                        random.shuffle(pairs)
                        trial = {"stimulus": stim, "pairs": pairs, "answer": answer, "order": order,
                                 "answer_type": answer_type, "with_equal": with_equal}
                        all_trials.append(trial)

    with_equal = True
    stimulus = [{"stim": ["A/B", r"B|C"], "order": "ABC"},
                {"stim": ["A/B", r"A|C"], "order": "CAB"},
                {"stim": [r"A\B", "C|B"], "order": "CBA"},
                {"stim": [r"A\B", "C|A"], "order": "BAC"}]

    for i, elem in enumerate(stimulus):
        stim = elem["stim"]
        order = elem["order"]
        for answer_type in ["identical", "reversed", "two_pairs"]:
            if answer_type == "identical":
                answer = stim[1]
            elif answer_type == "reversed":
                answer = reverse_pair(stim[1])
            elif answer_type == "two_pairs" and i == 0:
                answer = f"{order[0]}/{order[2]}"
            else:
                answer = f"{order[2]}\\{order[0]}"

            for incorrect_far in [f"{order[0]}\\{order[2]}", f"{order[2]}/{order[0]}"]:
                for incorrect_pair in [f"{stim[0][0]}|{stim[0][2]}", f"{stim[0][2]}|{stim[0][0]}",]:
                    pairs = [answer, incorrect_pair, incorrect_far]
                    trial = {"stimulus": stim, "pairs": pairs, "answer": answer, "order": order,
                             "answer_type": answer_type, "with_equal": with_equal}
                    all_trials.append(trial)

            for incorrect_far in [f"{order[0]}|{order[2]}", f"{order[2]}|{order[0]}"]:
                for incorrect_pair in [f"{stim[0][0]}\\{stim[0][2]}", f"{stim[0][2]}/{stim[0][0]}",
                                       f"{stim[1][0]}\\{stim[1][2]}", f"{stim[1][0]}/{stim[1][2]}",
                                       f"{stim[1][2]}\\{stim[1][0]}", f"{stim[1][2]}/{stim[1][0]}"]:
                    pairs = [answer, incorrect_pair, incorrect_far]
                    random.shuffle(pairs)
                    trial = {"stimulus": stim, "pairs": pairs, "answer": answer, "order": order,
                             "answer_type": answer_type, "with_equal": with_equal}
                    all_trials.append(trial)
    random.shuffle(all_trials)
    return all_trials

# For random generation
# class Trial:
#     def __init__(self, with_equal, memory=False, elements=("A", "B", "C"),
#                  answer_type=None, symbols=None, randomize_elements=True):
#         if symbols is None:
#             symbols = {"higher": "/", "lower": "\\", "equal": "|"}
#         if answer_type is None:
#             answer_type = random.choice(["two_pairs", "reversed", "identical"])
#         self.elements = elements
#         self.symbols = symbols
#         self.with_equal = with_equal
#         self.memory = memory
#         self.answer_type = answer_type
#         if randomize_elements:
#             random.shuffle(self.elements)
#
#         self.pairs = []
#         self.answers = []
#
#         if with_equal:
#             # stimulus
#             if random.random() < 0.5:
#                 self.pairs.append([self.elements[0], self.symbols["higher"], self.elements[1]])  # A/B
#                 if random.random() < 0.5:
#                     equal_pair = [self.elements[0], self.symbols["equal"], self.elements[2]]  # A|C
#                     self.order = [self.elements[2], self.elements[0], self.elements[1]]
#                 else:
#                     equal_pair = [self.elements[1], self.symbols["equal"], self.elements[2]]  # B|C
#                     self.order = [self.elements[0], self.elements[1], self.elements[2]]
#             else:
#                 self.pairs.append([self.elements[0], self.symbols["lower"], self.elements[1]])  # A\B
#                 if random.random() < 0.5:
#                     equal_pair = [self.elements[0], self.symbols["equal"], self.elements[2]]  # A|C
#                     self.order = [self.elements[1], self.elements[0], self.elements[2]]
#                 else:
#                     equal_pair = [self.elements[2], self.symbols["equal"], self.elements[1]]  # C|B
#                     self.order = [self.elements[2], self.elements[1], self.elements[0]]
#             self.pairs.append(equal_pair)
#             # answers
#             if self.answer_type == "identical":
#                 self.correct_answer = equal_pair
#             elif self.answer_type == "reversed":
#                 self.correct_answer = self.reverse_pair(equal_pair)
#             else:  # self.correct_answer == "two_pairs"
#                 self.correct_answer = random.choice([[self.order[0], self.symbols["higher"], self.order[2]],
#                                                      [self.order[2], self.symbols["lower"], self.order[0]]])
#             if random.random() < 0.5:
#                 incorrect_pair = random.choice([[self.pairs[0][0], self.symbols["equal"], self.pairs[0][2]],
#                                                 [self.pairs[0][2], self.symbols["equal"], self.pairs[0][0]]])
#                 incorrect_far = random.choice([[self.order[0], self.symbols["lower"], self.order[2]],
#                                                [self.order[2], self.symbols["higher"], self.order[0]]])
#             else:
#                 incorrect_pair = random.choice([self.pairs[0][::-1],
#                                                 self.reverse_pair(self.pairs[0])[::-1],
#                                                 [equal_pair[0], self.symbols["lower"], equal_pair[2]],
#                                                 [equal_pair[2], self.symbols["lower"], equal_pair[0]],
#                                                 [equal_pair[0], self.symbols["higher"], equal_pair[2]],
#                                                 [equal_pair[2], self.symbols["higher"], equal_pair[0]]])
#                 incorrect_far = random.choice([[self.order[0], self.symbols["equal"], self.order[2]],
#                                                [self.order[2], self.symbols["equal"], self.order[0]]])
#
#         else:
#             # stimulus
#             if random.random() < 0.5:
#                 self.pairs.append([self.elements[0], self.symbols["higher"], self.elements[1]])  # A/B
#                 if random.random() < 0.5:
#                     self.pairs.append([self.elements[2], self.symbols["lower"], self.elements[1]])  # C\B
#                     self.order = [self.elements[0], self.elements[1], self.elements[2]]
#                 else:
#                     self.pairs.append([self.elements[0], self.symbols["lower"], self.elements[2]])  # A\C
#                     self.order = [self.elements[2], self.elements[0], self.elements[1]]
#             else:
#                 self.pairs.append([self.elements[0], self.symbols["lower"], self.elements[1]])  # A\B
#                 if random.random() < 0.5:
#                     self.pairs.append([self.elements[2], self.symbols["higher"], self.elements[1]])  # C/B
#                     self.order = [self.elements[2], self.elements[1], self.elements[0]]
#                 else:
#                     self.pairs.append([self.elements[0], self.symbols["higher"], self.elements[2]])  # A/C
#                     self.order = [self.elements[1], self.elements[0], self.elements[2]]
#             # answers
#             if self.answer_type == "identical":
#                 self.correct_answer = random.choice(self.pairs)
#             elif self.answer_type == "reversed":
#                 self.correct_answer = self.reverse_pair(random.choice(self.pairs))
#             else:  # self.correct_answer == "two_pairs"
#                 self.correct_answer = random.choice([[self.order[0], self.symbols["higher"], self.order[2]],
#                                                      [self.order[2], self.symbols["lower"], self.order[0]]])
#
#             incorrect_pair = random.choice([[self.order[0], self.symbols["lower"], self.order[1]],
#                                             [self.order[1], self.symbols["lower"], self.order[2]],
#                                             [self.order[1], self.symbols["higher"], self.order[0]],
#                                             [self.order[2], self.symbols["higher"], self.order[1]]])
#
#             incorrect_far = random.choice([[self.order[0], self.symbols["lower"], self.order[2]],
#                                            [self.order[2], self.symbols["higher"], self.order[0]]])
#
#         self.answers = [incorrect_far, incorrect_pair, self.correct_answer]
#         random.shuffle(self.answers)
#
#     def reverse_pair(self, pair):
#         if pair[1] == self.symbols["lower"]:
#             return [pair[2], self.symbols["higher"], pair[0]]
#         elif pair[1] == self.symbols["higher"]:
#             return [pair[2], self.symbols["lower"], pair[0]]
#         else:
#             return [pair[2], self.symbols["equal"], pair[0]]
