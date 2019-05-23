import htmlGen4
import htmlgentools4
Tags = htmlGen4.Tags




# def findLastDescendentOfParent2(htmlObjectList, thisTag):
#     numChildrenToFind = thisTag.parentObject.numChildrenElems
#     numChildrenFound = 0
#     parentIndex = htmlObjectList.index(thisTag.parentObject)
#     i = parentIndex + 1
#     while numChildrenFound < numChildrenToFind:
#         currentTag = htmlObjectList[i]
#         if currentTag.parentObject == thisTag.parentObject:
#             numChildrenFound += 1





def findLastChildOfParent(htmlObjectList, thisTag):
    # This "Walks down the DOM" Starting at the location of this Tag's Parent
    # It uses the Tab Level Property to verify whether an item is a child or not
    # More tabs, mean its a child as its tabbed more deeply to the side, signifying that its a child
    # The tab level is determined by the parentID property  so it shouldn't be wrong.
    # If the tab value is less or equal to the parent level,
    # then you know it's not a child so you'll break at that
    # point and retun the index
    parentIndex = htmlObjectList.index(thisTag.parentObject)
    parentTabLevel = thisTag.parentObject.tabLevel
    lastChildIndex = parentIndex + 1
    for i in range(parentIndex+1,len(htmlObjectList),1):
        currentTag = htmlObjectList[i]
        if currentTag.tabLevel > parentTabLevel:
            lastChildIndex = i
        elif currentTag.tabLevel <= parentTabLevel: # Some potential code that can cause problems, but I think it will work
            break
    return lastChildIndex


# def findLastDescendentOfParent(htmlObjectList, thisTag):
#     # This "Walks down the DOM" Starting at the location of this Tag's Parent
#     # It uses the Tab Level Property to verify whether an item is a child or not
#     # More tabs, mean its a child as its tabbed more deeply to the side, signifying that its a child
#     # The tab level is determined by the parentID property  so it shouldn't be wrong.
#     # If the tab value is less or equal to the parent level,
#     # then you know it's not a child so you'll break at that
#     # point and retun the index
#     parentIndex = htmlObjectList.index(thisTag.parentObject)
#     parentTabLevel = thisTag.parentObject.tabLevel
#     lastChildIndex = parentIndex + 1
#     for i in range(parentIndex+1,len(htmlObjectList),1):
#         currentTag = htmlObjectList[i]
#         if currentTag.tabLevel > parentTabLevel:
#             lastChildIndex = i
#         elif currentTag.tabLevel <= parentTabLevel: # Some potential code that can cause problems, but I think it will work
#             break
#     return lastChildIndex


def findLastDirectChildOfParent(htmlObjectList, thisTag):
    numChildrenToFind = thisTag.parentObject.numChildrenElems
    numChildrenFound = 0
    parentIndex = htmlObjectList.index(thisTag.parentObject)
    i = parentIndex + 1
    lastFoundIndex = 0
    while (numChildrenFound < numChildrenToFind) and (i < len(htmlObjectList)):
        currentTag = htmlObjectList[i]
        if currentTag.parentObject == thisTag.parentObject:
            numChildrenFound += 1
            lastFoundIndex = i
            # i += currentTag.numChildrenElems # Experimental search speedup function. If problems arise, disable this
            # if currentTag.numChildrenElems > 0:
            #     i = findLastDirectChildOfParent(htmlObjectList, currentTag) # Exp speedup #2
        i += 1
    if i >= len(htmlObjectList): # DEBUG
        print("Got to the end of the document before enough children were found")
    return htmlObjectList[lastFoundIndex] # Returns the last child found  or the last element in the document


def findLastDescendentOfParentNew(htmlObjectList, thisTag):
    # This "Walks down the DOM" Starting at the location of this Tag's Parent
    # It uses the Tab Level Property to verify whether an item is a child or not
    # More tabs, mean its a child as its tabbed more deeply to the side, signifying that its a child
    # The tab level is determined by the parentID property  so it shouldn't be wrong.
    # If the tab value is less or equal to the parent level,
    # then you know it's not a child so you'll break at that
    # point and retun the index
    lastDirectChildObject = findLastDirectChildOfParent(htmlObjectList, thisTag)
    parentIndex = htmlObjectList.index(lastDirectChildObject)
    parentTabLevel = lastDirectChildObject.parentObject.tabLevel
    lastDescIndex = parentIndex
    for i in range(parentIndex+1,len(htmlObjectList),1):
        currentTag = htmlObjectList[i]
        if currentTag.tabLevel > parentTabLevel:
            lastDescIndex = i
        elif currentTag.tabLevel <= parentTabLevel: # Some potential code that can cause problems, but I think it will work
            break
    return lastDescIndex


def find_parent():
    pass


def isValidTagObject(thisTag):
    isValid = False
    if type(thisTag) == htmlgentools4.Tag:
        return True
    return isValid


