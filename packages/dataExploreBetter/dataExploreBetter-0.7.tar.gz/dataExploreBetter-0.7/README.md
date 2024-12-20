This package provides data visualiazation on dataset
To install press pip install dataExplore
To run please call
from dataExplore.builder import Builder
import seaborn as sns
tips = sns.load_dataset("tips")
print(tips.head())
b=Builder(tips)
d=b.getExplorer()