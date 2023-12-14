class TransientObject:
    __CurrentData = dict[str, object]()

    def __init__(self):

        data = list[str]()
        pass

    def GetValue[T](self, key: str, defaulValue: T = None) -> T:
        if key in self.__CurrentData:
            return self.__CurrentData[key]
        elif defaulValue is not None:
            return defaulValue

        return None

    def SetValue[T](self, key: str, value: T) -> None:
        self.__CurrentData[key] = value

    def GetCurrent(self):
        return self.__CurrentData

    def SetCurrent(self, dictionary: dict[str, object]) -> None:
        self.__CurrentData = dictionary
