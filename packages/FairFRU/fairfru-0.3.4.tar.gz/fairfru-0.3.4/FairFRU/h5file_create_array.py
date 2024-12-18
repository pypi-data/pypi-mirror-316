import numpy as np
from tables import *
from tqdm import tqdm

class Writearray:
    '''
    This class computes the similarity matrix based on which the fuzzy rough sets are later computed
    '''

    def __init__(self, df, alpha, variable, method):
        '''
        Preprocessing steps, the numeric variables are normalized in the interval [0,1]

        Attributes
        ----------
        df : pandas DataFrame
            a dataset consisting of several variables, note that no decision / outcome feature should be present
        
        alpha : float
            this variable in the interval [0,1] helps separating the fuzzy-rough regions, 
            the larger it is the more separated the regions
        
        variable : string
            name of variable that is uppressed

        Returns
        -------
        Creates a h5file in the specified location, the file contains the square distance matrix
        '''
        self.variable = variable
        self.numeric = [False if df[col].dtype == 'object' else True for col in df]
        self.nominal = [True if df[col].dtype == 'object' else False for col in df]

        num = df.loc[:,self.numeric]
        scaled=np.subtract(num,np.min(num,axis=0))/np.subtract(np.max(num,axis=0),np.min(num,axis=0))
        df.loc[:,df.columns[self.numeric]] = scaled.round(3).astype('float32')

        self.df = df.values
        self.alpha = alpha
        self.distance = method

    def sim_array(self, h5file, group, hide_progress = False):
       for instance in tqdm(range(0,len(self.df)), desc=self.variable+' building similarity matrix', disable=hide_progress, miniters=1000):
          sim = self.similarity(instance)
          h5file.create_array(group, 'col'+str(instance), sim, 'Distance instance '+str(instance))

    def similarity(self, i):
        '''
        See here for the equations: https://jair.org/index.php/jair/article/view/10182/24168
        '''

        if self.distance == 'HMOM':
           d = np.sum(np.abs(np.subtract(self.df[i][self.numeric], self.df[:,self.numeric])), axis=1) + np.sum(self.df[i][self.nominal] != self.df[:,self.nominal],axis=1)
        
        elif self.distance == 'HEOM':
           d_num = np.sum((np.subtract(self.df[i][self.numeric], self.df[:,self.numeric])**2), axis=1)
           d_nom = np.sum(self.df[i][self.nominal] != self.df[:,self.nominal],axis=1)
           d = (d_num + d_nom)**0.5

        else:
           print('Distance function not specified')
        
        return np.exp(-self.alpha * d.astype('float32'))
    
import sys
if __name__=="__main__":
  args = Writearray(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]).sim_array(sys.argv[5], sys.argv[6], sys.argv[7])
  print("In mymodule:",args)