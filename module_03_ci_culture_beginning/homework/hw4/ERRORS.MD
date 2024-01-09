# Ошибки #
* Не импортирован модуль datetime
> import datetime
* Из текущей даты вычитается год рождения
> return now.year - self.yob
* Отсутствовало обращение к экземпляру класса, в следствие чего получалось, что переменная address не определена
> return self.address is None
* Метод is_homeless не соответствовал документации: returns True if address is not set, false in other case
> return not self._address
* Геттеры и сеттеры были написаны неправильно, без декоратора @property
> * @property
    def age(self)
> * @property
    def name(self) -> str:
> * @name.setter
    def name(self, name: str) -> None:
> * @property
    def address(self) -> str:
> * @address.setter
    def address(self, address: str) -> None:
* Переменные в инициализаторе не были снабжены нижними подчёркиваниями
> self._name: str = name
  self._yob: int = year_of_birth
  self._address: str = address
* В сеттере name было неправильное присвоение: self.name = self.name
> self._name = name
* В сеттере address было сравнение вместо присвоения: self.address == address
> self._address = address