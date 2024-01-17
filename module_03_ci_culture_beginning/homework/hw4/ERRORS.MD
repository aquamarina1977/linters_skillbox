#Ошибки#
* В методе set_name(self, name) необходимо изменить значение переменной self.name на значение переданное в параметре name. Исправленный код:

> def set_name(self, name):
    self.name = name
* В методе set_address(self, address) ошибка в операторе сравнения. Вместо == нужно использовать = для присваивания значения переменной self.address. Исправленный код:

> def set_address(self, address):
    self.address = address
* В методе is_homeless(self) ошибка при проверке переменной address. Вместо address нужно использовать self.address. Исправленный код:

> def is_homeless(self):
    '''
    returns True if address is not set, false in other case
    '''
    return self.address is None



