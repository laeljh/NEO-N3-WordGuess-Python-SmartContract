from boa3.builtin import NeoMetadata, metadata, public
from boa3.builtin.interop import storage
'''
Simple NEO smart contract written in python in anaconda
with boa3 and neo-express testing environment 

The contract runs the most basic iteration of a guess word game,
one person sets up a keyword and everyone is trying to guess,
once a correct keyword is provided the slot for a new word 
opens again and whoever sends it first gets their word saved 
for the rest to guess

The code uses @metadata function which was a copy paste implementation
from boa3 website tutorial, this script could be optimized and easily 
developed into more complex functionality. If you feel like a challenge 
go ahead. Add ability to save a hint as well as keyword, and for others to 
be able to call function to get the hint. 

On the technical side, it's important to note the
script is written in python semantics but it's not exactly 
python. There are no multiple assignment variables
that can be used within the script,
any preserverence of the information
must be done by NEOs built in decentrilezd file system. 
Hence no variables but storage.put and storage.get calls
instead. 

'''    

#initialization function, needs to be called by the script owner as soon as the script is launched, to save information that no word was saved at the start of the game yet
#it saves the "False" boolean information into a storage with a key 'saved', by which the data can be pulled later, can't be used to reset the game bacuse of the "if check"
@public 
def Init():
    if(not answerSaved):
        storage.put('saved',False)

#copy paste function for meta data handling 
@metadata
def manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.author = "ljh"
    meta.email = "ljh@ljh.com (notmy true email)"
    meta.describtion = "guess word game"
    return meta

#checks if there was a word saved already, by checking what value has the 'saved' key

def answerSaved() -> bool:
    return bytes.to_bool(storage.get('saved'))

#function that allows player to submit a word to be saved as a word to guess by others
def saveAnswer(answ:str) -> str:
    if(not answerSaved()):
        #saves data for an answer to the storage
        storage.put('answer',answ)
        #and sets saved to True, to inform contract that there is already a challenge word in place
        storage.put('saved',True)
        return "saving: keyword saved"
    else:
        return "can't save: other word already in place"
    
#reads the saved answer from the dictionary, doesn't perform a check if the answer exists, so it needs it be combined with check if it's saved for practical use
def getAnswer()->str:
        return bytes.to_str(storage.get('answer'))

#compares provided words/string with the saved answer string and completes the game upon correct guess
def checkAnswer(tryAns:str) -> str:
        if(tryAns==getAnswer()):
            #if the answer is correct unlock the slot for the next word to be saved
            unlockWordSlot()
            #payout()
            #let the player know they were right
            return "quessed correct"
        else:
            return "wrong!"

#unlocks the ability to save a new word as an answer
def unlockWordSlot():
    storage.put('saved',False)
    
#def payout():
    # TODO function to send payout to the winner

#combines previous functions, takes a word from a player
@public
def sendWord(tryAns:str)->str:
    #if the answer wasn't saved yet
    if(not answerSaved()):
        #save the provided word as a new answer
        return saveAnswer(tryAns)
    else:
        #otherwise check it against the currently saved word
        return checkAnswer(tryAns)






