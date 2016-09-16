"""
Author: Ashwin
        Krutarth
This file is the heart of the system. It is the codified version of the MS-Apriori Algorithm.
Happy Programming
"""


# Sort the Data set according to MIS value
def getSortedItemList(origDataSet, MISdict):
    itemset = set()
    # For every itemList in data set, sort the list as per MIS value
    for itemList in origDataSet:
        for item in itemList:
            if item not in itemset:
                itemset.add(item)

    itemListTup = []

    # create tuples of (item, MIS value)
    for item in itemset:
        tup = (item, MISdict[item])
        itemListTup.append(tup)

    sortedItemList = []
    # Sort the tuple on second argument i.e. MISvalue
    for tup in sorted(sorted(itemListTup, key=lambda x: x[0]), key=lambda x: x[1]):
        sortedItemList.append(tup[0])

    return sortedItemList


# This functions reads and returns the support count for each item in data set
def getSupportCount(origDataSet, supportCountdict):
    for itemList in origDataSet:
        for item in itemList:
            if item not in supportCountdict.keys():
                supportCountdict[item] = 1
            else:
                supportCountdict[item] += 1


# Initial pass function.
# 1. It first scans the data once to record the support count of each item.
# 2. It then follows the sorted order to find the first item i in M that meets
# MIS(i). i is inserted into L. For each subsequent item j in M after i, if
# j.count/n >= MIS(i), then j is also inserted into L, where j.count is the
# support count of j, and n is the total number of transactions in T.
def InitPass(origDataSet, sortedItemList, MISdict, supportCountdict):
    # Get support counts of the items
    getSupportCount(origDataSet, supportCountdict)

    L_list = []
    firstItem = 0
    for item in sortedItemList:
        if len(L_list) < 1 and (supportCountdict[item] / len(origDataSet)) >= float(MISdict[item]):
            L_list.append(item)
            firstItem = item
        elif firstItem != 0 and (supportCountdict[item] / len(origDataSet)) >= float(MISdict[firstItem]):
            L_list.append(item)

    return L_list


# The function computes the frequent single element item set.
def calculateF1(L_List, MISdict, supportCountdict, datasetsize):
    F1_list = []

    for item in L_List:
        if (supportCountdict[item] / datasetsize) >= float(MISdict[item]):
            F1_list.append(item)

    return F1_list


# This function generates the candidate set for level 2
def generateCandidateForLevel2(L_List,
                               MISdict,
                               supportCountdict,
                               mustHaveElements,
                               cannotBeTogetherItemList,
                               sdcvalue,
                               datasetsize):
    C2_List = []

    for i in range(0, len(L_List)):
        sup_l = supportCountdict[L_List[i]] / datasetsize

        if sup_l >= float(MISdict[L_List[i]]):
            for j in range(i + 1, len(L_List)):
                sup_h = supportCountdict[L_List[j]] / datasetsize

                if sup_h >= float(MISdict[L_List[i]]) \
                        and (abs(sup_h - sup_l) <= float(sdcvalue)):
                    listitem = [[L_List[i], L_List[j]], 0, 0]
                    # C2_List.append(listitem)

                    # Insert the item set after checking cannot be together condition
                    if checkCannotBeTogetherElements(listitem[0], cannotBeTogetherItemList):
                        C2_List.append(listitem)

    return C2_List


# Given an itemlist and candidate list,
# it check whether candidate list is subset of itemlist
def isSubSetOf(itemlist, candidate):
    for candidateElement in candidate:
        isFound = False
        for item in itemlist:
            if candidateElement == item:
                isFound = True
                break
        # If element not found in itemset, return false
        if isFound == False:
            return False

    return True


# This function checks if the itemlist contains the given number
def itemListContainsNumber(itemlist, itemNumber):
    isFound = False
    for item in itemlist:
        if itemNumber == item:
            isFound = True
            break

    return isFound


# If the item list contains subset, return true else return false
def isContained(itemList, subset):
    for item in itemList:
        if item[0] == subset:
            return True

    return False


# Find all subsets of (k-1) length
def getSubsets(origitemList):
    subSetList = []
    itemList = origitemList.copy()

    for i in range(len(itemList) - 1, -1, -1):
        temp = itemList[i]
        itemList.remove(temp)
        subSetList.append(itemList.copy())
        itemList.insert(i, temp)

    return subSetList


# This functions whether the itemList has at least one element from must have list
def checkMustHaveElement(itemList, mustHaveElements):
    for item in itemList:
        if item in mustHaveElements:
            return True

    return False


# This function check whether the itemList contains 2 or more elements from
# cannot be together list. If yes, return False, else return True
def checkCannotBeTogetherElements(itemList, cannotBeTogetherItemList):
    for list in cannotBeTogetherItemList:
        intersection_list = set(list).intersection(itemList)
        if len(intersection_list) >= 2:
            return False

    return True


