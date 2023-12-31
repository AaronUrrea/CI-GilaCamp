import numbers

from Handlers.guiHandler import *
from Objects.camper import Camper
from Objects.materials import Materials
from firstDay.firstDay import assignTribes
from firstDay.firstDay import assignBunkhouses
from firstDay.firstDay import checkInCert
from postAcceptance.postAcceptance import withdrawCamper

from operator import attrgetter
from faker import Faker
import random, pickle, sys, os


#====================================================================================================================================
# UTILITY FUNCTIONS
def initializeData():
    global allCampers
    global juneCampers
    global julyCampers
    global augustCampers


    global locations
    global maxCampersTotal
    global maxCampersInSession
    global maxBunkhouses
    global maxCampersInBunkhouse
    global maxTribes
    global maxCampersInTribe

    locations = ['allCampers', 'juneCampers', 'julyCampers', 'augustCampers']

    maxCampersTotal = 216
    maxCampersInSession = 72
    maxBunkhouses = 6
    maxCampersInBunkhouse = 12
    maxTribes = 6
    maxCampersInTribe = 12

    for location in locations:
        path = './database/'+location+'.pkl'

        if os.path.exists(path):
            with (open(path, 'rb')) as openfile:
                while True:
                    try:
                        globals()[location] = list(pickle.load(openfile))
                    except EOFError:
                        print(location + ' loaded successfully!')
                        break

        elif not os.path.exists(path):
            fp = open(path, 'x')
            fp.close()
            print(location + ' not found! Creating...')

            if location == 'allCampers':
                allCampers = [ None for _ in range(maxCampersTotal)]

            else:
                campers = [ None for _ in range(maxCampersInSession)]
                bunkhouses = [ [ None for _ in range(maxCampersInBunkhouse)] for _ in range(maxBunkhouses)]
                tribes = [ [ None for _ in range(maxCampersInBunkhouse)] for _ in range(maxBunkhouses)]

                # This is how we're defining our seasonal campers
                #  The first list consists of every single camper
                #  The second list consists of the six bunkhouses, which consists of a list of campers
                #  The third list consists of the six tribes, which consists of a list of campers
                globals()[location] = [campers, bunkhouses, tribes]

        try:
            if location == 'allCampers':
                globals()[location].sort(key=lambda x: (x is None, x))
            else:
                for i in range(3):
                    globals()[location][i].sort(key=lambda x: (x is None, x))
        except Exception as e:
            print(e)

    #print(allCampers)
    #print(juneCampers)
    #print(julyCampers)
    #print(augustCampers)


def shutdown():
    print('| Shutting Down...                             |')
    print('|----------------------------------------------|')
    for location in locations:
        path = './database/'+location+'.pkl'
        try:
            pickle.dump(globals()[location], open(path, 'wb'))
        except EOFError:
            break


def searchCamperFullName(camperArr, fullname):
    try:
        for currCamper in camperArr:
            if isinstance(currCamper, Camper) and currCamper.getName() == fullname:
                return currCamper
    except AttributeError:
        pass
    return None


def searchCamperLastName(camperArr, camper):
    campersWithLastName = []

    lastName = camper.getName()
    lastName = lastName.split()[1]
    try:
        for currCamper in camperArr:
            currCamperLastName = currCamper.getName()
            currCamperLastName = currCamperLastName.split()[1]
            if not camper.__eq__(currCamper) and lastName == currCamperLastName:
                campersWithLastName.append(currCamper)
    except AttributeError:
        pass
    return campersWithLastName


def searchCamperGender(camperArr, camper):
    campersWithGender = []

    gender = camper.getGender()
    try:
        for currCamper in camperArr:
            currCamperGender = currCamper.getGender()
            if not camper.__eq__(currCamper) and gender == currCamperGender:
                campersWithGender.append(currCamper)
    except AttributeError:
        pass
    except TypeError:
        pass
    return campersWithGender


def searchEmptySlot(array):
    return any(elem is None for elem in array)


def searchFilledSlot(array):
    return any(elem is not None for elem in array)


def searchAllGender(array, singleGender):
    toReturn = []

    try:
        for camper in array:
            try:
                gender = camper.getGender()
                if(gender == singleGender):
                    toReturn.append(camper)
            except AttributeError:
                pass
            except TypeError:
                pass
    except Exception is e:
        print(e)

    return toReturn


def isCamperAccepted(camper):
    if camper.getAppStatus() == 0:
        print('| Camper has not been accepted!                |')
        print('|----------------------------------------------|')
        return False
    elif camper.getAppStatus() == 2:
        print('| Camper has been Rejected!                    |')
        print('|----------------------------------------------|')
        return False
    else:
        return True


