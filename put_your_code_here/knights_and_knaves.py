# EDIT THE FILE WITH YOUR SOLUTION

def readTheFile(path):
    '''
    Read the file.
    '''
    fileContent = []
    with open(path, "r") as file:
        for line in file:
            fileContent.append(line.replace("\n", " "))
    fileContent = ''.join(fileContent)
    return fileContent

def breakSentence(allContent):
    '''
    For break a paragraph into multiple sentences.
    Then return useful part
    '''
    res = [[]]
    breakNote = set(['.', '!', '?'])
    status = 'normal' # followCentence, aheadCentence
    
    for word in allContent:
        res[-1].append(word)

        if status == 'normal':
            if word in breakNote:
                res[-1] = ''.join(res[-1])
                res.append([])
            if word == ':':
                status = 'followCentence'
                quoteCount = 0
            elif word == '"':
                status = 'aheadCentence'
        elif status == 'aheadCentence':
            if word == '"':
                status = 'normal'
        elif status == 'followCentence':
            if word == '"':
                quoteCount += 1
            if quoteCount == 2:
                status = 'normal'
                res[-1] = ''.join(res[-1])
                res.append([])

    if type(res[-1]) == list:
        res[-1] = ''.join(res[-1])
    
    return list(filter(lambda x : 'Sir' in x, res))

def statementParser(content):
    res = {}
    tailRemover = lambda w : w if w == '' or (ord(w[-1]) >= 97 and ord(w[-1]) <= 122) else w[:-1]
    
    for line in content:
        # find gentleman first
        
        if '"' in line:
            wordStart = line.index('"') + 1
            wordEnd = wordStart + line[wordStart:].index('"')
            theySay = line[wordStart:wordEnd]
        else:
            theySay = ''
        
        restLine = line[:line.index(theySay)] + line[line.index(theySay)+len(theySay):]
        startPoint = restLine.index('Sir')
        multiple = True if restLine[startPoint:startPoint + 4] == 'Sirs' else False

        if not multiple:
            gentlemans = [restLine[startPoint + 4:].split()[0]]
            gentlemans = list(map(tailRemover, gentlemans))
        else:
            restLine = restLine[startPoint + 4:].split()
            restLine = restLine[:restLine.index('and')+2]
            restLine.pop(restLine.index('and'))
            gentlemans = list(map(tailRemover, restLine))
        
        for gentleman in gentlemans:
            if gentleman.lower() not in res:
                res[gentleman.lower()] = [tailRemover(theySay).lower()] if tailRemover(theySay).lower() != '' else []
            elif theySay != '':
                res[gentleman.lower()].append(tailRemover(theySay).lower())
        
        # by value 'theySay' to find the sir mentioned inside word
        wordList = theySay.split()
        for i,word in enumerate(wordList):
            if word == 'sir' or word == 'Sir':
                nextName = wordList[i + 1].lower()[:-1] if wordList[i + 1][-1] == ',' else wordList[i + 1].lower()
                if nextName not in res:
                    res[nextName] = []

    return res

# traverse all the posibility
def findSlution(gentlemansWord):
    possibleSlution = []
    gentlemansCount = len(gentlemansWord)
    gentlemansList = list(gentlemansWord.keys())
    gentlemansList.sort()

    # Go through all possibilities
    for slution in range(2 ** gentlemansCount):
        slution = list(bin(slution)[2:].zfill(gentlemansCount)) # slution = '1100' such like that
        slution = list(map(int, slution))
        judgeRes = []
        for man in gentlemansList:
            judgeRes.append(gentlemansWord[man].judgeRequirement(gentlemansList, slution))
        if False not in judgeRes:
            possibleSlution.append(slution)
    gentlemansList = list(map(lambda x: x[0].upper() + x[1:], gentlemansList))
    return [possibleSlution, gentlemansList]

