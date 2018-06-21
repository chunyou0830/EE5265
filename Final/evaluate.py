#########################################
#           Mapping Evaluator           #
#                                       #
#     NTHUEE VLSI EDA Final Project     #
#########################################

import json
import re
import time
import sys
import os

from hashlib import blake2b

def hash_b2b(str):
	return blake2b(str.encode(), digest_size=4).hexdigest()

def filt_arr(key):
	substr = re.findall('\[\d+\]', key)
	if len(substr) == 1:
		substr = substr[0]
		key_filted = key.replace(substr, '[0]')
		return hash_b2b(key_filted)
	else:
		return hash_b2b(key)

def process_post(str):
	if str not in posts:
		posts.append(str)
	return posts.index(str) 

##### VERIFY #####

start = time.time()

mapped = dict()

h = blake2b(digest_size=5)

case = str(sys.argv[1])
file_orig = 'cases/case'+case+'.json'
file_case = 'inputs/data'+case+'.json'
file_rule = 'dicts/dict'+case+'.json'

with open(file_orig, 'r') as fr:
	origs = json.load(fr)

with open(file_case, 'r') as fr:
	cases = json.load(fr)

keys = cases[0]

with open(file_rule, 'r') as fr:
	rules = json.load(fr)

posts = rules[1]
rules = rules[0]

cnt_neg = 0
cnt_pos = 0

for key in keys:
	key_filted = filt_arr(key)
	val_lkup_filt = rules.get(hash_b2b(key_filted), None)
	val_lkup_orig = rules.get(hash_b2b(key), None)

	val_lkup = val_lkup_orig if val_lkup_orig != None else val_lkup_filt

	key_replace = key.replace('[', '_').replace(']', '_').replace('.', '_')

	if val_lkup == None:
		check = ''

	elif val_lkup[0] == 1:

		# Replace, Same
		if val_lkup[1] == 0 and val_lkup[2] == 0:
			check = key_replace

		# Replace, Postfix no change
		elif val_lkup[1] == 0 and val_lkup[2] != 0:	
			check = key_replace + posts[val_lkup[2]]

		# Replace, Postfix rm tail
		elif val_lkup[1] != 0:
			check = key_replace[0:len(key_replace)-val_lkup[1]] + posts[val_lkup[2]]

	# Same
	elif val_lkup[1] == 0 and val_lkup[2] == 0:
		check = key
	
	# Postfix no change
	elif val_lkup[1] == 0 and val_lkup[2] != 0:
		check = key + posts[val_lkup[2]]
	
	# Postfix rm tail
	elif val_lkup[1] != 0:
		check = key[0:len(key)-val_lkup[1]] + posts[val_lkup[2]]

	mapped[key] = check

	if origs[key] != check:
		cnt_neg += 1
		break
	else:
		cnt_pos += 1

time_eva = time.time()-start

##### SUMMARY #####

print('Evaluate Elapsed Time:\t' + str(time_eva) + ' (sec)')
print('Evaluate Correct:\t' + str(cnt_pos) + ' (items)')
print('Evaluate Incorrect:\t' + str(cnt_neg) + ' (items)')