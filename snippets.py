import htmlGen4
import shelve
import os
import pprint
import copy

globalOpenDBList = []
quitCode = 'q'
ynChoiceList = ['y', 'n', '', quitCode]
previousFunction = -1
existingDecks = []
dbPrefix = 'pokemonDB'
exportPath = 'K:\\Users\\Reggie\\Desktop\\Pokemon HTML\\deckmaker\\'
htmlExportPath = 'K:\\Users\\Reggie\\Desktop\\Pokemon HTML\\'
os.chdir(exportPath)
debug = False

# TODO: Add a main menu that allows you to pick between exporting HTML for a deck or HTML for index.html
# TODO: Refactor most of the original pokemon code to be more modular (Turn Deck DB functions into generic DB ones)
# TODO: Remove pokemon specific naming conventions for most things. Ex: 'pokemonDBList' -> 'DBList'
# TODO: Export the HTML files instead of pasting them into the clipboard. Or give an option to do either.

def outputHTML(pokemonDBList, deckSize, deckFileName):
    listLength = len(pokemonDBList)
    if listLength == 0:
        print("No entries in this database. Try another")
        listDBEntries()
    else:
        print("%d Entries in this database." %listLength)
        htmlGen4.debug = False
        htmlGen4.verbose = False
        htmlList = htmlGen4.new_html_document()
        tag = htmlGen4.create_html_object
        tag(htmlList, 'meta','head',[{'charset': 'utf-8'}])
        tag(htmlList, 'link', 'head',[{'rel':'stylesheet'}, {'type':'text/css'}, {'href':'normalize.css'}])
        tag(htmlList, 'link', 'head',[{'rel':'stylesheet'}, {'type':'text/css'}, {'href':'main.css'}])
        tag(htmlList, 'title','head',[],('%s' % pokemonDBList[0]['deckName']))
        tag(htmlList, 'p','body',[{'id':'message'}], 'Shit')
        tag(htmlList, 'a', 'body', [{'href':'index.html'}])
        tag(htmlList, 'h1', 'a', [], 'Pokemon Catalog')
        tag(htmlList, 'h2', 'body', [], '%s Deck' % (pokemonDBList[0]['deckName']))
        tag(htmlList, 'img', 'h2', [{'src':'img/icons/icon_%s.png' % (deckFileName)}])
        tag(htmlList, 'div', 'body',[{'id':'wrapper'}])
        tag(htmlList, 'section', 'div')
        tag(htmlList, 'ul', 'section', [{'id':'gallery'}])
        updateMessage = '<span class="needupdate">NEEDS TO BE UPDATED </span>'
        for i in range(0, len(pokemonDBList)):
            needsUpdate = False
            card = pokemonDBList[i]
            hundreds = ''
            tens = ''
            if card['num'] >= 10 and card['num']<100:
                hundreds = '0'
            elif card['num']<10:
                tens = '0'
                hundreds = '0'
            imgSrc = "img/%s/%s%s%d.png" % (deckFileName, hundreds, tens, card['num'])

            contentListValues = [card['name'], card['rarity'].title(), '1', '1', ('%s/%s' % (str(card['num']), str(deckSize))),
                                 str(card['minPrice']),
                                 str(card['maxPrice']), str((card['minPrice'] + card['maxPrice']) / 2), '1']
            contentList = ['Name:', 'Rarity:', 'Count:', 'Holos:', 'Card Num:', 'Min Price:', 'Max Price:', 'Avg. Price:',
                           'Num Sold:']
            if card['name'] == '':  # If the name is an empty string
                contentListValues[0] = updateMessage
                needsUpdate = True
            tag(htmlList, 'li', 'ul', [{'class': 'pkmncard'}])
            tag(htmlList, 'div', 'li', [{'class': 'imagecontainer'}])
            tag(htmlList, 'img', 'div', [{'class': 'pkmncard'}, {'src': imgSrc}])
            tag(htmlList, 'table', 'li', [{'class': 'pokedata'}])
            tag(htmlList, 'tbody', 'table')
            for i in range(0, len(contentList)):
                tag(htmlList, 'tr', 'tbody')
                tag(htmlList, 'th', 'tr', [{'scope': 'row'}], contentList[i])
                if needsUpdate == True:
                    if contentList[i] ==  'Card Num:':
                        tag(htmlList, 'td', 'tr', [{'class': 'needupdate'}], contentListValues[i])
                        continue
                if contentList[i] == 'Rarity:':
                    if contentListValues[i].lower() == 'common':
                        tag(htmlList, 'td', 'tr', [{'class': 'common'}], contentListValues[i])
                    elif contentListValues[i].lower() == 'uncommon':
                        tag(htmlList, 'td', 'tr', [{'class': 'uncommon'}], contentListValues[i])
                    else:
                        tag(htmlList, 'td', 'tr', [{'class': 'rare'}], contentListValues[i])
                    continue
                tag(htmlList, 'td', 'tr', [], contentListValues[i])

        # htmlGen4.create_table(htmlList, 2,'li',[{'class':'pokedata'}])
        htmlDocument = htmlGen4.parseHtmlDocumentList(htmlList)
        outputHTMLDocument(htmlDocument, deckFileName)


