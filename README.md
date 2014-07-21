microbPLSA
==========

### Why microbPLSA?
Big data needs big analyses and big visualization. [Probabilistic Latent Semantic Analysis](http://cs.brown.edu/~th/papers/Hofmann-UAI99.pdf) (PLSA) was originally developped as an indexing tool to organize large collections of word documents from word occurences. PLSA is a dimension reduction technique that finds patterns in the dataset by probabilistically determining the 'topics' driving the word-document structure. For example, the frequent co-occurence of the words 'hollywood', 'love', and 'celebrity' could be detected in a collection of magazines as being strongly associated to a topic. Different visualization can are used to explore the relationship between topics and the word-document structure such as [parallel plots](http://syntagmatic.github.io/parallel-coordinates/). 

### What is microbPLSA?
MicrobPLSA expands [Mathieu Blondel's PLSA python package](http://www.mblondel.org/journal/2010/06/13/lsa-and-plsa-in-python/) by adding some analyses modules and automizing different visualization techniques.


*Packages*:
* numpy
* scipy
* matplotlib

Note: microbPLSA was developped in the 2.7 version of Python
