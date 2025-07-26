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
    def handle_input(self, context: "Elevator", event: Event, data: dict):
        pass


class Moving(State):
    step = None
    def handle_input(self, context: "Elevator", event: Event, data: dict):
        if not isinstance(event, Tick):
            return self

        context.n_floor += self.step
        print(f"{self.__class__.__name__}: floor {context.n_floor}")
        if context.n_floor != context.destination_floor:
            return self
        if context.n_floor == context.destination_floor:
            print(f"{self.__class__.__name__}: destination floor {context.n_floor}")
            context.destination_floor = None
            return DoorOpen()


class MovingUp(Moving):
    step = 1


class MovingDown(Moving):
    step = -1


class DoorOpen(State):
    def handle_input(self, context: "Elevator", event: Event, data: dict):
        if not isinstance(event, Tick):
            return self
        print("Door opened")
        return Idle()


class Idle(State):
    def handle_input(self, context: "Elevator", event: Event, data: dict):
        if isinstance(event, CallRequestOut) or isinstance(event, CallRequestCabin):
            if context.n_floor == context.destination_floor:
                print("Idle: We need to open the door")
                return DoorOpen()
            else:
                if context.destination_floor is None:
                    context.destination_floor = data.get("destination_floor")
                if context.n_floor < context.destination_floor:
                    print("Idle: We need to move up")
                    return MovingUp()
                elif context.n_floor > context.destination_floor:
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
