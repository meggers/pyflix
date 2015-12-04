import matplotlib.pyplot as plt
import csv

x = []
y = []
with open('data_dump.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        x.append(row[0])
        y.append(row[1])

colors = 'k'
area = 0

plt.scatter(x, y)
plt.show()