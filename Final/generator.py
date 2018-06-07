import json
import re
import time
import sys
import os

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
	#print(key, val)
	substr = re.findall('\[\d+\]', key)
	if len(substr) == 1:
		substr = substr[0]
		key_filted = key.replace(substr, '[0]')

		# Normal Operation
		if val == None:
			return hash(key_filted)
		# 0th record of the array
		if substr == '[0]':
			return hash(key_filted)
		# Not 0th record of the array, but 0th not parsed yet
		if substr != '[0]' and rules.get(hash(key_filted), None) == None:
			process_item(key_filted)
			return hash(key)
		# Exist same filtered record, need to verify if two records are identical
		elif rules[hash(key_filted)][2] == val:
			return hash(key_filted)
		# If not, create new record
		else:
			return hash(key)
	else:
		return hash(key)

def process_item(key, val=None):

	if val == None:
		val = dict.get(key, '')

	key_replace = key.replace('[', '_').replace(']', '_').replace('.', '_')

	same = strcmpsame(key, val)
	key_pos = key[len(same):]
	val_pos = val[len(same):]

	# Same
	if val.find(key) == 0 and len(key) == len(val):
		rules[filt_arr(key, val)] = [0, 0, '']

	# Postfix no change
	elif val.find(key) == 0 and len(key) != len(val):
		rules[filt_arr(key, val)] = [0, 0, val[len(key):]]

	# Replace, Same
	elif val.find(key_replace) == 0 and len(key_replace) == len(val):
		rules[filt_arr(key, val)] = [1, 0, '']

	# Replace, Same, Postfix no change
	elif val.find(key_replace) == 0 and len(key_replace) != len(val):
		rules[filt_arr(key, val)] = [1, 0, val[len(key_replace):]]

	# Postfix rm tail
	elif same in val and key_pos != val_pos:
		rules[filt_arr(key, val)] = [0, len(key)-len(same), val_pos]

	# Others
	else:
		print(key, val)

##### GENERATE #####

start = time.time()

rules = dict()

case = str(sys.argv[1])
file_case = 'cases8/case'+case+'.json'
file_rule = 'data_'+case+'.json'

with open(file_case, 'r') as fr:
	dict = json.load(fr)

for key, val in dict.items():
	process_item(key, val)

time_gen = time.time()-start

with open(file_rule, 'w') as fw:
	json.dump(rules, fw)

##### VERIFY #####

start = time.time()

with open(file_case, 'r') as fr:
	dict = json.load(fr)

print('--------------------------')
print('Wrong Generated Value List')

for key, val in dict.items():

	key_filted = filt_arr(key)
	
	val_lkup_filt = rules.get(hash(key_filted), None)
	val_lkup_orig = rules.get(hash(key), None)

	val_lkup = val_lkup_orig if val_lkup_orig != None else val_lkup_filt

	key_replace = key.replace('[', '_').replace(']', '_').replace('.', '_')

	if val_lkup == None:
		check = ''

	elif val_lkup[0] == 1:

		# Replace, Same
		if val_lkup[1] == 0 and val_lkup[2] == '':
			check = key_replace

		# Replace, Postfix no change
		elif val_lkup[1] == 0 and val_lkup[2] != '':	
			check = key_replace + val_lkup[2] 

		# Replace, Postfix rm tail
		elif val_lkup[1] != 0:
			check = key_replace[0:len(key_replace)-val_lkup[1]] + val_lkup[2]	

	# Same
	elif val_lkup[1] == 0 and val_lkup[2] == '':
		check = key
	
	# Postfix no change
	elif val_lkup[1] == 0 and val_lkup[2] != '':
		check = key+val_lkup[2]
	
	# Postfix rm tail
	elif val_lkup[1] != 0:
		check = key[0:len(key)-val_lkup[1]] + val_lkup[2]

	if check != val:
		print(key, check, val, val_lkup)

print('(If no record displayed means all passed)')
print('--------------------------')

time_ver = time.time()-start

##### SUMMARY #####

print('Dict Generate Elapsed Time:\t' + str(time_gen) + ' (sec)')
print('Dict Verify Elapsed Time:\t' + str(time_ver) + ' (sec) // This time will be meaningful only when the wrong gened value list is empty.')

print('Readed Dict Total Mem Size:\t' + str(sys.getsizeof(dict)) + ' (bytes)')
print('Gened Dict Total Mem Size:\t' + str(sys.getsizeof(rules)) + ' (bytes)')

fsize_case = os.path.getsize(file_case)
fsize_rule = os.path.getsize(file_rule)

print('Readed Dict Total File Size:\t' + str(fsize_case) + ' (bytes)')
print('Gened Dict Total File Size:\t' + str(fsize_rule) + ' (bytes)')