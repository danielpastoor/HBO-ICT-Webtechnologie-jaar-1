class TransientObject:
    __CurrentData = dict[str, object]()

    def __init__(self):
        pass

    def GetValue(self, key: str, defaulValue: object = None) -> object:
        if key in self.__CurrentData:
            return self.__CurrentData[key]
        elif defaulValue is not None:
            return defaulValue

        return None

    def SetValue(self, key: str, value: object) -> None:
        self.__CurrentData[key] = value

    def GetCurrent(self):
        return self.__CurrentData
