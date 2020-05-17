import splunklib.client as Client
import splunklib.results as results
import json
import collections

"""
method to retrieve data from splunk server
args: 
host => host ip address
port => server running port
username => username to login to splunk
password => password to login to splunk
time_range => the time range to retrieve data
returns => list
"""
def query_splunk(host, port, username, password, query, time_range):
    print(host, port, username, password, query, time_range)

    # connecting to splunk server
    service = Client.connect(
        host=host,
        port=port,
        username=username,
        password=password
    )

    # calculates earliest time based on time_range
    if time_range == "24h":
        earliest_time = "-24h"
    elif time_range == "7d":
        earliest_time = "-7d"
    elif time_range == "30d":
        earliest_time = "-30d"

    # keyword args to be passed to service
    kwargs_export = {
       "earliest_time": earliest_time,
       "latest_time": "now",
       "search_mode": "normal",
       "preview": False
    }

    # search string added with 'search ' as suggested by docs
    searchString = "search " + query
    
    # query method. queries data and parsed by ResultsReader
    rr = results.ResultsReader(service.jobs.export(searchString, **kwargs_export))
    
    # list to hold the final result
    result_data = []
    
    # method to seperate data and convert to json and store in list
    for result in rr:
        if isinstance(result, results.Message):
            print('%s: %s' % (result.type, result.message))
        elif isinstance(result, dict):
            str_result = json.dumps(result)  # converts to string
            json_result = json.loads(str_result)  # converts to json
            result_data.append(json_result)  # appends to final list
    
    return result_data