def numberOfGender(array, *singleGender):
    toReturn = [0, 0]

    try:
        for camper in array:
            try:
                gender = camper.getGender()
                if(gender == 'M'):
                    toReturn[0] += 1
                elif(gender == 'F'):
                    toReturn[1] += 1
            except AttributeError:
                pass
            except TypeError:
                pass
    except Exception is e:
        print(e)
    if singleGender:
        if (singleGender[0] == 'M'):
            return toReturn[0]
        elif (singleGender[0] == 'F'):
            return toReturn[1]

    return toReturn

#====================================================================================================================================


#====================================================================================================================================
# CAMPER OBJECT FUNCTIONS
def createCamper():
    if not searchEmptySlot(allCampers):
        mainMenu()
        print('| No more slots available!                     |')
        print('|----------------------------------------------|')
        return

    newCamper = Camper()

    try:
        newCamper.fullName = namePrompt()

        check = 0
        while check == 0:
            newCamper.age = agePrompt()
            if 9 <= int(newCamper.age) <= 18:
                check = 1
            else:
                nonFatalError("Applicant must be between 9 and 18 years old.")

        check = 0
        while check == 0:
            newCamper.gender = genderPrompt()
            if newCamper.gender == '':
                return False
            elif newCamper.gender == 'F' or newCamper.gender == 'M':
                check = 1
            else:
                nonFatalError('Applicant must be "M" or "F".')

        newCamper.address = addressPrompt()
        newCamper.balance = 1000.00
        newCamper.appStatus = 0

        newCamper.session = None
        newCamper.bunkhouse = None
        newCamper.tribe = None
        newCamper.arrivalReqCert = False
        newCamper.checkedIn = False

        newCamper.assignmentRequest = None
        newCamper.packetStatus = False
        newCamper.dateSentNotice = None
        newCamper.materials = Materials()

        while 1:
            clearScreen()

            try:
                allCampers.index(newCamper)
                mainMenu()
                print('| This camper already exists!                  |')
                print('|----------------------------------------------|')
                return
            except ValueError:
                pass
                # if this camper isn't a duplicate, then we want to create it

            confirmation = camperConfirmation(newCamper)
            if confirmation == 'Y':
                index = searchEmptySlot(allCampers)
                allCampers.insert(index, newCamper)
                mainMenu()
                return True
            elif confirmation == 'N':
                mainMenu()
                return False
            else:
                nonFatalError('Must be "Y" or "N"')
    except:
        exit("CODE 2: Exception during camper creation")


def deleteCamper():
    try:
        mainMenu()
        if not searchFilledSlot(allCampers):
            print('| There are currently no campers!              |')
            print('|----------------------------------------------|')
            return

        fullname = namePrompt()
        camper = searchCamperFullName(allCampers, fullname)

        if camper.getAssignmentRequest():
            partner = camper.getAssignmentRequest()
            partner.setAssignmentRequest(None)

        for location in locations:
            try:
                if location == 'allCampers':
                    globals()[location].remove(camper)
                    #globals()[location].sort(key=attrgetter('fullName'))
                else:
                    for i in range(3):
                        globals()[location][i].remove(camper)
                        #globals()[location][i].sort(key=attrgetter('fullName'))

            except ValueError:
                pass

        mainMenu()
        print('| Camper has been deleted!                     |')
        print('|----------------------------------------------|')

    except:
        mainMenu()
        statusGetFailure()


def printCamper():
    try:
        if not searchFilledSlot(allCampers):
            mainMenu()
            print('| There are currently no campers!              |')
            print('|----------------------------------------------|')
            return

        fullname = namePrompt()
        camper = searchCamperFullName(allCampers, fullname)

        print('|----------------------------------------------|')
        print('  Name:     ' + camper.getName())
        if camper.getAssignmentRequest():
            print('   Partner: ' + camper.getAssignmentRequest().getName())

        print('  Age:      ' + str(camper.getAge()))
        print('  Gender:   ' + camper.getGender())
        print('  Address:  ' + camper.getAddress())
        print('  Balance:  $' + str(camper.getBalance()))

        status = camper.getAppStatus()

        if status == 0:
            print('  Application Status: Pending')
        elif status == 1:
            print('  Application Status: Accepted')
            print('|----------------------------------------------|')

            session = camper.getSession()
            bunkhouse = camper.getBunkhouse()
            tribe = camper.getTribe()

            if session:
                print('  Session: ' + session)
            if bunkhouse:
                print('  Bunkhouse: ' + str(bunkhouse))
            if tribe:
                print('  Tribe: ' + str(tribe))

            print('  Checked In: ' + str(camper.getCheckedIn()))
            print('  Packet Status: : ' + str(camper.getPacket()))

            packetDate = camper.getPacketSendDate()

            if packetDate:
                print('  Packet Sent Date: ' + str(packetDate))

        elif status == 2:
            print('  Application Status: Rejected')


        print('|----------------------------------------------|')
        print('| Press enter to return!                       |')
        print('|----------------------------------------------|')
        input()
        mainMenu()


    except Exception as e:
        print(e)
        mainMenu()
        statusGetFailure()


