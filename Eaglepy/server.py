"""
 (C) Copyright 2013 Rob Watson rmawatson [at] hotmail.com  and others.

 All rights reserved. This program and the accompanying materials
 are made available under the terms of the GNU Lesser General Public License
 (LGPL) version 2.1 which accompanies this distribution, and is available at
 http://www.gnu.org/licenses/lgpl-2.1.html

 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 Lesser General Public License for more details.

 Contributors:
     Rob Watson ( rmawatson [at] hotmail )
"""


import sys
import time
import json
import platform

from urlparse import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from threading import Thread, Condition, Lock
from uuid import uuid4


from Eaglepy import EXECREPLY_TYPE_NAME, POLLING_TYPE_CODE, \
    POLLING_REPONSE_NOP, POLLING_REPONSE_EXIT, POLLING_TYPE_NAME, EXEC_TYPE_CODE


if platform.system() == "Windows" and "pythonw.exe" in sys.executable.lower():
    class NullOutput(object):
        def write(self, text): pass


    sys.stdout = NullOutput()
    sys.stderr = NullOutput()



class EagleRemoteHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def log_message(self, format, *args):
        return

    def do_POST(self):
        print("POST")
        params = urlparse(self.path)

        requestType = params.path[1:].split("?")[0] if len(
            params.path) > 0 else None
        requestData = params.path[1:].split("?")[0] if len(
            params.path) > 1 else None

        length = int(self.headers['Content-Length'])
        postData = self.rfile.read(length)

        if requestType == POLLING_TYPE_NAME:
            self.pollingHandler(requestData)
        if requestType == EXECREPLY_TYPE_NAME:
            self.execReplyHandler(postData)

    def execReplyHandler(self, postData):

        splitReplies = [item for item in postData.split(";") if item != ""]

        self.server.commandQueueLock.acquire()

        commandConditions = dict(self.server.commandCondition)
        for reply in splitReplies:

            splitReplyItem = reply.split("|")
            cmdid = str(splitReplyItem[0])

            cmddata = None
            if len(splitReplyItem) > 1:
                cmddata = str(splitReplyItem[1])

            commandConditions[cmdid][0].acquire()
            commandConditions[cmdid][1] = cmddata
            commandConditions[cmdid][0].notifyAll()
            commandConditions[cmdid][0].release()

            cond = commandConditions[cmdid][0]
            cond.acquire()
            del commandConditions[cmdid]
            cond.release()

        self.server.commandQueueLock.release()
        self.postResponse({str(POLLING_TYPE_CODE): str(POLLING_REPONSE_NOP)})

    def pollingHandler(self, data):
        time.sleep(0.005)
        self.server.commandQueueLock.acquire()

        if self.server.shuttingDown:
            self.postResponse(
                {str(POLLING_TYPE_CODE): str(POLLING_REPONSE_EXIT)})
            self.server.shutdownCondition.acquire()
            self.server.shutdownCondition.notifyAll()
            self.server.shutdownCondition.release()

        if len(self.server.commandQueue):
            commandItem = self.server.commandQueue.pop()
            commandData = str(commandItem[0]) + "|" + str(
                commandItem[1]) + "|" + "?".join(
                str(item) for item in commandItem[2])
            self.postResponse({str(EXEC_TYPE_CODE): commandData})
        else:
            self.postResponse(
                {str(POLLING_TYPE_CODE): str(POLLING_REPONSE_NOP)})

        self.server.commandQueueLock.release()

    def postResponse(self, keyvalues):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(keyvalues))


class EagleRemoteServer(HTTPServer):
    TIMEOUT = 3.0

    def __init__(self):
        self.connectData = None
        self.queuedRequests = []
        self.sessionID = None
        self.serverThread = None

        self.commandQueueLock = Lock()
        self.commandQueue = []

        self.shuttingDown = False
        self.shutdownCondition = Condition()
        self.commandCondition = {}

        HTTPServer.__init__(self, ("127.0.0.1", 7697), EagleRemoteHandler)

    def startup(self):
        self.serverThread = Thread(target=self.serve_forever)
        self.serverThread.start()

    def shutdown(self):
        self.shuttingDown = True

        self.shutdownCondition.acquire()
        self.shutdownCondition.wait()
        self.shutdownCondition.release()

        HTTPServer.shutdown(self)
        self.serverThread.join()

    def executeCommand(self, cmdtype, args=[]):
        cmdid = str(uuid4().hex)

        self.commandQueueLock.acquire()
        self.commandCondition[cmdid] = [Condition(), None]
        self.commandQueue.append([cmdid, cmdtype, args])
        self.commandCondition[cmdid][0].acquire()
        self.commandQueueLock.release()

        self.commandCondition[cmdid][0].wait()

        condition = self.commandCondition[cmdid][0]
        result = self.commandCondition[cmdid][1]

        condition.release()
        return result


EAGLE_SERVER_INSTANCE = None


def initialize():
    global EAGLE_SERVER_INSTANCE
    EAGLE_SERVER_INSTANCE = EagleRemoteServer()
    EAGLE_SERVER_INSTANCE.startup()


def shutdown():
    instance().shutdown()


def instance():
    global EAGLE_SERVER_INSTANCE
    return EAGLE_SERVER_INSTANCE




