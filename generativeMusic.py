import mido
from os import system
from math import floor, log10

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
    


outputs = mido.get_output_names()
if len(outputs) == 1:
    outport = mido.open_output(outputs[0])
else:
    outport = mido.open_output(pickFromOptions(outputs,"Option"))


outport.send(mido.Message("note_on",note=60))

input()

outport.reset()