def printAllCampers():
    try:
        if not searchFilledSlot(allCampers):
            mainMenu()
            print('| There are currently no campers!              |')
            print('|----------------------------------------------|')
            return

        clearScreen()
        print('|----------------------------------------------|')
        print(f'   Amount: {len(allCampers) - allCampers.count(None)}')

        genders = numberOfGender(allCampers)
        print(f'   Composition: {genders[0]} Male(s), {genders[1]} Female(s) ')
        print(f'   Names:')


        for camper in allCampers:
            if camper:
                print('    ' + camper.getName())

                if camper.getAssignmentRequest() is not None:
                    print('     Partner: ' + camper.getAssignmentRequest().getName())



        print('|----------------------------------------------|')
        print('| Press enter to return!                       |')
        print('|----------------------------------------------|')
        input()
        mainMenu()
    except AttributeError:
        pass
    except Exception as e:
        print(e)
#====================================================================================================================================


#====================================================================================================================================
# SESSIONS

def viewSessions():
    try:
        clearScreen()
        print('|----------------------------------------------|')
        print('| Sessions:                                    |')


        for location in locations[1:]:
            if location == 'allCampers':
                pass
            else:
                month = location.split("Camper", maxsplit=1)[0].capitalize()
                amount = len(globals()[location][0]) - globals()[location][0].count(None)

                print(f'    {month}:')
                print(f'     Amount: {amount}')

                genders = numberOfGender(globals()[location][0])
                print(f'     Composition: {genders[0]} Male(s), {genders[1]} Female(s)')
                print(f'     Names:')

                try:
                    for i in range(maxCampersInSession):
                        camper = globals()[location][0][i]
                        if camper:
                            print('       ' + camper.getName())

                            if camper.getAssignmentRequest() is not None:
                                print('        Partner: ' + camper.getAssignmentRequest().getName())
                except ValueError:
                    pass
                except AttributeError:
                    pass

        print('|----------------------------------------------|')
        print('| Press enter to return!                       |')
        print('|----------------------------------------------|')
        input()
        mainMenu()

    except Exception as e:
        mainMenu()
        statusGetFailure()


def viewBunkhouses():
    try:
        selection = -1
        iterator = 1

        while 1:
            clearScreen()
            print('|----------------------------------------------|')
            print('| What session would you like to assign?       |')
            print('| (0)  June                                    |')
            print('| (1)  July                                    |')
            print('| (2)  August                                  |')
            print('|----------------------------------------------|')

            command = input(">> ")

            if command == '0':
                selection = 0
                break
            elif command == '1':
                selection = 1
                break
            elif command == '2':
                selection = 2
                break
            else:
                nonFatalError('Incorrect Input!')
        clearScreen()
        print('|----------------------------------------------|')


        for bunkhouse in globals()[locations[selection+1]][1]:
            print(f'  Bunkhouse {iterator}:')


            amount = sum(x is not None for x in bunkhouse)
            print(f'   Amount: {amount}')
            print(f'   Name(s):')

            for camper in bunkhouse:
                try:
                    print(f'    {camper.getName()}')
                    print(f'     Age: {camper.getAge()}')

                    if camper.getAssignmentRequest:
                        print(f'     Partner: {camper.getAssignmentRequest().getName()}')

                except AttributeError:
                    pass
                except Exception as e:
                    print(e)
            iterator += 1

        print('|----------------------------------------------|')
        print('| Press enter to return!                       |')
        print('|----------------------------------------------|')
        input()
        mainMenu()

    except Exception as e:
        print(e)
        mainMenu()
        statusGetFailure()


def viewTribes():
    try:
        selection = -1
        iterator = 1

        while 1:
            clearScreen()
            print('|----------------------------------------------|')
            print('| What session would you like to assign?       |')
            print('| (0)  June                                    |')
            print('| (1)  July                                    |')
            print('| (2)  August                                  |')
            print('|----------------------------------------------|')

            command = input(">> ")

            if command == '0':
                selection = 0
                break
            elif command == '1':
                selection = 1
                break
            elif command == '2':
                selection = 2
                break
            else:
                nonFatalError('Incorrect Input!')
        clearScreen()
        print('|----------------------------------------------|')
        for bunkhouse in globals()[locations[selection+1]][2]:
            print(f'  Tribe {iterator}:')

            amount = sum(x is not None for x in bunkhouse)
            print(f'   Amount: {amount}')

            genders = numberOfGender(bunkhouse)
            print(f'   Composition: {genders[0]} Male(s), {genders[1]} Female(s)')
            print(f'   Name(s):')

            for camper in bunkhouse:
                try:
                    print(f'    {camper.getName()}')
                    print(f'     Age: {camper.getAge()}')

                    if camper.getAssignmentRequest:
                        print(f'     Partner: {camper.getAssignmentRequest().getName()}')

                except AttributeError:
                    pass
                except Exception as e:
                    print(e)
            iterator += 1

        print('|----------------------------------------------|')
        print('| Press enter to return!                       |')
        print('|----------------------------------------------|')
        input()
        mainMenu()

    except Exception as e:
        print(e)
        mainMenu()
        statusGetFailure()
