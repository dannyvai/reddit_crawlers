"use strict";

const express = require('express');
const multer  = require('multer');
const upload = multer({ dest: 'uploads/' });
const compression = require('compression');

const app = express();
app.use(express.static('static'));
app.disable('x-powered-by');
app.use(compression());


app.post('/upload', upload.array('photos', 10), (req, res) => {
    console.log("Photos uploaded!");

});

app.listen(3000, () => {
    console.log("Node server is running");
});
