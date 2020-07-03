import json
import os
'''
with open('./spiders/oldies.json') as fp:
    data = json.load(fp)

with open('./si_oldies.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)
'''
with open('./spiders/oldies.json') as fp:
    data = json.load(fp)
    for ele in data:
    	print(data)
    	break
#os.system('python new_write_to_sinhala')