# Candidate generation function for all itemset of size greater than 2
def generateCandidateList(prevFreqtemList,
                          MISdict,
                          supportCountdict,
                          mustHaveElements,
                          cannotBeTogetherItemList,
                          sdcvalue,
                          datasetsize):
    candidateList = []
    newItemList = []
    for i in range(0, len(prevFreqtemList)):

        itemList1 = prevFreqtemList[i][0].copy()

        for j in range(i + 1, len(prevFreqtemList)):
            itemList2 = prevFreqtemList[j][0].copy()

            if itemList1[0:-1] == itemList2[0:-1] \
                    and MISdict[itemList1[-1]] <= MISdict[itemList2[-1]] \
                    and abs((supportCountdict[itemList1[-1]] / datasetsize) - (
                                supportCountdict[itemList2[-1]] / datasetsize)) < float(sdcvalue):

                # Merge two item list to generate new item list having k+1 element
                newItemList.clear()
                newItemList = itemList1.copy()
                newItemList.append(itemList2[-1])

                insertItem = True

                # Prune step
                subsetsOfNewItemList = getSubsets(newItemList)

                for subset in subsetsOfNewItemList:

                    # if (c[1] belongs to s) or (MIS(c[2]) = MIS(c[1])) then
                    # i.e. if the subset contains first element of the new item set or
                    # the MIS values of first and second elements are same
                    if (itemListContainsNumber(subset, newItemList[0])) \
                            or (float(MISdict[newItemList[1]]) == float(MISdict[newItemList[0]])):

                        # if (s does not belong to Fk-1) then delete c from Ck
                        # i.e. if prevFreqtemListdoes not contain the subset,
                        # then set insertItem to False
                        if not isContained(prevFreqtemList, subset):
                            insertItem = False
                            break

                # Check if the Must have element is present in item list,
                # If present, insert the item list to candidate list
                #
                # Check if itemList contains 2 or more elements from cannot be together list,
                # If yes, do not insert
                # If No, then insert the new itemList to candidate List

                # if insertItem \
                #         and checkMustHaveElement(newItemList, mustHaveElements) \
                #         and checkCannotBeTogetherElements(newItemList, cannotBeTogetherItemList) \
                #         and len(newItemList) >= 1:
                if insertItem \
                        and checkCannotBeTogetherElements(newItemList, cannotBeTogetherItemList) \
                        and len(newItemList) >= 1:
                    # Insert new item list to candidateList
                    candidateList.append([newItemList.copy(), 0, 0])

    return candidateList


# Generate FrequentList according to must have
def generateMustHaveFrequentList(frequentItemList, mustHaveItemList):
    finalFrequentItemList = []
    finalFrequentset = []

    for frequentset in frequentItemList:

        finalFrequentset.clear()
        for itemset in frequentset:

            if checkMustHaveElement(itemset[0], mustHaveItemList):
                finalFrequentset.append(itemset.copy())

        finalFrequentItemList.append(finalFrequentset.copy())

    return finalFrequentItemList


# Print output in format
def print_output(frequentItemList):
    print("OUTPUT:\n")
    counter = 0
    for frequentset in frequentItemList:

        # Skip frequent set of zero length
        if counter == 0:
            counter += 1
            continue

        print("Frequent " + str(counter) + "-itemsets: \n")
        for itemset in frequentset:
            print("\t" + str(itemset[1]) + " : {" + ','.join(map(str, itemset[0])) + "}")
            # Print Tail count
            if counter > 1:
                print("Tailcount = " + str(itemset[2]))

        print("\tTotal number of freuqent " + str(counter) + "-itemsets = " + str(len(frequentset)) + "\n")

        counter += 1
        # End of Print function


# MS-Apriori algorithm implementation
def MSAprioriAlgo(origDataSet,
                  MISdict,
                  sdcvalue,
                  cannotBeTogetherItemList,
                  mustHaveItemList):
    # Sort the original Data Set
    sortedItemList = getSortedItemList(origDataSet, MISdict)
    # print(sortedItemList )

    # Init pass
    supportCountdict = {}
    L_List = InitPass(origDataSet,
                      sortedItemList,
                      MISdict,
                      supportCountdict)
    # print(supportCountdict)
    # print("L List: " + str(L_List))

    # Calculate F1 list
    F1_List = calculateF1(L_List,
                          MISdict,
                          supportCountdict,
                          len(origDataSet))
    # print("F1 List: " + str(F1_List))

    frequentItemList = []

    # Frequent item of zero size is null,
    # We will just append an empty list to frequestItemList
    frequentItemList.append(list())

    # Then we will insert the frequent Item list of 1 element
    singleFreqItems = []
    for item in F1_List:
        singleFreqItems.append([[item], supportCountdict[item], 0])
    frequentItemList.append(singleFreqItems.copy())

    prevFreqItemList = frequentItemList.copy()
    tailList = []

    itemSetCounter = 2
    while (len(prevFreqItemList) >= 1):

        candidateList = []
        candidateList.clear()

        if itemSetCounter == 2:
            # Generate candidate set for level 2
            candidateList = generateCandidateForLevel2(L_List,
                                                       MISdict,
                                                       supportCountdict,
                                                       mustHaveItemList,
                                                       cannotBeTogetherItemList,
                                                       sdcvalue,
                                                       len(origDataSet))
            # print("C2 List  " + str(candidateList))
        else:
            candidateList.clear()
            # Generate candidate set
            candidateList = generateCandidateList(prevFreqItemList,
                                                  MISdict,
                                                  supportCountdict,
                                                  mustHaveItemList,
                                                  cannotBeTogetherItemList,
                                                  sdcvalue,
                                                  len(origDataSet))

        for itemlist in origDataSet:
            for candidate in candidateList:
                if len(candidate[0]) >= 1 and isSubSetOf(itemlist, candidate[0]):
                    candidate[1] += 1

                # Line 13-14 of algorithm. which is used for rule generation by calculating tail count
                tailList.clear()
                tailList = candidate[0][1:].copy()
                if tailList and isSubSetOf(itemlist, tailList):
                    candidate[2] += 1

        # Compute Frequent Item set
        prevFreqItemList.clear()

        for candidate in candidateList:

            if len(candidate[0]) >= 1 \
                    and (candidate[1] / len(origDataSet)) >= float(MISdict[candidate[0][0]]):
                prevFreqItemList.append(candidate)

        if len(prevFreqItemList) >= 1:
            frequentItemList.append(prevFreqItemList.copy())
        itemSetCounter += 1

    # for line in frequentItemList:
    #     print(line)

    # Print output
    print_output(generateMustHaveFrequentList(frequentItemList, mustHaveItemList))
