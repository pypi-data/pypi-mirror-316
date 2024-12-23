from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, Iterable, List


__all__ = ['Event', 'State', 'Task']


class Event(Enum):
    STARTED = "started"
    COMPLETED = "completed"
    EPOCH_STARTED = "epoch_started"
    EPOCH_COMPLETED = "epoch_completed"
    ITERATION_STARTED = "iteration_started"
    ITERATION_COMPLETED = "iteration_completed"


@dataclass
class State:
    epoch: int = 0
    batch: int = 0
    output: Any = None


class Task(object):
    def __init__(self, update: Callable, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__update: Callable = update
        self.__event_handlers: Dict[Event, List[Callable]] = {
            event: [] for event in Event
        }
        self.state = State()

    def run(self, data: Iterable, max_epochs: int) -> None:
        self.__fire_event(Event.STARTED)
        for epoch in range(max_epochs):
            self.state.epoch = epoch + 1
            self.__fire_event(Event.EPOCH_STARTED)
            for index, batch in enumerate(data):
                self.state.batch = index + 1
                self.__fire_event(Event.ITERATION_STARTED)
                self.state.output = self.__update(batch, index, epoch)
                self.__fire_event(Event.ITERATION_COMPLETED)
            self.__fire_event(Event.EPOCH_COMPLETED)
        self.__fire_event(Event.COMPLETED)

    def __fire_event(self, event: Event) -> None:
        for handler, args, kwargs in self.__event_handlers[event]:
            handler(*args, **kwargs)

    def add_event_handler(
        self, event: Event, handler: Callable, *args: Any, **kwargs: Any
    ) -> None:
        self.__event_handlers[event].append((handler, args, kwargs))
