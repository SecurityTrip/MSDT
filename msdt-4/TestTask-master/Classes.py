import time
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

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
        self.RunToFloor(floor)

    def pressButtonCloseDoors(self):
        self.doorStatus = "Закрыты"
        logging.info("Двери лифта закрыты")

    def pressButtonOpenDoors(self):
        self.doorStatus = "Открыты"
        logging.info("Двери лифта открыты")

    def pressButtonCallDispatcher(self):
        self.CurrentStatusIndex = 5
        logging.warning(f"{self.status[self.CurrentStatusIndex]}: Идёт вызов диспетчера")

    def RunToFloor(self, floor):
        if floor > self.CurretFloor:
            self.CurrentStatusIndex = 3
            logging.info(self.status[self.CurrentStatusIndex])
            self.doorStatus = "Закрыты"

            self.CurrentStatusIndex = 0
            logging.info(self.status[self.CurrentStatusIndex])
            logging.info(f"Пассажирский лифт едет на {floor} этаж")

            meters = (floor - self.CurretFloor + 1) * self.FLOORHEIGHT
            time.sleep(meters / self.SPEED)

            self.CurretFloor = floor
            logging.info(f"Пассажирский лифт приехал на {self.CurretFloor} этаж")

            self.CurrentStatusIndex = 2
            logging.info(self.status[self.CurrentStatusIndex])
            self.doorStatus = "Открыты"

        elif floor < self.CurretFloor:
            self.CurrentStatusIndex = 3
            logging.info(self.status[self.CurrentStatusIndex])
            self.doorStatus = "Закрыты"

            self.CurrentStatusIndex = 1
            logging.info(self.status[self.CurrentStatusIndex])
            logging.info(f"Пассажирский лифт едет на {floor} этаж")

            meters = (self.CurretFloor - floor + 1) * self.FLOORHEIGHT
            time.sleep(meters / self.SPEED)

            self.CurretFloor = floor
            logging.info(f"Пассажирский лифт приехал на {self.CurretFloor} этаж")

            self.CurrentStatusIndex = 2
            logging.info(self.status[self.CurrentStatusIndex])
            self.doorStatus = "Открыты"

        else:
            logging.info(f"Пассажирский лифт уже на {self.CurretFloor} этаже")
            self.doorStatus = "Открыты"
            self.CurrentStatusIndex = 4
            logging.info(self.status[self.CurrentStatusIndex])

# Аналогично обновляем BigElevator, меняя сообщения на соответствующие
class BigElevator(SmallElevator):  # Грузовой лифт
    MAXWEIGHT = 800
    MAXPEOPLE = 10
    SPEED = 1.8  # m/s

# Обновляем класс Floor
class Floor:
    BigElevatorClass, SmallElevatorClass = BigElevator(), SmallElevator()
    THISFLOOR = 0

    def __init__(self, a):
        self.THISFLOOR = a

    def CallElevator(self):
        logging.info(f"Лифт вызван на {self.THISFLOOR} этаж")
        if abs(self.BigElevatorClass.CurretFloor - self.THISFLOOR) < abs(self.SmallElevatorClass.CurretFloor - self.THISFLOOR):
            self.BigElevatorClass.RunToFloor(self.THISFLOOR)
        else:
            self.SmallElevatorClass.RunToFloor(self.THISFLOOR)
