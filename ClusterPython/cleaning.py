import pandas as pd

data = pd.read_csv('query.csv', sep='\t')

bib_nums = data["record_num"].tolist()

dup_vals = set([x for x in bib_nums if bib_nums.count(x) > 1])

from collections import Counter

a = dict(Counter(bib_nums))


data['duplicated_total'] = data["record_num"].map(a)



data.to_csv('data_clean.csv', sep='\t', index=False)