# Description
Finite state machine pattern demonstration in elevator case.

# Example
elevator use:
```python
elevator = Elevator(Idle(), 1)
elevator.update(Tick())
elevator.update(Tick())
elevator.update(CallRequestOut(), destination_floor=7)
elevator.run_until_idle()
elevator.update(CallRequestCabin(), destination_floor=1)
elevator.run_until_idle()
```

Execution result:
```terminal
Event detected: Unit of time passes.
Idle: Waiting for commands
Event detected: Unit of time passes.
Idle: Waiting for commands
Event detected: Call request from external panel.
Idle: We need to move up
Event detected: Unit of time passes.
MovingUp: floor 2
Event detected: Unit of time passes.
MovingUp: floor 3
Event detected: Unit of time passes.
MovingUp: floor 4
Event detected: Unit of time passes.
MovingUp: floor 5
Event detected: Unit of time passes.
MovingUp: floor 6
Event detected: Unit of time passes.
MovingUp: floor 7
MovingUp: destination floor 7
Event detected: Unit of time passes.
Door opened
Event detected: Call request from cabin panel.
Idle: We need to move down
Event detected: Unit of time passes.
MovingDown: floor 6
Event detected: Unit of time passes.
MovingDown: floor 5
Event detected: Unit of time passes.
MovingDown: floor 4
Event detected: Unit of time passes.
MovingDown: floor 3
Event detected: Unit of time passes.
MovingDown: floor 2
Event detected: Unit of time passes.
MovingDown: floor 1
MovingDown: destination floor 1
Event detected: Unit of time passes.
Door opened
```