# proper reaction time is 1500ms
PROPER_REACTION_TIME = 1500

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

def csv_file_reactions(file_name,col_num):
    with open(file_name) as csvfile:
        reader = csv.reader(csvfile)
        # column K  = 10 is the vector of the reaction time
        #19 if the run is selective, 10 if the run is divided
        included_cols = [col_num]
        reaction_times = []
        i = 0
        counter_lines = 0
        reaction_times_ints = []
        # Meaning it is a run with Divided conditions
        if col_num != 18:
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
                    if t == '':
                        continue
                    time_num = float(t)
                    time_list.append(time_num)
                reaction_times_ints.append(time_list)
            return reaction_times_ints
        # meaning it is run with Selective conditions.
        else:
            for line in reader:

                if line[5] == 'trials.thisRepN':
                    #print(line[18])
                    continue
                elif line[5] =='':
                    #print(line[18])
                    continue
                else:
                    #print(line[18])
                    reaction_times.append(list(line[j] for j in included_cols))
                ###
                #if counter_lines != 10:
                 #   counter_lines += 1  # ignore the first row which is the category
                #else:
                 #   counter_lines = 10;
                    #reaction_times.append(list(line[j] for j in included_cols))
            reaction_times_no_space = []
            #for i in range(len(reaction_times) - 1):
            for i in range(len(reaction_times)):
                reaction_times_no_space.append(reaction_times[i])
                # print(reaction_times_no_space[i])
            for react in reaction_times_no_space:
                str1 = react[0].replace("'", "")
                str2 = str1.replace("[", "")
                str3 = str2.replace("]", "")
                str4 = str3.replace(" ", "")
                times = str4.split(",")
                time_list = []
                for t in times:
                    if t == '':
                        continue
                    time_num = float(t)
                    time_list.append(time_num)
                reaction_times_ints.append(time_list)

            # for e in reaction_times_ints:
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
    #list_false_alarms = []
    #list_misses = []
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
                #correct_RT.append("NA")
                correct_RT.append(0)
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
    ## here there is the place to make the mean and std of the  subjects results.. ready to R
    return correct_RT

def check(stimulus_times,reaction_times):
    RT = []
    for test in range(len(stimulus_times)):
        answer = detection(stimulus_times[test],reaction_times[test])
        # In case did not notice to all of the stimulus
        while(len(answer)!=len(stimulus_times[test])):
            answer.append(-1)
        RT.append(answer)

    return RT

# Takes every run which is a a list of lists and make it to one list of reactions - concatenated onw after the other.
def makeRuns(RT_for_subject):
    main_list = []
    for sublist in RT_for_subject:
        sub_main_list = []
        for item in sublist:
            for i in item:
                sub_main_list.append(i)
        main_list.append(sub_main_list)
    print()
    #for run in range(len(main_list)):
     #   print(len(main_list[run]))
      #  print(main_list[run])
    return main_list

# Write each run as a line in a file for the R project
def write_to_file(main_list):
    file = open("subject_reaction_times.txt","w")
    for run in range(len(main_list)):
        str1 = str(main_list[run])
        str2 = str1.replace("[", "")
        str3 = str2.replace("]", "")
        str4 = str3.replace(",", "")
       # print(str4)
        file.write(str4+"\n")

    file.close()

def detect_wrong_response(list_not_etz,sel_rections,sel_stims):
    times_stims_sel = csv_file_stimuli(list_not_etz)
    diff_etz = []
    for real_stim, etz_stim in zip(sel_stims, times_stims_sel):
        for stim in range(len(real_stim)):
            flag = 0
            for etz in range(len(etz_stim)):
                a = (etz_stim[etz] - real_stim[stim]) * 1000
                b = -PROPER_REACTION_TIME
                if a <= PROPER_REACTION_TIME and a >= b:
                    flag = 1
            if flag:
                diff_etz.append(1)
            else:
                diff_etz.append(0)
    return diff_etz




def main_function():
    div_list_stims =[]
    div_list_reaction_files = []
    sel_list_stims = []
    sel_list_reaction_files = []
    sel_rections = []
    sel_stims = []
    RT_for_subject = []
    list_wrong_sel = []
    div_list_stims.append('div1_time_stim.csv')
    div_list_stims.append('div2_time_stim.csv')
    div_list_stims.append('div3_time_stim.csv')
    sel_list_stims.append('sel1_time_stim.csv')
    sel_list_stims.append('sel2_time_stim.csv')
    sel_list_stims.append('sel3_time_stim.csv')
    div_list_reaction_files.append('pilot1_Divided1_2019_Mar_05_1127.csv')
    div_list_reaction_files.append('pilot1_Divided2_2019_Mar_05_1139.csv')
    div_list_reaction_files.append('pilot1_Divided3_2019_Mar_05_1159.csv')
    sel_list_reaction_files.append('pilot1_Selective1_2019_Mar_05_1133.csv')
    sel_list_reaction_files.append('pilot1_Selective2_2019_Mar_05_1152.csv')
    sel_list_reaction_files.append('pilot1_Selective3_2019_Mar_05_1204.csv')

    ####NOT ETZ#####
    list_not_etz = []
    list_not_etz.append('not_etz_1.csv')
    list_not_etz.append('‏‏not_etz_2.csv')
    list_not_etz.append('‏‏‏‏not_etz_3.csv')

    for run in range(len(div_list_stims)):
        stimulus_times = csv_file_stimuli(div_list_stims[run])
        reaction_times = csv_file_reactions(div_list_reaction_files[run], 10);
        RT_for_subject.append(check(stimulus_times, reaction_times))
    for run in range(len(sel_list_stims)):
        stimulus_times = csv_file_stimuli(sel_list_stims[run])
        reaction_times = csv_file_reactions(sel_list_reaction_files[run], 18);
        sel_stims.append(stimulus_times)
        sel_rections.append(reaction_times)
        RT_for_subject.append(check(stimulus_times, reaction_times))

    for trail in range(len(list_not_etz)):
        list_wrong_sel.append(detect_wrong_response(list_not_etz[trail], sel_rections[trail], sel_stims[trail]))


    for run in range(len(RT_for_subject)):
        print(RT_for_subject[run])
    main_list = makeRuns(RT_for_subject)
    write_to_file(main_list)




main_function()