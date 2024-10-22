# Frequent Itemset Miner

Python 3 standard library implementation of the Apriori algorithm. Expected input data format is one row per transaction, with space-separated integers representing items.

### Write frequent itemsets file
- Output format is \<itemset size\> \<co-occurrence frequency\> \<item 1 id\> \<item 2 id\> ... \<item n id\>

From a Python 3 shell, run:
```
python miner.py <data file> <output file> <(optional) support parameter> <(optional) minimum set size to consider>
```
Note that if the support parameter, minimum set size, or both are omitted, they will default to 4 and 3, respectively.


## Example
- Creates frequent_itemsets.txt file found in this repo, using included transactions.dat

```
python miner.py "./transactions.dat" "./frequent_itemsets.txt" 50 5
```
