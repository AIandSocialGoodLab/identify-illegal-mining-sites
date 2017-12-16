import csv

# file = open("training_labels.csv", "r")

# trainingLines = file.readlines()

# for i in range(1, length(trainingLines)):
# 	line = trainingLines[i]

with open('training_labels.csv', 'rb') as csvfile:
	training = csv.reader(csvfile)
	
	for row in training:
		try:
			if (int(float(row[4])) < 0 or int(float(row[5])) < 0 or 
				int(float(row[6])) > int(float(row[1])) or 
				int(float(row[7])) > int(float(row[2]))):
				print(', '.join(row))
		except:
			print(', '.join(row))
		

print('Testing')
print('')

with open('testing_labels.csv', 'rb') as csvfile:
	testing = csv.reader(csvfile)
	
	for row in testing:
		try:
                        if (int(float(row[4])) < 0 or int(float(row[5])) < 0 or
                                int(float(row[6])) > int(float(row[1])) or
                                int(float(row[7])) > int(float(row[2]))):
                                print(', '.join(row))
                except:
                        print(', '.join(row))
