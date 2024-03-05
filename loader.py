import os
import json
from scipy.io import arff
from lib import *

PATH = './discriminationsFlowBasedClassification/'
f = open('settings.json')
settingsJson = json.load(f)



if __name__=='__main__':
    totalData = []
    dataSetsName = os.listdir(PATH)
    print('Will load the datasets...')
    for dataset in dataSetsName:
        data = arff.loadarff(PATH+dataset)
        totalData.extend(data[0])
    joinUDPColumns(totalData)
    filteredResults = filterClasses(totalData)
    filteredDatabase = filteredResults['database']
    for i in range(0, len(filteredDatabase)):
    	print('Registro completo')
    	print(filteredDatabase[i])	
    	print('-------------------------------------')
    	if i>20:
    	   break
    print(len(totalData))
    print(len(filteredDatabase))
