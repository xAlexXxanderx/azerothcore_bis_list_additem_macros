import os
import sys
from dotenv import load_dotenv
import pymysql
import argparse
current_path = os.path.dirname(os.path.abspath(__file__))

def get_item_list(path_to_bis_list_file):
    bis_list = []
    bis_list_file = open(path_to_bis_list_file, 'r')
    for line in bis_list_file:
        bis_list.append(line.rstrip())
    bis_list_file.close()
    return(bis_list)

def get_item_id(item_name):
    conn = pymysql.connect(host=DATABASE_HOST, user=DATABASE_USER_NAME, passwd=DATABASE_PASSWORD, db=DATABASE_NAME)
    cur = conn.cursor()
    cur.execute('SELECT Entry,ItemLevel,name FROM '+TABLE_NAME+' WHERE name ="'+item_name+'"')
    conn.commit()
    cur_fetchall = cur.fetchall()
    cur_fetchall_len = int(len(cur_fetchall))
    if cur_fetchall_len > 1:
        max_id = 0
        max_ilvl = 0
        for i in range(0,cur_fetchall_len):
            item_id = cur_fetchall[i][0]
            item_ilvl = cur_fetchall[i][1]
            if item_ilvl > max_ilvl:
                max_id = item_id
                max_ilvl = item_ilvl
        item_id = max_id
    elif cur_fetchall_len == 1:
        item_id = cur_fetchall[0][0]
    else:
        item_id = 'Error'
    alias = len(cur.fetchall())
    cur.close()
    conn.close()
    return(item_id)

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filepath", help="Path to BIS list file", action='store')
args = parser.parse_args()

path_to_bis_list_file = current_path+'/bis.md'
if args.filepath:
    path_to_bis_list_file = args.filepath

load_dotenv()
DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
DATABASE_USER_NAME = os.environ.get("DATABASE_USER_NAME")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
TABLE_NAME = os.environ.get("TABLE_NAME")

sdm_id = -1
bis_dict = {}
bis_list = get_item_list(path_to_bis_list_file)
for i in bis_list:
    if '[' not in i:
        if '##' in i:
            if 'Template' not in i:
                sdm_id = sdm_id + 1
                bis_dict[sdm_id] = [i]
                #print(i)
    else:
        crop_one = i.split('[')[0]
        crop_two = i.split(']')[1]
        item_name = i.replace(crop_one,'').replace(crop_two,'').replace('[','').replace(']','').replace("\'","\\'")
        if len(item_name) > 0:
            command = '.additem '+str(get_item_id(item_name))
            if 'Error' not in command:
                bis_dict[sdm_id].append(command)
                #print(command)
            else:
                print('Error with '+item_name)
                break
                sys.exit()

sdm_config = '''sdm_version = "1.8.3"
sdm_listFilters = {
	["true"] = true,
	["s"] = true,
	["b"] = true,
	["false"] = true,
	["global"] = true,
	["f"] = true,
}
sdm_iconSize = 36
sdm_mainContents = {
'''

for key in bis_dict:
    sdm_config = sdm_config+'	'+str(key)+', -- ['+str(key)+']\n'

sdm_config = sdm_config + '''}
sdm_macros = {'''


for key in bis_dict:
    sdm_config = sdm_config + '''
	{
		["type"] = "b",
		["name"] = "'''+bis_dict[key][0].replace('## ','').replace(' ','')+'''",
		["ID"] = '''+str(key)+''',
		["text"] = "'''+'\\n'.join(bis_dict[key])+'''",
		["icon"] = 1,
	}, -- ['''+str(key)+''']'''

sdm_config = sdm_config + '\n}'

with open(current_path+'/SuperDuperMacro.lua', 'w') as f:
    f.write(sdm_config)

print('Done!')
