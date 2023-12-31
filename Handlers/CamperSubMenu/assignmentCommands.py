from Handlers.dataHandler import summerCamp
from Handlers.uiHandler import *

def assignCamperToSession():
    clearScreen()
    name = showPrompt("Please insert camper name:", prompt="(First + Last)", topBracket=True, bottomBracket=True)

    camper = summerCamp.searchCamper(name)

    if camper == STATUS_CODES["NO_CAMPER"]:
        camperSubMenu()
        showMessage("That camper doesn't exists!", bottomBracket=True)
        return

    elif camper.getSession() is not False and camper.getAppStatus() == 1:
        showMessage("This camper has already been accepted!", bottomBracket=True)
        printCamperUI(camper, attribute="applicationStatus", bottomBracket=True)
        showPrompt("Press 'Enter' to Return!", bottomBracket=True)
        camperSubMenu()
        return

    locations = [summerCamp.getJuneCampers(), summerCamp.getJulyCampers(), summerCamp.getAugustCampers()]
    sessionDates = [Objects.values.JUNE_SESSION_DATE, Objects.values.JULY_SESSION_DATE, Objects.values.AUGUST_SESSION_DATE]

    while True:
        clearScreen()

        print('|----------------------------------------------|')
        print('| Sessions:                                    |')
        print('| (0)  June                                    |')
        print(f'        Availability: {sum(elem == "" for elem in summerCamp.getJuneCampers())}')
        print('| (1)  July                                    |')
        print(f'        Availability: {sum(elem == "" for elem in summerCamp.getJulyCampers())}')
        print('| (2)  August                                  |')
        print(f'        Availability: {sum(elem == "" for elem in summerCamp.getAugustCampers())}')
        print('|----------------------------------------------|')
        try:
            location = int(showPrompt("Which session would you like to assign?", bottomBracket=True))
        except ValueError:
            showMessage("Invalid input!", bottomBracket=True, wait=2)
            continue
        if location != 0 and location != 1 and location != 2:
            showMessage("That is not a session!", bottomBracket=True, wait=2)
        else:
            sessionLocations = [JUNE_SESSION_DATE, JULY_SESSION_DATE, AUGUST_SESSION_DATE]
            if not any(elem == "" for elem in locations[location]):
                showMessage("There is no availability in that session!", bottomBracket=True, wait=2)
            if abs((((Objects.values.TODAYS_DATE - sessionLocations[location]).days) / 7) / 4) < 2:

                showMessage(["That session is less than two months away!",
                             " Session date: " + datetime.strftime(sessionDates[location], "%m/%d/%Y")], bottomBracket=True, wait=4)
            else:
                break

    clearScreen()

    camper.setSession(location)
    summerCamp.updateCamper(camper)

    printCamperUI(camper, attribute="session", topBracket=True, bottomBracket=True)
    showPrompt("Press 'Enter' to Return!", bottomBracket=True)
    camperSubMenu()


