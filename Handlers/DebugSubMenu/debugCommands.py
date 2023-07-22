from Handlers.dataHandler import summerCamp
from Handlers.uiHandler import mainMenu, camperSubMenu, debugSubMenu, clearScreen

def databaseView(runtime):
    clearScreen()
    print('|----------------------------------------------|')
    print("ALL CAMPERS LIST:")
    print(summerCamp.getAllCampers())
    print('|----------------------------------------------|')
    print("JUNE CAMPERS LIST:")
    print(" JUNE CAMPERS:")
    print(summerCamp.getJuneCampers())
    print(" JUNE BUNKHOUSES:")
    print(summerCamp.getJuneBunkhouses())
    print(" JUNE TRIBES:")
    print(summerCamp.getJuneTribes())
    print('|----------------------------------------------|')
    print("JULY CAMPERS LIST:")
    print(" JULY CAMPERS:")
    print(summerCamp.getJulyCampers())
    print(" JULY BUNKHOUSES:")
    print(summerCamp.getJulyBunkhouses())
    print(" JULY TRIBES:")
    print(summerCamp.getJulyTribes())
    print('|----------------------------------------------|')
    print("AUGUST CAMPERS LIST:")
    print(" AUGUST CAMPERS:")
    print(summerCamp.getAugustCampers())
    print(" AUGUST BUNKHOUSES:")
    print(summerCamp.getAugustBunkhouses())
    print(" AUGUST TRIBES:")
    print(summerCamp.getAugustTribes())
    print('|----------------------------------------------|')
    print("TEMPORARY CAMPERS LIST:")
    print(" JUNE CAMPERS:")
    print(summerCamp.getTempJuneCampers())
    print(" JULY CAMPERS:")
    print(summerCamp.getTempJulyCampers())
    print(" AUGUST CAMPERS:")
    print(summerCamp.getTempAugustCampers())
    print('|----------------------------------------------|')
    print()

    match runtime:
        case 'mainMenu':
            mainMenu(clearScreen=False)
        case 'camperSubMenu':
            camperSubMenu(clearScreen=False)
        case 'debugSubMenu':
            debugSubMenu(clearScreen=False)
