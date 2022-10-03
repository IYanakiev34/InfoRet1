from inverted_index import InvertedIndex

if __name__ == "__main__":
    a = [1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1]
    b = [1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1]

    inv_ind = InvertedIndex()

    print(inv_ind.cosine_comparison(a, b))
    print(inv_ind.spearman_comparison(a, b))
    print(inv_ind.pearson_comparison(a, b))
    print(inv_ind.euclidian_comparison(a, b))
    print(inv_ind.kendalltau_comparison(a, b))

    ##
    # Results
    # Cosine = 0.97
    # Spearman = 1
    # Pearson = 0.99
    # Euclidian dist = 5.19
    # Kendall = 1.0
