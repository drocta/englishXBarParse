"""Parser for english sentences under x-bar theory
by Matthew Corbelli"""

verbs=['punch','is','was','am','are','punched','took','takes','take','dance','are','flies','like','time']
nouns=['dog','cat','shoe','banana','void','apple','eon','arrow','flies']
pronouns=['I','i','you','they','he','she','we','me','myself','him','her','them','himself','herself','themselves','themself']
dets=['a','the','his','that','those','some','an']
prepositions=["above","across","after","against","along","around","as","at","before","below","on",'like']
auxilliaryVerbs=['be','is','am','are','is','was','were','being','been',
                 'can','could','dare','do','does','did','have','has','had',
                 'having','may','might','must','need','ought','shall','should','will','would']
adjectives=['time','red']
adverbs=['furiously']


nounlistFile=open('nounlist.txt','r')
nounlistContents=nounlistFile.read(-1)
nounlist=nounlistContents.split("\n")
nouns+=nounlist
nounlistFile.close()

prepositionlistFile=open('prepositionlist.txt','r')
prepositionlistContents=prepositionlistFile.read(-1)
prepositionlist=prepositionlistContents.split("\n")
prepositions+=prepositionlist
prepositionlistFile.close()

adjectiveslistFile=open('adjectiveslist.txt','r')
adjectiveslistContents=adjectiveslistFile.read(-1)
adjectiveslist=adjectiveslistContents.split("\n")
adjectives+=adjectiveslist
adjectiveslistFile.close()

verblistFile=open('verblist.txt','r')
verblistContents=verblistFile.read(-1)
verblist=verblistContents.split("\n")
verbs+=verblist
verblistFile.close()

adverblistFile=open('adverblist.txt','r')
adverblistContents=adverblistFile.read(-1)
adverblist=adverblistContents.split("\n")
adverbs+=adverblist
adverblistFile.close()


def t(maxDepth=50):
    sentenceString=raw_input("Enter sentence.").lower()
    sentenceArr=sentenceArrify(sentenceString)#split the sentence into a list of words
    parsingResults=[bracketed(parseResult[0]) for parseResult in parsePartNode('IP',sentenceArr,maxDepth) if parseResult[1]==[]]#find all the ways to parse the sentence, that don't leave extra words at the end.
    print "the possible parsings are:"
    for parsingResult in parsingResults:#list the different parsings to the user
        print parsingResult
    #print sentenceArr
def sentenceArrify(sentenceString):    
    sentenceString=sentenceString.strip('.')
    sentenceArr=sentenceString.split(' ')
    return sentenceArr

def isPartOfSpeech(word,partOfSpeech):
    if(partOfSpeech=="D"):
        return (word in dets) or (word in pronouns) #these should probably be combined.
    if(partOfSpeech=="V"):
        return word in verbs
    if(partOfSpeech=="N"):
        return word in nouns
    if(partOfSpeech=="P"):
        return word in prepositions
    if(partOfSpeech=="AUX"):
        return word in auxilliaryVerbs
    if(partOfSpeech=="A"):
        return word in adjectives
    if(partOfSpeech=="Adv"):
        return word in adverbs
    return False


subsLookup={
    "N'":[("N",None),
          ("N","PP"),
          ("AP","N'"),
          None],
    "AP":[("A'",None),
          None],
    "A'":[("A",None),
          None],
    "AdvP":[("Adv'",None),
            None],
    "Adv'":[("Adv",None),
            None],
    "S":[("IP",None),
         None],
    "IP":[("DP","I'"),
          (None,"I'"),
          None],
    "DP":[("D'",None),
          None],
    "D'":[("D",None),
          ("D","NP"),
          (None,"NP"),
          None],
    "NP":[("N'",None),
          None],
    "I'":[(None,"VP"),
          ("AUX","VP"),
          None],
    "AUX":[("AUX","AUX"),
           None],
    "VP":[("V'",None),
          None],
    "V'":[("V","DP"),
          ("V'","PP"),
          #("V'","AdvP"),
          #("AdvP","V'"),
          ("V",None),
          None],#Note: this doesn't handle prepositions and stuff yet, because max depth not implemented yet.
    "PP":[("P'",None),
          None],
    "P'":[("P","DP"),
          ("P",None),
          None],#has recursive stuff now!
    "DB1":[("DB2","DB3"),
           ("DB4","DB5"),
           None]#this is for debugging.
    }
