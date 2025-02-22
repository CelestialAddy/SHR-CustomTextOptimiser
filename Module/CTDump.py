# CTDump.py
# Convert ".ini" textbible to Python dictionary.
# Jan-2025 @CelestialAddy (edited Feb-2025 for structure support)

##### Functionality.

def Dump(Path="", Codec=""):
    Text = {}
    Src = open(str(Path), "rt", encoding=str(Codec).lower())
    Lns = Src.read().split("\n")
    Src.close()
    Locality = ""
    for Ln in Lns:
        # *** NEW AMAZING FUN LOGIC TO HANDLE ESCAPES FOR \ AND # ***
        EscapeEnabled = False
        EndsAt = len(Ln)
        for Char in range(0, len(Ln)):
            if EndsAt != len(Ln): continue
            if Ln[Char] == "\\":
                EscapeEnabled = True
                continue
            else:
                if (Ln[Char] == ";") or (Ln[Char] == "#"):
                    if EscapeEnabled == True: continue
                    else: EndsAt = Char
                EscapeEnabled = False
                continue
            continue
        Ln = Ln[0:EndsAt]
        # END OF THAT
        #Ln = Ln.split(";")[0]
        if (Ln.find("[") > -1) and (Ln.find("]") > -1) and (Ln.find("=") == -1):
            Locality = Ln[Ln.find("[") + 1:Ln.find("]")].upper()
            if len(Locality) > 0: Locality = Locality + "::"
            continue
        try:
            Ln = Ln.split("=")
            S = Ln[0].strip()
            T = Ln[1].strip()
            #if Locality.find("MISCELLANEOUS::") == -1: Text[Locality + S] = T
            Text[Locality + S] = T
        except:
            pass
        continue
    return Text

# End.
