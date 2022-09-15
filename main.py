import atexit
from os.path import join
import random
from math import ceil
import csv
from psychopy import visual, event

from code.show_info import part_info, show_info
from code.load_data import load_config
from code.screen_misc import get_screen_res
from code.trial import all_possible_trials, load_trials, save_trials, replace_stimulus
from code.choose_stimulus import choose_stimulus


# @atexit.register
# def save_beh_results():
#     with open(join('results_figury', PART_ID + '_beh.csv'), 'w') as beh_file:
#         beh_writer = csv.writer(beh_file)
#         beh_writer.writerows(RESULTS)


def main():
    config = load_config()
    info, part_id = part_info()

    screen_res = dict(get_screen_res())
    win = visual.Window(list(screen_res.values()), fullscr=True, monitor='testMonitor', units='pix', screen=0,
                        color=config["screen_color"])
    mouse = event.Mouse(visible=False)
    fixation = visual.TextStim(win, color=config["fixation_color"], text=config["fixation_text"],
                               height=config["fixation_size"])

    if info["Session"] == 1:
        trials = all_possible_trials()
        save_trials(trials, part_id[:-2])
        trials = trials[:int(len(trials)/2)]
    else:
        trials = load_trials(part_id[:-2])
        trials = trials[int(len(trials)/2):]

    show_info(win, join('.', 'messages', 'instruction.txt'), text_color=config["text_color"],
              text_size=config["text_size"], screen_res=screen_res)

    stimulus_type, stimulus_all = choose_stimulus(config["stimulus_type"])

    block_order = config["block_order"]
    if config["randomize_blocks"]:
        random.shuffle(block_order)

    block_size = ceil(len(trials)/len(block_order))
    blocks = list(trials[i:i+block_size] for i in range(0, len(trials), block_size))
    stimulus_last = []

    for block_idx, [block, block_type] in enumerate(zip(blocks, block_order)):
        show_info(win, join('.', 'messages', f'block_{block_type}.txt'), text_color=config["text_color"],
                  text_size=config["text_size"], screen_res=screen_res)
        for trial in block:
            stimulus_allowed = [elem for elem in stimulus_all if elem not in stimulus_last]
            trial, stimulus_last = replace_stimulus(trial, allowed_stimulus=stimulus_allowed)
            print(trial)


if __name__ == "__main__":
    main()
