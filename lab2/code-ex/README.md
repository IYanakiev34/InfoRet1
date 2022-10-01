# Questions

## 1

1. I will first explain the overall goal of the formula and then proceed to specifye each terms goals.
   The main goal of the Log-Entropy is given a discrete variable X to decide the amount of surprise if we encounter X.

2. The first component of the equation is logarithm of the term frequency in a certain document why do we need to use it one might ask. That
   is better explained by using the second term. The frequency of the term can also be described as the probability that this term occurs in document j.

3. The second term is the asctual amount of **surprise** for encountering the variable X. The reason we need the first variable is because we
   encounter X, n amount of times. In order to get the total entropy of the term X in a document we need the logarithm of the frequency times
   the surprise to encounter X in the document. The first part of this term is the actual probability of encountering X in the document.

## Problems with TF model

1. Repetition of terms rigs the system
2. Long documents favored
3. Global frequence as of local
4. Repetition does not mean relevant

## TD-IDF model

1. Rare term => high
2. Update term matrix

## Log-Entropy model

1. Calculate surprise base don probability, probability is just the frequence of local vs global
