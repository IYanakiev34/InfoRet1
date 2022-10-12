import json
import os
from urllib.parse import parse_qsl, urlsplit
from regex import E
from serpapi import GoogleSearch
import matplotlib.pyplot as plt

API_KEY = "c1b57a5186ae96e31b5966c89200e8fbe3491fb9854ad5089f56feed874dcf57"

"""
Method to obtain the top_n results for a specific search engine. This method will query the engine
and if need will perform more than 1 query to obtain the top_n organic results.
    Parameters:
    -----------
    params: {dictionary} Dictionary with parameters ued to query a specific search engine
            - engine: the engine we wish to query
            - q || p: The query made to the engine
            - api_key: The api_key used for the serp api
    curr_len: {int} The current length of the organic results its 0(can be local variable chnage that later)
    top_n: {int} The first N results of a specific search engine. Note these are the first N organic results.

    Returns:
    --------
    organic_results: {1d array} It contains the organic results for the top n results.
"""


def get_results_for_engine(params, curr_len, top_n):
    organic_results = []
    search = GoogleSearch(params)
    is_present = True
    # Get all the results
    while is_present:
        results = search.get_dict()
        curr_res = results["organic_results"]

        for res in curr_res:
            if curr_len < top_n:
                organic_results.append(res)
                curr_len += 1
            else:
                print(
                    "We reached the length we wanted! Engine: {0}".format(
                        params["engine"]
                    )
                )
                is_present = False
                break
        # Make sure to break before getting new page this svaes API calls
        if is_present == False:
            break

        try:
            if "next" in results["serpapi_pagination"]:
                print("There is next for engine:{0}".format(params["engine"]))
                search.params_dict.update(
                    dict(
                        parse_qsl(urlsplit(results["serpapi_pagination"]["next"]).query)
                    )
                )
            else:
                is_present = False
        except KeyError:
            is_present = False
    return organic_results


"""
Method to obtain the top_n result from each search engine.
    Parameters:
    -----------
    algo: The search engine being used. For example = {google,bing,duckduckgo}
    query: The query passed to the search engine. For example = {information retrieval evaluation}
    top_n (Optional paramter with default value of 20): The top_n results returned from the search query
    Returns:
    --------
    The organic results from the top_n results 
    
"""


def get_search_results(algo, query, top_n=20):
    if top_n > 50:
        raise Exception("Cannot pass top_n to be more than 50")

    params = {"engine": algo, "q": query, "api_key": API_KEY}
    if algo == "google":
        # Set start to 0 and num to 100 to get maximum results from a single query
        return get_results_for_engine(params, 0, top_n)
    elif algo == "bing":
        return get_results_for_engine(params, 0, top_n)
    elif algo == "duckduckgo":
        return get_results_for_engine(params, 0, top_n)
    elif algo == "yahoo":
        del params["q"]
        params["p"] = query
        return get_results_for_engine(params, 0, top_n)

    # If not one of the 4 search engine return null
    return None


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
        file = open(json_filename, "x")
        file.write(json_result)


"""
Method to load the json data for an engine's results.
    Parameters:
    -----------
    filename: {string} The filename of the document. We assume it is in the same folder

    Return:
    -------
    retrieved_docs: {1d array} A list of the retrieved documents (only the links to the web pages)
"""


def load_from_json(filename):
    input_file = open(filename)
    json_array = json.load(input_file)
    links = [i["link"] for i in json_array]
    return links


"""
Method to calculate the precision and recall for a specific engine's retrived document set
against the relevant document set:
    Parameters:
    -----------
    retrieved_docs: {1d array} A list of the links of the retrieved documents of an engine. The order of the links
    is the order in which they were retrieved from the engine. From first to last top_n
    relevant_docs: {1d array} A list of the links of the retrieved documents of the baseline engine. The order
    of the links is the order in which they were retrieved from the engine.

"""


def precision_recall(retrieved_docs, relevant_docs):
    p_r = []
    in_r = 0
    iterated_docs = 0
    for i in retrieved_docs:
        iterated_docs += 1
        found = False
        for j in relevant_docs:
            if i == j:
                in_r += 1
                found = True
                break
        if found:
            p_r.append((in_r / len(relevant_docs), in_r / iterated_docs))
        else:
            p_r.append((None, None))

    return p_r


