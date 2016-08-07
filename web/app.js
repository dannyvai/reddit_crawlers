"use strict";

const express = require('express');
const multer  = require('multer');
const upload = multer({ dest: 'uploads/' });
const compression = require('compression');
const Queue = require('./queue');
const config = require('./config');
const spawn = require('child_process').spawn;

const app = express();
app.use(express.static('static'));
app.disable('x-powered-by');
app.use(compression());

let queue = new Queue();

app.post('/upload', upload.single('photo'), (req, res) => {
    //Add the new photo to the queue and return the id
    let operation = queue.enqueue(req.file.path, req.file.originalname);
    res.json({
        id: operation.id
    });
});

app.get('/status/:id', (req, res) => {
    res.json(queue.query(req.params.id));
});

app.get('/output/:id', (req, res) => {
    let operation = queue.query(req.params.id);
    if (!operation) {
        res.status(404).send("Could not find image");
    }

    //new file name is '{filename}.colorized.{extension}'
    let newFilename = operation.fileName.replace(/\.(.+?$)/,".colorized.$1");
    res.download(operation.output, newFilename);
});

app.get('/output/multiple/:ids', (req, res) => {
    let ids = req.params.ids.split(",");
    let filesToZip = ids.map((e) => {
        let operation = queue.query(e);
        return operation.output;
    });
    let args = ['-rj', '-'].concat(filesToZip);
    let zip = spawn('zip', args);

    res.set('Content-Type', 'application/zip');
    zip.stdout.on('data', function (data) {
        res.write(data);
    });

    zip.stderr.on('data', function (data) {
        // Uncomment to see the files being added
        //console.log('zip stderr: ' + data);
    });

    // End the response on zip exit
    zip.on('exit', function (code) {
        if(code !== 0) {
            res.statusCode = 500;
            console.log('zip process exited with code ' + code);
            res.end();
        } else {
            res.end();
        }
    });
});

app.listen(config.port, () => {
    console.log(`Colorize web server is running on port ${config.port}`);
    queue.start();
});
