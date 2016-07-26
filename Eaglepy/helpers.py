import re
from types import ListType

from Eaglepy import EaglepyException, ERROR_VALUES, instance, COMMAND, \
    CONTEXT, ULSheet, ULBoard, ULPackage, PALETTE, GRID


def splitEscapedString(unescaped, splitchar):
    skipNext = False
    currentString = ""
    result = []
    for index, char in enumerate(unescaped):
        if skipNext:
            skipNext = False
            continue

        if char == "\\":
            if index + 1 < len(unescaped) and unescaped[index + 1] == splitchar:
                currentString += splitchar
                skipNext = True
                continue
            else:
                currentString += "\\"
                continue

        if char == splitchar:
            result.append(currentString)
            currentString = ""
            continue
        currentString += char
    result.append(currentString)
    return result




def handleReplyError(resultString):
    errors = re.search("ERROR:(\d+)", resultString)
    if errors:
        value = int(errors.group(1))
        raise EaglepyException(ERROR_VALUES[value - 1] + " id:" + str(value))

    return resultString


def marker(value=None, relative=False):
    if value and len(value) != 2:
        raise EaglepyException("marker value must be a tuple of numeric values")
    if not value:
        executescr("Mark;")
    else:
        relativeValue = "R" if relative else ""
        executescr("Mark (%s%f %s%f);" % (
        relativeValue, value[0], relativeValue, value[1]))


def dlgMessageBox(message):
    return handleReplyError(
        instance().executeCommand(COMMAND.dlgMessageBox, [message]))


def executescr(script):
    result = handleReplyError(
        instance().executeCommand(COMMAND.executescr, [script]))


def _objectsFromIndicies(result):
    splitResult = result.split(":")

    context = int(splitResult[0])

    resultList = []

    netIndicies = []
    elementIndicies = []
    instanceIndicies = []
    circleIndicies = []
    framesIndicies = []
    polygonsIndicies = []
    rectanglesIndicies = []
    textsIndicies = []
    wiresIndicies = []
    holesIndicies = []
    signalsIndicies = []
    contactIndicies = []

    netList = []
    elementList = []
    instanceList = []
    circleList = []
    framesList = []
    polygonsList = []
    rectanglesList = []
    textsList = []
    wiresList = []
    holesList = []
    signalsList = []
    contactList = []

    if context == CONTEXT.SHEET:

        netIndicies = [int(i) for i in splitResult[1].split("#") if i]
        instanceIndicies = [int(i) for i in splitResult[2].split("#") if i]
        circleIndicies = [int(i) for i in splitResult[3].split("#") if i]
        framesIndicies = [int(i) for i in splitResult[4].split("#") if i]
        polygonsIndicies = [int(i) for i in splitResult[5].split("#") if i]
        rectanglesIndicies = [int(i) for i in splitResult[6].split("#") if i]
        textsIndicies = [int(i) for i in splitResult[7].split("#") if i]
        wiresIndicies = [int(i) for i in splitResult[8].split("#") if i]

        netList = ULSheet().nets()
        instanceList = ULSheet().instances()
        circleList = ULSheet().circles()
        framesList = ULSheet().frames()
        polygonsList = ULSheet().polygons()
        rectanglesList = ULSheet().rectangles()
        textsList = ULSheet().texts()
        wiresList = ULSheet().wires()



    elif context == CONTEXT.BOARD:

        circleIndicies = [int(i) for i in splitResult[1].split("#") if i]
        elementIndicies = [int(i) for i in splitResult[2].split("#") if i]
        framesIndicies = [int(i) for i in splitResult[3].split("#") if i]
        holesIndicies = [int(i) for i in splitResult[4].split("#") if i]
        polygonsIndicies = [int(i) for i in splitResult[5].split("#") if i]
        rectanglesIndicies = [int(i) for i in splitResult[6].split("#") if i]
        signalsIndicies = [int(i) for i in splitResult[7].split("#") if i]
        textsIndicies = [int(i) for i in splitResult[8].split("#") if i]
        wiresIndicies = [int(i) for i in splitResult[9].split("#") if i]

        circleList = ULBoard().circles()
        elementList = ULBoard().elements()
        framesList = ULBoard().frames()
        holesList = ULBoard().holes()
        polygonsList = ULBoard().polygons()
        rectanglesList = ULBoard().rectangles()
        signalsList = ULBoard().signals()
        textsList = ULBoard().texts()
        wiresList = ULBoard().wires()

    elif context == CONTEXT.PACKAGE:
        circleIndicies = [int(i) for i in splitResult[1].split("#") if i]
        contactIndicies = [int(i) for i in splitResult[2].split("#") if i]

        circleList = ULPackage().circles()
        contactList = ULPackage().contacts()
        print(contactIndicies)
        print(contactList)

    for index in netIndicies:
        resultList.append(netList[index])
    for index in elementIndicies:
        resultList.append(elementList[index])
    for index in instanceIndicies:
        resultList.append(instanceList[index])
    for index in circleIndicies:
        resultList.append(circleList[index])
    for index in framesIndicies:
        resultList.append(framesList[index])
    for index in polygonsIndicies:
        resultList.append(polygonsList[index])
    for index in rectanglesIndicies:
        resultList.append(rectanglesList[index])
    for index in textsIndicies:
        resultList.append(textsList[index])
    for index in wiresIndicies:
        resultList.append(wiresList[index])
    for index in holesIndicies:
        resultList.append(holesList[index])
    for index in signalsIndicies:
        resultList.append(signalsList[index])
    for index in contactIndicies:
        resultList.append(contactList[index])

    return resultList


