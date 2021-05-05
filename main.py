#Coded by Karanbir Gill
#May 5/2021

#Use python main.py to run the code

import json
import unittest

with open('standard_definition.json') as f:
    data = json.load(f)
    
with open('error_codes.json') as f1:
    errordata = json.load(f1)

errorcode={}

def checkingmaxlength(givenlength, maxlength):
    if(givenlength<=maxlength):
        return bool(True)
    else:
        return bool(False)

def checkingdatatype(givendata, expecteddata):
    if(givendata==expecteddata):
        return bool(True)
    else:
        return bool(False)

#Getting error code       
def gettingerrorcode(givendata, expecteddata,givenlength, maxlength, section, subsection):
    if((givendata=="empty") | (expecteddata=="Nothing")):
        writingbrieferror("E05", section, subsection, maxlength, expecteddata)
        return "E05"
    else:
        if((int(givenlength)<=int(maxlength)) & (givendata==expecteddata)):
            writingbrieferror("E01", section, subsection, maxlength, expecteddata)
            return "E01"
        if((givenlength>maxlength) & (givendata==expecteddata)):
            writingbrieferror("E03", section, subsection, maxlength, expecteddata)
            return "E03"
        if((givenlength<=maxlength) & (givendata!=expecteddata)):
            writingbrieferror("E02", section, subsection, maxlength, expecteddata)
            return "E02"
        if((givenlength>maxlength) & (givendata!=expecteddata)):
            writingbrieferror("E04", section, subsection, maxlength, expecteddata)
            return "E04"

#writing brief about the code      
def writingbrieferror(errorname, section, subsection, maxlength, expecteddata):
    for error in errordata:
        if(errorname==error['code']):
            outputfile1.write((((error['message_template'].replace('LXY', subsection)).replace('LX', section)).replace('max_length', maxlength )).replace('data_type', expecteddata )+"\n")
            return (((error['message_template'].replace('LXY', subsection)).replace('LX', section)).replace('max_length', maxlength )).replace('data_type', expecteddata )

#This method compare the json and the input file
def comparingwithjson(fname):
  for key in data:
    #Checking the key
    if(fname[0]==key['key']):
        current=0
        for subcheck in key['sub_sections']:
            outputstring=fname[0]+", "+subcheck['key']
            current=current+1
            if(current<len(fname)):
                if(subcheck['data_type']=='digits'):
                    if(fname[current].isdigit()):
                        digitlength=len(fname[current])
                        outputstring=outputstring+", "+"digits"+", digits, "+str(digitlength)+", "+str(subcheck['max_length'])+", "+gettingerrorcode("digits", subcheck['data_type'],str(digitlength), str(subcheck['max_length']), fname[0], subcheck['key'])+"\n"
                    elif(fname[current].isalpha() & len(fname[current])>0):
                        digitlength=len(fname[current])
                        outputstring=outputstring+", "+"word_characters"+", digits, "+str(digitlength)+", "+str(subcheck['max_length'])+", "+gettingerrorcode("word_characters", subcheck['data_type'],str(digitlength), str(subcheck['max_length']), fname[0], subcheck['key'])+"\n"
                    else:
                        digitlength=len(fname[current])
                        outputstring=outputstring+", "+"other"+", digits, "+str(digitlength)+", "+str(subcheck['max_length'])+", "+gettingerrorcode("other", subcheck['data_type'],str(digitlength), str(subcheck['max_length']), fname[0], subcheck['key'])+"\n"
                elif(subcheck['data_type']=='word_characters'):
                    if all(x.isalpha() or x.isspace() for x in fname[current]):
                        digitlength=len(fname[current])
                        outputstring=outputstring+", "+"word_characters"+", word_characters, "+str(digitlength)+", "+str(subcheck['max_length'])+", "+gettingerrorcode("word_characters", subcheck['data_type'],str(digitlength), str(subcheck['max_length']), fname[0], subcheck['key'])+"\n"
                    elif(fname[current].isdigit()):
                        digitlength=len(fname[current])
                        outputstring=outputstring+", "+"digits"+", word_characters, "+str(digitlength)+", "+str(subcheck['max_length'])+", "+gettingerrorcode("digits", subcheck['data_type'],str(digitlength), str(subcheck['max_length']), fname[0], subcheck['key'])+"\n"
                    else:
                        digitlength=len(fname[current])
                        outputstring=outputstring+", "+"other"+", word_characters, "+str(digitlength)+", "+str(subcheck['max_length'])+", "+gettingerrorcode("other", "word_characters",str(digitlength), str(subcheck['max_length']), fname[0], subcheck['key'])+"\n"                       
            else:
                outputstring=outputstring+", "+"empty"+", "+subcheck['data_type']+", "+"0, "+str(subcheck['max_length'])+","+gettingerrorcode("empty", subcheck['data_type'],"0", str(subcheck['max_length']), fname[0], subcheck['key'])+"\n"
            outputfile.write(outputstring)

        #This is a special case if the input is empty
        if(int(current)<(int(len(fname))-1)):
            current=current+1
            outputstring=fname[0]+", "+" Nothing "
            if all(x.isalpha() or x.isspace() for x in fname[current]) & len(fname[current])>0:
                digitlength=len(fname[current])
                outputstring=outputstring+", "+"word_characters"+", Nothing, "+str(digitlength)+", Nothing"+", Nothing"+"\n"
            elif(fname[current].isdigit()):
                digitlength=len(fname[current])
                outputstring=outputstring+", "+"digits"+", Nothing, "+str(digitlength)+", Nothing"+", Nothing"+"\n"
            else:
                digitlength=len(fname[current])
                outputstring=outputstring+", "+"other"+", Nothing, "+str(digitlength)+", Nothing"+", Nothing"+"\n"
            outputfile.write(outputstring)
            
            
        
  
#Reading input File
file = open("input_file.txt", "r")
Lines = file.readlines()

#Creating output files
outputfile = open("report.csv", "a")
outputfile1 = open("summry.txt", "a")
count = 0
outputfile.write("Sections, Sub-Sections, Given Data Types, Expected Data Types, Given Length, Expected MaxLength, Error Code\n")
# Strips the newline character
for line in Lines:
    count += 1
    subset=line.strip().split('&')
    comparingwithjson(subset)
    
outputfile.write("\n\nCoded by Karanbir Gill")  

#Unit Tests
class TestStringMethods(unittest.TestCase):
    #To test if the errorcode summary
    def errorcode_summary(self):
        self.assertEqual(writingbrieferror("E05", "L1", "L12", "2", "digits"), 'L12 field under section L1 is missing.')
    #Test Error code
    def errorcode(self):
        self.assertEqual(gettingerrorcode("digits", "digits", "2", "3", "L1", "L12"), 'E01')


unittest.main()