class gentlemanRequirement():
    def __init__(self, gentleman, statement) -> None:
        '''
        gentleman: String of this man name
        statement: A list representing the person's statements
        '''
        self.gentlemanName = gentleman
        self.statement = statement
    
    def judgeRequirement(self, gentlemansList, slution):
        '''
        input slution then try to 
        gentlemansList: Sorted list of names
        slution: String, 1 represents good guy, 0 represents bad guy
        '''
        res = True
        # if selfStatus == 0, all the result need to be reverse
        selfStatus = slution[gentlemansList.index(self.gentlemanName)]
        for requirement in self.statement:
            # 这个循环是为了判断每一个句子是否合理
            requirement = requirement.split()

            mentioned = [0 for _ in range(len(gentlemansList))]
            for i, word in enumerate(requirement):
                if word == 'sir':
                    index = gentlemansList.index(requirement[i + 1] if requirement[i + 1][-1] != ',' else requirement[i + 1][:-1])
                    mentioned[index] = 1
                elif word == 'i':
                    index = gentlemansList.index(self.gentlemanName)
                    mentioned[index] = 1
                elif word == 'us':
                    mentioned = [1 for _ in range(len(gentlemansList))]
            
            characterSetting = 1 if ('knight' in requirement) or ('knights' in requirement) else 0

            # 目前使用的参数包括requirement， mentioned， characterSetting
            # youNeed = [requirement, mentioned, slution, characterSetting]

            if requirement[0] == 'at':
                if requirement[1] == 'least':
                    judgeRes = self.atLeast(mentioned, slution, characterSetting)
                elif requirement[1] == 'most':
                    judgeRes = self.atMost(mentioned, slution, characterSetting)
            elif requirement[0] == 'exactly':
                judgeRes = self.onlyHave(1, mentioned, slution, characterSetting)
            elif requirement[0] == 'all':
                judgeRes = self.areAll(mentioned, slution, characterSetting)
            elif 'is' in requirement:
                judgeRes = self.onlyHave(1, mentioned, slution, characterSetting)
            else:
                judgeRes = self.areAll(mentioned, slution, characterSetting)
            
            judgeRes = judgeRes if selfStatus else not judgeRes
            res = judgeRes and res
        return res


    def atLeast(self, takePartIn, slution, direction):
        for i in range(len(slution)):
            if takePartIn[i] and slution[i] == direction:
                return True
        return False

    def atMost(self, takePartIn, slution, direction):
        res = 0
        for i in range(len(slution)):
            if takePartIn[i] and slution[i] == direction:
                res += 1
        return True if res <= 1 else False

    def onlyHave(self, num, takePartIn, slution, direction):
        res = 0
        for i in range(len(slution)):
            if takePartIn[i] and slution[i] == direction:
                res += 1
        return True if res == num else False

    def areAll(self, takePartIn, slution, direction):
        for i in range(len(slution)):
            if takePartIn[i] and slution[i] != direction:
                return False
        return True

if __name__ == "__main__":
    # input
    # filePath = 'zyl_test_12.txt'
    filePath = input("Which text file do you want to use for the puzzle? ")
    
    # To read and process the file
    fullContent = readTheFile(filePath)
    usefulContent = breakSentence(fullContent)

    # Find how many people in this game:
    gentlemansWord = statementParser(usefulContent)

    # list everyone then sort it
    # gentlemansList = list(gentlemansWord.keys())
    # gentlemansList.sort()
    
    for gentleman in gentlemansWord:
        gentlemansWord[gentleman] = gentlemanRequirement(gentleman, gentlemansWord[gentleman])

    slutions, mansList = findSlution(gentlemansWord)
    
    print(f'The Sirs are: {" ".join(mansList)}')
    if len(slutions) == 0:
        print('There is no solution.')
    elif len(slutions) > 1:
        print(f'There are {len(slutions)} solutions.')
    else:
        print('There is a unique solution:')
        onlySolution = slutions[0]
        for i, man in enumerate(mansList):
            print(f'Sir {man} is a {"Knight" if onlySolution[i] else "Knave"}.')