#====================================================================================================================================


#====================================================================================================================================
# CAMPER ATTRIBUTE FUNCTIONS
#  BALANCE
def viewCamperBalance():
    try:
        fullname = namePrompt()
        camper = searchCamperFullName(allCampers, fullname)

        camperSubMenu()

        print('  Camper Found: ' + camper.getName())
        print('  Balance Due: $' + str(camper.getBalance()))
        print('|----------------------------------------------|')

    except:
        camperSubMenu()
        statusGetFailure()


def raiseCamperBalance():
    try:
        fullname = namePrompt()
        camper = searchCamperFullName(allCampers, fullname)

        amount = amountPrompt()

        camperSubMenu()

        print('  Camper Found: ' + camper.getName())
        print('  Old Balance: $' + str(camper.getBalance()))

        camper.setBalance(camper.getBalance() + float(amount))

        print('  New Balance: $' + str(camper.getBalance()))
        print('|----------------------------------------------|')

    except:
        camperSubMenu()
        statusGetFailure()


def reduceCamperBalance():
    try:
        fullname = namePrompt()
        camper = searchCamperFullName(allCampers, fullname)

        amount = amountPrompt()

        camperSubMenu()

        print('  Camper Found: ' + camper.getName())
        print('  Old Balance: $' + str(camper.getBalance()))

        camper.setBalance(camper.getBalance() - float(amount))
        if camper.getBalance() < 0:
            camper.setBalance(0)

        print('  New Balance: $' + str(camper.getBalance()))
        print('|----------------------------------------------|')

    except:
        camperSubMenu()
        statusGetFailure()


def clearCamperBalance():
    try:
        fullname = namePrompt()
        camper = searchCamperFullName(allCampers, fullname)

        camperSubMenu()

        print('  Camper Found: ' + camper.getName())
        print('  Old Balance: $' + str(camper.getBalance()))

        camper.setBalance(0)

        print('  New Balance: $' + str(camper.getBalance()))
        print('|----------------------------------------------|')

    except:
        camperSubMenu()
        statusGetFailure()

#  APPLICATION
def viewCamperApplication():
    try:
        fullname = namePrompt()
        camper = searchCamperFullName(allCampers, fullname)

        status = camper.getAppStatus()

        camperSubMenu()
        if status == 0:
            print('  Camper Found: ' + camper.getName())
            print('  Application Status: Pending!')
            print('|----------------------------------------------|')
            return
        elif status == 1:
            print('  Camper Found: ' + camper.getName())
            print('  Application Status: Accepted!')
            print('|----------------------------------------------|')
            return
        elif status == 2:
            print('  Camper Found: ' + camper.getName())
            print('  Application Status: Rejected!')
            print('|----------------------------------------------|')
            return
    except:
        camperSubMenu()
        statusGetFailure()


def acceptCamperApplication():
    try:
        fullname = namePrompt()
        camper = searchCamperFullName(allCampers, fullname)

        balance = camper.getBalance()

        camperSubMenu()
        if balance != 0:
            print('  Camper Found: ' + camper.getName())
            print('  Balance: $' + str(balance))
            print('   NOTE: Balance must be $0 to be accepted!')
            print('|----------------------------------------------|')
            return
        elif camper.setAppStatus(1):
            print('  Camper Found: ' + camper.getName())
            print('  Application Status: Accepted!')
            print('|----------------------------------------------|')
            return
        else:
            camperSubMenu()
            statusGetFailure()
            return

    except:
        camperSubMenu()
        statusGetFailure()


def rejectCamperApplication():
    try:
        fullname = namePrompt()
        camper = searchCamperFullName(allCampers, fullname)

        camperSubMenu()

        if camper.setAppStatus(2):
            print('  Camper Found: ' + camper.getName())
            print('  Application Status: Rejected!')
            print('|----------------------------------------------|')
        else:
            camperSubMenu()
            statusGetFailure()

    except:
        camperSubMenu()
        statusGetFailure()

