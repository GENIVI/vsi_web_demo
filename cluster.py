###############################################################################
##
## Copyright (C) 2017, Jaguar Land Rover and/or collaborators.
##
## Licensed according to the terms provided by the LICENSE file.
##
###############################################################################

from twisted.internet.defer import inlineCallbacks
from twisted.logger import Logger

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError

from vsi_py import *

import queue


class Signal(object):
    name = None
    subscribed = None
    value = None
    filter = None
    
    def __init__(self, name, subscribed, filter=None):
        self.name = name
        self.subscribed = subscribed
        self.filter = filter
        
    def setValue(self, value):
    	self.value = value

class AppSession(ApplicationSession):

    log = Logger()
    
    signals = {}
    
    vsi = [
        "vehicle.ignition",
        "vehicle.turnsignal.right",
        "vehicle.turnsignal.left",
        "vehicle.speed",
        "vehicle.fuel",
        "vehicle.battery",
        "vehicle.engine.rpm",
        "vehicle.engine.temperature",
        "vehicle.engine.oilpressure",
        "vehicle.transmission.gear"
    ]
    
    queue = queue.Queue()
    
    sigsets = [1, 0]

    @inlineCallbacks
    def onJoin(self, details):

        ## Subcribe to signal
        ##
        def subscribe(signame, filter):
            self.log.info("subscribe() called with signal: <{signame}> and filter: <{filter}>",
                           signame=signame, filter=filter)
            self.signals[signame] = Signal(signame, True, filter)
            return True

        reg = yield self.register(subscribe, u'org.genivi.subscribe')
        self.log.info("procedure subscribe() registered")


        ## Unsubcribe from signal
        ##
        def unsubscribe(signame):
            self.log.info("unsubscribe() called with {signame}", signame=signame)
            self.signals.pop(signame, None)
            return True

        reg = yield self.register(unsubscribe, u'org.genivi.unsubscribe')
        self.log.info("procedure unsubscribe() registered")
        
        
        ## Set a signal
        ##
        def set(signame, value):
            self.log.info("set() called with <{signame}> and <{value}>", signame=signame, value=value)
            self.signals.setdefault(signame, Signal(signame, False))
            signal = self.signals[signame]
            signal.setValue(value)
            self.queue.put(signal)
            return True

        reg = yield self.register(set, u'org.genivi.set')
        self.log.info("procedure set() registered")


        ## Get a signal
        ##
        def get(signame):
            self.log.info("get() called with {signame}", signame=signame)
            signal = self.signals.get(signame)
            if (signal is not None):
                return signal.value
            else:
                return None

        reg = yield self.register(get, u'org.genivi.get')
        self.log.info("procedure get() registered")


        ## PUBLISH and CALL every second .. forever
        ##
        sigset = 0
        while True:
            
            for name in self.vsi:
                status, value = getSignalData(1, 0, name, False, True)
                if (status == 0):
                    set(name, value)
            
            while not self.queue.empty():
                 signal = self.queue.get(False)
                 self.log.info("queue <{signame}> and <{value}>", signame=signal.name, value=signal.value)
                 yield self.publish(u'org.genivi.update', 
                    [{'path':signal.name, 'value':signal.value}]
                 )

            yield sleep(0.1)


