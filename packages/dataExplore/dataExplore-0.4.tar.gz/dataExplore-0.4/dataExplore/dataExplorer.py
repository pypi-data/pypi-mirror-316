from pandas.api.types import is_numeric_dtype
import seaborn as sns
from wordcloud import  WordCloud
import math
import matplotlib.pyplot as plt
class Util:
    def __init__(self, i):
        self.figure= plt.figure( figsize=(10, 15))
        self.figure.title='t'
        self.figure.tight_layout()
        self.Tot = i
        self.Cols = 3
        self.i=0
        # Compute Rows required

        self.Rows = self.Tot // self.Cols

        #     EDIT for correct number of rows:
        #     If one additional row is necessary -> add one:

        if self.Tot % self.Cols != 0:
            self.Rows += 1

        # Create a Position index

        self.Position = range(1, self.Tot + 1)
        print(f'a {self.Rows} b {self.Cols} c {self.Position} d {self.Tot}')
class DataExplorer:
    def __init__(self, dataset):
        self.dataset=dataset
        u=Util(self.dataset.shape[1])
        self.n=NumericExplorer(self.dataset.select_dtypes(include=['float64', 'int64']).copy(),  u)

        self.s=StringExplorer(self.dataset.select_dtypes(include=['object']).copy(),  u)
        self.c=CategoryExplorer(self.dataset.select_dtypes(include=['category']).copy(),  u)

    def hideNan(self):
        self.n.hideNan()
        self.s.hideNan()
        self.c.hideNan()
    def draw(self):

        self.n.draw()
        self.s.draw()
        self.c.draw()
        plt.show()
    def drawInit(self):
        pass
class NumericExplorer(DataExplorer):
    def __init__(self, dataset,  u):
        self.dataset=dataset
        self.u=u

    def hideNan(self):
        self.dataset.fillna(-5, inplace=True)

    def draw(self):
        print(self.u.i)
        for column in self.dataset:
            t = self.u.figure.add_subplot(self.u.Rows, self.u.Cols, self.u.Position[self.u.i])
            sns.violinplot(x=self.dataset[column], ax=t)
            t.set_xlabel(column)
            t.xaxis.set_label_position('top')
            self.u.i+=1


class StringExplorer(DataExplorer):
    def __init__(self, dataset,  u):
        self.dataset=dataset
        self.u = u

    def hideNan(self):

        self.dataset.fillna('-5', inplace=True)
    def draw(self):
        for column in self.dataset:
            t = self.u.figure.add_subplot(self.u.Rows, self.u.Cols, self.u.Position[self.u.i])
            t.set_xlabel(column)
            t.xaxis.set_label_position('top')
            counter = self.dataset[column].value_counts()  # set top 10: df_stack.value_counts()[0:10]
            t.bar(counter.index, counter.values)
            self.u.i += 1

class CategoryExplorer(DataExplorer):
    def __init__(self, dataset,  u):
        self.dataset = dataset

        self.u = u

    def hideNan(self):

        pass

    def draw(self):

        for column in self.dataset:
            t = self.u.figure.add_subplot(self.u.Rows, self.u.Cols, self.u.Position[self.u.i])
            t.set_xlabel(column)
            t.xaxis.set_label_position('top')
            counter = self.dataset[column].value_counts()  # set top 10: df_stack.value_counts()[0:10]
            t.bar(counter.index, counter.values)
            self.u.i+=1



