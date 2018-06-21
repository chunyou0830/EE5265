#########################################
# Evaluation Phase Input File Generator #
#                                       #
#     NTHUEE VLSI EDA Final Project     #
#########################################

import json
import re
import time
import sys
import os

##### GENERATE #####

keys = []
vals = []

case = str(sys.argv[1])
file_case = 'cases/case'+case+'.json'
file_eval = 'inputs/data'+case+'.json'

with open(file_case, 'r') as fr:
	dict = json.load(fr)

for key, val in dict.items():
	keys.append(key)
	vals.append(val)

with open(file_eval, 'w') as fw:
	json.dump([keys, vals], fw)

print('Evaluation phase input file generated.')