def outputHTMLDocument(htmlDocument, fileName):
    htmlDoc = open('%s%s.html' %(htmlExportPath, fileName), 'w')
    numBytes = htmlDoc.write(htmlDocument) # Just to stifle the return
    print('Created HTML Document at %s%s.html' %(htmlExportPath, fileName))
    htmlDoc.close()

def quitProgram():
    print('Thank you for using Pokemon Deck Maker!')
    quit()


def testValidChoice(choiceList, userChoice):
    userChoice = userChoice.lower()
    choiceList.append(quitCode)
    if userChoice in choiceList:
        # print('That choice is valid!')
        if (userChoice == quitCode):
            # Quit is handled here, instead of locally.
            quitProgram()
        else:
            # Return True if the choice is VALID. The calling program
            # handles the specfics of what a valid choice means.
            return True
    else:
        # Returns False if the value is not in the list of valid entries
        print("That's not a valid choice. Try again \n")
        return False


def displayOpenDatabases(databaseIdentifier=''):
    # The databaseIdentifier should be the string value of a element in that database's dictionary that
    # can be used to identify which databse is which. A filename is good.
    global globalOpenDBList
    print("\nCurrently Open Databases: ")
    for i in globalOpenDBList:
        if databaseIdentifier == '':
            print(i)


def removeDatabaseFromGlobalList(thisDatabase):
    # Removes a database from the global list of open databases
    global globalOpenDBList
    if thisDatabase in globalOpenDBList:
        while thisDatabase in globalOpenDBList:
            # In any weird instances that this database was added to the globalList multiple times
            globalOpenDBList.remove(thisDatabase)
    if debug:
        displayOpenDatabases()

def addDatabaseToGlobalList(thisDatabase):
    # Adds a database to the Global List of Open Databases
    global globalOpenDBList
    alreadyOpen = False
    if thisDatabase not in globalOpenDBList:
        globalOpenDBList.append(thisDatabase)
    else:
        print("You attempted to open a database that is already open.")
        alreadyOpen = True
    if debug:
        displayOpenDatabases()
    if alreadyOpen:
        return True
    else:
        return


def closeOpenDB(thisDatabase):
    # Closes an open database
    if debug:
        print("\nAttempting to Close a Database...")
    removeDatabaseFromGlobalList(thisDatabase)
    thisDatabase.close()
    if debug:
        print("\nClosing a Database. Saving Data...")
        print("Database closed successfully!")
        print("Data Saved")
    return


def openDBForUse(dbFileName):
    if debug:
        print("\nAttempting to Open A Database") #TODO: Add try/except in case the database doesnt exist
    # checkFileExists(dbFileName) #TODO Create a function that checks if the file exists too?
    thisDatabase = shelve.open(dbFileName)
    if debug:
        print("Database opened successfully!")
    addDatabaseToGlobalList(thisDatabase)
    if debug:
        print("Database Added To The Database Tracker")
    return thisDatabase


def displayDBContent(db, returnChoiceList = False, prompt='Currently Stored Information:'):
    # Prints the list of keys within a DB, and stores the list of keys as choices and returns the choices.
    # This choiceList can be useful for other functions, but its not necessary to use the choice list. giving the
    # program flexibility
    dbKeyList = list(db.keys())  # store list of db dict key names
    choiceList = []
    print(prompt)
    for i in range(0, len(db)):
        print('%s. ' % (i + 1) + dbKeyList[i])  # Formatting string
        choiceList.append(str(i + 1))  # Append the potential choices in this list
    if returnChoiceList:
        return choiceList
    else:
        return

