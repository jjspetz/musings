// scrap main links from navbar
const cheerio = require('cheerio');
const request = require('request');
const bodyParser = require('body-parser');
const URLparse = require('url-parse');

function main(url, callback) {
  var results = []
  var homeURL = URLparse(url)

  request(url, function(error, response, html) {

    var $ = cheerio.load(html);

    $("a").each(function(i, element) {
      var linkURL = URLparse($(this).attr("href"));
      var linkHost, homeHost;

      // format hostname to ignore subdomains
      let tmp = linkURL.hostname.split('.')
      tmp.shift();
      linkHost = tmp.join('.');

      if (homeURL.hostname.split('.').length === 3) {
        let tmp = homeURL.hostname.split('.')
        tmp.shift();
        homeHost = tmp.join('.');
      } else {
        homeHost = homeURL.hostname;
      }

      // console.log(linkURL)
      // console.log(linkURL.host, homeURL.host)
      if (linkHost === homeHost) {
        results.push($(this).attr("href"));
      }
    });
    callback(results);
  });
} // end main

module.exports = main;
