"use strict";

const exec = require('child_process').exec;
const config = require('./config');
const scriptPath = "./colorize.sh";

module.exports = function(input, output, callback) {
    let command = `sh ${config.scriptPath} ${input} ${output}`;
    exec(command, (error, stdout, stderr) => {

        if (stderr.length > 0) {
            return callback(stderr);
        }

        callback(null);
    });
};