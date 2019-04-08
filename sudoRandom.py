# decide randomly on a run order. there are 4 options:
# 1342 - Div1 -> Sel1 -> Sel2 -> Div2
# 3124 - Sel1 -> Div1 -> Div2 -> Div2
# 3142 - Sel1 -> Div1 -> Sel2 -> Div2
# 1324 - Div1 -> Sel1 -> Div2 -> Sel1

import random
# Generate a Run Order for a new subject.
def sudoRandom():
    runOrder = {
        "1342": 1,
        "3124": 2,
        "3142": 3,
        "1324": 4,
    }
    return random.randint(1,4)



