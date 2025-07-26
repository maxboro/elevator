from abc import ABC, abstractmethod

class Event(ABC):
    pass

class CallRequestOut(Event):
    pass

class CallRequestCabin(Event):
    pass

class State(ABC):
    
    @abstractmethod
    def handle_input(self, contex, event: Event, data: dict):
        pass

class MovingUp(State):
    def handle_input(self, contex, event: Event, data: dict):
        if contex.n_floor < data.get("destination_floor"):
            pass

class MovingDown(State):
    def handle_input(self, contex, event: Event, data: dict):
        pass

class DoorOpen(State):
    def handle_input(self, contex, event: Event, data: dict):
        pass

class Idle(State):
    def handle_input(self, contex, event: Event, data: dict):
        if isinstance(event, CallRequestOut) or isinstance(event, CallRequestCabin):
            if contex.n_floor < data.get("destination_floor"):
                print("Idle: We need to move up")
                return MovingUp()
            elif contex.n_floor > data.get("destination_floor"):
                print("Idle: We need to move down")
                return MovingDown()
            elif contex.n_floor == data.get("destination_floor"):
                print("Idle: We need to open the door")
                return DoorOpen()

class Elevator:
    """Context class."""
    def __init__(self, state: State, n_floor: int):
        self.state = state
        self.n_floor = n_floor

    def update(self, event: Event, **data):
        new_state = self.state.handle_input(self, event, data)
        if new_state != self.state:
            self.state = new_state

def main():
    elevator = Elevator(Idle(), 1)
    elevator.update(CallRequestOut(), destination_floor=4)
    elevator.update(CallRequestCabin(), destination_floor=1)

if __name__ == "__main__":
    main()