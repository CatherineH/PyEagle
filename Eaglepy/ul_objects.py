from types import ListType
import os

from Eaglepy import configuredToEagle, ULMethodAttribute, ULPropertyAttribute, \
    COMMAND, CONTEXT, EaglepyException



class ULObject(object):
    def __init__(self, parent=None):
        self.ul_name = str(self.__class__.__name__)
        self.parent = parent
        self.simplePropertyList = []
        self.index = -1
        self.args = None

    def createAttribute(self, ul_name, datatype, writeable=False, readable=True,
                        args=None):
        self.args = args
        if isinstance(datatype, ListType):
            self.__dict__[ul_name] = ULMethodAttribute(self, ul_name,
                                                       datatype[0])
        else:
            self.__dict__[ul_name] = ULPropertyAttribute(self, ul_name,
                                                         datatype)
            if issubclass(datatype, (str, int, float)) and not self.args:
                self.simplePropertyList.append(self.__dict__[ul_name])

        if ul_name == "name" and datatype == str:
            def rename_func(newname):

                globals()["rename"](self.name(), newname)

            self.rename = rename_func

        elif ul_name == "x":
            def move_func(unitx, unity, currentUnits=None):

                eaglex = configuredToEagle(unitx, currentUnits)
                eagley = configuredToEagle(unity, currentUnits)
                self.x.__dict__["cachedValue"] = eaglex
                self.y.__dict__["cachedValue"] = eagley
                globals()["move"](self.name(), unitx, unity)

            self.move = move_func

    def setIndex(self, index):
        self.__dict__["index"] = index
        return self

    def path(self):

        pathList = []
        parent = self
        while parent:

            if hasattr(parent, "index") and parent.index >= 0:
                pathList.append(str(parent.index))
                pathList.append("^")
            pathList.append(parent.ul_name)
            pathList.append("@")
            parent = parent.parent
        pathList.reverse()
        return "".join(pathList)


