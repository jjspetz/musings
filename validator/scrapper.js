// scrap main links from navbar
const cheerio = require('cheerio');
const request = require('request');
const bodyParser = require('body-parser');

function main(url, callback) {
  var results = []

  request(url, function(error, response, html) {

    var $ = cheerio.load(html);

    $("a").each(function(i, element) {
      results.push($(this).attr("href"));
    });
    callback(results);
  });
} // end main

module.exports = main;