#  ASSIGNMENT
def assignCamperToSession():
    try:
        maxCampersInSession

        fullname = namePrompt()
        camper = searchCamperFullName(allCampers, fullname)

        availability = [searchEmptySlot(juneCampers[0]), searchEmptySlot(julyCampers[0]), searchEmptySlot(augustCampers[0])]

        if camper.getAppStatus() != 1:
            camperSubMenu()
            print('| Camper must be accepted!                     |')
            print('|----------------------------------------------|')
            return

        elif not any(availability):
            camperSubMenu()
            print('| Sorry, all sessions are full!                |')
            print('|----------------------------------------------|')
            return

        for location in locations:
            try:
                if location == "allCampers":
                    pass
                else:
                    globals()[location][0].index(camper)
                    camperSubMenu()
                    camperAlreadyEnrolled()
                    return
            except ValueError:
                pass
                # if this camper isn't a duplicate, then we want to create it
            
        while 1:

            clearScreen()

            print('|----------------------------------------------|')
            print('| What session would you like to assign?       |')
            print('| (0)  June                                    |')
            print(f'|  Availability: {maxCampersInSession - juneCampers[0].index(None)}' + '                            |')
            print('| (1)  July                                    |')
            print(f'|  Availability: {maxCampersInSession - julyCampers[0].index(None)}' + '                            |')
            print('| (2)  August                                  |')
            print(f'|  Availability: {maxCampersInSession - augustCampers[0].index(None)}' + '                            |')
            print('|----------------------------------------------|')

            command = input(">> ")

            if command == '0' and availability[0]:
                juneCampers[0].insert(juneCampers[0].index(None), camper)
                camper.setSession("June")
                break
            elif command == '1' and availability[1]:
                julyCampers[0].insert(julyCampers[0].index(None), camper)
                camper.setSession("July")
                break
            elif command == '2' and availability[2]:
                augustCampers[0].insert(augustCampers[0].index(None), camper)
                camper.setSession("August")
                break
            else:
                nonFatalError('That session is full!')

        camperSubMenu()
        print('| Camper successfully added to session!        |')
        print('|----------------------------------------------|')


    except Exception as e:
        print(e)
        #mainMenu()
        #statusGetFailure()


def assignCamperToBunkhouse():
    try:
        camperSubMenu()
        assignBunkhouses(allCampers)
        print(' Bunkhouses: ')
        for camper in allCampers:
            print(' ' + str(camper.getName()) + " Bunkhouse: " + str(camper.getBunkhouse()))
        print('|----------------------------------------------|')
    except:
        camperSubMenu()
        statusGetFailure()


def assignCamperToTribe():
    try:
        camperSubMenu()
        assignTribes(allCampers)
        print(' Tribes: ')
        for camper in allCampers:
            print(' ' + str(camper.getName()) + " Tribe: " + str(camper.getTribe()))
        print('|----------------------------------------------|')
    except:
        camperSubMenu()
        statusGetFailure()


def assignPairRequest():
    try:
        subjectname = namePrompt()
        subjectcamper = searchCamperFullName(allCampers, subjectname)

        if subjectcamper.getAssignmentRequest() is not None:
                print('| Camper already has request:                  |')
                print(f'|  {subjectcamper.getAssignmentRequest().getName()}')
                print('|----------------------------------------------|')
                print('| Press "Enter" to return!                     |')
                print('|----------------------------------------------|')
                input(">> ")
                camperSubMenu()
                return

        requestname = namePrompt()
        requestcamper = searchCamperFullName(allCampers, requestname)

        if requestcamper.getAssignmentRequest() is not None:
                print('| Camper already has request:                  |')
                print(f'|  {requestcamper.getAssignmentRequest().getName()}')
                print('|----------------------------------------------|')
                print('| Press "Enter" to return!                     |')
                print('|----------------------------------------------|')
                input(">> ")
                camperSubMenu()
                return

        if(subjectcamper.getGender() != requestcamper.getGender()):
            print('| Campers must have the same gender!           |')
            print('|----------------------------------------------|')
            print('| Press "Enter" to return!                     |')
            print('|----------------------------------------------|')
            input(">> ")
            camperSubMenu()
            return
        
        subjectcamper.setAssignmentRequest(requestcamper)
        requestcamper.setAssignmentRequest(subjectcamper)

        camperSubMenu()
        print(' Added pair request between ' + str(subjectcamper.getName()) + ' and ' + str(requestcamper.getName()))
        print('|----------------------------------------------|')
    except:
        camperSubMenu()
        statusGetFailure()


def withdrawRefundCamper():
    try:
        name = namePrompt()
        camper = searchCamperFullName(allCampers, name)
        #withdrawCamper(camper, allCampers, tribes, bunkhouses)
        camperSubMenu()
        print(' Withdrew ' + str(camper.getName()))
        print('|----------------------------------------------|')
    except:
        camperSubMenu()
        statusGetFailure()

#  FIRST DAY MATERIALS
def viewCamperPacketStatus():
    try:
        fullname = namePrompt()
        camper = searchCamperFullName(allCampers, fullname)

        camperSubMenu()

        print('  Camper Found: ' + camper.getName())
        print('  Packet Status: ' + str(camper.getPacket()))
        print('  Send Date: ' + str(camper.getPacketSendDate()))
        print('|----------------------------------------------|')

    except:
        camperSubMenu()
        statusGetFailure()


def updateCamperPacketStatus():
    try:
        fullname = namePrompt()
        camper = searchCamperFullName(allCampers, fullname)

        camperSubMenu()

        camper.setPacketSend()
        print('  Camper Found: ' + camper.getName())
        print('  Packet Status: ' + str(camper.getPacket()))
        print('  Send Date: ' + str(camper.getPacketSendDate()))
        print('|----------------------------------------------|')
    except:
        camperSubMenu()
        statusGetFailure()


