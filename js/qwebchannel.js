(function (global, factory) {
    if (typeof define === 'function' && define.amd) {
        define([], factory);
    } else if (typeof module === 'object' && module.exports) {
        module.exports = factory();
    } else {
        global.QWebChannel = factory();
    }
}(this, (function () {
    'use strict';

    var QWebChannel = function(transport, initCallback)
    {
        var self = this;
        this.transport = transport;

        this.transport.onmessage = function(message) {
            self.messageHandler(message);
        };

        this.transport.onerror = function(error) {
            console.error("QWebChannel error:", error);
        };

        this.execCallbacks = {};
        this.execId = 0;

        this.objects = {};

        this.debug = false;
        this.exec = function(command, args, callback) {
            var execId = ++this.execId;
            if (callback) {
                this.execCallbacks[execId] = callback;
            }
            var message = {
                type: QWebChannel.messageTypes.invokeMethod,
                object: command,
                args: args,
                id: execId
            };
            this.send(message);
        };

        this.send = function(data)
        {
            if (this.debug) {
                console.log("sending", data);
            }
            this.transport.send(JSON.stringify(data));
        };

        this.messageHandler = function(messageString)
        {
            var message = JSON.parse(messageString);
            if (this.debug) {
                console.log("received", message);
            }
            if (message.id !== undefined) {
                var callback = this.execCallbacks[message.id];
                if (callback) {
                    callback(message);
                    delete this.execCallbacks[message.id];
                }
            } else if (message.type === QWebChannel.messageTypes.propertyUpdate) {
                for (var i in message.data) {
                    var propertyData = message.data[i];
                    var object = this.objects[propertyData.object];
                    if (!object) {
                        console.error("Cannot update property", propertyData.object, "unknown object");
                        continue;
                    }
                    object[propertyData.property] = propertyData.value;
                }
            } else if (message.type === QWebChannel.messageTypes.signal) {
                var object = this.objects[message.object];
                if (!object) {
                    console.error("Cannot deliver signal", message.object, "unknown object");
                    return;
                }
                var signal = object[message.signal];
                if (typeof signal !== "function") {
                    console.error("Cannot deliver signal", message.signal, "unknown signal");
                    return;
                }
                signal.apply(object, message.args);
            }
        };

        this.init = function(data)
        {
            for (var objectName in data) {
                var objectData = data[objectName];
                this.objects[objectName] = objectData;
            }
            if (initCallback) {
                initCallback(this);
            }
        };

        this.messageTypes = {
            signal: 1,
            propertyUpdate: 2,
            invokeMethod: 3
        };

        this.send({
            type: QWebChannel.messageTypes.invokeMethod,
            object: "org.qtproject.qtwebchannel.init",
            args: []
        });
    };

    return QWebChannel;
})));