def updateIndexHTML(allData):
    # 'allData' Dictionary Entries: 'deckName', 'deckFileName', 'deckSize'
    tag = htmlGen4.create_html_object
    indexHTML = htmlGen4.new_html_document()
    tag(indexHTML,'title', 'head',[], 'Pokemon Catalog')
    tag(indexHTML, 'link', 'head', [{'rel': 'stylesheet'}, {'type': 'text/css'}, {'href': 'normalize.css'}])
    tag(indexHTML, 'link', 'head', [{'rel': 'stylesheet'}, {'type': 'text/css'}, {'href': 'style.css'}])
    tag(indexHTML, 'h1', 'body', [], 'Pokemon Catalog')
    tag(indexHTML, 'nav', 'body')
    tag(indexHTML, 'ul', 'nav')
    for i in allData:
        tag(indexHTML, 'li', 'ul')
        tag(indexHTML, 'a', 'li', [{'href':'%s.html'% (i['deckFileName'])}], i['deckName'])
        tag(indexHTML, 'img','a', [{'class': 'icon'}, {'src':'img/icons/icon_%s.png'% (i['deckFileName'])}])
    htmlGen4.parseHtmlDocumentList(indexHTML)



def listDeckEntries(decksDB):
    decksDBKeys = list(decksDB.keys())
    allData = []
    for i in decksDBKeys:
        deck = decksDB[i]
        allData.append(deck)
    updateIndexHTML(allData)
    # 'allData' Dictionary Entries: 'deckName', 'deckFileName', 'deckSize'


def listEntries(deckFileName, deckKey, deckSize):
    deckDB = openDBForUse('pokemonDB_%s' % (deckFileName))
    deckDBKeys = list(deckDB.keys())
    pokemonCard = {}
    filledData = []
    allData = []
    emptyData = []
    filledNames = []
    for i in deckDBKeys:
    #   print(i)
        pokemonCard = deckDB[i]
        # print(pokemonCard)
        values = list(pokemonCard.values())
        allData.append(pokemonCard)
        astring = ''
        # print(pokemonCard['rarity'].title())
        if '' in values:
            pass
            # emptyData.append(i)
        else:
            filledData.append(pokemonCard)
            # filledNames.append('%s. %s' % (i, deckDB[i]['name']))
    # print("'%s' Stored Card List:" % (pokemonCard['deckName']))
    # pprint.pprint('Empty Entries: ' + str(emptyData))
    # print()
    # print('Filled Entries:')
    # pprint.pprint('Names: ' + str(filledNames))
    # pprint.pprint(filledData)
    # print()
    closeOpenDB(deckDB)
    # deckDB.close()
    # print(filledData)
    # outputHTML(filledData, deckSize, deckFileName)
    outputHTML(allData, deckSize, deckFileName)


def convertChoiceToDeckKey(decks, prompt="\nWhich deck would you like to see data for? "):
    choiceList = displayDBContent(decks, True, '')
    deckList = list(decks.keys())  # store list of dict deck key names
    prompt += "\nYou can input a value from %s - %s or type 'Q' to quit.\n" % (choiceList[0], choiceList[len(choiceList)-1])
    userChoice = (input(prompt)).lower()  # Store user input
    if testValidChoice(choiceList, userChoice) is True:  # Pass the valid
        # choices and the user input to see if the user inserted a
        # valid choice
        choice = choiceList.index(userChoice.lower())  # if the input was
        #  valid, store the index for the user inputsted valid value in choice
        deckKey = str(deckList[choice])  # match up the index choice given to the decklist index
        # chosenDeck = decks[deckKey]  # store the dictionary for chosen deck
        return deckKey
    else:
        closeOpenDB(decks)
        listDBEntries()


def listDBEntries():
    # TODO If there are no decks, call createDeck()
    print('\nPick a Deck!')
    decks = openDBForUse('pokemonDB_decknames')
    # listDeckEntries(decks) # THIS IS USED UPDATE DECKS AND INDEX.HTML, Don't use this unless you need to do that
    # TODO: Add a menu option that allows you to pick this ^-- and create index HTML
    deckKey = convertChoiceToDeckKey(decks)
    chosenDeck = decks[deckKey] #  'chosenDeck' Dictionary Attributes: ['deckName'], ['deckFileName'], ['deckSize']
    deckFileName = chosenDeck['deckFileName']  # store deck file name
    deckSize = chosenDeck['deckSize']
    listEntries(deckFileName, deckKey, deckSize)
    closeOpenDB(decks)
    # listDBEntries()

listDBEntries()