def certifyCamperReqs():
        fullname = namePrompt()
        camper = searchCamperFullName(allCampers, fullname)
        clearScreen()

        try:
            checkInCert(camper)
        except:
            pass #lol
#====================================================================================================================================


#====================================================================================================================================
# AUTOMATION
def setEveryBalance():
    try:
        amount = amountPrompt()
        mainMenu()
        if not searchFilledSlot(allCampers):
            print('| There are currently no campers!              |')
            print('|----------------------------------------------|')
            return

        for camper in allCampers:
            if camper:
                camper.setBalance(amount)

        print('| Every balance cleared!                       |')
        print('|  PS: HR would like a word with you!          |')
        print('|----------------------------------------------|')

    except AttributeError:
        pass
    except Exception as e:
        print(e)


def setEveryApplication():
    try:
        status = applicationStatusPrompt()
        mainMenu()
        if not searchFilledSlot(allCampers):
            print('| There are currently no campers!              |')
            print('|----------------------------------------------|')
            return

        for camper in allCampers:
            if camper:
                if camper.getBalance() == 0:
                    camper.setAppStatus(status)

        print('| Every application status changed!            |')
        print('|  PS: Some excellent quality control there...   |')
        print('|----------------------------------------------|')

    except AttributeError:
        pass
    except Exception as e:
        print(e)


def assignCampersToSessions():
    try:

        for camper in allCampers:
            if camper:
                camper.setAppStatus(1)


        availability = [searchEmptySlot(juneCampers[0]), searchEmptySlot(julyCampers[0]), searchEmptySlot(augustCampers[0])]

        maxGenderPerSession = 36

        random.shuffle(allCampers)

        for camper in allCampers:
            if camper.getSession():
                continue
            elif not camper.getAssignmentRequest():
                continue

            index = random.randint(1, availability.count(True))
            currentSession = globals()[locations[index]][0]
            sessionName = locations[index].split("Camper", 1)[0].capitalize()
            numberOfMalesOrFemales = numberOfGender(currentSession, camper.getGender())
            partner = camper.getAssignmentRequest()

            if numberOfMalesOrFemales > maxGenderPerSession:
                continue
            elif numberOfMalesOrFemales + 2 > maxGenderPerSession:
                continue
            elif partner and partner.getSession() is None:
                globals()[locations[index]][0].remove(None)
                globals()[locations[index]][0].remove(None)

                camper.setSession(sessionName)
                partner.setSession(sessionName)

                globals()[locations[index]][0].insert(index, camper)
                globals()[locations[index]][0].insert(index, partner)
        for location in locations:
            if location == "allCampers":
                continue
            else:
                for camper in allCampers:
                    count = globals()[location][0].count(None)
                    currentSession = globals()[location][0]
                    numberOfMalesOrFemales = numberOfGender(currentSession, camper.getGender())

                    if camper.getSession():
                        continue
                    elif count == 0:
                        continue

                    if numberOfMalesOrFemales > maxGenderPerSession:
                        continue
                    elif numberOfMalesOrFemales + 1 > maxGenderPerSession:
                        continue
                    else:
                        globals()[location][0].remove(None)
                        camper.setSession(location.split("Camper", 1)[0].capitalize())
                        globals()[location][0].append(camper)



    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

    allCampers.sort(key=lambda x: x.fullName)

    mainMenu()
    print('| All session filled!                          |')
    print('|----------------------------------------------|')


def assignCampersToBunkhouses():
    try:
        for location in locations:
            if location == "allCampers":
                continue
            else:
                maleCampers = [camper for camper in globals()[location][0] if camper.gender == 'M']
                femaleCampers = [camper for camper in globals()[location][0] if camper.gender == 'F']

                maleCampers.sort(key=lambda x: x.age)
                femaleCampers.sort(key=lambda x: x.age)

                genderArray = 'maleCampers'

                for i in range(6):
                    if i >= 3:
                        genderArray = 'femaleCampers'
                    for camper in locals()[genderArray]:
                        partner = camper.getAssignmentRequest()
                        if camper.getBunkhouse() is not None:
                            continue
                        elif globals()[location][1][i].count(None) == 0:
                            continue

                        elif partner and partner.getBunkhouse() is not None:
                            if globals()[location][1][i].count(None) == 1:
                                continue
                            elif camper.getAge() < partner.getAge():
                                continue
                            elif camper.getAge() > partner.getAge():
                                camper.setBunkhouse(i)
                                partner.setBunkhouse(i)
                                try:
                                    globals()[location][1][i].remove(None)
                                    globals()[location][1][i].remove(None)
                                except ValueError:
                                    skip
                                globals()[location][1][i].append(camper)
                                globals()[location][1][i].append(partner)

                        else:
                            camper.setBunkhouse(i)
                            try:
                                globals()[location][1][i].remove(None)
                            except ValueError:
                                skip
                            globals()[location][1][i].append(camper)

        for location in locations:
            if location == "allCampers":
                continue
            else:
                for i in range(6):
                    for j in range(12):
                        camper = globals()[location][1][i][j]

                        aCIndex = -1
                        gLIndex = -1

                        try:
                            aCIndex = allCampers.index(searchCamperFullName(allCampers, camper.getName()))
                        except ValueError:
                            pass
                        except AttributeError:
                            pass
                        try:
                            gLIndex = globals()[location][0].index(searchCamperFullName(globals()[location][0], camper.getName()))
                        except ValueError:
                            pass
                        except AttributeError:
                            pass

                        if aCIndex != -1:
                            allCampers.pop(aCIndex)
                            allCampers.insert(aCIndex, camper)
                        if gLIndex != -1:
                            globals()[location][0].pop(gLIndex)
                            globals()[location][0].insert(gLIndex, camper)


    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

    mainMenu()
    print('| All bunkhouses filled!                       |')
    print('|----------------------------------------------|')


