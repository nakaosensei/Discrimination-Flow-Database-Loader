import json
f = open('settings.json')
settingsJson = json.load(f)

def joinUDPColumns(totalData):
    for register in totalData:
        if str(register[-1])=="b'FTP-CONTROL'" or str(register[-1])=="b'FTP-PASV'" or str(register[-1])=="b'FTP-DATA'":
            register[-1]='Bulk (UDP)'

def filterClasses(arffLoadedData):
    classesHashMap = {} #key: classname value: array [] of registers
    outputDataset = []
    for i in range(0, len(arffLoadedData)):
        arffLoadedData[i] = filterColumns(arffLoadedData[i].tolist())
        arffLoadedData[i] = convertVoidNoneTypesToEmptyStr(arffLoadedData[i])      

    for i in range(0,len(arffLoadedData)):            
        className = arffLoadedData[i][-1]
        if className not in classesHashMap:
            classesHashMap[className]=[]
        classesHashMap[className].append(arffLoadedData[i])
                       
    for i in range(0,len(arffLoadedData)):           
        className = arffLoadedData[i][-1]
        if className not in classesHashMap:
            continue
        if len(classesHashMap[className])<=2000:
            del classesHashMap[className]
            continue    
        outputDataset.append(arffLoadedData[i])       
    
    return {'database':outputDataset,'classesHashMap':classesHashMap}

def filterColumns(trafficInstance):
    usedColumns = settingsJson['colunasConsideradasRawIndex']
    newInstance = []
    for columnIndex in usedColumns:
        newInstance.append(float(trafficInstance[int(columnIndex)]))
    newInstance.append(trafficInstance[-1])
    return newInstance
    
def convertVoidNoneTypesToEmptyStr( trafficInstance):
    convertedTrafficInstance = []
    distinctTypes = {}
    for i in range(0, len(trafficInstance)):
        distinctTypes[type(trafficInstance[i])]=trafficInstance[i]   
                
        if type(trafficInstance[i])==None:
            convertedTrafficInstance.append("")                
        elif type(trafficInstance[i])==bytes:
            try:
                tmp = str(trafficInstance[i])
                convertedTrafficInstance.append(tmp)
            except:
                signedValue = []
                for j in trafficInstance[i]:
                    if type(trafficInstance[j])==bytes:
                        signedValue.append(str(j))
                        continue
                    signedValue.append(j)
                    
                convertedTrafficInstance.append(signedValue)
        else:
            convertedTrafficInstance.append(trafficInstance[i])       
    return convertedTrafficInstance
