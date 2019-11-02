import sys
fileHandle = open('myFile.txt') 
people = {} 
def getAncestors(subject):
    ancestors = []
    for parent, child in people.items():
        if(subject in child):
            ancestors.append(parent)
    if(len(ancestors) > 0):
        for ancestor in ancestors:
            ancestors.extend(getAncestors(ancestor))
    return ancestors
def getDescendents(subject):
    if(subject not in people):
        return subject
    descendents = people[subject]
    # print(descendents)
    for kid in descendents:
        if(kid in people):
            descendents.extend(getDescendents(kid))
    return descendents
def getAllCousins(subject):
    print("here we get", subject, "'s cousins")
    ancs = getAncestors(subject)
    decs = getDescendents(subject)
    directLine = []
    directLine.extend(ancs)
    directLine.extend(decs)

    potentialCousins = []
    for cuz in directLine:
        potentialCousins.extend(getDescendents(cuz))
    cousins = []
    for cuz in potentialCousins:
        if cuz not in ancs and cuz not in decs and cuz not in cousins:
            cousins.append(cuz)
    return cousins
def getCousinDegree(subject, potentialCousin):
    subjectAncs = getAncestors(subject)
    potentialAncs = getAncestors(potentialCousin)
    subjectCt = potCt = 0
    commonLink = False
    subjectDegree = potentialDegree = 0
    while not commonLink and subjectCt < len(subjectAncs):
        while potCt < len(potentialAncs):
            if(subjectAnc(subjectCt) is potentialAnc(potCt)):
                # this is their closest common ancestor!
                subjectDegree = subjectCt
                potentialDegree = potCt
                commonLink = True
                break
            potCt += 1
        subjectCt += 1
    cousinDegree = 0
    if subjectCt == potCt:
        cousinDegree = subjectCt/2
    elif subjectCt > potCt:
        cousinDegree = potCt/2
    else:
        cousinDegree = subjectCt/2
for line in fileHandle:
    command = line[0]
    contents = line.split()
    if(command == "E"):
        if(len(contents) == 4):
            if(contents[1] in people):
                people[contents[1]].append(contents[3])
            else: 
                people[contents[1]] = [contents[3]]
            if(contents[2] in people):
                people[contents[2]].append(contents[3])
            else: 
                people[contents[2]] = [contents[3]]
    if(command == "W"):
        #child, sibling, ancestor, cousin, descendent, unrelated
        print("broad query ->", line[1:])
        key = contents[1]
        subject = contents[2]
        if(key == "child"):
            print(people.get(subject))
        if(key == "sibling"):
            siblings = []
            for parent, child in people.items():
                if(subject in child):
                    for potentialSibling in people[parent]:
                        if(potentialSibling != subject and potentialSibling not in siblings):
                            siblings.append(potentialSibling)
            print(subject, "-> siblings ->", ", ".join(siblings))
        if(key == "ancestor"):
            ancestors = getAncestors(subject)
            print(subject, "-> ancestors ->", ", ".join(ancestors))
        if(key == "descendent"):
            descendents = getDescendents(subject)
            print(subject, "-> descendents ->", ", ".join(descendents))
        if(key == "cousin"):
            cousins = getAllCousins(subject)
            print(subject, "-> cousins -> ", ", ".join(cousins))
    if(command == "X"):
        subject = contents[3]
        personInQuestion = contents[1]
        quality = contents[2]
        print("we're looking at ", subject, personInQuestion, "and their relationship as", quality)
        if(quality == "child"):
            if(personInQuestion in people.get(subject)):
                print(personInQuestion, "is a child of", subject)
            else:
                print(personInQuestion, "is NOT a child of", subject)
        if(quality == "ancestor"):
            ancestors = getAncestors(subject)
            if(personInQuestion in ancestors):
                print(personInQuestion, "is an ancestor of", subject)
            else:
                print(personInQuestion, "is NOT an ancestor of", subject)  
        if(quality == "descendent"):
            descendents = getDescendents(subject)
            if(personInQuestion in descendents):
                print(personInQuestion, "is a descendent of", subject)
            else:
                print(personInQuestion, "is NOT a descendent of", subject)  
        if(quality == "cousins"):
            print("TRYIN COUSINS")
            degree = contents[3]
            degreeFound = getCousinDegree(subject, personInQuestion)
            print(degreeFound)
        if(quality == "sibling"):
            siblings = []
            for parent, child in people.items():
                if(subject in child):
                    for potentialSibling in people[parent]:
                        if(potentialSibling != subject and potentialSibling not in siblings):
                            siblings.append(potentialSibling)
            if(personInQuestion in siblings):
                print(personInQuestion, "is a sibling of", subject)
            else:
                print(personInQuestion, "is NOT a sibling of", subject)  
fileHandle.close()