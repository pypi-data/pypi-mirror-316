from tables import *
import re
import pandas as pd
from .FRSpy import FRSpy
from .h5file_create_array import Writearray
import h5py
import pickle
import os 

def compute_membership_values(df,
                              columns,
                              target,
                              h5_name, 
                              path, 
                              method = 'HMOM', 
                              alpha = 0.5, 
                              implication = 'Luka',
                              conjunction = 'Luka',
                              complete = False, 
                              hide_progress = False):
  '''
  A function that computes the membership values to fuzzy-rough regions for larger datasets. It computes a similarity matrix and stores it in a h5 file. 
  It also computes the fuzzy-rough regions and saves them in a pickle file.

  Attributes
  ------------
  df : pandas DataFrame
    Contains all variables in the dataset plus the decision variable which must be located in the LAST column
  
  columns: list of strings
    a list of the column names to be suppressed or removed from the dataset. after removal, the fuzzy-rough
    set regions will be computed using the rest of the data
    
  h5_name : str
    name of the h5 file where the similarity values are saved
    
  path : str
    path to file, can also be empty and the file will be saved in the current directory
  
  method: string
    Heterogeneus distance functions able to process both numeric and nominal features
    Cane be either 'HMOM', 'HEOM' or 'HVDM'; see journal paper Fuzzy-Rough Cognitive Networks (Nápoles et al., 2018) for the equations

  alpha: float
    parameter to separate the fuzzy-rough regions

  implication: string
    fuzzy implication, options are 'Luka', 'Godel', 'Fodor', 'Goguen' (see publication for details)

  conjunction: string
    fuzzy conjunction, options are 'Standard', 'Algebraic', 'Luka', 'Drastic' (see publication for details)

  complete: boolean
    if True, the membership values to the fuzzy-rought regions are created using the complete set of data. 
    if this object already exists, you can set it to False to save time if dealing with large dataset
  
  '''

  # rename the column names cause they contain illegal characters and h5 cannot index columns properly
  df.columns = list(map(lambda x: re.sub('=<', 'less',x), list(df.columns)))
  df.columns = list(map(lambda x: re.sub('=>', 'more',x), list(df.columns)))
  df.columns = list(map(lambda x: re.sub('/|\(|\)|>|<|=| ', '',x), list(df.columns)))

  # fr values to fuzzy rough regions
  membership = pd.get_dummies(df[target])
  file_name = os.path.join(path, "matrix_"+h5_name+".h5")

  if not complete:
    h5file = open_file(file_name, mode="w", title=h5_name) # create h5 file to store distance matrix

    group = h5file.create_group("/", 'full', 'Distances after removing full') # full
    Writearray(df[columns], alpha, 'full', method=method).sim_array(h5file = h5file, group = group, hide_progress = hide_progress)

    h5file.close()

    h5file = open_file(file_name, mode="r")
    frregions = FRSpy(membership, implication = implication, conjunction = conjunction).regions(file_name,'full', hide_progress = hide_progress)

    file_name_pickle = os.path.join(path, 'full_mem.pickle')
    with open(file_name_pickle, 'wb') as handle:
      pickle.dump(frregions, handle, protocol=pickle.HIGHEST_PROTOCOL)
    h5file.close()

    h5file = h5py.File(file_name, mode="a")
    del h5file['full']
    h5file.close()

  for s_attr in columns:
    # if hide_progress:
    #   print(s_attr)

    h5file = open_file(file_name, mode="a")
    dataset = df[columns].drop(s_attr, axis=1) # remove protected
    group = h5file.create_group("/", s_attr, 'Distances after removing '+s_attr)
    Writearray(dataset, alpha, s_attr, method=method).sim_array(h5file = h5file, group = group, hide_progress = hide_progress)

    h5file.close()
    h5file = open_file(file_name, mode="r")

    frregions = FRSpy(membership, implication = implication, conjunction = conjunction).regions(file_name,s_attr, hide_progress = hide_progress)
    file_name_pickle = os.path.join(path, s_attr+'_mem.pickle')
    with open(file_name_pickle, 'wb') as handle:
      pickle.dump(frregions, handle, protocol=pickle.HIGHEST_PROTOCOL)
    h5file.close()

    h5file = h5py.File(file_name, mode="a")
    del h5file[s_attr]
    h5file.close()

import sys
if __name__=="__main__":
  args = compute_membership_values(sys.argv)
  print("In mymodule:",args)