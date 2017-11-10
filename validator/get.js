// TODO
// get error and warnings from https://validator.w3.org/ for HTML validation
// get error and warnings from https://jigsaw.w3.org/css-validator/ for CSS validation
// get test speed date from https://developers.google.com/speed/pagespeed/insights/
// make system for looking deeper based on class and scrapper

const HTMLValidator = require('html-validator')
var CSSValidator = require('w3c-css');
const pagespeedInsights = require('pagespeed-insights');

const URL = process.argv[2];

// HTML validation
const options = {
 url: URL,
 format: 'json'
}

HTMLValidator(options)
  .then((data) => {
    var error = 0
    var warning = 0;
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

// CSS validation
CSSValidator.validate(URL, function(err, data) {
  if(err) {
    // an error happened
    console.error(err);
  } else {
    // validation warnings
    console.log('CSS Warnings', data.warnings.length);

    // validation errors
    console.log('CSS Errors', data.errors.length);
  }
});

// Speed tester
var opts = {
  url: URL,
  apiKey: 'AIzaSyCJtrRIyMVDxjwj8vN260eMUw5aoGdjBfg',
};

function getSpeedScore(strat) {
  opts.strategy = strat

  pagespeedInsights(opts, (err, data) => {
    // console.log(data)
    console.log(strat + ' page speed: ' + data[opts.url + '/'].pageSpeed);
  });
};

// for desktop
getSpeedScore('desktop');
// for mobile
getSpeedScore('mobile');
