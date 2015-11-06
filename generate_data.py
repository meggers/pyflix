#generates a csv containing 30,000 1024 byte frames and their order

import os, struct

csv_file = "server/movie_data.bin"
frame_size = 1020
num_frames = 30000

target = open(csv_file, 'wb')
target.truncate()

for index in range(0, num_frames):
    target.write(struct.pack("I", index))
    target.write(os.urandom(frame_size))

target.close()
