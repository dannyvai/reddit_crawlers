"use strict";

const colorize = require('./colorize');
const Operation = require('./operation');
const config = require('./config');
const path = require('path');

const OperationStatus = {
    Queued: "Queued",
    Running: "Running",
    Finished: "Finished",
    Error: "Error"
};

module.exports = class Queue {
    constructor() {
        this.queue = [];
        this.operationMap = {};
        this.runningOperations = 0;
    }

    enqueue(path, fileName) {
        let operation = new Operation(path, fileName);
        operation.queueTime = new Date();
        operation.status = OperationStatus.Queued;

        this.queue.push(operation);
        this.operationMap[operation.id] = operation;
        return operation;
    }

    queueLoop() {
        console.log(`queueLoop: running: ${this.runningOperations} max: ${config.maxConcurrentOperations} pending: ${this.queue.length}`);

        //check if we are already processing max allowed photos
        if (this.runningOperations >= config.maxConcurrentOperations) {
            return;
        }

        //check if queue is empty
        if (this.queue.length == 0) {
            return;
        }

        //dequeue operation from the queue and run it
        let operation = this.queue.shift();
        operation.startTime = new Date();
        operation.output = path.join(config.outputPath, operation.id);
        operation.status = OperationStatus.Running;
        this.runningOperations++;
        console.log("operation started");
        colorize(operation.input, operation.output, (err) =>{
            console.log("operation ended");
            operation.endTime = new Date();
            this.runningOperations--;
            if(err) {
                operation.status = OperationStatus.Error;
                operation.error = err;
            }

            operation.status = OperationStatus.Finished;
        });
    }

    start() {
        this.queueIntervalId = setInterval(this.queueLoop.bind(this), config.queueIntervalTime);
    }

    end() {
        clearInterval(this.queueIntervalId);
    }

    query(operationId) {
        let operation = this.operationMap[operationId];

        if (!operation) {
            return null;
        }

        if (operation.status === OperationStatus.Queued) {
            operation.queuePosition = this.getQueuePosition(operation.id) || "N/A";
        }
        else {
            delete operation.queuePosition;
        }

        return operation;
    }

    getQueuePosition(operationId) {
        // TODO: can be optimize to O(1) using global id tracker
        for(let i = 0; i < this.queue.length; i++) {
            if (this.queue[i].id === operationId) {
                return i+1;
            }
        }

        return null;
    }
};