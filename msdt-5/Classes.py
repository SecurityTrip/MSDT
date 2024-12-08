import time


class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance


class SmallElevator(Singleton):  # Пассажирский лифт
    MAXWEIGHT = 400
    MAXPEOPLE = 5


    alavlable = True

    SPEED = 2  # m/s

    FLOORHEIGHT = 2.7  # meters

    CurretFloor = 1

    status = ["Едет вверх", "Едет вниз", "Открывает двери", "Закрывает двери", "Стоит с открытыми дверьми",
              "Вызов диспетчера"]
    CurrentStatusIndex = 4

    doorStatus = "Открыты"

    def GetStatus(self):
        return self.status[self.CurrentStatusIndex]

    def pressButtonFloor(self, floor):
        #if 1 >= floor <= 20:
            self.RunToFloor(floor)

    def pressButtonCloseDoors(self):
        self.doorStatus = "Открыты"

    def pressButtonOpenDoors(self):
        self.doorStatus = "Закрыты"

    def pressButtonCallDispatcher(self):
        self.CurrentStatusIndex = 5
        print(self.status[self.CurrentStatusIndex])
        print("Идёт вызов диспетчера")

    def RunToFloor(self, floor):
        if floor > self.CurretFloor:
            self.CurrentStatusIndex = 3
            print(self.status[self.CurrentStatusIndex])
            self.doorStatus = "Закрыты"

            self.CurrentStatusIndex = 0
            print(self.status[self.CurrentStatusIndex])

            print(f"Пассажирский лифт едет на {floor} этаж")

            meters = (floor - self.CurretFloor + 1) * self.FLOORHEIGHT
            time.sleep(meters / self.SPEED)

            self.CurretFloor = floor
            print(f"Пассажирский лифт приехал на {self.CurretFloor} этаж")

            self.CurrentStatusIndex = 2
            print(self.status[self.CurrentStatusIndex])
            self.doorStatus = "Открыты"

        elif floor < self.CurretFloor:
            self.CurrentStatusIndex = 3
            print(self.status[self.CurrentStatusIndex])
            self.doorStatus = "Закрыты"

            self.CurrentStatusIndex = 1
            print(self.status[self.CurrentStatusIndex])

            print(f"Пассажирский лифт едет на {floor} этаж")

            meters = (self.CurretFloor - floor + 1) * self.FLOORHEIGHT
            time.sleep(meters / self.SPEED)

            self.CurretFloor = floor
            print(f"Пассажирский лифт приехал на {self.CurretFloor} этаж")

            self.CurrentStatusIndex = 2
            print(self.status[self.CurrentStatusIndex])
            self.doorStatus = "Открыты"

        elif floor == self.CurretFloor:
            print(f"Пассажирский лифт уже на {self.CurretFloor} этаже")
            self.doorStatus = "Открыты"
            self.CurrentStatusIndex = 4
            print(self.status[self.CurrentStatusIndex])


class BigElevator(Singleton):  # Грусзовой лифт
    MAXWEIGHT = 800
    MAXPEOPLE = 10

    alavlable = True

    SPEED = 1.8  # m/s

    FLOORHEIGHT = 2.7  # meters

    CurretFloor = 1

    status = ["Едет вверх", "Едет вниз", "Открывает двери", "Закрывает двери", "Стоит с открытыми дверьми",
              "Вызов диспетчера"]
    CurrentStatusIndex = 4

    doorStatus = "Открыты"

    def GetStatus(self):
        return self.status[self.CurrentStatusIndex]

    def pressButtonFloor(self, floor):
        #if 1 >= floor <= 20:
            self.RunToFloor(floor)

    def pressButtonCloseDoors(self):
        self.doorStatus = "Открыты"

    def pressButtonOpenDoors(self):
        self.doorStatus = "Закрыты"

    def pressButtonCallDispatcher(self):
        self.CurrentStatusIndex = 5
        print(self.status[self.CurrentStatusIndex])
        print("Идёт вызов диспетчера")

    def RunToFloor(self, floor):
        if floor > self.CurretFloor:
            self.CurrentStatusIndex = 3
            print(self.status[self.CurrentStatusIndex])
            self.doorStatus = "Закрыты"

            self.CurrentStatusIndex = 0
            print(self.status[self.CurrentStatusIndex])

            print(f"Грузовой лифт едет на {floor} этаж")

            meters = (floor - self.CurretFloor + 1) * self.FLOORHEIGHT
            time.sleep(meters / self.SPEED)

            self.CurretFloor = floor
            print(f"Грузовой лифт приехал на {self.CurretFloor} этаж")

            self.CurrentStatusIndex = 2
            print(self.status[self.CurrentStatusIndex])
            self.doorStatus = "Открыты"


        elif floor < self.CurretFloor:
            self.CurrentStatusIndex = 3
            print(self.status[self.CurrentStatusIndex])
            self.doorStatus = "Закрыты"

            self.CurrentStatusIndex = 1
            print(self.status[self.CurrentStatusIndex])

            print(f"Грузовой лифт едет на {floor} этаж")

            meters = (self.CurretFloor - floor + 1) * self.FLOORHEIGHT
            time.sleep(meters / self.SPEED)

            self.CurretFloor = floor
            print(f"Грузовой лифт приехал на {self.CurretFloor} этаж")

            self.CurrentStatusIndex = 2
            print(self.status[self.CurrentStatusIndex])
            self.doorStatus = "Открыты"
            pass

        elif floor == self.CurretFloor:
            print(f"Грузовой лифт уже на {self.CurretFloor} этаже")
            self.doorStatus = "Открыты"
            self.CurrentStatusIndex = 4
            print(self.status[self.CurrentStatusIndex])


class Floor:
    BigElevatorClass, SmallElevatorClass = BigElevator(), SmallElevator()

    THISFLOOR = 0

    def __init__(self, a):
        self.THISFLOOR = a

    BigEvevatorFloor = 1
    BigEvevatorStatus = BigElevatorClass.GetStatus()

    SmallEvevatorFloor = 1
    SmallEvevatorStatus = SmallElevatorClass.GetStatus()

    def CallElevator(self):
        print(f"Лифт вызван на {self.THISFLOOR} этаж")
        if (abs(self.BigElevatorClass.CurretFloor - self.THISFLOOR)) < (
                abs(self.SmallElevatorClass.CurretFloor - self.THISFLOOR)):
            self.BigElevatorClass.RunToFloor(self.THISFLOOR)
        else:
            self.SmallElevatorClass.RunToFloor(self.THISFLOOR)
