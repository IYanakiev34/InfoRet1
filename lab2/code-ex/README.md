# Questions

## 1

1. I will first explain the overall goal of the formula and then proceed to specifye each terms goals.
   The main goal of the Log-Entropy is given a discrete variable X to decide the amount of surprise if we encounter X.

2. The first component of the equation is logarithm of the term frequency in a certain document why do we need to use it one miught ask. That
   is better explained by using the second term.

3. The second term is the asctual amount of **surprise** for encountering the variable X. The reason we need the first variable is because we
   encounter X, n amount of times. In order to get the total entropy of the term X in a document we need the logarithm of the frequency times
   the surprise to encounter X in the document. The first part of this term is the actual probability of encountering X in the document.
