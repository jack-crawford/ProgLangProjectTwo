import sys
import math

fileHandle = open(input("Please enter a file name in quotes: "))
people = {}

def getAncestors(subject):
    ancestors = []
    for parent, child in people.items():
        if (subject in child):
            ancestors.append(parent)
    if (len(ancestors) > 0):
        for ancestor in ancestors:
            ancestors.extend(getAncestors(ancestor))
    noDuplicates = [] 
    for i in ancestors: 
        if i not in noDuplicates: 
            noDuplicates.append(i)
    return noDuplicates


def getDescendents(subject):
    if (subject not in people):
        return subject
    descendents = people[subject]
    for kid in descendents:
        if (kid in people):
            descendents.extend(getDescendents(kid))
    return descendents

def areCousins(person1, person2):
    if person1 == person2:
        return False
    for anc in getAncestors(person1):
        if anc in getAncestors(person2):
            return True
    return False

def areCousinsDegree(person1, person2, degree):
    if person1 == person2:
        return False
    gencount1 = 0
    gencount2 = 0
    commonAnc = []
    for anc in getAncestors(person1):
        if anc in getAncestors(person2):
            commonAnc.append(anc)
    for i in getAncestors(person1):
        gencount1 += 1
        if i in commonAnc:
            break
    for i in getAncestors(person2):
        gencount2 += 1
        if i in commonAnc:
            break

    gencount1 = math.ceil(gencount1 / 2)
    gencount2 = math.ceil(gencount2 / 2)
    gencount1 -= 1
    gencount2 -= 1
    minCount = min(gencount1, gencount2)
    if int(minCount) == int(degree):
        return True

def isUnrelated(person1, person2):
    ancestors = getAncestors(person2)
    descendents = getDescendents(person2)
    cousins = getCousins(person2)
    if (person1 == person2):
        return False
    if (person1 in ancestors):
        return False
    if (person1 in descendents):
        return False
    if person1 in cousins:
        return False
    siblings = []
    for parent, child in people.items():
        if (person2 in child):
            for potentialSibling in people[parent]:
                if (potentialSibling != person2 and potentialSibling not in siblings):
                    siblings.append(potentialSibling)
    if (person1 in siblings):
        return False
    else:
        return True

def getUnrelated(subject):
    outp = []
    for person in people:
        if isUnrelated(person, subject):
            outp.append(person)
    return outp

def getCousins(subject):
    outp = []
    for cousin in people:
        if areCousins(subject,cousin):
            outp.append(cousin)
    return outp

def getCousinsDegree(subject, degree):
    outp = []
    for cousin in people:
        if areCousinsDegree(subject,cousin,degree):
            outp.append(cousin)
    return outp


for line in fileHandle:
    command = line[0]
    contents = line.split()
    if (command == "E"):
        if (len(contents) == 4):
            if (contents[1] in people):
                people[contents[1]].append(contents[3])
            else:
                people[contents[1]] = [contents[3]]
            if (contents[2] in people):
                people[contents[2]].append(contents[3])
            else:
                people[contents[2]] = [contents[3]]
    if (command == "W"):
        print(line[0:])
        if len(contents) == 3:
            key = contents[1]
            subject = contents[2]
            if (key == "child"):
                print(people.get(subject))
            if (key == "sibling"):
                siblings = []
                for parent, child in people.items():
                    if (subject in child):
                        for potentialSibling in people[parent]:
                            if (potentialSibling != subject and potentialSibling not in siblings):
                                siblings.append(potentialSibling)
                print("\n".join(siblings))
            if (key == "ancestor"):
                ancestors = getAncestors(subject)
                print("\n".join(ancestors))
            if (key == "descendent"):
                descendents = getDescendents(subject)
                print("\n".join(descendents))
            if (key == "cousin"):
                cousins = getCousins(subject)
                print("\n".join(cousins))
            if (key == "unrelated"):
                unrelated = getUnrelated(subject)
                print("\n".join(unrelated))
        if len(contents) == 4:
            key = contents[1]
            if (key == "cousin"):
                subject = contents[3]
                degree = contents[2]
                cousins = getCousinsDegree(subject,degree)
                print("\n".join(cousins))
    if (command == "X"):
        print(line[0:])
        if len(contents) == 4:
            subject = contents[3]
            personInQuestion = contents[1]
            relation = contents[2]
            # print("we're looking at ", subject, personInQuestion, "and their relationship as", relation)
            if (relation == "child"):
                if (personInQuestion in people.get(subject)):
                    print("Yes")
                else:
                    print("No")
            if (relation == "ancestor"):
                ancestors = getAncestors(subject)
                if (personInQuestion in ancestors):
                    print("Yes")
                else:
                    print("No")
            if (relation == "descendent"):
                descendents = getDescendents(subject)
                if (personInQuestion in descendents):
                    print("Yes")
                else:
                    print("No")
            if (relation == "sibling"):
                siblings = []
                for parent, child in people.items():
                    if (subject in child):
                        for potentialSibling in people[parent]:
                            if (potentialSibling != subject and potentialSibling not in siblings):
                                siblings.append(potentialSibling)
                if (personInQuestion in siblings):
                    print("Yes")
                else:
                    print("No")
            if (relation == "unrelated"):
                if isUnrelated(personInQuestion,subject):
                    print("Yes")
                else:
                    print("No")
            if relation == "cousin":
                if areCousins(personInQuestion, subject):
                    print("Yes")
                else:
                    print("No")
        if len(contents) == 5:
            relation = contents[2]
            if (relation == "cousin"):
                degree = contents[3]
                subject = contents[4]
                personInQuestion = contents[1]
                if areCousinsDegree(personInQuestion, subject, degree):
                    print("Yes")
                else:
                    print("No")

fileHandle.close()