__allobjects_cached_list = []


def allobjects():
    for index in range(len(__allobjects_cached_list)):
        __allobjects_cached_list.pop(0)
    for item in _objectsFromIndicies(
            handleReplyError(instance().executeCommand(COMMAND.allobjects))):
        __allobjects_cached_list.append(item)
    return __allobjects_cached_list


def selected():
    return _objectsFromIndicies(
        handleReplyError(instance().executeCommand(COMMAND.getselected)))


def move(objectname, unitx, unity):
    executescr("MOVE %s (%f %f);" % (objectname, unitx, unity))


def rename(oldname, newname):
    executescr("NAME %s %s;" % (oldname, newname))


def ingroup(objects):
    multi = False
    if isinstance(objects, ListType):
        multi = True

    objectsArg = objects if not multi else ";".join(objects)

    result = instance().executeCommand(COMMAND.ingroup, [objectsArg])


def palette(index, type=PALETTE.DEFAULT):
    if index < 0 or index > PALETTE.ENTRIES - 1:
        raise EaglepyException(
            "Invalid index %d. 0<index<%d" % (index, PALETTE.ENTRIES))
    if type < PALETTE.DEFAULT or type > 2:
        raise EaglepyException("Invalie type index %d" % type)

    result = instance().executeCommand(COMMAND.palette, [index, type])
    result = int(result)
    color = (
    result >> 16 & 255, result >> 8 & 255, result & 255, result >> 24 & 255)
    return color


def paletteall(type=PALETTE.DEFAULT):
    if type < PALETTE.DEFAULT or type > 2:
        raise EaglepyException("Invalie type index %d" % type)

    result = instance().executeCommand(COMMAND.paletteall, [type])
    entries = []
    for colorstr in result[1:].split(":"):
        color = int(colorstr)
        entries.append((color >> 16 & 255, color >> 8 & 255, color & 255,
                        color >> 24 & 255))

    return entries


def executescr(script):
    instance().executeCommand(COMMAND.executescr, [script])


def status(message):
    instance().executeCommand(COMMAND.status, [message])


def moveobjects(objects, x, y):
    moveObjects = [objects]
    if isinstance(objects, ListType):
        moveObjects = objects

    script = ""
    for object in moveObjects:
        script += "MOVE " + object + (" (%f %f);" % (x, y))
    instance().executeCommand(COMMAND.executescr, [script])


def clrgroup(objects):
    pass


def refreshview(): window()


def window():
    instance().executeCommand(COMMAND.executescr, ["Window;"])


def clrgroupall():
    result = instance().executeCommand(COMMAND.clrgroupall)


def addgroup(objects):
    pass


def setgroup(objects):
    multi = False
    if isinstance(objects, ListType):
        multi = True

    objectsArg = objects if not multi else ";".join(objects)
    clrgroupall()
    result = instance().executeCommand(COMMAND.setgroup, [objectsArg])


def setGridUnitType(value):
    script = "GRID "
    if value == GRID.UNIT.MIC:
        script += "MIC;"
    elif value == GRID.UNIT.MM:
        script += "MM;"
    elif value == GRID.UNIT.MIL:
        script += "MIL;"
    elif value == GRID.UNIT.INCH:
        script += "INCH;"
    else:
        raise EaglepyException("Invalid unit type %s." % value)

    instance().executeCommand(COMMAND.executescr, [script])


def setGridUnitValue(value=-1):
    script = "GRID "
    if value == GRID.VALUE.FINEST:
        script += "FINEST;"
    elif value == GRID.VALUE.LAST:
        script += "LAST;"
    elif value == GRID.VALUE.DEFAULT or value == 0:
        script += "DEFAULT;"
    else:
        script += str(value)

    instance().executeCommand(COMMAND.executescr, [script])


def getcontext():
    return int(instance().executeCommand(COMMAND.getcontext))

