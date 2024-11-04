import shodan
import requests
import pandas as pd
import time

#api-key
SHODAN_API_KEY = 'here_your_api_key_from_shodan'
#your client
api = shodan.Shodan(SHODAN_API_KEY)


data = []

#exmple of search-queries for vulnerable services
queries = ["ftp anonymous", 'port:9200 "elastic"', 'http.title:"robots.txt" port:80']

for query in queries:
    try:
        results = api.search(query, limit=50)
        for result in results['matches']:
            data.append({
                "IP": result["ip_str"],
                "Port": result["port"],
                "Org": result.get("org", "N/A"),
                "Location": f"{result['location']['city']}, {result['location']['country_name']}",
                "Query": query,
                "Timestamp": result["timestamp"]
            })

    except shodan.APIError as e:
        print(f"Error with query '{query}': {e}")

#Convert list to DataFrame
df = pd.DataFrame(data)

#Display DataFrame or save it as a CSV
print(df)
df.to_csv("vulnerable_services.csv", index=False)