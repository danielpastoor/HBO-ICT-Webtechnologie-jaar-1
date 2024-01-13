class TransientObject:
    def __createCurrentIfNotExist(self):
        if "_TransientObject__CurrentData" not in self.__dict__ and "__CurrentData" not in self.__dict__:
           self.__CurrentData = {}

    def GetValue[T](self, key: str, defaulValue: T = None) -> T:
        self.__createCurrentIfNotExist()
        if key in self.__CurrentData:
            return self.__CurrentData[key]
        elif defaulValue is not None:
            return defaulValue

        return None

    def SetValue[T](self, key: str, value: T) -> None:
        self.__createCurrentIfNotExist()
        self.__CurrentData[key] = value

    def GetCurrent(self):
        self.__createCurrentIfNotExist()
        return self.__CurrentData

    def SetCurrent(self, dictionary: dict[str, object]) -> None:
        self.__createCurrentIfNotExist()
        self.__CurrentData = dictionary
