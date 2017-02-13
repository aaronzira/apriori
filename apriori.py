from collections import Counter,defaultdict
from itertools import dropwhile

class APriori():

    def __init__(self,data,out):

        self.data = data
        self.out = out
        self.previous = []
        self.frequent = defaultdict(Counter)


    def find_frequent(self,support,min_set_size):

        self.sigma = support
        self.min_set = min_set_size
        self.frequent[1] = self._generate_data()

        k = 2
        # there must be at least k itemsets of size k-1 already found to
        # be frequent for there to be any frequent k-itemsets
        while len(self.frequent[k-1]) >= k:

            for i in range(len(self.previous)):
                # find per-transaction candidates of size k-1. groups generated
                # on previous pass, and checked against frequent itemsets now
                k_minus_1 = [group for group in self.previous[i]
                if group in self.frequent[k-1]]

                # order is cruicial: items in tuples are sorted here, while
                # ordering of tuples was established on the first pass
                cand = [tuple(sorted(frozenset(x).union(y))) for x in k_minus_1
                for y in k_minus_1 if x < y and x[:-1] == y[:-1]]

                # only those candidates need to be considered on the next pass
                self.previous[i] = cand

                # increment counts
                for group in cand:
                    self.frequent[k][group] += 1

            # drop infrequent keys
            self.frequent[k] = self._drop_infrequent(k)

            k += 1

        # write out file with format:
        # <itemsize> <support> <item 1 id > <item 2 id> ... <item N id>
        # ordered by itemsize, descending frequency, and item id
        with open(self.out,"w") as f:
            for key in self.frequent.keys():
                if key >= self.min_set:
                    for k,v in sorted(self.frequent[key].items(),
                                      key=lambda x:(-x[1],x[0])):
                        print(key,v,*k,file=f)

        return


    def _drop_infrequent(self,k):
        """Remove keys from frequent items counter if their counts are below the
        support threshold. Check counts in descending order until reaching the
        first that is below the support threshold, then safely delete all such
        keys that follow."""

        for key,count in dropwhile(lambda key_ct: key_ct[1] >= self.sigma,
                                   self.frequent[k].most_common()):
                del self.frequent[k][key]

        print("Frequent {}-itemsets generated.".format(k))

        return self.frequent[k]


    def _generate_data(self):
        """Generate a list of viable transactions and counts of frequent
        singletons on the first pass. Only transactions as long as the minimum
        set size are considered, and frequent itemset keys are k-tuples of
        integers of item ids, in order to generalize for k > 1. Transactions
        themselves are not stored in memory, but rather a list of sorted lists
        of size k-1 candidates from each transaction, as only those could
        possibly generate frequent itemsets of size k.
        """

        with open(self.data, "r") as f:
            for line in f.readlines():
                # ensure there are no duplicate items in the transaction
                items = [tuple([int(item)]) for item in set(line.split())]

                # ignore transactions shorter than the min set size
                if len(items) >= self.min_set:
                    # sort to avoid generating duplicate candidate with k > 1
                    self.previous.append(sorted(items))
                    for item in items:
                        self.frequent[1][item] += 1

        self.frequent[1] = self._drop_infrequent(1)

        return self.frequent[1]
