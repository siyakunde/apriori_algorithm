import os
import numpy as np  
from collections import OrderedDict
import sys
import matplotlib.pyplot as plt  
import pandas as pd
from scipy.io import arff
import apriori

# Verify correct input arguments: 1 or 2
if (len(sys.argv) < 4 or len(sys.argv) > 4):
	print("Invalid number of arguments:   " + str(len(sys.argv)))
	print("Try: 'python3 main.py data_file.arff min_sup min_conf'")
	sys.exit(1)
elif (len(sys.argv) == 4):
	data_file_name = str(sys.argv[1])
	min_sup = float(sys.argv[2])
	min_conf = float(sys.argv[3])
	print("processing data now......")
else:
	print("bad argument(s): " + str(sys.argv))	#shouldnt really come up
	sys.exit(1)

# ---------------------------------------------------------------------------------------------
# --------------------------------Start Data Pre-processing Section----------------------------
# ---------------------------------------------------------------------------------------------

# Define and vectorize function so that each item in each tuple of the np array can be decoded.
# def f(x):
# 	return tuple(itup.decode('utf8') for itup in x)
# f = np.vectorize(f)
def g(x):
	return str(x.decode('utf8'))
data = arff.loadarff(data_file_name)
dataset = pd.DataFrame(data[0])
for i in range(0, len(dataset.columns)):
	dataset[dataset.columns[i]] = dataset.columns[i] + '=' + dataset[dataset.columns[i]].apply(g)

print(dataset)
# data, meta = arff.loadarff(data_file_name)
# data = f(data)
# dataser = pd.DataFrame(data)
# dataset = pd.DataFrame({'handicapped-infants':data[0],'water-project-cost-sharing':data[1],'adoption-of-the-budget-resolution':data[2],'physician-fee-freeze':data[3],
# 	'el-salvador-aid':data[4], 'religious-groups-in-schools':data[5], 'anti-satellite-test-ban':data[6], 'aid-to-nicaraguan-contras':data[7], 'mx-missile':data[8], 
# 	'immigration':data[9], 'synfuels-corporation-cutback':data[10], 'education-spending':data[11], 'superfund-righ-to-use':data[12], 'crime':data[13], 
# 	'duty-free-exports':data[14], 'export-administration-act-south-africa':data[15], 'class':data[16]})

# print(len(data))
# print(meta)

# # The following changes are being made so that output can match Weka style
# # eg handicapped-infants=y
# dataset['handicapped-infants'] = 'handicapped-infants='+dataset['handicapped-infants']
# dataset['water-project-cost-sharing'] = 'water-project-cost-sharing='+dataset['water-project-cost-sharing']
# dataset['adoption-of-the-budget-resolution'] = 'adoption-of-the-budget-resolution='+dataset['adoption-of-the-budget-resolution']
# dataset['physician-fee-freeze'] = 'physician-fee-freeze='+dataset['physician-fee-freeze']
# dataset['el-salvador-aid'] = 'el-salvador-aid='+dataset['el-salvador-aid']
# dataset['religious-groups-in-schools'] = 'religious-groups-in-schools='+dataset['religious-groups-in-schools']
# dataset['anti-satellite-test-ban'] = 'anti-satellite-test-ban='+dataset['anti-satellite-test-ban']
# dataset['aid-to-nicaraguan-contras'] = 'aid-to-nicaraguan-contras='+dataset['aid-to-nicaraguan-contras']
# dataset['mx-missile'] = 'mx-missile='+dataset['mx-missile']
# dataset['immigration'] = 'immigration='+dataset['immigration']
# dataset['synfuels-corporation-cutback'] = 'synfuels-corporation-cutback='+dataset['synfuels-corporation-cutback']
# dataset['education-spending'] = 'education-spending='+dataset['education-spending']
# dataset['superfund-righ-to-use'] = 'superfund-righ-to-use='+dataset['superfund-righ-to-use']
# dataset['crime'] = 'crime='+dataset['crime']
# dataset['duty-free-exports'] = 'duty-free-exports='+dataset['duty-free-exports']
# dataset['export-administration-act-south-africa'] = 'export-administration-act-south-africa='+dataset['export-administration-act-south-africa']
# dataset['class'] = 'class='+dataset['class']

# ---------------------------------------------------------------------------------------------
# --------------------------------End Data Pre-processing Section------------------------------
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# -------------------------------------Start Aprioti Section-----------------------------------
# ---------------------------------------------------------------------------------------------

outputData = OrderedDict()
start_time, end_time, C, L, supportL, R, confidenceR = apriori.main(dataset, min_sup, min_conf)
# print("--------------------------------------")
# print(C)
# print("------------------------------------")
# print(L)
# print("--------------------------------------")
# print(supportL)
# print("--------------------------------------")
# print(R)
# print("--------------------------------------")
# print(confidenceR)
# print("--------------------------------------")

run_time = end_time - start_time
outputData[str(min_sup) + '_' + str(min_conf)] = [min_sup, min_conf, start_time, end_time, run_time, C, L, supportL, R, confidenceR, len(confidenceR)]

dfOutputData = pd.DataFrame.from_dict(outputData, orient='index')
dfOutputData.columns = ['MinimumSupport', 'MinimumConfidence', 'StartTime', 'EndTime', 'RunTime', 'C', 'L', 'SupportL', 'R', 'ConfidenceR', 'NumberOfRules']
dfOutputData.to_csv(os.getcwd()+'/apriori_algorithm_experiment_data.csv')

# ---------------------------------------------------------------------------------------------
# -------------------------------------End Apriori Section-------------------------------------
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# ----------------------------------------Start Output Section---------------------------------
# ---------------------------------------------------------------------------------------------

print('Minimum Support: ' + str(min_sup))# + '(' + str(instances) + ' instances)')
print('Minimum Confidence: ' + str(min_conf))
# print('Number of Cycles: ' + str(cycles))
print('Generated set of large itemsets:')
for i in range(len(L)):
	print('Size of set for large itemset L(' + str(i+1) + '): ' + str(len(L[i])))
print('Best rules found:')
for i in range(len(confidenceR)):
	print(confidenceR[i][0])
# ToDo : Print out the rules and frequencies
print('Total Runtime (seconds): ' + str(end_time - start_time))

# ---------------------------------------------------------------------------------------------
# -----------------------------------------End Output Section----------------------------------
# ---------------------------------------------------------------------------------------------
