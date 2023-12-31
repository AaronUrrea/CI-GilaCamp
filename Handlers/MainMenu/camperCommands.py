from Handlers.dataHandler import summerCamp

from Handlers.uiHandler import *

def signUpCamper():
    if not any(elem == "" for elem in summerCamp.getAllCampers()):
        mainMenu()
        showMessage("There are no more slots available!", bottomBracket=True)
        return

    newCamper = Camper()

    clearScreen()
    name = showPrompt("Please insert camper name:", prompt= "(First + Last)", topBracket=True, bottomBracket=True)

    if summerCamp.searchCamper(name) != STATUS_CODES["NO_CAMPER"]:
        mainMenu()
        showMessage("That camper already exists!", bottomBracket=True)
        return

    newCamper.name = name

    while True:
        clearScreen()
        try:
            newCamper.age = int(showPrompt("Please insert camper age:", prompt="(9 - 18)", topBracket=True, bottomBracket=True))
        except ValueError:
            showMessage("Invalid input!", bottomBracket=True, wait=2)
            continue

        if 9 <= int(newCamper.age) <= 18:
            break
        else:
            showMessage("Applicant must be between 9 and 18 years old.", bottomBracket=True, wait=2)

    while True:
        clearScreen()
        newCamper.gender = showPrompt('Please insert camper gender:', prompt='"M" or "F"', bottomBracket=True, topBracket=True).upper()
        if newCamper.gender == 'F' or newCamper.gender == 'M':
            break
        else:
            showMessage('Applicant must be between "M" or "F"', bottomBracket=True, wait=2)

    clearScreen()
    newCamper.address = showPrompt("Please insert camper home address:", topBracket=True, bottomBracket=True)

    while True:
        clearScreen()

        printCamperUI(newCamper, camperCreation= True, topBracket=True, bottomBracket=True)
        confirmation = showPrompt("Is this information correct?", prompt= '"Y" for Yes, "N" for No', bottomBracket=True)

        if confirmation == 'Y':
            summerCamp.insertCamper(newCamper)
            summerCamp.sortList(parameter="name")

            mainMenu()
            showMessage("Camper successfully created!", bottomBracket=True)
            return
        elif confirmation == 'N':
            break
        else:
            showMessage('Must be "Y" or "N"', bottomBracket=True, wait=2)

    while True:
        confirmation = showPrompt("Would you like to try again?", prompt='"Y" for Yes, "N" for No', topBracket=True, bottomBracket=True)
        if confirmation == 'Y':
            break
        elif confirmation == 'N':
            mainMenu()
            return
        else:
            showMessage('Must be "Y" or "N"', bottomBracket=True, wait=2)

    createCamper()


def withdrawCamper():
    clearScreen()
    name = showPrompt("Please insert camper name:", prompt= "(First + Last)", topBracket=True, bottomBracket=True)

    camper = summerCamp.searchCamper(name)

    if camper == STATUS_CODES["NO_CAMPER"]:
        mainMenu()
        showMessage("That camper doesn't exists!", bottomBracket=True)
        return

    elif camper.getBalance() < 1000:
        showMessage(["Camper has an outstanding balance! Request a refund to continue.",
                    "Paid: $" + str(1000-camper.getBalance())], topBracket=True,
                    bottomBracket=True)

        showPrompt("Press 'Enter' to Return!", bottomBracket=True)
        mainMenu()
        return

    while True:
        clearScreen()
        printCamperUI(camper, detailed=True, topBracket=True, bottomBracket=True)

        confirmation = showPrompt("Are you sure you want to withdraw this camper?",
                                      prompt='"Y" for Yes, "N" for No', bottomBracket=True)
        if confirmation == 'Y':
            if camper.getHasPartner() is True:
                partner = camper.getPartner()
                partner.setHasPartner(False)
                partner.setPartner(None)

                summerCamp.updateCamper(partner)

            camper.setSession(False)
            camper.setBunkhouse(False)
            camper.setTribe(False)

            summerCamp.updateCamper(camper, remove=True)
            mainMenu()
            showMessage("Camper withdraw successful", bottomBracket=True)
            return
        elif confirmation == 'N':
            mainMenu()
            showMessage("Camper withdraw aborted", bottomBracket=True)
            return
        else:
            showMessage('Must be "Y" or "N"', bottomBracket=True, wait=2)


def printCamper():
    clearScreen()
    if not any(elem != "" for elem in summerCamp.getAllCampers()):
        mainMenu()
        showMessage("There are currently no campers!", bottomBracket=True)
        return

    name = showPrompt("Please insert camper name:", prompt="(First + Last)", topBracket=True, bottomBracket=True)
    camper = summerCamp.searchCamper(name)

    if camper == STATUS_CODES["NO_CAMPER"]:
        mainMenu()
        showMessage("That camper doesn't exist!", bottomBracket=True)

    else:
        clearScreen()
        printCamperUI(camper, detailed=True, topBracket=True, bottomBracket=True)
        showPrompt("Press 'Enter' to Return!", bottomBracket=True)
        mainMenu()


def printAllCampers():
    if not any(elem != "" for elem in summerCamp.getAllCampers()):
       mainMenu()
       showMessage("There are currently no campers!", bottomBracket=True)
       return

    summerCamp.sortList(parameter="name")

    clearScreen()
    print('|----------------------------------------------|')
    print(f'   Amount: {sum(elem != "" for elem in summerCamp.getAllCampers()):}')

    genders = summerCamp.countGender()
    print(f'   Composition: {genders[0]} Male(s), {genders[1]} Female(s) ')

    for camper in summerCamp.getAllCampers():
        if isinstance(camper, Camper):
            printCamperUI(camper, simple=True)

    showPrompt("Press 'Enter' to Return!", topBracket=True, bottomBracket=True)
    mainMenu()