def verify_obj_in_list(htmlObjectList, objToFind):
    isInList = False
    if (objToFind in htmlObjectList):
        isInList = True
    return isInList


def verify_id_in_list(idToFind):
    isInList = False
    if (idToFind in Tags.tagIDList):
        isInList = True
    return isInList

    # if type(thisTag.parentObject) == htmlgentools4.Tag:
    #     name = thisTag.parentObject.name
    #     print (name)


def find_obj_by_id(htmlObjectList, idToFind):
    # Returns an Object from the html object list that has a specific tagID
    if debug:
        print('find_obj_by_id()')
    if (verify_id_in_list(idToFind)):
        for i in htmlObjectList:
            if i.tagID == idToFind:
                return i
    else:
        print("Couldn't find that id in the list")

def areSiblings(firstTag, secondTag):
    isSibling = False
    if (firstTag.parentID == secondTag.parentID):
        isSibling = True
    return isSibling


def findParentIndex (htmlObjectList, thisTag):
    return htmlObjectList.index(thisTag.parentObject)  # Make this into one function?


def find_insertion_point(htmlObjectList, thisTag):
    tagListLength = len(htmlObjectList)
    if thisTag.parentID == 'none':
        # Elements without a parent can be appended right away
        return tagListLength
    if (verify_obj_in_list(htmlObjectList, thisTag.parentObject)):
        # First make sure the parent is in the list
        if thisTag.parentObject.numChildrenElems == 0:
            # If this object's parent doesn't have children yet, just insert it directly after the parent
            return (findParentIndex(htmlObjectList, thisTag)) + 1
        else:
            return findLastDescendentOfParentNew(htmlObjectList, thisTag) + 1


def add_tag_obj_to_html_obj_list(htmlObjectList, thisTag):
    insertionPoint = find_insertion_point(htmlObjectList, thisTag)
    htmlObjectList.insert(insertionPoint, thisTag)

# In order TO add a tag obj to the obj list, we have to find where the object should be inserted at and insert it there.

# In order TO add a tag obj to the obj list, we have to check whether the list is empty or not. If so, append the item.
# If not, we have to find where the object should be inserted at and insert it there.

# TO find the insertion location you must first find the length of the list. If the list is empty, you can just return
# the value right away. If not, then you have find out if the last element in the list has the same parent element as
# the tag currently being processed.


def add_tag_obj_to_list(htmlObjectList, thisTag):
    # Adds a html.Tag Object, to the list given
    tagListLength = len(htmlObjectList)
    if tagListLength <= 1:
        # If this list is empty, you have to fill it with something
        if debug:
            print("List Empty or only has HTML tag, so appending this new tag")
        htmlObjectList.append(thisTag)
        return
    lastItemIndex = tagListLength-1
    lastItem = htmlObjectList[lastItemIndex]  # Declare the last item in the html list
    lastItemParent = find_obj_by_id(htmlObjectList, lastItem.parentID)  # Find the parent element of the last Item in the htmlList
    if lastItemParent.parentID == thisTag.parentID:
        if debug:
            print("Last item parent: %s has the same parentID(%s) as '%s'" % (lastItemParent.tagID, lastItemParent.parentID, thisTag.tagID))
        # If the parent element of the last item on the list, has the same nesting ID as this tag, append this
        # Item to the end of the html list
        insertionPoint = lastItemIndex
        insert_append_data(htmlObjectList, thisTag, insertionPoint, tagListLength)
        return
    for i in range(lastItemIndex, -1, -1):  # Loop backwards to find the last item that matches the criteria
        # print("Loop Backwards")
        currListObject = htmlObjectList[i]
        if currListObject.parentID == thisTag.parentID:  # If you found the location of the tag to be nested in...
            insertionPoint = findLastChildOfParent(htmlObjectList, thisTag)  # Store that location
            insert_append_data(htmlObjectList, thisTag, insertionPoint, tagListLength)  # Add it to the object list
            return
    # If you got here, then the item doesn't have another item it can nest next to, so that would mean this item
    # is the first item to be nested within that tag, so change the behavior:
    if debug:
        print("Fell Through")
    parent = find_obj_by_id(htmlObjectList, thisTag.parentID)
    # print("This %s tag is the first tag to be nested in the %s tag" %
    #       (thisTag.tagID, convert_parentID_to_name(htmlObjectList, thisTag.parentID)))
    if debug:
        print("This %s tag is the first tag to be nested in the %s tag" %(thisTag.tagID, parent.tagID))
    # TODO: Try to find a way to consolidate these two for loops in some kind of way. There's a lot of code repetition
    for i in range(lastItemIndex, -1, -1):
        currListObject = htmlObjectList[i]
        if currListObject.tagID == thisTag.parentID:  # Compare the tag ID's instead if its the first of its type
            insertionPoint = i
            insert_append_data(htmlObjectList, thisTag, insertionPoint, tagListLength)  # Add it to the object list
            return
