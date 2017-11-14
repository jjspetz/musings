// TODO
// get error and warnings from https://validator.w3.org/ for HTML validation
// get error and warnings from https://jigsaw.w3.org/css-validator/ for CSS validation
// get test speed date from https://developers.google.com/speed/pagespeed/insights/
// make system for looking deeper based on class and scrapper

const HTMLValidator = require('html-validator')
const CSSValidator = require('w3c-css');
const pagespeedInsights = require('pagespeed-insights');
const URLparse = require('url-parse');
const scrapper = require('./scrapper.js');

const URL = URLparse(process.argv[2]);
const scrapDepth = process.argv[3] || 0;

function main() {
  // validate URL and format
  var url;
  // console.log(site)
  if (URL.protocol) {
    url = URL.toString()
  } else {
    url = 'http://' + URL.pathname;
    // console.log(url)
  }

  HTMLCheck(url);
  CSSCheck(url);
  speedTest(url);
}


// HTML validation
function HTMLCheck(site){
  var HTMLOptions = {
   url: site,
   format: 'json'
  }

  HTMLValidator(HTMLOptions)
    .then((data) => {
      let error = 0
      let warning = 0;
      // console.log(data.messages.length)
      for(let i=0; i<data.messages.length; i++) {
        if (data.messages[i].type === 'error') {
          error++;
        } else {
          warning++;
        }
      }

      console.log('HTML Warnings: ' + warning);
      console.log('HTML Errors: ' + error);
    })
    .catch((error) => {
      console.error(error)
    })
  }

// CSS validation
function CSSCheck(site) {
  let CSSOptions = {
    url: site,
    warning: 1,
  }

  CSSValidator.validate(CSSOptions, function(err, data) {
    if(err) {
      // an error happened
      console.error(err);
    } else {
      // validation warnings
      console.log('CSS Warnings:', data.warnings.length);

      // validation errors
      console.log('CSS Errors:', data.errors.length);
    }
  });
}

// Speed tester
function speedTest(site) {
  var opts = {
    url: site,
    apiKey: 'AIzaSyCJtrRIyMVDxjwj8vN260eMUw5aoGdjBfg',
  };

  function getSpeedScore(strat) {
    opts.strategy = strat

    pagespeedInsights(opts, (err, data) => {
      // console.log(data)
      for (url in data){
        console.log(strat + ' page speed: ' + data[url].pageSpeed);
      }
    });
  };

  // for desktop
  getSpeedScore('desktop');
  // for mobile
  getSpeedScore('mobile');
}


// execute main function
main();

scrapper(URL.toString(), function(results) {
  console.log(results);
})
// handles suburls (poorly)
if (scrapDepth > 0) {
  scrapper(URL.toString(), function(results) {
    for (let i=0; i<scrapDepth; i++) {
      HTMLCheck(results[i]);
      CSSCheck(results[i]);
    }
  });
}