def assignCamperToBunkhouse():
    clearScreen()
    name = showPrompt("Please insert camper name:", prompt="(First + Last)", topBracket=True, bottomBracket=True)

    camper = summerCamp.searchCamper(name)

    if camper == STATUS_CODES["NO_CAMPER"]:
        camperSubMenu()
        showMessage("That camper doesn't exists!", bottomBracket=True)
        return
    elif camper.getAppStatus() != 1:
        printCamperUI(camper, attribute="applicationStatus", topBracket=True, bottomBracket=True)
        showMessage('Camper must be accepted!')

        showPrompt("Press 'Enter' to Return!", topBracket=True, bottomBracket=True)
        camperSubMenu()
        return
    elif camper.getSession() is False:
        printCamperUI(camper, attribute="session", topBracket=True, bottomBracket=True)
        showMessage('Camper must be assigned to a session!')

        showPrompt("Press 'Enter' to Return!", topBracket=True, bottomBracket=True)
        camperSubMenu()
        return
    elif camper.getCheckedIn() is False:
        printCamperUI(camper, attribute="checkedIn", topBracket=True, bottomBracket=True)
        showMessage('Camper must be be checked in before assignment!')

        showPrompt("Press 'Enter' to Return!", topBracket=True, bottomBracket=True)
        camperSubMenu()
        return
    elif camper.getBunkhouse() is not False:
        while True:
            printCamperUI(camper, attribute="bunkhouse", topBracket=True, bottomBracket=True)
            confirmation = showPrompt("Camper already has a bunkhouse. Would you like to reassign?",
                                      prompt='"Y" for Yes, "N" for No', bottomBracket=True)

            if confirmation == 'Y':
                camper.setBunkhouse(False)

                summerCamp.updateCamper(camper)

                break
            elif confirmation == 'N':
                camperSubMenu()
                showMessage("Action aborted.", bottomBracket=True)
                return
            else:
                showMessage('Must be "Y" or "N"', bottomBracket=True, wait=2)

    locations = [summerCamp.getJuneBunkhouses(), summerCamp.getJulyBunkhouses(), summerCamp.getAugustBunkhouses()]
    session = locations[int(camper.getSession())]

    while True:
        clearScreen()

        gender = camper.getGender()

        if gender == "M":
            print('|----------------------------------------------|')
            print('| Bunkhouses:                                  |')
            print('| (0)  Bunkhouse 1                             |')
            print(f'        Availability: {sum(elem == "" for elem in session[0])}')
            print('| (1)  Bunkhouse 2                             |')
            print(f'        Availability: {sum(elem == "" for elem in session[1])}')
            print('| (2)  Bunkhouse 3                             |')
            print(f'        Availability: {sum(elem == "" for elem in session[2])}')
            print('|----------------------------------------------|')

        elif gender == "F":
            print('|----------------------------------------------|')
            print('| Bunkhouses:                                  |')
            print('| (0)  Bunkhouse 4                             |')
            print(f'        Availability: {sum(elem == "" for elem in session[3])}')
            print('| (1)  Bunkhouse 5                             |')
            print(f'        Availability: {sum(elem == "" for elem in session[4])}')
            print('| (2)  Bunkhouse 6                             |')
            print(f'        Availability: {sum(elem == "" for elem in session[5])}')
            print('|----------------------------------------------|')

        try:
            location = int(showPrompt("Which bunkhouse would you like to assign?", bottomBracket=True))
        except ValueError:
            showMessage("Invalid input!", bottomBracket=True, wait=2)
            continue

        if not 0 <= location <= 2:
            showMessage("That is not a bunkhouse!", bottomBracket=True, wait=2)
        else:
            if gender == "F":
                location += 3

            if not any(elem == "" for elem in session[location]):
                showMessage("There is no availability in that bunkhouse!", bottomBracket=True, wait=2)
            else:
                camper.setBunkhouse(location)
                break


    clearScreen()

    summerCamp.updateCamper(camper)

    printCamperUI(camper, attribute="bunkhouse", topBracket=True, bottomBracket=True)
    showPrompt("Press 'Enter' to Return!", bottomBracket=True)
    camperSubMenu()


def assignCamperToTribe():
    clearScreen()
    name = showPrompt("Please insert camper name:", prompt="(First + Last)", topBracket=True, bottomBracket=True)

    camper = summerCamp.searchCamper(name)

    if camper == STATUS_CODES["NO_CAMPER"]:
        camperSubMenu()
        showMessage("That camper doesn't exists!", bottomBracket=True)
        return
    elif camper.getAppStatus() != 1:
        printCamperUI(camper, attribute="applicationStatus", topBracket=True, bottomBracket=True)
        showMessage('Camper must be accepted!')

        showPrompt("Press 'Enter' to Return!", topBracket=True, bottomBracket=True)
        camperSubMenu()
        return
    elif camper.getSession() is False:
        printCamperUI(camper, attribute="session", topBracket=True, bottomBracket=True)
        showMessage('Camper must be assigned to a session!')

        showPrompt("Press 'Enter' to Return!", topBracket=True, bottomBracket=True)
        camperSubMenu()
        return
    elif camper.getCheckedIn() is False:
        printCamperUI(camper, attribute="checkedIn", topBracket=True, bottomBracket=True)
        showMessage('Camper must be be checked in before assignment!')

        showPrompt("Press 'Enter' to Return!", topBracket=True, bottomBracket=True)
        camperSubMenu()
        return
    elif camper.getTribe() is not False:
        while True:
            printCamperUI(camper, attribute="tribe", topBracket=True, bottomBracket=True)
            confirmation = showPrompt("Camper already has a tribe. Would you like to reassign?",
                                      prompt='"Y" for Yes, "N" for No', bottomBracket=True)

            if confirmation == 'Y':
                camper.setTribe(False)

                summerCamp.updateCamper(camper)

                break
            elif confirmation == 'N':
                camperSubMenu()
                showMessage("Action aborted.", bottomBracket=True)
                return
            else:
                showMessage('Must be "Y" or "N"', bottomBracket=True, wait=2)

    locations = [summerCamp.getJuneTribes(), summerCamp.getJulyTribes(), summerCamp.getAugustTribes()]
    session = locations[int(camper.getSession())]

    while True:
        clearScreen()

        print('|----------------------------------------------|')
        print('| Tribes:                                      |')
        print('| (0)  Tribe 1                                 |')
        print(f'        Availability: {sum(elem == "" for elem in session[0])}')
        print('| (1)  Tribe 2                                 |')
        print(f'        Availability: {sum(elem == "" for elem in session[1])}')
        print('| (2)  Tribe 3                                 |')
        print(f'        Availability: {sum(elem == "" for elem in session[2])}')
        print('| (3)  Tribe 4                                 |')
        print(f'        Availability: {sum(elem == "" for elem in session[3])}')
        print('| (4)  Tribe 5                                 |')
        print(f'        Availability: {sum(elem == "" for elem in session[4])}')
        print('| (5)  Tribe 6                                 |')
        print(f'        Availability: {sum(elem == "" for elem in session[5])}')
        print('|----------------------------------------------|')

        try:
            location = int(showPrompt("Which tribe would you like to assign?", bottomBracket=True))
        except ValueError:
            showMessage("Invalid input!", bottomBracket=True, wait=2)
            continue

        if not 0 <= location <= 5:
            showMessage("That is not a tribe!", bottomBracket=True, wait=2)
        else:
            if not any(elem == "" for elem in session[location]):
                showMessage("There is no availability in that tribe!", bottomBracket=True, wait=2)
            else:
                camper.setTribe(location)
                break

    clearScreen()

    summerCamp.updateCamper(camper)

    printCamperUI(camper, attribute="tribe", topBracket=True, bottomBracket=True)
    showPrompt("Press 'Enter' to Return!", bottomBracket=True)
    camperSubMenu()


