#generates a csv containing 30,000 1024 byte frames and their order

import os, binascii

csv_file = "server/movie_data.txt"
frame_size = 1029
num_frames = 30000

target = open(csv_file, 'wb')
target.truncate()

for index in range(0, num_frames):
    frame_no   = '{0:05d}'.format(index)
    frame_data = binascii.b2a_hex(os.urandom(frame_size))
    target.write("{0}{1}\n".format(frame_no, frame_data))

target.close()
