import datetime

class Person:
    def __init__(self, name: str, year_of_birth: int, address: str = '') -> None:
        self._name: str = name
        self._yob: int = year_of_birth
        self._address: str = address

    @property
    def age(self) -> int:
        now: datetime.datetime = datetime.datetime.now()
        return now.year - self._yob

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def address(self) -> str:
        return self._address

    @address.setter
    def address(self, address: str) -> None:
        self._address = address

    def is_homeless(self) -> bool:
        return not self._address

