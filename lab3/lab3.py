import json
import os

from serpapi import GoogleSearch

API_KEY = "c1b57a5186ae96e31b5966c89200e8fbe3491fb9854ad5089f56feed874dcf57"

"""
Method to obtain the top_n result from each search engine.
    Parameters:
    -----------
    algo: The search engine being used. For example = {google,bing,duckduckgo}
    query: The query passed to the search engine. For example = {information retrieval evaluation}
    top_n (Optional paramter with default value of 20): The top_n results returned from the search query
    Returns:
    --------
    The organic results from the top_n results # Might want to change that later so that we return all of them
    
"""


def get_search_results(algo, query, top_n=20):
    if top_n > 50:
        raise Exception("Cannot pass top_n to be more than 50")

    params = {"engine": algo, "q": query, "api_key": API_KEY}
    if algo == "google":
        params["start"] = 0
        params["num"] = top_n
    elif algo == "bing":
        params["first"] = 0
        params["count"] = top_n  # Cannot be more than 50 so fix this later
    elif algo == "duckduckgo":
        # Modify results offset to skiip first so we can get 50 results
        params["start"] = 1
    elif algo == "yahoo":
        del params["q"]
        params["p"] = query
        params["pz"] = top_n

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results["organic_results"]
    # Check if length of organic results == top_n if not query again
    # Check if length is organic results > top_n if so then slice the results

    # Return the top_n organic results
    return organic_results


"""
Method to save the results from a specific engine to a filename. We assume 
a file with that name does not exists and that the filename is without any extension.
If the file does exist we remove it and create a new one and write the data there
    
    Paramters:
    ----------
    results: The results list from a query using the get_search_results() Method
    filename: The name of the file you wish to create to save the results to
"""


def save_results_to_file(result, filename):
    json_result = json.dumps(result)
    json_filename = filename + ".json"
    try:
        file = open(json_filename, "x")
        file.write(json_result)
    except FileExistsError:
        os.remove(json_filename)
        file = open(json_filename,"x")
        file.write(json_result)


if __name__ == "__main__":
    search_query = "information retrieval evaluation"
    search_results = {
        "google": get_search_results("google", search_query, top_n=7),
        "bing": get_search_results("bing", search_query, top_n=20),
        "duckduckgo": get_search_results("duckduckgo", search_query, top_n=20),
        "yahoo": get_search_results("yahoo", search_query, top_n=20),
    }
    
    save_results_to_file(search_results["google"],"google")
    save_results_to_file(search_results["bing"],"bing")
    save_results_to_file(search_results["duckduckgo"],"duckduckgo")
    save_results_to_file(search_results["yahoo"],"yahoo")
    