def assignPairRequest():
    clearScreen()
    name = showPrompt("Please insert camper name:", prompt="(First + Last)", topBracket=True, bottomBracket=True)

    camper = summerCamp.searchCamper(name)

    if camper == STATUS_CODES["NO_CAMPER"]:
        camperSubMenu()
        showMessage("That camper doesn't exists!", bottomBracket=True)
        return
    elif camper.getHasPartner() is not False:
        while True:
            printCamperUI(camper, attribute="hasPartner", topBracket=True, bottomBracket=True)
            showMessage('Camper already has a partner!')

            confirmation = showPrompt("Camper already has a partner! Would you like to reassign?",
                                  prompt='"Y" for Yes, "N" for No', bottomBracket=True)

            if confirmation == 'Y':
                partner = camper.getPartner()

                camper.setHasPartner(False)
                camper.setPartner(None)

                partner.setHasPartner(False)
                partner.setPartner(None)

                summerCamp.updateCamper(camper)
                summerCamp.updateCamper(partner)

                break
            elif confirmation == 'N':
                camperSubMenu()
                showMessage("Action aborted.", bottomBracket=True)
                return
            else:
                showMessage('Must be "Y" or "N"', bottomBracket=True, wait=2)

    clearScreen()
    name = showPrompt("Please insert partner name:", prompt="(First + Last)", topBracket=True, bottomBracket=True)

    partner = summerCamp.searchCamper(name)

    if partner == STATUS_CODES["NO_CAMPER"]:
        camperSubMenu()
        showMessage("That camper doesn't exists!", bottomBracket=True)
        return
    elif partner.getHasPartner() is not False:
        while True:
            printCamperUI(partner, attribute="hasPartner", topBracket=True, bottomBracket=True)
            showMessage('Camper already has a partner!')

            confirmation = showPrompt("Camper already has a partner! Would you like to reassign?",
                                      prompt='"Y" for Yes, "N" for No', bottomBracket=True)

            if confirmation == 'Y':
                partnersPartner = partner.getPartner()

                partner.setHasPartner(False)
                partner.setPartner(None)

                partnersPartner.setHasPartner(False)
                partnersPartner.setPartner(None)

                summerCamp.updateCamper(partner)
                summerCamp.updateCamper(partnersPartner)

                break
            elif confirmation == 'N':
                camperSubMenu()
                showMessage("Action aborted.", bottomBracket=True)
                return
            else:
                showMessage('Must be "Y" or "N"', bottomBracket=True, wait=2)

    clearScreen()
    camper.setHasPartner(True)
    camper.setPartner(partner)

    partner.setHasPartner(True)
    partner.setPartner(camper)

    summerCamp.updateCamper(camper)
    summerCamp.updateCamper(partner)

    printCamperUI(camper, attribute="hasPartner", topBracket=True, bottomBracket=True)
    printCamperUI(partner, attribute="hasPartner", bottomBracket=True)

    showMessage("Partner partner successful!", bottomBracket=True)
    showPrompt("Press 'Enter' to Return!", bottomBracket=True)
    camperSubMenu()