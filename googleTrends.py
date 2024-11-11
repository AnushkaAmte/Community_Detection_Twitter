from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

def fetch_google_trends_data(keywords, timeframe, geo='US'):
    """
    Fetches Google Trends data for the given keywords, timeframe, and geographic region.

    Args:
        keywords: A list of keywords to search for.
        timeframe: The time frame for the search.
        geo: The geographic region.

    Returns:
        A pandas DataFrame containing the interest over time data.
    """

    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(kw_list=keywords, timeframe=timeframe, geo=geo)
    return pytrends, pytrends.interest_over_time()

def analyze_related_queries(related_queries):
    """
    Analyzes related queries and creates a network graph.

    Args:
        related_queries: A dictionary containing related queries.

    Returns:
        A NetworkX graph representing the relationships between queries.
    """

    G = nx.Graph()
    for query_group in related_queries.values():
        for query in query_group['query']:
            G.add_node(query)
            for related_query in query_group['value']:
                G.add_edge(query, related_query)

    return G

# Example usage
keywords = ['COVID-19', 'coronavirus', 'pandemic']
timeframe = '2020-01-01 2023-11-11'

# Fetch interest over time data
pytrends, interest_over_time_df = fetch_google_trends_data(keywords, timeframe)

# Visualize the trend
interest_over_time_df.plot()
plt.title('Google Trends: COVID-19 Related Searches')
plt.xlabel('Date')
plt.ylabel('Search Interest')
plt.show()

# Get related queries
# pytrends.build_payload(kw_list=keywords)
# related_queries = pytrends.related_queries()

# # Create a network graph
# G = analyze_related_queries(related_queries)

# # Visualize the network graph
# nx.draw_spring_layout(G, with_labels=True)
# plt.title('Network of Related Queries')
# plt.show()