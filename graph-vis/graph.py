import csv
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from collections import OrderedDict

# get dir to look for csv files
csv_dir = str(sys.argv[1])

states_to_watch = str(sys.argv[2])
states_to_watch = states_to_watch.split(',')

# list of files that have already been loaded
loaded_files_list = set()

# loaded data
all_rows = list()

# the list of fields in each row
row_fields = list()

# create graph
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

# number of times animate has been run
num_anims = list()
num_anims.append(0)

# called every second
def animate(i, all_rows, row_fields, num_anims, loaded_files_list, states_to_watch):
     
    # get all files in dir
    all_files_list = set(os.listdir(csv_dir))
    
    # determine which files have not been loaded
    new_files_list = all_files_list.symmetric_difference(loaded_files_list)
    print('loading new files:' + str(new_files_list))

    # note that new files will be loaded
    for f in new_files_list:
        loaded_files_list.add(f)    

    # load data from all files
    # count how many elements were loaded so we know how many to remove
    num_new_rows_loaded = 0
    for input_file in new_files_list:
        with open(csv_dir + '/' + input_file) as csv_file:
            reader = csv.reader(csv_file)
            try:
                for row in reader:
                    num_new_rows_loaded += 1
                    all_rows.append(row)
            except:
                pass
    # remove old batch on all except first anim
    if num_anims[0] > 0:
        num_rows_to_remove = min(len(all_rows), num_new_rows_loaded)
        print('num old entries removed:' + str(num_rows_to_remove))
        del all_rows[:num_rows_to_remove]
    
    # on first animation get row field identifiers (only the first file loaded wil have these)
    if num_anims[0] == 0:
        # get the list of field names in the csv
        row_fields = all_rows[0]
        all_rows.pop(0)
        print('row fields:' + str(row_fields))

    num_anims[0] = num_anims[0] + 1

    # todo: load xarr and yarr

    # load data
    # map of location -> avg sent at loc, num tweets from loc
    loc_sent_map = OrderedDict()
    loc_num_map = OrderedDict()
    for row in all_rows:
        if len(row) > 2:
            loc = row[2]
            if loc == 'location' or loc not in states_to_watch:
                continue
            sent = float(row[1])
            num = int(row[0])
            loc_sent_map[loc] = sent
            loc_num_map[loc] = num

    locations = loc_sent_map.keys()
    yarr = loc_sent_map.values()
    ax1.clear()
    y_pos = np.arange(len(locations))
    ax1.set_xticks(y_pos, locations)
    ax1.set_xticklabels(locations)
    ax1.bar(y_pos, yarr, align='center', label='perfect')

anim = animation.FuncAnimation(fig, animate, fargs=(all_rows,row_fields,num_anims,loaded_files_list,states_to_watch,), interval=1000)
plt.show()