"""
Method to obtain the next recall point in order to obtain accurate precision in case of edge cases.
Follow the formula: P(r_j)=max P(r),r_j <= r
    Parameters:
    -----------
    recall: {float} current recall value
    precision_recall: {1d array of tuples (float,float)} the precision recall array for the specific search engine

    Returns:
    --------
    (i,j): {float,float} If next reclal exists we return the recall and the precision value of it
    (None,None): If no precision value exists different than current one then return none none
"""


def get_next_recall(recall, precision_recall):
    for (i, j) in precision_recall:
        if i != None and i >= recall:
            return (i, j)

    return (None, None)


"""
Method to plot the precision at the standard 11 recall levels for a given search engine
results.
    Parameters:
    -----------
    precision_recall: {1d array (Float,Float)} array containig the precision and recall for each results in the result
    set of links for the speciifc search engine
    engine: {string} The search engine for which we are plotting
"""


def precision_at_11_standard_recall_levels(precision_recall, engine):
    precision = []
    recall = []
    curr_recall = 0.0
    for i in range(11):
        recall.append(round(curr_recall, 2))
        (j, k) = get_next_recall(round(curr_recall, 2), precision_recall)
        if k == None:
            precision.append(0)
        else:
            precision.append(round(k, 2))
        curr_recall += 0.1

    plt.plot(recall, precision)
    plt.plot(recall, precision, "ro")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Recall Precision plot for " + engine + "algorithm")
    plt.show()


if __name__ == "__main__":
    # This is used only to get the files ones we got them we will analyze them
    # This will reduce the number of requests made to the serp api engine
    """
    search_query = "information retrieval evaluation"
    search_results = {
        "google": get_search_results("google", search_query, top_n=10),
        "bing": get_search_results("bing", search_query, top_n=20),
        "duckduckgo": get_search_results("duckduckgo", search_query, top_n=20),
        "yahoo": get_search_results("yahoo", search_query, top_n=20),
    }

    save_results_to_file(search_results["google"], "google")
    save_results_to_file(search_results["bing"], "bing")
    save_results_to_file(search_results["duckduckgo"], "duckduckgo")
    save_results_to_file(search_results["yahoo"], "yahoo")
    """
    # If we have the json files just load them for analysis
    # Load json files and trim them to only contain the links of the webpages
    google_links = load_from_json("google.json")
    bing_links = load_from_json("bing.json")
    duckduckgo_links = load_from_json("duckduckgo.json")
    yahoo_links = load_from_json("yahoo.json")
    # Analyze the precision and recall for all of the 4 engine agains the baseline (google)
    precision_recall_google = precision_recall(google_links, google_links)
    precision_recall_bing = precision_recall(bing_links, google_links)
    precision_recall_duckduckgo = precision_recall(duckduckgo_links, google_links)
    precision_recall_yahoo = precision_recall(yahoo_links, google_links)

    print("Precision recall Google:\n{0}\n".format(precision_recall_google))
    print("Precision recall Bing:\n{0}\n".format(precision_recall_bing))
    print("Precision recall Duckduckgo:\n{0}\n".format(precision_recall_duckduckgo))
    print("Precision recall Yahoo:\n{0}\n".format(precision_recall_yahoo))

    # Plot the precision vs recall
    precision_at_11_standard_recall_levels(precision_recall_google, "Google")
    precision_at_11_standard_recall_levels(precision_recall_bing, "Bing")
    precision_at_11_standard_recall_levels(precision_recall_duckduckgo, "DuckDuckGo")
    precision_at_11_standard_recall_levels(precision_recall_yahoo, "Yahoo")

# Precision fraction of retrieved documents which are relevant |R  Intersection with A|/|A|
# 10 relevant 5 ansewrs 2 are in relevant thus 2/5

# Recall fraction of relevant documents that are retrievd |R intersection with A|/|R|
# 10 relevant 5 answers 2 are in relevant 2/10
