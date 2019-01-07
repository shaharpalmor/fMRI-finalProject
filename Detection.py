# proper reaction time is 700ms
PROPER_REACTION_TIME = 700
import pandas as pd

import csv
import os

#def csv_file(file_name,interest_col):
def csv_file_stimuli():
    #os.chdir('C:\Users\Owner\PycharmProjects\test') sel1_Run1_2018_Dec_14_1203.csv
    with open('sel1_time_stim.csv') as csvfile:
        reader = csv.reader(csvfile)
        # column A = 1 is the stimulus times
        included_cols = [1]
        stimulus_times = []
        i= 0
        for line in reader:
            if not i:
                i=1 # ignore the first row which is the category
            else:
                stimulus_times.append(list(line for i in included_cols))
        for stimuli in stimulus_times:
            print(stimuli)
        return stimulus_times


def csv_file_reactions():
    # os.chdir('C:\Users\Owner\PycharmProjects\test')
    with open('sel1_Run1_2018_Dec_14_1203.csv') as csvfile:
        reader = csv.reader(csvfile)
        # column K  = 10 is the vector of the reaction time
        included_cols = [10]
        reaction_times = []
        i = 0
        for line in reader:
            if not i:
                i = 1  # ignore the first row which is the category
            else:
                reaction_times.append(list(line[i] for i in included_cols))
        for react in reaction_times:
            print(react)
        return reaction_times


# return the next stimulus time
def getNextStim(stim, stimulus):
    flag = 0
    for i in stimulus:
        if flag == 1:
            return i;
        if i == stim:
            flag = 1


def detection(stimulus, reaction):
    list_accuracy = []
    # Represents times of stimulus
    list_stimulus = []
    # Represents times of reaction
    list_reaction = []

    correct_RT = []

    # Normalize each stimulus/reaction form seconds to milli seconds
    for stim in stimulus:
        list_stimulus.append(stim*1000)
    for react in reaction:
        list_reaction.append(react*1000)

    for stim in list_stimulus:
        reacts_between = []
        last_stim = 0
        for react in list_reaction:
            next_stim = getNextStim(stim,list_stimulus)
            if next_stim != None and not last_stim:
                if react > stim and react < next_stim:
                    reacts_between.append(react)
            else:
                last_stim = 1
                if react > stim:
                    reacts_between.append(react)
                # In case there is only one stimulus check if its reasonable and less then 700 ms
        if len(reacts_between) == 1:
            # Correct response
            if reacts_between[0] - stim <= PROPER_REACTION_TIME:
                list_accuracy.append(1)
                correct_RT.append(reacts_between[0] - stim)
            else:
                # Incorrect response
                list_accuracy.append(0)
                correct_RT.append("NA")
        elif len(reacts_between) > 1:
            # there are more than one response, check if any is reasonable
            # if the first is reasonable then will be taken
            first_press = 0
            for multiple_react in reacts_between:
                if not first_press:
                    if multiple_react - stim <= PROPER_REACTION_TIME:
                        first_press = 1
                        list_accuracy.append(1)
                        correct_RT.append(reacts_between[0] - stim)
        else:
            # No response
            list_accuracy[stim] = 0
            correct_RT[stim] = -1  # signify that there was no response



# testing
stimulus = [3.6, 4.5, 8]
reaction = [3.9, 5, 5.1 ,6 , 8.9]
#detection(stimulus,reaction)
stimulus_times = csv_file_stimuli()
reaction_times = csv_file_reactions()