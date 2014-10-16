from pythonPWA.utilities.minuitLikelihood import minuitLikelihood
import os

class generator(object):
    def __init__(self):
        self.fileName=None

    def createFile(self,numberOfTerms):
        """
        Writes out a file containing a wrapper function for hI.lnLikelihood,
        simply give this function the number of terms and it will write the needed wrapper function to the file
        specified by self.filename.
        """
        outputFile=open(self.fileName,'w')
        outputString="def fn("
        bufferString=""

        totalList=[]

        for i in range(numberOfTerms):
            totalList.append("t"+str(i))

        for i in range(len(totalList)):
            if i!=len(totalList)-1:
                outputString+="t"+str(i)+","
                
            if i==len(totalList)-1:
                outputString+="t"+str(i)
                

        outputString+="):\n\tretList=["
        
        for i in range(len(totalList)):
            if i!=len(totalList)-1:
                outputString+="t"+str(i)+","
                
            if i==len(totalList)-1:
                outputString+="t"+str(i)

        outputString+="]\n\treturn hI.lnLikelihood(retList)\n\n"
        
        outputFile.write(outputString)
        
        stringBuffer="m=Minuit(fn,"
        for i in range(len(totalList)):
            if i!=len(totalList)-1:
                stringBuffer+="t"+str(i)+"=.01,"
                
            if i==len(totalList)-1:
                stringBuffer+="t"+str(i)+"=.01"
                
        stringBuffer+=")\n"

        outputFile.write(stringBuffer)
        outputFile.close()
