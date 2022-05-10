#!/usr/bin/env python3
import glob
import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# Read Data for existing experimental data
df = pd.read_csv("existing_essay.csv")
df2 = pd.read_csv("existing_library.csv")
df = df.append(df2)

d = {'ex1': 'library_asp',
     'ex2': '-library_asp',
     'ex3': 'essay_asp',
     'ex4': '-essay_asp',
     }

# parse data from ASP outputs
# df_nu = pd.DataFrame(columns=list(df.columns) + ['essay_asp', '-essay_asp', 'library_asp', '-library_asp'])
df_nu = pd.DataFrame(
    columns=['program', 'smodels_total', 'smodels_assumpt', 'essay_asp', '-essay_asp', 'library_asp', '-library_asp'])
for file in glob.glob("ex*.lp_models"):
    with open(file, 'r') as f:
        prog = file.split('_models')[0]
        plaus, nom, denom = 0, 0, 0
        for line in f.readlines():
            if line.startswith('plaus'):
                plaus = "{:.1f}".format(float(line.split('\n')[0].split('=')[1].strip()) * 100)
            elif line.startswith('num_denom'):
                denom = line.split('\n')[0].split('=')[1].strip()
            elif line.startswith('num_nom'):
                nom = line.split('\n')[0].split('=')[1].strip()

        df_nu = df_nu.append({'program': prog, d[prog[:3]]: plaus, 'smodels_total': denom, 'smodels_assumpt': nom},
                             ignore_index=True)

# print(df.sort_values(by=['program']))
# print(df_nu.sort_values(by=['program']))

df_res = pd.merge(df, df_nu, how="inner", on='program').fillna('-')
columns = ['cases', 'program', 'group', 'smodels_assumpt', 'smodels_total',
           'library_asp', 'library_b', 'library_d', '-library_asp', '-library_b', '-library_d',
           'essay_asp', 'essay_b', 'essay_d', '-essay_asp', '-essay_b', '-essay_d']
df_res = df_res.reindex(columns, axis=1).sort_values(by=['program'])
print(df_res)
df_res.to_csv("result_asp.csv")
df_res.to_latex("result_asp.tex")

# exit(2)
