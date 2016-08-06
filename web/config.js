"use strict";

const process = require('process');

let config = { };

// ----------------------- PRODUCTION SETTINGS ----------------------- //
if (process.env.NODE_ENV === 'production') {
    config = {
        port: 80,
        maxConcurrentOperations: 4,
        outputPath: "./output",
        queueIntervalTime: 100, //ms
        scriptPath: "./colorize.sh"
    };
}

// ----------------------- DEV SETTINGS ----------------------- //
else {
    config = {
        port: 3000,
        maxConcurrentOperations: 4,
        outputPath: "./output",
        queueIntervalTime: 100, //ms
        scriptPath: "./colorize.sh"
    };
}

module.exports = config;