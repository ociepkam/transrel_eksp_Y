import atexit
import time
from os.path import join
import random
from math import ceil
import csv
from psychopy import visual, event, core

from code.show_info import part_info, show_info
from code.load_data import load_config
from code.screen_misc import get_screen_res
from code.trial import all_possible_trials, load_trials, save_trials, replace_stimulus, prepare_stim
from code.choose_stimulus import choose_stimulus
from code.check_exit import check_exit

PART_ID = None
RESULTS = []


@atexit.register
def save_beh_results():
    with open(join('results', f'{PART_ID}_beh.csv'), 'w', newline='') as beh_file:
        dict_writer = csv.DictWriter(beh_file, RESULTS[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(RESULTS)
        # beh_writer = csv.writer(beh_file)
        # beh_writer.writerows(RESULTS)


def draw_stim(stim, flag):
    for pair in stim:
        for elem in pair:
            elem.setAutoDraw(flag)


def main():
    global PART_ID
    config = load_config()
    info, PART_ID = part_info()

    screen_res = dict(get_screen_res())
    win = visual.Window(list(screen_res.values()), fullscr=True, monitor='testMonitor', units='pix', screen=0,
                        color=config["screen_color"])
    event.Mouse(visible=False)
    clock = core.Clock()
    fixation = visual.TextStim(win, color=config["fixation_color"], text=config["fixation_text"],
                               height=config["fixation_size"])

    if info["Session"] == 1:
        trials = all_possible_trials()
        save_trials(trials, PART_ID[:-2])
        trials = trials[:int(len(trials)/2)]
    else:
        trials = load_trials(PART_ID[:-2])
        trials = trials[int(len(trials)/2):]

    stimulus_type, stimulus_all = choose_stimulus(config["stimulus_type"])

    block_order = config["block_order"]
    if config["randomize_blocks"]:
        random.shuffle(block_order)

    block_size = ceil(len(trials)/len(block_order))
    blocks = list(trials[i:i+block_size] for i in range(0, len(trials), block_size))
    stimulus_last = []

    show_info(win, join('.', 'messages', 'instruction.txt'), text_color=config["text_color"],
              text_size=config["text_size"], screen_res=screen_res)
    n = 0
    for block_idx, [block, block_type] in enumerate(zip(blocks, block_order)):
        show_info(win, join('.', 'messages', f'block_{block_type}.txt'), text_color=config["text_color"],
                  text_size=config["text_size"], screen_res=screen_res)
        for trial_raw in block:
            key = None
            reaction_time = None
            acc = -1
            n += 1

            # prepare trial stimulus
            stimulus_allowed = [elem for elem in stimulus_all if elem not in stimulus_last]
            trial_raw, stimulus_last = replace_stimulus(trial_raw, allowed_stimulus=stimulus_allowed)
            trial = prepare_stim(win, trial_raw, config, stimulus_type)

            # fixation
            fixation.setAutoDraw(True)
            win.flip()
            time.sleep(config["fixation_time"])
            fixation.setAutoDraw(False)
            win.flip()

            # draw trial
            draw_stim(trial["stimulus"], True)
            win.callOnFlip(clock.reset)
            win.flip()
            while clock.getTime() < config["stim_time"]:
                check_exit()
                win.flip()
            if block_type == "memory":
                draw_stim(trial["stimulus"], False)
            draw_stim(trial["pairs"], True)
            win.callOnFlip(clock.reset)
            win.callOnFlip(event.clearEvents)
            win.flip()
            while clock.getTime() < config["answer_time"]:
                key = event.getKeys(keyList=config["reaction_keys"])
                if key:
                    reaction_time = clock.getTime()
                    key = key[0]
                    break
                check_exit()
                win.flip()
            draw_stim(trial["stimulus"], False)
            draw_stim(trial["pairs"], False)
            win.callOnFlip(clock.reset)
            win.callOnFlip(event.clearEvents)
            win.flip()

            # wait
            wait_time = config["wait_time"] + random.random() * config["wait_jitter"]
            while clock.getTime() < wait_time:
                check_exit()
                win.flip()

            # results
            if key:
                acc = 1 if trial_raw["pairs"][config["reaction_keys"].index(key)] == trial_raw["answer"] else 0
            trial_results = {"n": n, "block_n": block_idx, "block_type": block_type,
                             "trial_type": trial_raw["answer_type"], "with_equal": trial_raw["with_equal"],
                             "rt": reaction_time, "acc": acc,
                             "order": trial_raw["order"], "stimulus": trial_raw["stimulus"],
                             "answers": trial_raw["pairs"], "correct_answer": trial_raw["answer"]}
            RESULTS.append(trial_results)


if __name__ == "__main__":
    main()
