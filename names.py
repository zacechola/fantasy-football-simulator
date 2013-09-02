import pandas as pd
import numpy as np


years = range(1880, 2012)
pieces = []
columns = ['name', 'sex', 'births']

for year in years:
    path = 'names/yob%d.txt' % year
    frame = pd.read_csv(path, names=columns)

    frame['year'] = year
    pieces.append(frame)

names = pd.concat(pieces, ignore_index=True)

total_births = names.pivot_table('births', rows='year', cols='sex', aggfunc=sum)

total_births.plot(title='Total biths by sex and year')

def add_prop(group):
    births = group.births.astype(float)

    group['prop'] = births / births.sum()
    return group

names = names.groupby(['year', 'sex']).apply(add_prop)

np.allclose(names.groupby(['year', 'sex']).prop.sum(), 1)