class ULClass(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("clearance", int, args=[(None), (int)])
        self.createAttribute("drill", int)
        self.createAttribute("name", str)
        self.createAttribute("number", int)
        self.createAttribute("width", int)


class ULGate(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("addlevel", int)
        self.createAttribute("name", str)
        self.createAttribute("swaplevel", int)
        self.createAttribute("symbol", ULSymbol)
        self.createAttribute("x", int)
        self.createAttribute("y", int)


class ULPinRef(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("contact", ULPart)
        self.createAttribute("direction", ULPin)


class ULPin(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("angle", float)
        self.createAttribute("direction", int)
        self.createAttribute("function", int)
        self.createAttribute("length", int)
        self.createAttribute("name", str)
        self.createAttribute("net", str)
        self.createAttribute("route", int)
        self.createAttribute("swaplevel", int)
        self.createAttribute("visible", int)
        self.createAttribute("x", int)
        self.createAttribute("y", int)
        self.createAttribute("circles", [ULCircle])
        self.createAttribute("contacts", [ULContact])
        self.createAttribute("texts", [ULText])
        self.createAttribute("wires", [ULWire])


class ULNet(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("class", ULClass)
        self.createAttribute("column", str)
        self.createAttribute("name", str)
        self.createAttribute("row", str)
        self.createAttribute("pinrefs", [ULPinRef])
        self.createAttribute("segments", [ULSegment])


class ULLabel(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("angle", float)
        self.createAttribute("layer", int)
        self.createAttribute("mirror", int)
        self.createAttribute("spin", int)
        self.createAttribute("text", ULText)
        self.createAttribute("x", int)
        self.createAttribute("y", int)
        self.createAttribute("xref", int)
        self.createAttribute("wires", [ULWire])


class ULSegment(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("junctions", [ULJunction])
        self.createAttribute("labels", [ULLabel])
        self.createAttribute("pinrefs", [ULPinRef])
        self.createAttribute("texts", [ULText])
        self.createAttribute("wires", [ULWire])


class ULPart(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("attribute", str, args=[(int)])
        self.createAttribute("device", ULDevice)
        self.createAttribute("deviceset", [ULDeviceSet])
        self.createAttribute("name", str)
        self.createAttribute("populate", int)
        self.createAttribute("value", str)
        self.createAttribute("attributes", [ULAttribute])
        self.createAttribute("variants", [ULVariant])
        self.createAttribute("instances", [ULInstance])


class ULSignal(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("airwireshidden", int)
        self.createAttribute("class", ULClass)
        self.createAttribute("name", str)
        self.createAttribute("contactrefs", [ULContactRef])
        self.createAttribute("polygons", [ULPolygon])
        self.createAttribute("vias", [ULVia])
        self.createAttribute("wires", [ULWire])


class ULSymbol(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("area", [ULArea])
        self.createAttribute("description", str)
        self.createAttribute("headline", str)
        self.createAttribute("library", str)
        self.createAttribute("name", str)
        self.createAttribute("circles", [ULCircle])
        self.createAttribute("dimensions", [ULDimension])
        self.createAttribute("frames", [ULFrame])
        self.createAttribute("rectangles", [ULRectangle])
        self.createAttribute("pins", [ULPin])
        self.createAttribute("polygons", [ULPolygon])
        self.createAttribute("texts", [ULText])
        self.createAttribute("wires", [ULWire])


class ULDeviceSet(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("activedevice", ULDevice)
        self.createAttribute("area", ULArea)
        self.createAttribute("description", str)
        self.createAttribute("headline", str)
        self.createAttribute("library", str)
        self.createAttribute("name", str)
        self.createAttribute("prefix", str)
        self.createAttribute("value", str)
        self.createAttribute("devices", [ULDevice])
        self.createAttribute("gates", [ULGate])


class ULDevice(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("activetechnology", str)
        self.createAttribute("area", ULArea)
        self.createAttribute("description", str)
        self.createAttribute("headline", str)
        self.createAttribute("library", str)
        self.createAttribute("name", str)
        self.createAttribute("package", ULPackage)
        self.createAttribute("prefix", str)
        self.createAttribute("technologies", str)
        self.createAttribute("value", str)
        self.createAttribute("attributes", [ULAttribute])
        self.createAttribute("gates", [ULGate])


class ULLibrary(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("description", str)
        self.createAttribute("grid", ULGrid)
        self.createAttribute("headline", str)
        self.createAttribute("name", str)
        self.createAttribute("devices", [ULDevice])
        self.createAttribute("devicesets", [ULDeviceSet])
        self.createAttribute("layers", [ULLayer])
        self.createAttribute("packages", [ULPackage])
        self.createAttribute("symbols", [ULSymbol])


class ULPackage(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("area", ULArea)
        self.createAttribute("description", str)
        self.createAttribute("headline", str)
        self.createAttribute("library", str)
        self.createAttribute("name", str)
        self.createAttribute("circles", [ULCircle])
        self.createAttribute("contacts", [ULContact])
        self.createAttribute("dimensions", [ULDimension])
        self.createAttribute("frames", [ULFrame])
        self.createAttribute("holes", [ULHole])
        self.createAttribute("rectangles", [ULRectangle])
        self.createAttribute("texts", [ULText])
        self.createAttribute("wires", [ULWire])


class ULContactRef(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)

        self.createAttribute("contact", ULContact)
        self.createAttribute("element", ULElement)
        self.createAttribute("route", int)
        self.createAttribute("routetag", str)


class ULVia(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)

        self.createAttribute("drill", int)
        self.createAttribute("drillsymbol", int)
        self.createAttribute("end", int)
        self.createAttribute("flags", int)
        self.createAttribute("shape", int, args=[(int)])
        self.createAttribute("start", int)
        self.createAttribute("x", int)
        self.createAttribute("y", int)


class ULBus(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("name", str)
        self.createAttribute("segments", [ULSegment])


class ULJunction(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("diameter", int)
        self.createAttribute("x", int)
        self.createAttribute("y", int)


class ULVariantDef(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("name", str)


class ULVariant(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("populate", int)
        self.createAttribute("value", str)
        self.createAttribute("technology", str)
        self.createAttribute("variantdef", str)


class ULRectangle(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("angle", float)
        self.createAttribute("layer", int)
        self.createAttribute("x1", int)
        self.createAttribute("x2", int)
        self.createAttribute("y1", int)
        self.createAttribute("y2", int)


class ULHole(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("diameter", int, args=[(int)])
        self.createAttribute("drill", int)
        self.createAttribute("drillsymbol", int)
        self.createAttribute("x", int)
        self.createAttribute("y", int)


class ULFrame(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("columns", int)
        self.createAttribute("rows", int)
        self.createAttribute("border", int)
        self.createAttribute("x1", int)
        self.createAttribute("x2", int)
        self.createAttribute("y1", int)
        self.createAttribute("y2", int)
        self.createAttribute("texts", [ULText])
        self.createAttribute("fillings", [ULWire])


class ULPolygon(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("isolate", int)
        self.createAttribute("layer", int)
        self.createAttribute("orphans", int)
        self.createAttribute("pour", int)
        self.createAttribute("rank", int)
        self.createAttribute("spacing", int)
        self.createAttribute("thermals", int)
        self.createAttribute("width", int)
        self.createAttribute("contours", [ULWire])
        self.createAttribute("fillings", [ULWire])
        self.createAttribute("wires", [ULWire])


class ULContact(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("name", str)
        self.createAttribute("pad", ULPad)
        self.createAttribute("signal", str)
        self.createAttribute("smd", ULSmd)
        self.createAttribute("x", int)
        self.createAttribute("y", int)
        self.createAttribute("polygons", [ULPolygon])
        self.createAttribute("wires", [ULWire])


class ULSmd(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("angle", float)
        self.createAttribute("dx", float, args=[(int)])
        self.createAttribute("dy", float, args=[(int)])
        self.createAttribute("flags", int)
        self.createAttribute("layer", int)
        self.createAttribute("name", str)
        self.createAttribute("roundness", str)
        self.createAttribute("signal", str)
        self.createAttribute("x", int)
        self.createAttribute("y", int)


class ULPad(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("angle", float)
        self.createAttribute("diameter", int, args=[(int)])
        self.createAttribute("drill", int)
        self.createAttribute("drillsymbol", int)
        self.createAttribute("elongation", int)
        self.createAttribute("flags", int)
        self.createAttribute("name", str)
        self.createAttribute("shape", int, args=[(int)])
        self.createAttribute("signal", int)
        self.createAttribute("x", int)
        self.createAttribute("y", int)


class ULArc(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("angle1", float)
        self.createAttribute("angle2", float)
        self.createAttribute("cap", int)
        self.createAttribute("layer", int)
        self.createAttribute("radius", int)
        self.createAttribute("width", int)
        self.createAttribute("x1", int)
        self.createAttribute("x2", int)
        self.createAttribute("xc", int)
        self.createAttribute("y1", int)
        self.createAttribute("y2", int)
        self.createAttribute("yc", int)


class ULWire(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("arc", ULArc)
        self.createAttribute("cap", int)
        self.createAttribute("curve", float)
        self.createAttribute("layer", int)
        self.createAttribute("style", int)
        self.createAttribute("width", int)
        self.createAttribute("x1", int)
        self.createAttribute("x2", int)
        self.createAttribute("y1", int)
        self.createAttribute("y2", int)
        self.createAttribute("pieces", [ULWire])


class ULText(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("align", int)
        self.createAttribute("angle", float)
        self.createAttribute("font", int)
        self.createAttribute("layer", int)
        self.createAttribute("mirror", int)
        self.createAttribute("ratio", int)
        self.createAttribute("size", int)
        self.createAttribute("spin", int)
        self.createAttribute("value", str)
        self.createAttribute("x", int)
        self.createAttribute("y", int)
        self.createAttribute("wires", [ULWire])


class ULPackage(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("area", ULArea)
        self.createAttribute("description", str)
        self.createAttribute("headline", str)
        self.createAttribute("library", str)
        self.createAttribute("name", str)
        self.createAttribute("circles", [ULCircle])
        self.createAttribute("contacts", [ULContact])
        self.createAttribute("dimensions", [ULDimension])
        self.createAttribute("frames", [ULFrame])
        self.createAttribute("holes", [ULHole])
        self.createAttribute("polygons", [ULPolygon])
        self.createAttribute("rectangles", [ULRectangle])
        self.createAttribute("texts", [ULText])
        self.createAttribute("wires", [ULWire])

    def grid(self):
        return ULLibrary().grid

    def groups(self):
        if ULContext() != ULPackage:
            return []

        return ULGroupSet(ULPackage)


class ULElement(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("angle", float)
        self.createAttribute("attribute", str, args=[(str)])
        self.createAttribute("column", str)
        self.createAttribute("locked", int)
        self.createAttribute("mirror", int)
        self.createAttribute("name", str)
        self.createAttribute("package", ULPackage)
        self.createAttribute("populate", int)
        self.createAttribute("row", str)
        self.createAttribute("smashed", int)
        self.createAttribute("spin", int)
        self.createAttribute("value", int)
        self.createAttribute("x", int)
        self.createAttribute("y", int)
        self.createAttribute("attributes", [ULAttribute])
        self.createAttribute("texts", [ULText])
        self.createAttribute("variants", [ULVariant])


class ULDimension(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("dtype", int)
        self.createAttribute("layer", int)
        self.createAttribute("x1", int)
        self.createAttribute("x2", int)
        self.createAttribute("x3", int)
        self.createAttribute("y1", int)
        self.createAttribute("y2", int)
        self.createAttribute("y3", int)
        self.createAttribute("texts", [ULText])
        self.createAttribute("wires", [ULWire])


class ULLayer(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("color", int)
        self.createAttribute("fill", int)
        self.createAttribute("name", str)
        self.createAttribute("number", int)
        self.createAttribute("used", int)
        self.createAttribute("visible", int)


class ULCircle(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("layer", int)
        self.createAttribute("radius", int)
        self.createAttribute("width", int)
        self.createAttribute("x", int)
        self.createAttribute("y", int)



class ULArea(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("x1", int)
        self.createAttribute("x2", int)
        self.createAttribute("y1", int)
        self.createAttribute("y2", int)


class ULGrid(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("distance", float)
        self.createAttribute("dots", int)
        self.createAttribute("multiple", int)
        self.createAttribute("on", int)
        self.createAttribute("unit", int)
        self.createAttribute("unitdist", int)


class ULInstance(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("angle", float)
        self.createAttribute("column", str)
        self.createAttribute("gate", ULGate)
        self.createAttribute("mirror", int)
        self.createAttribute("name", str)
        # self.createAttribute("part",ULPart)
        self.createAttribute("row", str)
        self.createAttribute("sheet", int)
        self.createAttribute("smashed", int)
        self.createAttribute("value", str)
        self.createAttribute("x", int)
        self.createAttribute("y", int)
        self.createAttribute("attributes", [ULAttribute])
        self.createAttribute("texts", [ULText])
        self.createAttribute("xrefs", [ULGate])


class ULBoard(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("area", ULArea)
        self.createAttribute("description", str)
        self.createAttribute("grid", ULGrid)
        self.createAttribute("headline", str)
        self.createAttribute("name", str)
        self.createAttribute("attributes", [ULAttribute])
        self.createAttribute("circles", [ULCircle])
        self.createAttribute("classes", [ULClass])
        self.createAttribute("dimensions", [ULDimension])
        self.createAttribute("elements", [ULElement])
        self.createAttribute("frames", [ULFrame])
        self.createAttribute("holes", [ULHole])
        self.createAttribute("layers", [ULLayer])
        self.createAttribute("libraries", [ULLibrary])
        self.createAttribute("polygons", [ULPolygon])
        self.createAttribute("rectangles", [ULRectangle])
        self.createAttribute("signals", [ULSignal])
        self.createAttribute("texts", [ULText])
        self.createAttribute("variantdefs", [ULVariantDef])
        self.createAttribute("wires", [ULWire])

    def groups(self):
        return ULGroupSet(ULBoard)


class ULSchematic(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("alwaysvectorfont", int)
        self.createAttribute("description", str)
        self.createAttribute("grid", ULGrid)
        self.createAttribute("headline", str)
        self.createAttribute("name", str)
        self.createAttribute("verticaltext", int)
        self.createAttribute("xreflabel", str)
        self.createAttribute("attributes", [ULAttribute])
        self.createAttribute("classes", [ULClass])
        self.createAttribute("layers", [ULLayer])
        self.createAttribute("libraries", [ULLibrary])
        self.createAttribute("nets", [ULNet])
        self.createAttribute("parts", [ULPart])
        self.createAttribute("sheets", [ULSheet])
        self.createAttribute("instances", [ULInstance])
        self.createAttribute("variantdefs", [ULVariantDef])

    def groups(self):
        return ULGroupSet(ULSchematic)


class ULSheet(ULObject):
    def __init__(self, parent=None):
        ULObject.__init__(self, parent)
        self.createAttribute("area", ULArea)
        self.createAttribute("description", str)
        self.createAttribute("headline", str)
        self.createAttribute("number", int)
        self.createAttribute("busses", [ULBus])
        self.createAttribute("circles", [ULCircle])
        self.createAttribute("dimensions", [ULDimension])
        self.createAttribute("frames", [ULFrame])
        self.createAttribute("nets", [ULNet])
        self.createAttribute("polygons", [ULPolygon])
        self.createAttribute("rectangles", [ULRectangle])
        self.createAttribute("texts", [ULText])
        self.createAttribute("wires", [ULWire])
        self.createAttribute("instances", [ULInstance])

    def groups(self):
        return ULGroupSet(ULSheet)


class ULGroupSet(list):
    GROUP_FILE_LOCK = Lock()

    def __init__(self, contextObject):
        list.__init__(self)
        self.contextObject = contextObject
        self.groupsFilePath = None
        self._enabledupdates = True

        if not self.contextObject in [ULBoard, ULSchematic]:
            raise EaglepyException("Invalid context object")

        matches = re.match("(.+)\.[\w\d]+", self.contextObject().name())
        if not matches or len(matches.groups()) < 1:
            return

        self.groupsFilePath = matches.groups()[0] + ".epy"

        self._loadfromxml()

    def enableupdates(self, value):
        self._enabledupdates = value

    def append(self, group):

        if not isinstance(group, ULGroup):
            raise EaglepyException("Only ULGroup objects can be appended")

        group._parentset = self

        list.append(self,
                    group)  # Circular Reference Here.. weakref.proxy(group))

        self._updatexml()

    def remove(self, group):

        if not isinstance(group, ULGroup):
            raise EaglepyException("Only ULGroup objects can be removed")

        list.remove(self, group)
        group._parentset = None
        self._updatexml()

    def _loadfromxml(self):

        self.GROUP_FILE_LOCK.acquire()
        groupsData = "<?xml version=\"1.0\" ?><Eaglepy></Eaglepy>"
        if self.groupsFilePath and os.path.exists(self.groupsFilePath):
            groupsFile = file(self.groupsFilePath, "r")
            groupsData = groupsFile.read()
            groupsFile.close()
        self.GROUP_FILE_LOCK.release()
        eaglepyDom = parseString(groupsData)

        def getSingleElement(parent, name):
            elements = parent.getElementsByTagName(name)
            if not len(elements):
                return None
            return elements[0]

        eaglePyElement = getSingleElement(eaglepyDom, "Eaglepy")
        boardElement = getSingleElement(eaglePyElement, "BoardContext")
        schematicElement = getSingleElement(eaglePyElement, "SchematicContext")
        packageElement = getSingleElement(eaglePyElement, "PackageContext")

        if self.contextObject == ULBoard:
            contextElement = boardElement
        elif self.contextObject == ULSchematic:
            contextElement = schematicElement
        elif self.cojntextObject == ULPackage:
            contextElement = packageElement

        if not contextElement:   return

        contextGroupList = getSingleElement(contextElement, "GroupList")
        if not contextGroupList: return

        allObjectsList = allobjects()

        for groupItem in contextGroupList.childNodes:
            groupName = groupItem.getAttribute("name")
            loadedGroup = ULGroup()
            loadedGroup._name = groupName
            for groupMember in groupItem.childNodes:

                elementNameString = groupMember.getAttribute("name")
                elementClassString = groupMember.getAttribute("class")
                elementPath = groupMember.getAttribute("path")

                foundElement = False
                for element in allObjectsList:
                    if hasattr(element,
                               "name") and element.name() == elementNameString:
                        foundElement = True
                        break

                if foundElement:
                    loadedGroup.append(element)
            if len(loadedGroup):
                loadedGroup._parentset = self
                list.append(self, loadedGroup)

    def update(self):
        if self._enabledupdates:
            self._updatexml()

    def _updatexml(self):

        if not self._enabledupdates:
            return

        self.GROUP_FILE_LOCK.acquire()
        groupsData = "<?xml version=\"1.0\" ?><Eaglepy></Eaglepy>"
        if self.groupsFilePath and os.path.exists(self.groupsFilePath):
            groupsFile = file(self.groupsFilePath, "r")
            groupsData = groupsFile.read()
            groupsFile.close()
        self.GROUP_FILE_LOCK.release()

        eaglepyDom = parseString(groupsData)

        def getOrCreateElement(parent, name):
            elements = parent.getElementsByTagName(name)
            if not len(elements):
                element = eaglepyDom.createElement(name)
                parent.appendChild(element)
                return element
            return elements[0]

        def createElement(parent, name):
            element = eaglepyDom.createElement(name)
            parent.appendChild(element)
            return element

        eaglePyElement = getOrCreateElement(eaglepyDom, "Eaglepy")
        boardElement = getOrCreateElement(eaglePyElement, "BoardContext")
        schematicElement = getOrCreateElement(eaglePyElement,
                                              "SchematicContext")
        packageElement = getOrCreateElement(eaglePyElement, "PackageContext")

        if self.contextObject == ULBoard:
            contextElement = boardElement
        elif self.contextObject == ULSchematic:
            contextElement = schematicElement
        elif self.cojntextObject == ULPackage:
            contextElement = packageElement

        contextGroupList = getOrCreateElement(contextElement, "GroupList")

        for child in list(contextGroupList.childNodes):
            contextGroupList.removeChild(child)

        currentGroupCount = len(self)

        for group in self:
            groupName = group.name()
            if not groupName:
                index = 0
                while True:
                    newGroupName = "Group" + str(currentGroupCount + index)
                    if not len([item for item in self if
                                item.name() == newGroupName]):
                        groupName = newGroupName
                        break
                    index += 1

                group._name = groupName

            newGroup = createElement(contextGroupList, "Group")
            newGroup.setAttribute("name", group.name())

            for ulobject in group:
                newobject = createElement(newGroup, "object")
                newobject.setAttribute("name", ulobject.name())
                newobject.setAttribute("class", ulobject.__class__.__name__)
                newobject.setAttribute("path", ulobject.path())

        self.GROUP_FILE_LOCK.acquire()
        groupsData = eaglepyDom.toxml()
        groupsFile = file(self.groupsFilePath, "w")
        groupsFile.write(groupsData)
        groupsFile.close()
        self.GROUP_FILE_LOCK.release()


class ULGroup(list):
    def __init__(self, name=None):
        self._name = name
        self._parentset = None
        self._enabledupdates = True
        list.__init__(self)

    def enableupdates(self, value):
        self._enabledupdates = value

    def update(self):
        if self._enabledupdates:
            self._parentset._updatexml()

    def name(self):
        return self._name

    def rename(self, newname):
        self._name = newname
        if self._enabledupdates and self._parentset:
            self._parentset._updatexml()

    def remove(self, item):

        if not isinstance(item, ULObject):
            raise EaglepyException("Only ULObject objects can be removed")

        list.remove(self, item)

        if self._enabledupdates and self._parentset:
            self._parentset._updatexml()

    def parentset(self):
        return self._parentset

    def append(self, item):

        if not isinstance(item, ULObject):
            raise EaglepyException("Only ULObject objects can be appended")

        list.append(self, item)

        if self._enabledupdates and self._parentset:
            self._parentset._updatexml()

def ULContext():
    context = int(instance().executeCommand(COMMAND.getcontext))
    if context == CONTEXT.BOARD:
        return ULBoard()
    elif context == CONTEXT.SCHEMATIC:
        return ULSchematic()
    elif context == CONTEXT.SHEET:
        return ULSheet()
    elif context == CONTEXT.PACKAGE:
        return ULPackage()
