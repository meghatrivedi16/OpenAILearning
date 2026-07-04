# Reading a CSV File
import csv
with open('data.csv', mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

# Writing to a CSV File
# import csv
d = [['Name', 'Sal'], ['John', 30], ['Smith', 25]]
with open('output.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(d)