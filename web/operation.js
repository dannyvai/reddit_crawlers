"use strict";

module.exports = class Operation {
    constructor(inputFile, fileName) {
        this.id = Math.random().toString(36).substr(2, 10);
        this.fileName = fileName;
        this.input = inputFile;
        this.output = null;
        this.status = null;
        this.error = null;
        this.queueTime = null;
        this.startTime = null;
        this.endTime = null;
    };
};