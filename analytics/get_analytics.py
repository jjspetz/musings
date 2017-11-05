"""Analytics Reporting API V4."""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = './client_secret.json'
METRICS = [
    {
      "expression": "ga:sessions",
      "alias": "Sessions"
    },
    {
        "expression": "ga:Users",
        "alias": "User"
    },
    {
        "expression": "ga:pageviews",
        "alias": "Page Views"
    },
    {
      "expression": "ga:pageviewsPerSession",
      "alias": "Page/Session"
    },
    {
        "expression": "ga:avgSessionDuration",
        "alias": "Avg. Session Duration"
    },
    {
        "expression": "ga:bounceRate",
        "alias": "Bounce Rate"
    },
    {
        "expression": "ga:percentNewSessions",
        "alias": "% New Sessions"
    },
    {
      "expression": "ga:transactionsPerSession",
      "alias": "Ecommerce Conversion Rate"
    },
    {
        "expression": "ga:transactions",
        "alias": "Transactions"
    },
    {
        "expression": "ga:transactionRevenue",
        "alias": "Revenue"
    },
]

def initialize_analytics():
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)

  # Build the service object.
  analytics = build('analytics', 'v3', credentials=credentials)

  return analytics

def initialize_analyticsreporting():
  """Initializes an Analytics Reporting API V4 service object.

  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)

  # Build the service object.
  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics


def get_report(analytics, view_id, time_frame, compare):
  """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """
  if (compare):
      return analytics.reports().batchGet(
          body={
            'reportRequests': [
            # report for compare
            {
              'viewId': view_id,
              'dateRanges': [{'startDate': str(int(time_frame)*2), 'daysAgo': time_frame + 'daysAgo'}],
              'metrics': METRICS,
                'dimensions': [{'name': 'ga:channelGrouping'}]
            },
            ]
          }
      ).execute()
  else:
      return analytics.reports().batchGet(
          body={
            'reportRequests': [
            # report for basic
            {
              'viewId': view_id,
              'dateRanges': [{'startDate': time_frame + 'daysAgo', 'endDate': 'today'}],
              'metrics': METRICS,
                'dimensions': [{'name': 'ga:channelGrouping'}]
            },
            ]
          }
      ).execute()


# ALL PRINT functions mainly for testing purposes, remove later
def print_response(response):
  """Parses and prints the Analytics Reporting API V4 response.

  Args:
    response: An Analytics Reporting API V4 response.
  """
  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

    for row in report.get('data', {}).get('rows', []):
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])

      for header, dimension in zip(dimensionHeaders, dimensions):
        print (header + ': ' + dimension)

      for i, values in enumerate(dateRangeValues):
        print ('Date range: ' + str(i))
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          print (metricHeader.get('name') + ': ' + value)

def print_property_summaries(account_summary):
  if account_summary:
    for property in account_summary.get('webProperties', []):
      print ('   %s (%s)' % (property.get('name'), property.get('id')))
      print ('   [%s | %s]' % (property.get('websiteUrl'), property.get('level')))
      print_profile_summary(property)


def print_profile_summary(property_summary):
  if property_summary:
    for profile in property_summary.get('profiles', []):
      print ('     %s (%s) | %s' % (profile.get('name'), profile.get('id'),
                                   profile.get('type')))

def get_account_info():
    # Note: This code assumes you have an authorized Analytics service object.
    # See the Account Summaries Developer Guide for details.
    analytics = initialize_analytics()

    # Example #1:
    # Requests a list of all account summaries for the authorized user.
    try:
      account_summaries = analytics.management().accountSummaries().list().execute()

    except TypeError:
      # Handle errors in constructing a query.
      print ('There was an error in constructing your query : %s' % error)

    # Example #2:
    # The results of the list method are stored in the account_summaries object.
    # The following code shows how to iterate through them.

    # for account in account_summaries.get('items', []):
    #   print ('\n%s (%s)' % (account.get('name'), account.get('id')))
    #   print_property_summaries(account)

    return account_summaries

def main(view_id, time_frame, compare):
  analytics = initialize_analyticsreporting()
  response = get_report(analytics, view_id, time_frame, compare)
  return response

if __name__ == '__main__':
  main()
  # get_account_info()
