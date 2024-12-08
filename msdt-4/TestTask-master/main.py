import random
import logging
from Classes import Floor, SmallElevator, BigElevator

logging.basicConfig(level=logging.INFO)

floors = [Floor(i) for i in range(1, 21)]
BE = BigElevator()
SE = SmallElevator()

def simulation():
    logging.info("Запуск симуляции")
    floors[0].CallElevator()
    if random.choice([True, False]):
        SE.pressButtonFloor(14)
    else:
        BE.pressButtonFloor(14)

    floors[14].CallElevator()
    if BE.CurretFloor == 15:
        BE.pressButtonFloor(1)
    if SE.CurretFloor == 15:
        SE.pressButtonFloor(1)

def handSim(floors):
    while True:
        tmpBool = input("Начать ручную симуляцию работы лифтов? (Y/N): ").strip().upper()
        if tmpBool == "Y":
            while True:
                floor = int(input("Введите на каком вы этаже: "))
                floors[floor-1].CallElevator()
                newfloor = int(input("На какой этаж едем? "))
                if floors[floor-1].THISFLOOR == floors[floor-1].SmallElevatorClass.CurretFloor:
                    floors[floor - 1].SmallElevatorClass.pressButtonFloor(newfloor)
                elif floors[floor-1].THISFLOOR == floors[floor-1].BigElevatorClass.CurretFloor:
                    floors[floor - 1].BigElevatorClass.pressButtonFloor(newfloor)

                tmpBool = input("Продолжить симуляцию? (Y/N): ").strip().upper()
                if tmpBool == "N":
                    break
        elif tmpBool == "N":
            break

if __name__ == "__main__":
    simulation()
    handSim(floors)
