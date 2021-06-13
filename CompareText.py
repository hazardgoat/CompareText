# This script compares two .txt files for differences and then writes any differences to a .txt file. 
# Additionally, it creates two .txt files that each contain the enumerated "sentences" for files 1 & 2, split at periods.
# This allows for more easily referencing the context of any differences that are found.



# import regular expressions
import re


# establishes paths to text for comparison
f1 = 'A.txt'
f2 = 'B.txt'
# establishes the names of the text documents that will be generated
docNames = ['File_1_Enumerated_Sentences.txt', 'File_2_Enumerated_Sentences.txt', 'Differences.txt']
# establishes whether to parse text assuming mostly correct grammer (regular) or not (irregular)
textType = ['regular', 'irregular']
textType = textType[0]



# compares file 1 against file 2 and returns any differences between them
def CompareText(f1, f2, docNames, textType):

    # establishes which conditioning regex patterns to use
    if textType == 'regular':
        replacements = {'\n':'. ', '\.\.+':'. ', '-':'', '\s':' '}
    else:
        replacements = {'\n':'', '-':'', '\s':''}

    # opens file 1 and conditons the text, splits it to a list at each period, then enumerates the list as a dictionary
    with open(f1,'r', encoding='utf-8') as f:
        f1_rawText = f.read()
        for key, value in replacements.items():
            # subsitutes text using the patterns in "replacements"
            f1_text = re.sub(key, value, f1_rawText)
        if textType == 'regular':
            f1_text = f1_text.split('. ')
        else:
            f1_text = f1_text.split('.')
        # iterates through the list and strips the white space off the ends of each string. Creates a map object of the result
        f1_text = map(str.strip, f1_text)
        # creates a dictionary by enumerating the items in the map object
        f1_sentences = dict(enumerate(f1_text))  

    # performs the same operations to file 2
    with open(f2,'r', encoding='utf-8') as f:
        f2_rawText= f.read()
        for key, value in replacements.items():
            f2_text = re.sub(key, value, f2_rawText)
        if textType == 'regular':
            f2_text = f2_text.split('. ')
        else:
            f2_text = f2_text.split('.')
        f2_text = map(str.strip, f2_text)
        f2_sentences = dict(enumerate(f2_text))

    f_sentences = [f1_sentences, f2_sentences]
    # keeps track of which file is being accessed
    docCounter = -1

    # creates files to record the enumerated sentences of files 1 & 2, as well as a file to record the differences between files 1 & 2.
    # Then it compares file 1 & 2 and records the differences.
    while True:
        docCounter += 1
        print('Creating', docNames[docCounter])

        # creates the documents from docNames if they don't already exist
        open(docNames[docCounter],'w').close()
        # opens each document in append mode
        with open(docNames[docCounter],'a',  encoding='utf-8') as f:
            # creates the enumerated sentences documents
            if docNames[docCounter] != docNames[-1]:
                for number, sentence in f_sentences[docCounter].items():
                    sentence = '['+str(number)+']: '+sentence+'\n'
                    f.write(sentence)
                continue
            # begins creating the document that records the text differences.
            # establishes the overall differential between files 1 & 2.
            else:
                if len(f1_rawText) == len(f2_rawText):
                    documentStatus = 'Status: File 1 and File 2 are the same length.\n'    
                elif len(f1_rawText) < len(f2_rawText):
                    documentStatus = 'Status: File 2 is longer than File 1.\n'
                else:
                    documentStatus = 'Status: File 1 is longer than File 2.\n'
                f.write(documentStatus)
        
                # keeps track of file comparison order
                switchCounter = 0
                # while loop compares file 1 against file 2 then reverses the order and does it again. Writes results to output file
                while True:
                    switchCounter += 1
                    if switchCounter == 1:
                        fa_sentences = f_sentences[1]
                        fb_sentences = f_sentences[0]
                        documentStatus = '\n'+'In File 1:\n'+'\n'
                        documentName = 'File_1_Enumerated_Sentences.txt'
                    else:
                        fa_sentences = f_sentences[0]
                        fb_sentences = f_sentences[1]
                        documentStatus = '\n'+'In File 2:\n'+'\n'
                        documentName = 'File_2_Enumerated_Sentences.txt'

                    f.write(documentStatus)
            
                    # compares files 1 & 2 and writes results to output file
                    for number, sentence in fb_sentences.items():
                        if sentence not in fa_sentences.values():
                            sentence = '['+str(number)+']: '+sentence+'\n'
                            f.write(sentence)
                    if switchCounter == 2:
                        break 
        break



# Runs the text comparison function
CompareText(f1, f2, docNames, textType)
