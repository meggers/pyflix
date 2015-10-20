#generates a csv containing 30,000 1024 byte frames and their order

import os,binascii

csv_file = "movie_data.csv"
frame_size = 1024
num_frames = 30000

target = open(csv_file, 'w')
target.truncate()

for index in range(0, num_frames):
    target.write("{0},{1}\n".format(index, binascii.b2a_hex(os.urandom(frame_size))))

target.close()