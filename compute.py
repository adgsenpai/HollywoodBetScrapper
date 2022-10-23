import glob
import os
from re import T
import pandas as pd


# if best.xlsx exists, delete it
if os.path.exists('best.xlsx'):
    os.remove('best.xlsx')

# find all xlsx files
path = './'
all_files = glob.glob(os.path.join(path, "*.xlsx"))

# open all the files as a pandas dataframe (t1,t2,o1,o2,o3) add it to seperate dfs
dfs = []
for filename in all_files:
    # extract filename without extension
    bookmaker = os.path.splitext(os.path.basename(filename))[0]
    if bookmaker == 'best':
        pass
    dfs.append({bookmaker: pd.read_excel(filename)})

# find the best (o1,o2,o3) for each match (t1,t2) in all dfs

df_best = pd.DataFrame(
    columns=['t1', 't2', 'o1', 'o2', 'o3', 'b1', 'b2', 'b3'])

# iterate over dfs find the best (o1,o2,o3) for each match (t1,t2) and add a new column bookmaker for (o1,o2,o3)
for df in dfs:
    for bookmaker, ds in df.items():
        currentDF = ds
        # iterate over rows in currentDF
        for index, row in currentDF.iterrows():
            t1 = row['t1']
            t2 = row['t2']
            o1 = row['o1']
            o2 = row['o2']
            o3 = row['o3']
            b1 = bookmaker
            b2 = bookmaker
            b3 = bookmaker
            for compDF in dfs:
                for compbookmaker, compds in compDF.items():
                    for compindex, comprow in compds.iterrows():
                        compt1 = comprow['t1']
                        compt2 = comprow['t2']
                        compo1 = comprow['o1']
                        compo2 = comprow['o2']
                        compo3 = comprow['o3']
                        if (t1 == compt1) and (t2 == compt2):
                            if o1 < compo1:
                                o1 = compo1
                                b1 = compbookmaker
                            if o2 < compo2:
                                o2 = compo2
                                b2 = compbookmaker
                            if o3 < compo3:
                                o3 = compo3
                                b3 = compbookmaker
            if t1 not in df_best['t1'].values:
                df_best = df_best.append(
                    {'t1': t1, 't2': t2, 'o1': o1, 'o2': o2, 'o3': o3, 'b1': b1, 'b2': b2, 'b3': b3}, ignore_index=True)


# calculate the (1/o1+1/o2+1/o3) for each match in a column called 'arb'
df_best['arb'] = 1/df_best['o1'] + 1/df_best['o2'] + 1/df_best['o3']

# sort the dataframe by 'arb' in descending order
df_best.sort_values(by=['arb'], ascending=True, inplace=True)

df_best

# save as best.xlsx
df_best.to_excel('best.xlsx')
