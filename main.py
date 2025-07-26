from abc import ABC, abstractmethod

class Event(ABC):
    description = ""
    def __repr__(self):
        return self.description

class CallRequestOut(Event):
    description = "Call request from external panel."

class CallRequestCabin(Event):
    description = "Call request from cabin panel."

class Tick(Event):
    description = "Unit of time passes."

class State(ABC):
    
    @abstractmethod
    def handle_input(self, contex, event: Event, data: dict):
        pass

class MovingUp(State):
    def handle_input(self, contex, event: Event, data: dict):
        contex.n_floor += 1
        print(f"MovingUp: floor {contex.n_floor}")
        if contex.n_floor < contex.destination_floor:
            return MovingUp()
        if contex.n_floor == contex.destination_floor:
            print(f"MovingUp: destination floor {contex.n_floor}")
            contex.destination_floor = None
            return DoorOpen()

class MovingDown(State):
    def handle_input(self, contex, event: Event, data: dict):
        contex.n_floor -= 1
        print(f"MovingDown: floor {contex.n_floor}")
        if contex.n_floor > contex.destination_floor:
            return MovingDown()
        if contex.n_floor == contex.destination_floor:
            print(f"MovingDown: destination floor {contex.n_floor}")
            contex.destination_floor = None
            return DoorOpen()

class DoorOpen(State):
    def handle_input(self, contex, event: Event, data: dict):
        print("Door opened")
        return Idle()

class Idle(State):
    def handle_input(self, contex, event: Event, data: dict):
        if isinstance(event, CallRequestOut) or isinstance(event, CallRequestCabin):
            if contex.n_floor == contex.destination_floor:
                print("Idle: We need to open the door")
                return DoorOpen()
            else:
                if contex.destination_floor is None:
                    contex.destination_floor = data.get("destination_floor")
                if contex.n_floor < contex.destination_floor:
                    print("Idle: We need to move up")
                    return MovingUp()
                elif contex.n_floor > contex.destination_floor:
                    print("Idle: We need to move down")
                    return MovingDown()
        elif isinstance(event, Tick):
            print("Idle: Waiting for commands")
            return Idle()
            

class Elevator:
    """Context class."""
    def __init__(self, state: State, n_floor: int):
        self.state = state
        self.n_floor = n_floor
        self.destination_floor = None

    def update(self, event: Event, **data):
        if event:
            print(f"Event detected: {event}")
        new_state = self.state.handle_input(self, event, data)
        if new_state != self.state:
            self.state = new_state
    
    def run_until_idle(self):
        while type(self.state) != Idle:
            self.update(Tick())

def main():
    elevator = Elevator(Idle(), 1)
    elevator.update(Tick())
    elevator.update(Tick())
    elevator.update(CallRequestOut(), destination_floor=7)
    elevator.run_until_idle()
    elevator.update(CallRequestCabin(), destination_floor=1)
    elevator.run_until_idle()

if __name__ == "__main__":
    main()
