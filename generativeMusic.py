import mido
from os import system
from math import floor, log10
from time import sleep
from random import randint

def clearTerminal():
    system("cls")
    
def validatedNumericalInput(prompt:str , minimum:int , maximum:int) -> int:
    while True:
        clearTerminal()
        testInput = input(prompt)
        try:
            intInput = int(testInput)
            if minimum <= intInput and intInput <= maximum:
                return intInput
        except ValueError:
            continue

def pickFromOptions(options:list[str|int] , returnType="Option") -> str|int:
    if returnType not in ["Index","Option","Both"]: raise ValueError('returnType must be one of the following: "Index","Option","Both"')
    
    numberOfOptions = len(options)
    maxNumberOfSpaces = floor(log10(numberOfOptions)) + 1
    
    optionsDisplay = ""
    for option , index in zip( options , range(numberOfOptions) ):
        prefix = " "*(maxNumberOfSpaces-len(str(index)))
        optionsDisplay += f"{prefix}{index} : {option}\n"
        
    optionsDisplay +="----- Pick An Option -----\n"
    
    index = validatedNumericalInput(prompt=optionsDisplay , minimum=0 , maximum=numberOfOptions-1)
    clearTerminal()
    match returnType:
        case "Index":
            return index
        case "Option":
            return options[index]
        case "Both":
            return [index,options[index]]

progressions = {
    "Happy"
}

ChordPairs = {
    "Sad":{
        "Sadness":[["Maj", [4, "min"]]],
        "Tragic":[["min", [5, "min"]],["min", [7, "min"]]],
        "BitterSweet":[["min", [7, "Maj"]],["min", [10, "Maj"]],["Maj", [2, "min"]]],
    },
    "Evil":{
        "MysteryTense":[["min", [1, "min"]],["min", [11, "min"]],["min", [9, "Maj"]],["Maj", [3, "min"]]],
        "Uneasy":[["min", [2, "min"]],["min", [10, "min"]]],
        "Otherworld":[["min", [3, "min"]],["min", [9, "min"]]],
        "Dark":[["min", [4, "min"]],["min", [8, "min"]]],
        "Danger":[["min", [6, "min"]]],
    },
    "EvilNeutral":{
        "Drama":[["min", [11, "Maj"]],["Maj", [1, "min"]]],
        "Dark":[["min", [2, "Maj"]],["Maj", [10, "min"]]],
        "Space":[["min", [6, "Maj"]],["Maj", [6, "min"]]],
    },
    "Neutral":{
        "Exotic":[["Maj", [1, "Maj"]],["Maj", [11, "Maj"]]],
        "Space":[["Maj", [6, "Maj"]]],
        "CautiousOptimism":[["Maj", [11, "min"]],["min", [1, "Maj"]]],
        "RisingAction":[["min", [3, "Maj"]]],
        "PowerMystery":[["min", [4, "Maj"]],["Maj", [8, "min"]]],
        "Resolution":[["min", [8, "Maj"]]],
    },
    "GoodNeutral":{
        "Romantic":[["Maj", [5, "Maj"]],["Maj", [7, "min"]]],
        "Heavenly":[["Maj", [9, "min"]]],
        "Wonder":[["min", [5, "Maj"]],["Maj", [7, "min"]]],
    },
    "Good":{
        "Protagonist":[["Maj", [2, "Maj"]],["Maj", [10, "Maj"]]],
        "Heroic":[["Maj", [3, "Maj"]],["Maj", [9, "Maj"]]],
        "Fantastic":[["Maj", [4, "Maj"]],["Maj", [8, "Maj"]]],
        "Good`Energy":[["Maj", [5, "Maj"]],["Maj", [7, "Maj"]]],
    }
}

startingNote = 60


def formChord(startNote,chordType):
    chord = [startNote]
    chord.append(startNote + (4 if chordType == "Maj" else 3))
    chord.append(startNote + 7)
    return chord

def playNotes(*args):
    global messages
    global outport
    
    for note in args:
        outport.send(mido.Message("note_on",note=note))
        messages.append(note)

def stopNotes(*args):
    global messages
    global outport
    for note in args:
        outport.send(mido.Message("note_off",note=note))
        messages.remove(note)

def inversion(chord,num):
    if num == 0:
        return chord
    for i in range(num+1):
        chord[i] = chord[i] + 12
    return chord
        

outports = mido.get_output_names()
if len(outports) == 1:
    outport = mido.open_output(outports[0])
else:
    outport = mido.open_output(pickFromOptions(outports,"Option"))

messages = []

# outport.send(mido.Message("note_on",note=startingNote))

for a in ChordPairs:
    for b in ChordPairs[a]:
        for chordInfo in ChordPairs[a][b]:
            chord0 = formChord(startingNote,chordInfo[0])
            chord1 = formChord(startingNote + chordInfo[1][0],chordInfo[1][1])
            
            bass0 = [chord0[0] - 12,chord0[0]-24]
            
            # chord0 = inversion(chord0,randint(0,1))
            # chord1 = inversion(chord1,randint(0,1))
            
            
            playNotes(*bass0,*chord0)
            sleep(1)
            stopNotes(*chord0)
            playNotes(*chord1)
            sleep(1)
            stopNotes(*bass0,*chord1)

            

outport.reset()