import pytest
from Classes import SmallElevator, BigElevator, Floor

@pytest.fixture
def small_elevator():
    return SmallElevator()

@pytest.fixture
def big_elevator():
    return BigElevator()

@pytest.fixture
def floor_instance():
    return Floor(5)

# Тест Singleton поведения
def test_singleton_behavior(small_elevator, big_elevator):
    another_small = SmallElevator()
    another_big = BigElevator()
    assert small_elevator is another_small
    assert big_elevator is another_big

# Тесты для SmallElevator
def test_small_elevator_initial_state(small_elevator):
    assert small_elevator.CurretFloor == 1
    assert small_elevator.GetStatus() == "Стоит с открытыми дверьми"
    assert small_elevator.doorStatus == "Открыты"

def test_small_elevator_move_up(small_elevator):
    small_elevator.pressButtonFloor(5)
    assert small_elevator.CurretFloor == 5
    assert small_elevator.GetStatus() == "Открывает двери"
    assert small_elevator.doorStatus == "Открыты"

def test_small_elevator_move_down(small_elevator):
    small_elevator.CurretFloor = 10
    small_elevator.pressButtonFloor(3)
    assert small_elevator.CurretFloor == 3
    assert small_elevator.GetStatus() == "Открывает двери"
    assert small_elevator.doorStatus == "Открыты"

# Тесты для BigElevator
def test_big_elevator_initial_state(big_elevator):
    assert big_elevator.CurretFloor == 1
    assert big_elevator.GetStatus() == "Стоит с открытыми дверьми"
    assert big_elevator.doorStatus == "Открыты"

def test_big_elevator_move_up(big_elevator):
    big_elevator.pressButtonFloor(8)
    assert big_elevator.CurretFloor == 8
    assert big_elevator.GetStatus() == "Открывает двери"
    assert big_elevator.doorStatus == "Открыты"

def test_big_elevator_move_down(big_elevator):
    big_elevator.CurretFloor = 15
    big_elevator.pressButtonFloor(7)
    assert big_elevator.CurretFloor == 7
    assert big_elevator.GetStatus() == "Открывает двери"
    assert big_elevator.doorStatus == "Открыты"

# Тесты для Floor
def test_floor_call_elevator(floor_instance):
    floor_instance.BigElevatorClass.CurretFloor = 2
    floor_instance.SmallElevatorClass.CurretFloor = 7
    floor_instance.CallElevator()
    assert floor_instance.BigElevatorClass.CurretFloor == 5 or floor_instance.SmallElevatorClass.CurretFloor == 5

def test_floor_initialization():
    floor = Floor(10)
    assert floor.THISFLOOR == 10

# Тест вызова диспетчера
def test_call_dispatcher(small_elevator, big_elevator):
    small_elevator.pressButtonCallDispatcher()
    assert small_elevator.GetStatus() == "Вызов диспетчера"
    big_elevator.pressButtonCallDispatcher()
    assert big_elevator.GetStatus() == "Вызов диспетчера"
