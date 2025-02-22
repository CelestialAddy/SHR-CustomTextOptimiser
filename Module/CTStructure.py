# CTStructure.py
# Convert CTDump output into something more INI/tier-like (but lazy but easier).
# Feb-2025 @CelestialAddy

def Make(Source={}, IgnoredSections=[]):
    Stc = {"VARIABLES" : {}}
    for SectionPlusString, Text in Source.items():
        try:
            Section = SectionPlusString.split("::")[0]
            String = SectionPlusString.split("::")[1]
        except:
            Section = ""
            String = SectionPlusString
        if Section != "" and Section in IgnoredSections:
            continue
        try:
           Stc[Section][String] = Text
        except:
            Stc[Section] = {}
            Stc[Section][String] = Text
        continue
    return Stc

# End.
