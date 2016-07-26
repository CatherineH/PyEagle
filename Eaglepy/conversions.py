from Eaglepy import GRID


def eagleToConfigured(value, configuredUnits=None):
    if configuredUnits is None:
        configuredUnits = ULContext().grid().unit()
    if configuredUnits == GRID.UNIT.MIC:
        return eagleToMic(value)
    elif configuredUnits == GRID.UNIT.MM:
        return eagleToMM(value)
    elif configuredUnits == GRID.UNIT.MIL:
        return eagleToMil(value)
    elif configuredUnits == GRID.UNIT.INCH:
        return eagleToInch(value)


def configuredToEagle(value, configuredUnits=None):
    if configuredUnits is None:
        configuredUnits = ULContext().grid().unit()
    if configuredUnits == GRID.UNIT.MIC:
        return micToEage(value)
    elif configuredUnits == GRID.UNIT.MM:
        return mmToEagle(value)
    elif configuredUnits == GRID.UNIT.MIL:
        return milToEagle(value)
    elif configuredUnits == GRID.UNIT.INCH:
        return inchToEagle(value)


def unitToUnit(value, firstType, secondType):
    return eagleToConfigured(configuredToEagle(value, firstType), secondType)


def eagleToMic(value):
    return value * 0.003125


def eagleToMM(value):
    return value * 0.000003125


def eagleToMil(value):
    return value * 0.0001230314959375


def eagleToInch(value):
    return value * 0.0000001230314959375


def micToEage(value):
    return value / 0.003125


def mmToEagle(value):
    return value / 0.000003125


def milToEagle(value):
    return value / 0.0001230314959375


def inchToEagle(value):
    return value / 0.0000001230314959375