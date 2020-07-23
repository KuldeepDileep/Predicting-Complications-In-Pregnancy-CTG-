from cluster_data_creation import data_for_cluster, cluster_extract
import pandas as pd
import numpy as np
from shutil import copyfile
from datetime import datetime
import xlsxwriter

# load data
xls = pd.ExcelFile('../CTG.xls')
data = pd.read_excel(xls, 'Data')

# no. of features, no. of classes
feat_num, classes = 21, 3
feature_names = np.array([data[i][0] for i in range(1, feat_num+classes)])

# 2126 examples, must enhance set
N = 2126

data_features = np.array([[data[i][j] for i in range(1, feat_num+1)]
                                 for j in range(1, N+1)])
data_labels = np.array([data[23][i] for i in range(1, N+1)])

# create copy of original file to add new data
# we shall work in this new file now
# '''
dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
workbook = xlsxwriter.Workbook('artificial_FINAL.xlsx')
worksheet = workbook.add_worksheet()
cell_format = workbook.add_format()
cell_format.set_bold()
cell_format = workbook.add_format({'bold': True})
row = 0
for i in range(1, 24):
	worksheet.write(row, i-1, i, cell_format)

row += 1
for i in range(len(feature_names)):
	worksheet.write(row, i, feature_names[i], cell_format)

# add old data

for i in range(len(data_features)):
	row += 1
	for j in range(len(data_features[i])):
		worksheet.write(row, j, data_features[i][j])
	worksheet.write(row, 22, data_labels[i])


#'''
clusters = cluster_extract(data_features, data_labels)
normal = clusters.get_cluster_from_data(1)
suspect = clusters.get_cluster_from_data(2)
pathologic = clusters.get_cluster_from_data(3)

new_normal = data_for_cluster(normal)
new_suspect = data_for_cluster(suspect)
new_patho = data_for_cluster(pathologic)

print(row)
# add new normal rows:
for i in range(1800 - len(normal)):
	row += 1
	x = new_normal.create_row()
	if i%50==0:
		print(i,"rows filled for normal.", row)
	while True:
		if not new_normal.check_cluster_validity(x, i) or new_normal.check_datapoint_presence(x):
			x = new_normal.create_row()
		else:
			break
	for j in range(len(x)):
		worksheet.write(row, j, x[j])
	worksheet.write(row, 22, 1)


# add new suspect rows:
for i in range(1800 - len(suspect)):
	row += 1
	x = new_suspect.create_row()
	if i%50==0:
		print(i,"rows filled for suspect.", row)
	while True:
		if not new_suspect.check_cluster_validity(x, i) or new_suspect.check_datapoint_presence(x):
			x = new_suspect.create_row()
		else:
			break
	for j in range(len(x)):
		worksheet.write(row, j, x[j])
	worksheet.write(row, 22, 2)
		

# add new patho rows:
print(row)
for i in range(1800 - len(pathologic)):
	x = new_patho.create_row()
	row += 1
	if i%50==0:
		print(i,"rows filled for patho.", row)
	while True:
		if not new_patho.check_cluster_validity(x, i) or new_patho.check_datapoint_presence(x):
			x = new_patho.create_row()
		else:
			break
	for j in range(len(x)):
		worksheet.write(row, j, x[j])
	worksheet.write(row, 22, 3)

workbook.close()
print(row)