verbose=False#this is for debugging. Change to verbose=True to see a bunch of information about the process the parser is going through
class parsePartNode:
    def __init__(self,partType,tokensList,maxDepth=10):
        if(verbose):print "new with partType:",partType,"and tokensList:",tokensList
        self.partType=partType
        self.maxDepth=maxDepth
        self.i=-1
        #self.n=3
        self.tokensList=tokensList[:]
        try:
            self.subs=subsLookup[partType]#check what this part can be made of
        except:
            self.subs=[]#if its not listed, it can't be made of smaller bits.
        #print "subs:",self.subs
        self.leftgen=None
        self.rightgen=None#rightgen needs to be updated each time leftgen is run
        self.previousResult=None
    def __iter__(self):#this is apparently neccesary for other things to realize that this is iteratable.
        return self
    def next(self):
        if(verbose):print "attempting to find a",self.partType
        if(verbose):print "where",self.partType," i is",self.i,"and subs is",str(self.subs)
        if(self.tokensList==[] and self.partType!=None):
            if(verbose):print "could not find a",self.partType," because list is empty."
            raise StopIteration()# if there are no things, there are no 
        i=self.i
        #self.i+=1
        if(i==-1 and self.partType==None):
            self.i=0
            self.previousResult="None"
            #print "returning a None (w/ tokenlist)"
            if(verbose):print "returning a None."
            return self.previousResult,self.tokensList
        elif(self.partType==None):
            if(verbose):print "already counted this none once, can't use it again."
            raise StopIteration()#theres only one way to None.
        elif(i==-1 and self.tokensList[0]==self.partType):#change to if token matches type
            self.i=0
            self.previousResult=self.tokensList[0]
            if(verbose):print "returning thing literal (for testing)"
            #print "returning thing literal:",self.tokensList[0],"and",self.tokensList[1:]
            return self.previousResult,self.tokensList[1:]
        elif(i==-1 and isPartOfSpeech(self.tokensList[0],self.partType)):
            self.i=0
            self.previousResult=[self.partType,self.tokensList[0]]#,self.tokensList[1:]
            if(verbose):print "found a",self.partType,". It is",self.tokensList[0]
            #print "returning thing word literal:",self.partType,self.tokensList[0],"and",self.tokensList[1:]
            return self.previousResult,self.tokensList[1:]
        else:
            if(self.maxDepth<=1):
                raise StopIteration()#max depth exceeded.
            self.i=max(self.i,0)
            #notfoundyet=True
            
            while(self.subs and self.subs[self.i]!=None):#as long as it hasn't run out of rules for this type
                #print "i:",self.i
                if(self.leftgen==None):#if case this is the first time the iterator is being used,
                    self.i=-1#make it so that it sets it up correctly
                while(True):
                    try:#try and find the next parsing right away
                        rightgenResult,rightgenRemTokens=self.rightgen.next()#by looking at the next thing for rightgen
                        self.previousResult=[self.partType, self.leftgen.previousResult, rightgenResult]
                        if(verbose):print "returning a ",self.partType
                        return self.previousResult,rightgenRemTokens#and returning the newly found parsing (along with the list of words that weren't used yet)
                    except:#If one couldn't find the next parsing of the iterator for the right half
                        try:#it probably ran out (or was never set in the first place)
                            leftgenval,leftgenRemaining=self.leftgen.next()#so try finding the next parsing the the left half
                            self.rightgen=parsePartNode(self.subs[self.i][1],leftgenRemaining,self.maxDepth-1)#and set up the right iterator again based on that
                            continue#then continue, and go back to the start of this loop to see if you can quickly get a result now
                        except:#if we couldn't get the next value for the left iterator, then we need a new left iterator, because its either out or was never set.
                            self.i+=1#so go to the next rule for how this part of a sentence can be formed
                            self.rightgen=None
                            #so a new leftgen is used. Then when trying to take from rightgen, it will take leftgen next
                            #and so make the new rightgen.
                            if(self.subs[self.i]==None):#we can't make a new left iterator from the next rule if there is no next rule, so we have to check that
                                break#if there are no more ways to form the thing, then see if there aren't any more ways to find this type of thing.
                            self.leftgen=parsePartNode(self.subs[self.i][0],self.tokensList,self.maxDepth-1)#set up the leftgen iterator with the next rule
                            if(verbose):print "next way to form a",self.partType," is ",str(self.subs[self.i])
                            break
                    #this is the end of the inner loop. It should never reach this comment, as it should always reach a continue or a break first.
            if(verbose):print "failed to find a",self.partType
            raise StopIteration()

withoutNone=True
def bracketed(parseTreeArr):
    if(parseTreeArr==None):
        return ""
    if(withoutNone and parseTreeArr=="None"):
        return ""
    if(not isinstance(parseTreeArr,list)):
        return parseTreeArr
    return "["+parseTreeArr[0]+" "+' '.join(map(bracketed,parseTreeArr[1:]))+"]"

          
print """Matthew Corbelli's Parser for English Sentences.
Note that this program does not parse questions, conjunctions, or punctuation."""
t()
raw_input("Press enter to exit.")
