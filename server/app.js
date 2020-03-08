const path = require("path");
const express = require("express");
const fs = require("fs");

const args = process.argv.slice(2);

if (args.length == 0) {
  console.log("Please specify a PDF file name");
  process.exit(1);
}
const filename = args[0];
const base = path.parse(filename).name;
const app = express();

app.get("/", function(req, res) {
  res.sendFile(path.join(__dirname, "index.html"));
});

app.get("/pdf", function(req, res) {
  var file = path.join(__dirname, "..", filename);
  res.sendFile(file);
});

app.get("/md5", function(req, res) {
  let md5 = base + ".md5";
  var file = path.join(__dirname, "..", md5);
  fs.open(file, "r", function(err, fileToRead) {
    if (!err) {
      fs.readFile(fileToRead, { encoding: "utf-8" }, function(err, data) {
        if (!err) {
          res.writeHead(200, { "Content-Type": "text/html" });
          res.write(data);
          res.end();
        } else {
          console.log(err);
        }
      });
    } else {
      res.status(500).send("Something wrong");
    }
  });
});

app.use(express.static(path.join(__dirname, "dist")));
app.use(express.static(path.join(__dirname, "../node_modules")));
app.listen(3000);