def assignCampersToTribes():

    maxGenderPerTribe = 6

    try:
        for location in locations:
            if location == "allCampers":
                continue
            else:
                globals()[location][0].sort(key=lambda x: x.age)

                for i in range(6):
                    for camper in globals()[location][0]:
                        numberOfMalesOrFemales = numberOfGender(globals()[location][2][i], camper.getGender())
                        partner = camper.getAssignmentRequest()

                        if camper.getTribe() is not None:
                            continue
                        elif globals()[location][2][i].count(None) == 0:
                            continue

                        if partner:
                            if partner.getTribe():
                                continue

                            if camper.getAge() < partner.getAge():
                                continue

                            elif camper.getGender() == partner.getGender():
                                camperGender = numberOfGender(globals()[location][2][i], camper.getGender())

                                if camperGender > maxGenderPerTribe:
                                    continue

                                elif camperGender + 2 > maxGenderPerTribe:
                                    removedCamper = globals()[location][2][i].pop()
                                    globals()[location][0].remove(removedCamper)
                                    globals()[location][0].append(removedCamper)
                                    globals()[location][0].sort(key=lambda x: x.age)

                            elif camper.getGender() != partner.getGender():
                                camperGender = numberOfGender(globals()[location][2][i], camper.getGender())
                                partnerGender = numberOfGender(globals()[location][2][i], partner.getGender())

                                if camperGender + 1 > maxGenderPerTribe:
                                    removedCamper = globals()[location][2][i].pop()
                                    globals()[location][0].remove(removedCamper)
                                    globals()[location][0].append(removedCamper)
                                    globals()[location][0].sort(key=lambda x: x.age)

                                elif partnerGender + 1 > maxGenderPerTribe:
                                    removedCamper = globals()[location][2][i].pop()
                                    globals()[location][0].remove(removedCamper)
                                    globals()[location][0].append(removedCamper)
                                    globals()[location][0].sort(key=lambda x: x.age)

                            camper.setTribe(i)
                            partner.setTribe(i)
                            try:
                                globals()[location][2][i].remove(None)
                                globals()[location][2][i].remove(None)
                            except ValueError:
                                pass
                            globals()[location][2][i].append(camper)
                            globals()[location][2][i].append(partner)

                        else:
                            numberOfMalesOrFemales = numberOfGender(globals()[location][2][i], camper.getGender())

                            if numberOfMalesOrFemales + 1 > maxGenderPerTribe:
                                continue
                            camper.setTribe(i)
                            try:
                                globals()[location][2][i].remove(None)
                            except ValueError:
                                pass
                            globals()[location][2][i].append(camper)

        for location in locations:
            if location == "allCampers":
                continue
            else:
                for i in range(6):
                    for j in range(12):
                        try:
                            camper = globals()[location][2][i][j]
                        except Exception as e:
                            print(e)

                        aCIndex = -1
                        gLIndex = -1

                        try:
                            aCIndex = allCampers.index(searchCamperFullName(allCampers, camper.getName()))
                        except ValueError:
                            pass
                        except AttributeError:
                            pass
                        try:
                            gLIndex = globals()[location][0].index(searchCamperFullName(globals()[location][0], camper.getName()))
                        except ValueError:
                            pass
                        except AttributeError:
                            pass

                        if aCIndex != -1:
                            allCampers.pop(aCIndex)
                            allCampers.insert(aCIndex, camper)
                        if gLIndex != -1:
                            globals()[location][0].pop(gLIndex)
                            globals()[location][0].insert(gLIndex, camper)


    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


#====================================================================================================================================


