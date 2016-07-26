from Eaglepy import COMMAND, ULObject, ULText


class ULAttribute(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("constant", int)
        self.createAttribute("defaultvalue", str)
        self.createAttribute("display", int)
        self.createAttribute("name", str)
        self.createAttribute("text", ULText)
        self.createAttribute("value", str)


class ULBaseAttribute(object):
    def __init__(self, owner, ul_name, datatype):
        self.parent = owner
        self.ul_name = ul_name
        self.datatype = datatype

    def cleanString(self, string):
        return string.replace("uF", "")


class ULMethodAttribute(ULBaseAttribute):
    def __init__(self, owner, ul_name, datatype):
        ULBaseAttribute.__init__(self, owner, ul_name, datatype)

    def __call__(self, cacheAhead=True):
        result = []
        path = self.parent.path() + "@" + self.ul_name
        resultString = instance().executeCommand(COMMAND.getattribute,
                                                 [path, int(cacheAhead)])

        if not resultString:
            return result

        handleReplyError(resultString)

        if cacheAhead:

            splitResult = splitEscapedString(resultString[1:], ":")
            for index, cachedItem in enumerate(splitResult):
                result.append(self.datatype(self).setIndex(index))
                cachedItem = cachedItem[:-1]
                splitCached = splitEscapedString(cachedItem, "?")
                for attrIndex, value in enumerate(splitCached):

                    try:
                        result[-1].simplePropertyList[attrIndex].cachedValue = \
                        result[-1].simplePropertyList[attrIndex].datatype(
                            self.cleanString(value))
                    except:
                        # print "ERROR: Unable to convert value to native type with value='%s' and type=%s" % (value,result[-1].simplePropertyList[attrIndex].datatype.__name__)
                        result[-1].simplePropertyList[attrIndex].cachedValue = \
                        result[-1].simplePropertyList[attrIndex].datatype()

            return result
        else:
            return [self.datatype(self).setIndex(index) for index in
                    range(int(resultString))]


class ULPropertyAttribute(ULBaseAttribute):
    def __init__(self, owner, ul_name, datatype):
        ULBaseAttribute.__init__(self, owner, ul_name, datatype)
        self.cachedValue = None

    def __call__(self, cached=True):
        return self.get(cached)

    def get(self, cached=True):
        if self.parent and self not in self.parent.simplePropertyList:
            return self
        if not cached or not self.cachedValue:
            path = self.path()
            self.cachedValue = self.datatype(
                instance().executeCommand(COMMAND.getattribute, [path]))

        return self.cachedValue

    def set(self, value):
        pass
        # path = self.path()
        # return self.datatype(instance().executeCommand(COMMAND.setattribute,[path + "?" + str(value)]))

    def __getattr__(self, attr):
        if attr == "value":
            if issubclass(self.__dict__["datatype"], ULObject):
                return self.__dict__["datatype"](self)

            else:
                return self.__dict__["datatype"]()
        elif attr == "__dict__":
            return self.__dict__
        elif attr == "path":
            if not issubclass(self.__dict__["datatype"], ULObject):
                def simplePropertyPath():
                    parent = self.__dict__["parent"]
                    pathList = parent.path()
                    pathList += "@" + self.__dict__["ul_name"] + "@" + str(
                        self.__dict__["datatype"].__name__)
                    return pathList

                return simplePropertyPath
            return getattr(self.value, attr)
        elif attr == "index":
            return getattr(self.value, attr)

        return getattr(self.value, attr)
