from xml.etree import ElementTree	#installed easy_install urllib3
from xml.dom.minidom import parseString

#Create RTW Header XML		
def createRTWXMLHeader(rtwId,simId,beginRTWTs,endRTWTs,tsSize,tsSampInterval,neuronId,neuronVariablesBeingRecorded):
	rtwXml = ElementTree.Element('RTW')
	rtwXml.set('rtwId',str(rtwId))
	rtwXml.set('simId',str(simId))
	rtwXml.set('beginRTW',str(beginRTWTs))
	rtwXml.set('endRTW',str(endRTWTs))
	rtwXml.set('tsSize',str(tsSize))
	rtwXml.set('tsInterval',str(tsSampInterval))
	rtwXml.set('neuronId',str(neuronId))
	#for each variable being recorded
	i=0;
	rtwXmlNeuronVariable = []
	for v in neuronVariablesBeingRecorded:
		rtwXmlNeuronVariable.append(ElementTree.SubElement(rtwXml, 'item'))
		rtwXmlNeuronVariable[i].text = neuronVariablesBeingRecorded[i]
		i+=1
		
	rtwXmlStr = ElementTree.tostring(rtwXml)
	return rtwXmlStr
	
#Create Header for transmission of Timestep Variable Data
def createVarDataXMLHeader(simId,neuronId,rtwId,beginTs,endTs):
	varDataXml = ElementTree.Element('VarData')
	varDataXml.set('simId',str(simId))
	varDataXml.set('neuronId',str(neuronId))
	varDataXml.set('rtwId',str(rtwId))
	varDataXml.set('beginTs',str(beginTs))
	varDataXml.set('endTs',str(endTs))	

	varDataXmlStr = ElementTree.tostring(varDataXml)
	return varDataXmlStr
	
#Print humanly readable XML
def printPrettyXML(xmlStr):
	dom = parseString(xmlStr)
	pretty_xml_as_string = dom.toprettyxml()
	print(pretty_xml_as_string)
	
#for error checking that number of bytes corresponds to the variables being recorded
def errorCheckNumOfVars(neuronVariablesBeingRecorded, dataBytes, beginTs, endTs):		
	numTimeSteps = endTs - beginTs + 1;
	#calculate number of variables being recorded
	numVars = len(neuronVariablesBeingRecorded)
	#print "numVars: " + str(numVars)
	expectedNumberOfBytes = (8+(4*numVars)) * numTimeSteps

	#print "expectedNumberOfBytes: " + str(expectedNumberOfBytes)
	#print "len(dataBytes): " + str(len(dataBytes))
	if(expectedNumberOfBytes == len(dataBytes)):
		print('Number of bytes is correct')
	else:
		#print('Number of bytes is incorrect')
		raise ValueError('Number of bytes is incorrect: ' + "expectedNumberOfBytes: " + str(expectedNumberOfBytes) + ", len(dataBytes): " + str(len(dataBytes)))
		
#Create Header for transmission of Spike Data
def createSpikeDataXMLHeader(simId,beginTs,endTs):
	spikeDataXml = ElementTree.Element('SpikeData')
	spikeDataXml.set('simId',str(simId))
	spikeDataXml.set('beginTs',str(beginTs))
	spikeDataXml.set('endTs',str(endTs))	

	spikeDataXmlStr = ElementTree.tostring(spikeDataXml)
	return spikeDataXmlStr
	
#Error check that number of bytes in spikeBytes is correct and corresponds to header
def errorCheckSpikeBytes(spikeBytes, beginTs, endTs):		#for error checking	

	if(len(spikeBytes)/10 == int(len(spikeBytes)/10)):
		print('Number of bytes is correct')
	else:
		print('Number of bytes is incorrect')
		raise