#====================================================================================================================================
# DEBUG
def populateMaxCampers():

    clearAllCampers()


    print('| Creating max campers...                      |')
    print('|----------------------------------------------|')

    random.seed()
    fake = Faker()


    for i in range(maxCampersTotal):
        empty = searchEmptySlot(allCampers)
        if empty:
            newCamper = Camper()

            check = 0

            while check == 0:
                if i < maxCampersTotal/2:
                    newCamper.fullName = fake.first_name_male() + ' ' + fake.last_name_male()
                    newCamper.gender = 'M'
                elif i >= maxCampersTotal/2:
                    newCamper.fullName = fake.first_name_female() + ' ' + fake.last_name_female()
                    newCamper.gender = 'F'

                if searchCamperFullName(allCampers, newCamper.fullName) is None:
                    check = 1

            newCamper.age = random.randint(9, 18)

            newCamper.address = fake.street_address()

            newCamper.balance = 1000.00
            newCamper.appStatus = 0

            newCamper.session = None
            newCamper.bunkhouse = None
            newCamper.tribe = None
            newCamper.arrivalReqCert = False
            newCamper.checkedIn = False

            newCamper.assignmentRequest = None
            newCamper.packetStatus = False
            newCamper.dateSentNotice = None
            newCamper.materials = Materials()

            try:
                allCampers.remove(None)
                allCampers.append(newCamper)
            except ValueError:
                pass
                # we shouldn't be getting this error, as above the empty check confirms
                #  there is an empty slot to use

    allCampers.sort(key=lambda x: (x is None, x))

    for camper in allCampers:

        try:
            if camper.getAssignmentRequest() is None:
                # Here we find all campers with the same last name
                matchingCampers = searchCamperLastName(allCampers, camper)

                # Here we find all campers with the same last name
                #  We can't pair up two campers of different genders
                matchingCampers = searchCamperGender(matchingCampers, camper)

                if len(matchingCampers) > 0:

                    chanceRequest = random.randint(1, 4)
                    if chanceRequest == 4:
                        #print("Pairing request started!")
                        try:
                            index = random.randint(0, len(matchingCampers) - 1)

                            camper.setAssignmentRequest(matchingCampers[index])
                            matchingCampers[index].setAssignmentRequest(camper)

                            #print(f"Successful pair! {camper.getName()} {matchingCampers[index].getName()}")
                        except Exception as e:
                            print(e)

        except Exception as e:
            print(e)

    time.sleep(2)

    mainMenu()
    print('| Max campers created, calm down there God...  |')
    print('|----------------------------------------------|')


def clearAllCampers():
    print('| Clearing all campers...                      |')       
    print('|----------------------------------------------|')       

    try:
        for location in locations:
            if location == 'allCampers':
                globals()[location] = []
                globals()[location] = [ None for _ in range(maxCampersTotal)]
            else:
                globals()[location] = []

                campers = [ None for _ in range(maxCampersInSession)]
                bunkhouses = [ [ None for _ in range(maxCampersInBunkhouse)] for _ in range(maxBunkhouses)]
                tribes = [ [ None for _ in range(maxCampersInBunkhouse)] for _ in range(maxBunkhouses)]

                globals()[location] = [campers, bunkhouses, tribes]

    except Exception as e:
        print(e)

    time.sleep(2)

    mainMenu()
    print('| Cleared all campers, you monster!            |')
    print('|----------------------------------------------|')


##def clearAllSessions():
#    print('| Clearing all sessions...                      |')
#    print('|----------------------------------------------|')
#
#    try:
#        for location in locations:
#            if location == 'allCampers':
#                continue
#            else:
#                globals()[location][0] = []
#                globals()[location][0] = list(itertools.repeat(None, maxCampersInSession))
#
#    except Exception as e:
#        print(e)
#
#    time.sleep(2)
#
#    mainMenu()
#    print('| Cleared all sessions, do we need them?       |')
#    print('|----------------------------------------------|')


##def clearAllBunkHouses():
#    print('| Clearing all bunkhouses                      |')
#    print('|----------------------------------------------|')
#
#    try:
#        for location in locations:
#            if location == 'allCampers':
#                continue
#            else:
#                globals()[location][1] = []
#                globals()[location][1] = list(itertools.repeat(list(itertools.repeat(None, maxCampersInBunkhouse)), maxBunkhouses))
#    except Exception as e:
#        print(e)
#
#    time.sleep(2)
#
#    mainMenu()
#    print('| Cleared all bunkhouses, homelessness is in!  |')
#    print('|----------------------------------------------|')


#def clearAllTribes():
#   print('| Clearing all bunkhouses                      |')
#   print('|----------------------------------------------|')
#
#   try:
#       for location in locations:
#           if location == 'allCampers':
#               continue
#           else:
#               globals()[location][2] = []
#               globals()[location][2] = list(itertools.repeat(list(itertools.repeat(None, maxCampersInBunkhouse)), maxBunkhouses))
#   except Exception as e:
#       print(e)
#
#   time.sleep(2)
#
#   mainMenu()
#   print('| Cleared all tribes, we\'re civilized now!     |')
#   print('|----------------------------------------------|')


#==========================================================================================================================