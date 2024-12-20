import seaborn as sns
from dataExplore.builder import Builder

tips = sns.load_dataset("tips")
print(tips.head())
b=Builder(tips)
d=b.getExplorer()
