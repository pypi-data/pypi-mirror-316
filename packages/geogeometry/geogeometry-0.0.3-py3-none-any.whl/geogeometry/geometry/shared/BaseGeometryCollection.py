from abc import ABC, abstractmethod
from typing import List, TypeVar, Iterator, Optional, Union, Generic, TYPE_CHECKING

if TYPE_CHECKING:
    import pyvista as pv

T = TypeVar('T')


class BaseGeometryCollection(Generic[T], ABC):

    def __init__(self, name: Optional[str] = None):
        self.name: Optional[str] = name
        self.id: int = id(self)

        # Plot properties
        self.color: str = 'red'
        self.opacity: float = 1.0

        self.elements: List[T] = []

    def __len__(self) -> int:
        return len(self.elements)

    def __iter__(self) -> Iterator[T]:
        for e in self.elements:
            yield e

    def __getitem__(self, identifier: Union[int, str]) -> T:
        if isinstance(identifier, int):
            return self.elements[identifier]
        else:
            for e in self.elements:
                if e.getName() == identifier:
                    return e
            else:
                raise ValueError(f"Element '{identifier}' not found in collection.")

    def setName(self, name: str) -> None:
        self.name = name

    def setColor(self, color: str) -> None:
        self.color = color

    def setOpacity(self, opacity: float) -> None:
        self.opacity = opacity

    def getName(self) -> Optional[str]:
        return self.name

    def getColor(self) -> str:
        return self.color

    def getOpacity(self) -> float:
        return self.opacity

    def addElement(self, element: T) -> None:
        self.elements += [element]

    def deleteElement(self, identifier: Union[int, str]):
        for e in self.elements:
            if e.getName() == identifier:
                self.elements.remove(e)
                break
        else:
            raise ValueError(f"Element '{identifier}' not found in collection.")

    @abstractmethod
    def addToPyvistaPlotter(self, plotter: 'pv.Plotter', **kwargs) -> None: ...

    @abstractmethod
    def plot3d(self, screenshot: bool = False, filepath: Optional[str] = None, **kwargs) -> None: ...
