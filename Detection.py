# proper reaction time is 700ms
PROPER_REACTION_TIME = 700

import csv

def csv_file_stimuli(file_name):
    with open(file_name) as csvfile:
        reader = csv.reader(csvfile)
        # column A = 1 is the stimulus times
        included_cols = [1]
        stimulus_times = []
        for line in reader:
            time_list = []
            for value in line:
                times = value.split()
                for t in times:
                    time_num = float(t)
                    time_list.append(time_num)
            stimulus_times.append(list(time_list))
        #for stimuli in stimulus_times:
            #print(stimuli)
        return stimulus_times

def csv_file_reactions(file_name):
    with open(file_name) as csvfile:
        reader = csv.reader(csvfile)
        # column K  = 10 is the vector of the reaction time
        included_cols = [10]
        reaction_times = []
        i = 0
        reaction_times_ints = []
        for line in reader:
            if not i:
                i = 1  # ignore the first row which is the category
            else:
                reaction_times.append(list(line[j] for j in included_cols))
        reaction_times_no_space = []
        for i in range(len(reaction_times) - 1):
            reaction_times_no_space.append(reaction_times[i + 1])
            #print(reaction_times_no_space[i])
        for react in reaction_times_no_space:
            str1 = react[0].replace("'", "")
            str2 = str1.replace("[", "")
            str3 = str2.replace("]", "")
            str4 = str3.replace(" ", "")
            times = str4.split(",")
            time_list = []
            for t in times:
                time_num = float(t)
                time_list.append(time_num)
            reaction_times_ints.append(time_list)

        #for e in reaction_times_ints:
        #    print(e)

        return reaction_times_ints
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
                correct_RT.append((reacts_between[0] - stim))
            else:
                # Incorrect response
                list_accuracy.append(0)
                # in case the reaction time is bigger than proper reaction time
                # means that the subject reacted but after a long of time
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
                        correct_RT.append((reacts_between[0] - stim))
        else:
            # No response
            list_accuracy.append(0)
            correct_RT.append(-1)  # signify that there was no response
    return correct_RT

def check(stimulus_times,reaction_times):
    RT = []
    for test in range(len(stimulus_times)):
        RT.append(detection(stimulus_times[test],reaction_times[test]))
    return RT

# testing
#stimulus = [3.6, 4.5, 8]
#reaction = [3.9, 5, 5.1 ,6 , 8.9]
#detection(stimulus,reaction)

def main_function():
    list_stims =[]
    list_reaction_files = []
    RT_for_subject = []
    list_stims.append('div1_time_stim.csv')
    list_stims.append('div2_time_stim.csv')
    list_stims.append('div3_time_stim.csv')
    list_stims.append('sel1_time_stim.csv')
    list_stims.append('sel2_time_stim.csv')
    list_stims.append('sel3_time_stim.csv')
    list_reaction_files.append('div1_Run1_2018.csv')
    list_reaction_files.append('div2_Run1_2018.csv')
    list_reaction_files.append('div3_Run1_2018.csv')
    list_reaction_files.append('sel1_Run1_2018.csv')
    list_reaction_files.append('sel2_Run1_2018.csv')
    list_reaction_files.append('sel3_Run1_2018.csv')
    for run in range(len(list_stims)):
        stimulus_times = csv_file_stimuli(list_stims[run])
        reaction_times = csv_file_reactions(list_reaction_files[run])
        RT_for_subject.append(check(stimulus_times, reaction_times))
        print(RT_for_subject[run])


main_function()