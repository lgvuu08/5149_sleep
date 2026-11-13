import warnings; warnings.filterwarnings('ignore')
import numpy as np, pandas as pd
# patsy degree 0
from patsy import dmatrix
x=np.array([1,2,3,4,6,8,9,10.])
for f in ["bs(x, knots=(5,7), degree=0)","bs(x, df=6, degree=3)","bs(x, knots=(2,5), degree=3)","ns(x, df=4)","bs(x, knots=(5,7), degree=3, include_intercept=True)"]:
    try:
        d=dmatrix(f,{"x":x}); print(f, d.shape)
    except Exception as e: print(f,'ERR',type(e).__name__,str(e)[:100])
d=dmatrix("bs(x, knots=(5,7), degree=0)",{"x":x}); print(np.asarray(d))
# pgmpy
from pgmpy.models import DiscreteBayesianNetwork, DiscreteMarkovNetwork
from pgmpy.factors.discrete import TabularCPD, DiscreteFactor, State
print([n for n in dir(DiscreteBayesianNetwork) if 'dconn' in n.lower() or 'blanket' in n.lower() or 'active' in n.lower() or 'indep' in n.lower()])
from pgmpy.sampling import BayesianModelSampling
from pgmpy.inference import VariableElimination
import pgmpy.estimators as E; print([n for n in dir(E) if 'MLE' in n or 'Bayes' in n or 'MaximumL' in n or 'PC' in n or 'CI' in n])
import pgmpy.estimators.CITests as C; print([n for n in dir(C) if not n.startswith('_')][:20])
try:
    import torchcrf; print('torchcrf ok')
except Exception as e: print('torchcrf missing')
from sklearn.manifold import TSNE; print(hasattr(TSNE(),'transform'))
