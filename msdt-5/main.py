import random

from Classes import Floor, SmallElevator, BigElevator

floors = []
for i in range(1, 21):
    floors.append(Floor(i))

BE = BigElevator()
SE = SmallElevator()


def simulation():
    floors[0].CallElevator()
    tmp = random.randrange(1, 2, 1)
    if tmp == 1:
        SE.pressButtonFloor(14)
    else:
        BE.pressButtonFloor(14)

    # print(f"Грузовой лифт на {BE.CurretFloor} этаже")
    # print(f"Пассажирский лифт на {SE.CurretFloor} этаже")

    floors[14].CallElevator()

    if BE.CurretFloor == 15:
        BE.pressButtonFloor(1)
    if SE.CurretFloor == 15:
        SE.pressButtonFloor(1)


def handSim(floors):
    stop = True
    while True:
        tmpBool = str(input("Начать ручную симуляцию работы лифтов? (Y/N)")).upper()
        if tmpBool == "Y":
            stop = False
            break
        if tmpBool == "N":
            stop = True
            break

    while(not stop):
        floor = int(input("Введите на каком вы этаже: "))
        floors[floor-1].CallElevator()

        while(True):
            if floors[floor-1].THISFLOOR == floors[floor-1].SmallElevatorClass.CurretFloor:
                newfloor = int(input("На какой этаж едем? "))
                floors[floor - 1].SmallElevatorClass.pressButtonFloor(newfloor)
                break
            if floors[floor-1].THISFLOOR == floors[floor-1].BigElevatorClass.CurretFloor:
                newfloor = int(input("На какой этаж едем? "))
                floors[floor - 1].BigElevatorClass.pressButtonFloor(newfloor)
                break


        print(f"Лифт приехал на {floor} этаж")
        tmpBool = str(input("Продолжить симуляцию? (Y/N)")).upper()
        if tmpBool == "Y":
            stop = False
        if tmpBool == "N":
            stop = True



if __name__ == "__main__":
    simulation()
    handSim(floors)
