var express = require('express');
var app = express();

app.use(express.static(__dirname + '/'));

// routes
app.get('/', function(request, response) {
  response.sendFile('index.html')
});

app.listen(3000, function() {
  console.log('listening on port 3000.')
})

// test
// function makeApiCall() {
//   var apiQuery = gapi.client.analytics.data.ga.get({
//     'ids': TABLE_ID,
//     'start-date': '2010-01-01',
//     'end-date': '2010-01-15',
//     'metrics': 'ga:sessions',
//     'dimensions': 'ga:source,ga:keyword',
//     'sort': '-ga:sessions,ga:source',
//     'filters': 'ga:medium==organic',
//     'max-results': 25
//   });
//   return apiQuery;
// }
