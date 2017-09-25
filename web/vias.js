///////////////////////////////////////////////////////////////////////////////
//
// Copyright (C) 2017, Jaguar Land Rover and/or collaborators.
//
// Licensed according to the terms provided by the LICENSE file.
//
///////////////////////////////////////////////////////////////////////////////


//
// VISClientOptions
//
var VISClientOptions = function(options) {
	var self = this;
    self._options = options;
    
    self.uri = function() {
    	return self._options.protocol + "://" + self._options.host + ":" +
    	       self._options.port + "/ws";
    };
};


//
// VISClient
//
var VISClient = function(visClientOptions) {
	var self = this;
	self._options = visClientOptions;
	
	// callbacks
	var onConnect = null;
	var onDisconnect = null;
	var onMessage = null;
	var onError = null;
	self.onSub = {};
	
	// WAMP router connection
	var connection = new autobahn.Connection({
        url: self._options.uri(),
        realm: "genivi"
    });
    
    // WAMP session
    var session = null;
    var details = null;
    
    self.onOpen = function (session, details) {
        self.session = session;
        self.details = details;
        self.session.subscribe('org.genivi.update', self.update).then(
            function (sub) {
                console.log('subscribed to topic');
            },
            function (err) {
                console.log('subscription failed', err);
            }
        );
        self.onConnect(session, details);
    }
    
    self.onClose = function(reason, details) {
        self.onDisconnect(reason, details);
    }
    
    self.connect = function (connectCallback, disconnectCallback) {
        self.onConnect = connectCallback;
    	self.onDisconnect = disconnectCallback;
        connection.onopen = self.onOpen;
        connection.onclose = self.onClose;
        connection.open();
    }
    
    self.disconnect = function (callback) {
    	self.onDisconnect = callback;
    	connection.close();
    }
    
    self.update = function (args) {
        var signals = args[0];
        for (var i = 0; i < signals.length; i++) {
            var path = signals[i].path;
            var value = signals[i].value;
	        console.log("received signal update: <" + path + ":(" + typeof(value) + ")" + value + ">");
	        var callback = self.onSub[path];
	        if (callback != null) {
	    	    callback(value);
	        }
	    }
    }
    
    self.subscribe = function (signal, callback, filter) {
    	self.session.call('org.genivi.subscribe', [signal, filter]).then(
            function (res) {
                console.log("subscribe() result:", res);
            },
            function (err) {
                console.log("subscribe() error:", err);
            }
        );
        self.onSub[signal] = callback;
    }

	
}; 