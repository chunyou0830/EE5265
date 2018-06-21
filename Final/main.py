#########################################
#     Mapping Dictionary Generator      #
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

def strcmpsame(a, b):
	iterate = min(len(a), len(b))
	ret = ''
	for i in range(iterate):
		if a[i] == b[i]:
			ret += a[i]
		else:
			break
	return ret

def filt_arr(key, val=None):
	substr = re.findall('\[\d+\]', key)
	if len(substr) == 1:
		substr = substr[0]
		key_filted = key.replace(substr, '[0]')

		# Normal Operation
		if val == None:
			return hash_b2b(key_filted)
		# 0th record of the array
		if substr == '[0]':
			return hash_b2b(key_filted)
		# Not 0th record of the array, but 0th not parsed yet
		if substr != '[0]' and rules.get(hash_b2b(key_filted), None) == None:
			process_item(key_filted)
			if rules[hash_b2b(key_filted)][2] == val:
				return hash_b2b(key_filted)
			else:
				return hash_b2b(key)
		# Exist same filtered record, need to verify if two records are identical
		elif rules[hash_b2b(key_filted)][2] == val:
			return hash_b2b(key_filted)
		# If not, create new record
		else:
			return hash_b2b(key)
	else:
		return hash_b2b(key)

def process_post(str):
	if str not in posts:
		posts.append(str)
	return posts.index(str) 

def process_item(key, val=None):
	if val == None:
		val = rules.get(key, '')

	key_replace = key.replace('[', '_').replace(']', '_').replace('.', '_')

	same = strcmpsame(key, val)
	key_pos = key[len(same):]
	val_pos = val[len(same):]

	# Same
	if val.find(key) == 0 and len(key) == len(val):
		rules[filt_arr(key, val)] = [0, 0, 0]

	# Postfix no change
	elif val.find(key) == 0 and len(key) != len(val):
		rules[filt_arr(key, val)] = [0, 0, process_post(val[len(key):])]

	# Replace, Same
	elif val.find(key_replace) == 0 and len(key_replace) == len(val):
		rules[filt_arr(key, val)] = [1, 0, 0]

	# Replace, Same, Postfix no change
	elif val.find(key_replace) == 0 and len(key_replace) != len(val):
		rules[filt_arr(key, val)] = [1, 0, process_post(val[len(key_replace):])]

	# Postfix rm tail
	elif same in val and key_pos != val_pos:
		rules[filt_arr(key, val)] = [0, len(key)-len(same), process_post(val_pos)]

	# Others
	else:
		print(key, val)

##### GENERATE #####

start = time.time()

rules = dict()
posts = ['']

case = str(sys.argv[1])
file_case = 'cases/case'+case+'.json'
file_rule = 'dicts/dict'+case+'.json'

with open(file_case, 'r') as fr:
	cases = json.load(fr)

for key, val in cases.items():
	process_item(key, val)

time_gen = time.time()-start

with open(file_rule, 'w') as fw:
	json.dump([rules, posts], fw)

##### SUMMARY #####

print('Dict Generate Elapsed Time:\t' + str(time_gen) + ' (sec)')

fsize_case = os.path.getsize(file_case)
fsize_rule = os.path.getsize(file_rule)

print('Readed Dict Total File Size:\t' + str(fsize_case) + ' (bytes)')
print('Gened Dict Total File Size:\t' + str(fsize_rule) + ' (bytes)')