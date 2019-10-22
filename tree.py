import sys
# fileHandle = open('TestInputs/test4.txt') 
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
    descendents = people[subject]
    print(descendents)
    for kid in descendents:
        if(kid in people):
            descendents.extend(getDescendents(kid))
    return descendents
def getCousins(subject):
    # get cousings here
    print("here we get", subject, "'s cousins")
for line in fileHandle:
    command = line[0]
    contents = line.split()
    # print(people)
    #print(contents)
    if(command == "E"):
        # we're adding a couple or a child
        # print("add ->", line[1:])
        if(len(contents) == 4):
            # this is a couple
            if(contents[1] in people):
                # it exists, append
                people[contents[1]].append(contents[3])
            else: 
                people[contents[1]] = [contents[3]]
            if(contents[2] in people):
                # it exists, append
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
            # get parents
            siblings = []
            for parent, child in people.items():
                if(subject in child):
                    # print(parent)
                    # print(people[parent])
                    for potentialSibling in people[parent]:
                        if(potentialSibling != subject and potentialSibling not in siblings):
                            siblings.append(potentialSibling)
            print("the siblings are", ", ".join(siblings))
        if(key == "ancestor"):
            ancestors = getAncestors(subject)
            print("the ancestors are", ", ".join(ancestors))
        if(key == "descendent"):
            descendents = getDescendents(subject)
            print("the descendents are", ", ".join(descendents))
    if(command == "X"):
        # we're querying specifically
        print("specific query ->", line[1:])
        subject = contents[3]
        personInQuestion = contents[1]
        quality = contents[2]
        print("we're looking at ", subject, personInQuestion, "and their relationship as", quality)
        if(quality == "child"):
            if(personInQuestion in people.get(subject)):
                print(personInQuestion, "is a child of", subject)
            else:
                print(personInQuestion, "is NOT child of", subject)
fileHandle.close()