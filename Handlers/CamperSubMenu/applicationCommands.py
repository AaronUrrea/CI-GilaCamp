from Handlers.dataHandler import summerCamp
from Handlers.CamperSubMenu.assignmentCommands import assignCamperToSession

from Handlers.uiHandler import *

def viewCamperApplication():
    clearScreen()
    name = showPrompt("Please insert camper name:", prompt="(First + Last)", topBracket=True, bottomBracket=True)

    camper = summerCamp.searchCamper(name)

    if camper == STATUS_CODES["NO_CAMPER"]:
        camperSubMenu()
        showMessage("That camper doesn't exists!", bottomBracket=True)
        return

    clearScreen()
    printCamperUI(camper, attribute="applicationStatus", topBracket=True, bottomBracket=True)
    showPrompt("Press 'Enter' to Return!", bottomBracket=True)
    camperSubMenu()


def acceptCamperApplication():
    locations = [JUNE_SESSION_DATE, JULY_SESSION_DATE, AUGUST_SESSION_DATE]

    clearScreen()
    name = showPrompt("Please insert camper name:", prompt="(First + Last)", topBracket=True, bottomBracket=True)

    camper = summerCamp.searchCamper(name)

    if camper == STATUS_CODES["NO_CAMPER"]:
        camperSubMenu()
        showMessage("That camper doesn't exists!", bottomBracket=True)
        return
    elif camper.getAppStatus() == 1:
        showMessage("This camper has already been accepted!", bottomBracket=True)
        printCamperUI(camper, attribute="applicationStatus", bottomBracket=True)
        showPrompt("Press 'Enter' to Return!", bottomBracket=True)
        camperSubMenu()
        return
    elif camper.getAppStatus() == 2:
        showMessage("This camper has been rejected!", bottomBracket=True)
        printCamperUI(camper, attribute="applicationStatus", bottomBracket=True)
        showPrompt("Press 'Enter' to Return!", bottomBracket=True)
        camperSubMenu()
        return

    elif camper.getSession() is False:
        showMessage("Camper must be assigned to a session before application review!", bottomBracket=True)
        printCamperUI(camper, attribute="session", bottomBracket=True)
        showPrompt("Press 'Enter' to Return!", bottomBracket=True)
        camperSubMenu()
        return

    monthDifference = abs((((Objects.values.TODAYS_DATE - locations[camper.getSession()]).days)/7)/4)

    if monthDifference < 2:
        showMessage("Applications are due before two months of the session start date!", bottomBracket=True)
        printCamperUI(camper, attribute="sessionDate", bottomBracket=True)
        showPrompt("Press 'Enter' to Return!", bottomBracket=True)
        camperSubMenu()
        return

    elif monthDifference > 8:
        showMessage("Applications can not be submitted more than eight months in advance of the session start date!", bottomBracket=True)
        printCamperUI(camper, attribute="sessionDate", bottomBracket=True)
        showPrompt("Press 'Enter' to Return!", bottomBracket=True)
        camperSubMenu()
        return

    elif camper.getBalance() > 0:
        showMessage("Camper must not have any outstanding balance!", bottomBracket=True)
        printCamperUI(camper, attribute="balance", bottomBracket=True)
        showPrompt("Press 'Enter' to Return!", bottomBracket=True)
        camperSubMenu()
        return

    while True:
        clearScreen()

        printCamperUI(camper, attribute="applicationStatus", topBracket=True, bottomBracket=True)

        confirmation = showPrompt(["Are you sure you would like to accept this camper?",
                                  "This will automatically send an acceptance notice to the camper today!"], prompt= '"Y" for Yes, "N" for No', bottomBracket=True)

        if confirmation == 'Y':
            break
        elif confirmation == 'N':
            camperSubMenu()
            showMessage("Action aborted.", bottomBracket=True)
            return
        else:
            showMessage('Must be "Y" or "N"', bottomBracket=True, wait=2)

    clearScreen()
    camper.setAppStatus(1)
    camper.setAppNoticeIsSent(True)
    camper.setDateAppNoticeSent(Objects.values.TODAYS_DATE)

    summerCamp.updateCamper(camper)

    showMessage("Camper has been accepted!",topBracket=True, bottomBracket=True)
    printCamperUI(camper, attribute="applicationStatus")

    showPrompt("Press 'Enter' to Return!", topBracket=True, bottomBracket=True)
    camperSubMenu()


def rejectCamperApplication():
    clearScreen()
    name = showPrompt("Please insert camper name:", prompt="(First + Last)", topBracket=True, bottomBracket=True)

    camper = summerCamp.searchCamper(name)

    if camper == STATUS_CODES["NO_CAMPER"]:
        camperSubMenu()
        showMessage("That camper doesn't exists!", bottomBracket=True)
        return

    while True:
        clearScreen()

        printCamperUI(camper, attribute="applicationStatus", topBracket=True, bottomBracket=True)

        confirmation = showPrompt(["Are you sure you would like to reject this camper?",
                                    " If rejected, this camper will no longer be able to be accepted!"],
                                  prompt= '"Y" for Yes, "N" for No', bottomBracket=True)

        if confirmation == 'Y':
            break
        elif confirmation == 'N':
            camperSubMenu()
            showMessage("Action aborted.", bottomBracket=True)
            return
        else:
            showMessage('Must be "Y" or "N"', bottomBracket=True, wait=2)

    clearScreen()

    camper.setAppStatus(2)
    camper.setAppNoticeIsSent(False)
    camper.setDateAppNoticeSent(None)

    camper.setSession(False)
    camper.setBunkhouse(False)
    camper.setTribe(False)

    summerCamp.updateCamper(camper)

    showMessage("Camper has been rejected!",topBracket=True, bottomBracket=True)
    printCamperUI(camper, attribute="applicationStatus")

    showPrompt("Press 'Enter' to Return!", topBracket=True, bottomBracket=True)
    camperSubMenu()
