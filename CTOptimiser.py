# CTOptimiser.py
# Custom Text Optimiser frontend/main.
# Feb-2025 @CelestialAddy

# Requirements

import Module.CTDump       as Dumper
import Module.CTStructure  as Structure
import sys                 as System

# Initialisations

IPath = 1
OPath = 2
Dict = 3
NoCR = 4
UTF8 = 5
Wipe = 6

def Fail(Reason="Error."):
    print("(!)", str(Reason))
    exit()

CompressionStringActors = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def NewCompressionString(Current=-1):
    return Current + 1

# Startup, evaluate CLA options
print("CustomText Optimiser (revision 1) by CelestialAddy" + "\n" + "-" * 100)

try:
    CLA = System.argv
    IPath = CLA[IPath]
    if IPath.find(";") == -1: FAIL()
    OPath = CLA[OPath]
    Dict = CLA[Dict].upper() == "DICT"
    NoCR = CLA[NoCR].upper() == "NOCR"
    UTF8 = CLA[UTF8].upper() == "UTF8"
    Wipe = CLA[Wipe].upper() == "WIPE"
except:
    Fail("Bad command line arguments. Format: \"<i> <o> [toggles]\". See documentation.")

# Dump, structure the textbible

try:
    Dmp = Dumper.Dump(IPath.split(";")[0], IPath.split(";")[1])
    Stc = Structure.Make(Dmp)
except:
    Fail("Unable to open or convert input file.")
#print(Stc)

# Dictionary-ify?

if Dict:
    ##########-------##########
    # Begin variableisation madness.

    # (it's gonna be a long day...)
    
    # STEP 1:
    # Iterate through every valid section and string, build a non-var word count.
    Words = {} # Words[Word]=Count
    for Section in Stc.keys():
        if Section == "MISCELLANEOUS" or Section == "VARIABLES": continue
        for String, Text in Stc[Section].items():
            Text = Text.split(" ")
            for Word in Text:
                Word = Word.strip()
                if len(Word) > 0:
                    if Word[0] == "$" and Word.find("(") != -1 and Word.find(")") != -1: continue
                    try:
                        Words[Word] = Words[Word] + 1
                    except:
                        Words[Word] = 1
                continue
            continue
        continue

    # STEP 2:
    # Eliminate words that appear only once.
    Eliminator = []
    for Word, Count in Words.items():
        if Count < 2: Eliminator.append(Word)
    for Word in Eliminator:
        del Words[Word]

    # STEP 3:
    # Sort words by count, highest first.
    Words = {key: val for key, val in sorted(Words.items(), key = lambda ele: ele[1], reverse=True)}
    #print(Words)

    # STEP 4:
    # Initialise variable "xx"/"##" names/counts.
    # Go through the words list.
    # If the length of $(variahle-ID-ising) this word is less than the word is, do it, and gswap.
    CStr = NewCompressionString()
    Show = str(hex(CStr)).replace("0x","")
    FirstRun = True
    UpdateIsRequired = False
    for Word in Words:
        if not FirstRun and UpdateIsRequired:
            CStr = NewCompressionString(CStr)
            Show = str(hex(CStr)).replace("0x","")
        if len(f"$({Show})") < len(Word):
            UpdateIsRequired = True
            Stc["VARIABLES"][Show] = Word
            for Section in Stc.keys():
                if Section == "MISCELLANEOUS" or Section == "VARIABLES": continue
                for String, Text in Stc[Section].items():
                    Text = Text.replace(" " + Word, " " + f"$({Show})", Text.count(Word))
                    Text = Text.replace(Word + " ", f"$({Show})" + " ", Text.count(Word))
                    Text = Text.replace(Word + "\n", f"$({Show})" + "\n", Text.count(Word))
                    Text = Text.replace(Word + ".", f"$({Show})" + ".", Text.count(Word))
                    Text = Text.replace(Word + ",", f"$({Show})" + ",", Text.count(Word))
                    Text = Text.replace(Word + "!", f"$({Show})" + "!", Text.count(Word))
                    Text = Text.replace(Word + "?", f"$({Show})" + "?", Text.count(Word))
                    Stc[Section][String] = Text
                    continue
                continue
        else:
            UpdateIsRequired = False
        FirstRun = False
        continue
        
    print("DICTIONARY SIZE:", str(CStr + 1))

    # End variableisation madness.
    ##########-------##########
    #print(Stc)
    pass
else:
    if len(Stc["VARIABLES"]) < 1: del Stc["VARIABLES"]

# Remove unused strings (also get the list of unused strings if needed)?

try:
    GetUnuStr = open("UnusedStrings.txt", "r")
    LstUnuStr = GetUnuStr.read().split("\n")
    GetUnuStr.close()
except:
    LstUnuStr = []
    pass

if Wipe:
    for Section in Stc.keys():
        if Section == "MISCELLANEOUS" or Section == "VARIABLES": continue
        Eliminator = []
        for String in Stc[Section].keys():
            if String in LstUnuStr: Eliminator.append(String)
            continue
        for String in Eliminator:
            del Stc[Section][String]
        continue
    print("PRUNED ALLEGEDLY UNUSED:", str(len(Eliminator)))
    pass

# Output path, as UTF-8/LF linebreaks?

if OPath.upper() == "SHADOW":
    # Terrible way of doing
    OPath = IPath.replace(".ini", "_OP.ini")
    OPath = OPath.replace(".INI", "_OP.INI")
    OPath = OPath.replace(".txt", "_OP.txt")
    OPath = OPath.replace(".TXT", "_OP.TXT")
    OPath = OPath.split(";")[0]
elif OPath.upper() == "OVERWRITE":
    OPath = IPath.split(";")[0]
else:
    OPath = OPath

if UTF8: OEnco = "UTF-8"
else: OEnco = IPath.split(";")[1]

if NoCR: ONewl = "\n"
else: ONewl = None

# Output process + confirmation

OData = ""
for Section in Stc:
    OData = OData + "[" + Section + "]\n"
    for Text, String in Stc[Section].items():
        OData = OData + Text + "=" + String + "\n"
        continue
    continue
try:
    Out = open(OPath, "w", encoding=OEnco, newline=ONewl)
    Out.write(OData)
    Out.close()
except:
    Fail("Unable to create or write to output file.")

print("Optimisation process complete.")

# End.
