"""All code shown in the exam. Each entry is executed by run_all.py to obtain the TRUE output
(the answer key is written from these outputs, never from memory)."""

CODE = {}

# ------------------------------------------------------------------ MCQ
CODE['A1'] = '''import numpy as np, pandas as pd

df = pd.DataFrame({'Area':  [50, 60, np.nan, 80, 70],
                   'Type':  ['A', 'B', 'A', np.nan, 'B'],
                   'Price': [200, 250, 230, 300, 280]})
df['Area'] = df['Area'].fillna(df['Area'].mean())
df['Type'] = df['Type'].fillna(df['Type'].mode()[0])
X = pd.get_dummies(df[['Area', 'Type']], drop_first=True)

print(df['Area'].tolist())
print(df['Type'].tolist())
print(X.shape, list(X.columns))
print(df.isna().sum().sum())
print(round(df['Area'].std(), 2), round(np.std(df['Area'].to_numpy()), 2))'''

CODE['A2'] = '''import numpy as np

neg_mse = np.array([-9.0, -16.0, -25.0])      # what cross_val_score(..., scoring="neg_mean_squared_error") returned
rmse = np.sqrt(-neg_mse)

print(rmse)
print(rmse.mean())
print(np.sqrt((-neg_mse).mean()))
print(rmse.std())
print(rmse.std(ddof=1))'''

CODE['A3'] = '''import numpy as np
from sklearn.metrics import confusion_matrix

y_true = np.array([0, 0, 0, 0, 0, 0, 1, 1, 1, 1])
prob   = np.array([0.10, 0.20, 0.30, 0.40, 0.55, 0.60, 0.35, 0.50, 0.80, 0.90])   # P(default = 1)
pred = (prob > 0.5).astype(int)
cm = confusion_matrix(y_true, pred)

print(pred)
print(cm)
print((pred != y_true).mean())
print(cm[1, 1] / cm[1].sum())
print(cm[1, 1] / cm[:, 1].sum())
pred2 = (prob >= 0.5).astype(int)
print(confusion_matrix(y_true, pred2)[1, 1] / 4)'''

CODE['A4'] = '''import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from patsy import dmatrix

P = PolynomialFeatures(degree=2)
print(P.fit_transform([[2, 3]]))
print(P.get_feature_names_out(['a', 'b']))
print(PolynomialFeatures(degree=2, include_bias=False, interaction_only=True).fit_transform([[2, 3]]))

x = np.linspace(0, 10, 11)
print(dmatrix("bs(x, df=6, degree=3)", {"x": x}).shape)
print(dmatrix("bs(x, knots=(3, 6), degree=3)", {"x": x}).shape)'''

CODE['A5'] = '''import numpy as np
from sklearn.datasets import make_blobs
from sklearn.svm import SVC

X, y = make_blobs(n_samples=200, centers=[[0, 0], [3, 3]], cluster_std=1.5, random_state=0)
for C in [0.001, 0.1, 100]:
    m = SVC(kernel='linear', C=C).fit(X, y)
    print(C, m.n_support_, round(m.score(X, y), 3))'''

CODE['A6'] = '''import torch, torch.nn as nn

x = torch.randn(8, 3, 64, 64)                     # (batch, channels, height, width)
conv = nn.Conv2d(3, 16, kernel_size=5, stride=2, padding=2)
pool = nn.MaxPool2d(kernel_size=2, stride=2)
gap  = nn.AdaptiveAvgPool2d(1)

h = conv(x)
p = pool(h)
print(h.shape)
print(p.shape)
print(gap(p).shape)
print(nn.Flatten()(p).shape)
print(sum(q.numel() for q in conv.parameters()))'''

CODE['A7'] = '''import torch, torch.nn as nn

w = torch.tensor([2.0], requires_grad=True)
for _ in range(2):
    loss = (3 * w) ** 2
    loss.backward()
print(w.grad)

w.grad.zero_()
loss = (3 * w) ** 2
loss.backward()
print(w.grad)

logits = torch.tensor([[2.0, 0.0]])
target = torch.tensor([0])
ce = nn.CrossEntropyLoss()
print(round(ce(logits, target).item(), 3))
print(round(ce(torch.softmax(logits, dim=1), target).item(), 3))'''

CODE['A8'] = '''import torch, math

Q = K = V = torch.tensor([[1.0, 0.0],
                          [0.0, 1.0]])
scores = Q @ K.T / math.sqrt(Q.size(-1))
w = torch.softmax(scores, dim=-1)
print(w.round(decimals=3))
print((w @ V).round(decimals=3))

mask = torch.tensor([[1, 0],
                     [1, 1]])                      # 1 = may attend, 0 = blocked
w2 = torch.softmax(scores.masked_fill(mask == 0, float('-inf')), dim=-1)
print(w2.round(decimals=3))
print(w.sum(dim=-1))'''

CODE['A9'] = '''import numpy as np
from sklearn.cluster import KMeans

X = np.array([[1], [2], [3], [10], [11], [12]])
km = KMeans(n_clusters=2, n_init=10, random_state=0).fit(X)

print(np.sort(km.cluster_centers_.ravel()))
print(km.inertia_)
print(km.predict([[6]]) == km.labels_[0])
print(len(set(km.labels_[:3])), len(set(km.labels_[3:])))
print(KMeans(n_clusters=3, n_init=10, random_state=0).fit(X).inertia_)'''

CODE['A10'] = '''import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, fcluster

X = np.array([[0.], [1.], [3.], [7.], [12.]])
d = pdist(X)
Z = linkage(d, method='single')
print(len(d))
print(Z)
print(fcluster(Z, t=2, criterion='maxclust'))
Zc = linkage(X, method='complete')
print(Zc[:, 2])
print(fcluster(Zc, t=2, criterion='maxclust'))'''

CODE['A11'] = '''import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE

X = np.array([[2, 0], [0, 1], [-2, 0], [0, -1]], dtype=float)

pca = PCA(n_components=2).fit(X)
print(pca.explained_variance_ratio_.round(2))
print(np.abs(pca.transform([[1, 1]])).round(2))
print(pca.components_.shape)

Z = StandardScaler().fit_transform(X)
print(PCA().fit(Z).explained_variance_ratio_.round(2))
print(PCA(n_components=0.75).fit(X).n_components_)
print(hasattr(TSNE(n_components=2), 'transform'))'''

CODE['A12'] = '''from pgmpy.models import DiscreteBayesianNetwork

m = DiscreteBayesianNetwork([('D', 'G'), ('I', 'G'), ('G', 'L'), ('I', 'S')])
print(m.is_dconnected('D', 'I'))
print(m.is_dconnected('D', 'I', observed=['L']))
print(m.is_dconnected('D', 'S'))
print(m.is_dconnected('D', 'S', observed=['G']))
print(m.is_dconnected('L', 'S', observed=['G']))
print(sorted(m.get_markov_blanket('G')))
print(sorted(m.get_markov_blanket('I')))'''

CODE['A13'] = '''import numpy as np
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD

m = DiscreteBayesianNetwork([('D', 'G'), ('I', 'G'), ('G', 'L'), ('I', 'S')])
m.add_cpds(
    TabularCPD('D', 2, [[0.6], [0.4]], state_names={'D': ['easy', 'hard']}),
    TabularCPD('I', 2, [[0.7], [0.3]], state_names={'I': ['low', 'high']}),
    TabularCPD('G', 3, [[0.30, 0.05, 0.90, 0.50],
                        [0.40, 0.25, 0.08, 0.30],
                        [0.30, 0.70, 0.02, 0.20]],
               evidence=['I', 'D'], evidence_card=[2, 2],
               state_names={'G': ['A', 'B', 'C'], 'I': ['low', 'high'], 'D': ['easy', 'hard']}),
    TabularCPD('S', 2, [[0.95, 0.20], [0.05, 0.80]], evidence=['I'], evidence_card=[2],
               state_names={'S': ['weak', 'strong'], 'I': ['low', 'high']}),
    TabularCPD('L', 2, [[0.10, 0.40, 0.99], [0.90, 0.60, 0.01]], evidence=['G'], evidence_card=[3],
               state_names={'L': ['weak', 'strong'], 'G': ['A', 'B', 'C']}),
)
print(m.check_model())
print(round(m.get_state_probability({'D': 'hard', 'I': 'low', 'G': 'B', 'S': 'weak', 'L': 'strong'}), 4))
print(sum((c.variable_card - 1) * int(np.prod(c.cardinality[1:])) for c in m.get_cpds()))
print(2 * 2 * 3 * 2 * 2 - 1)'''

CODE['A14'] = '''from pgmpy.factors.discrete import DiscreteFactor

phi1 = DiscreteFactor(['A', 'B'], [2, 2], [3, 1, 1, 3])   # values listed as (A0B0, A0B1, A1B0, A1B1)
phi2 = DiscreteFactor(['B', 'C'], [2, 2], [2, 1, 1, 2])   # values listed as (B0C0, B0C1, B1C0, B1C1)

psi = phi1 * phi2
print(psi.scope(), psi.values.shape)
tau = psi.marginalize(['B'], inplace=False)
print(tau.scope())
print(tau.values)
print(tau.values.sum())
tau.normalize()
print(tau.values.round(3))
print(phi1.reduce([('A', 0)], inplace=False).values)'''

CODE['A15'] = '''def run(order):
    factors = [{'A', 'B'}, {'B', 'C'}, {'C', 'D'}, {'B', 'D'}, {'D', 'E'}]
    sizes = []
    for v in order:
        involved = [f for f in factors if v in f]
        scope = set().union(*involved)           # scope of psi before the sum
        sizes.append(len(scope))
        factors = [f for f in factors if v not in f] + [scope - {v}]
    return sizes

print(run('ABCDE'))
print(run('BDACE'))
print(max(run('ABCDE')), max(run('BDACE')))'''

CODE['A16'] = '''def skel(E):
    return {frozenset(e) for e in E}

def immor(E):
    pa = {}
    for u, v in E:
        pa.setdefault(v, set()).add(u)
    s = skel(E)
    return {(frozenset((a, b)), c) for c, ps in pa.items() for a in ps for b in ps
            if a < b and frozenset((a, b)) not in s}

G1 = [('X', 'Y'), ('Y', 'Z')]
G2 = [('Z', 'Y'), ('Y', 'X')]
G3 = [('X', 'Y'), ('Z', 'Y')]
G4 = [('Y', 'X'), ('Y', 'Z')]
for G in (G1, G2, G3, G4):
    print(sorted(map(sorted, skel(G))), len(immor(G)))
same = lambda A, B: skel(A) == skel(B) and immor(A) == immor(B)
print(same(G1, G2), same(G1, G3), same(G1, G4))'''

# ------------------------------------------------------------------ Short answer
CODE['B1'] = '''import numpy as np
from scipy.linalg import hadamard
from sklearn.linear_model import Lasso, Ridge

H = hadamard(8).astype(float)
X = H[:, 1:6]                              # 5 columns of +-1 that are mutually orthogonal: X.T @ X = 8 * I
beta = np.array([4.0, -3.0, 2.0, 1.0, 0.5])
y = X @ beta                               # no noise

print(np.linalg.lstsq(X, y, rcond=None)[0].round(3) + 0.0)
for a in [0.5, 1.5, 3.5]:
    print('lasso', a, Lasso(alpha=a, fit_intercept=False).fit(X, y).coef_.round(3) + 0.0)
print('ridge', 8, Ridge(alpha=8, fit_intercept=False).fit(X, y).coef_.round(3) + 0.0)'''

CODE['B2'] = '''import numpy as np, pandas as pd
import statsmodels.formula.api as smf

df = pd.DataFrame({'x': [1, 2, 3, 4, 6, 6.5, 8, 9, 10],
                   'y': [2, 4, 3, 3, 8, 9, 5, 7, 6]})
m = smf.ols('y ~ bs(x, knots=(5, 7), degree=0)', data=df).fit()

print(m.params.round(2).tolist())
print(m.predict(pd.DataFrame({'x': [2.5, 6.2, 9.5]})).round(2).tolist())
print(m.df_model)
print(round(m.ssr, 2))'''

CODE['B3'] = '''import numpy as np
from sklearn.svm import SVC

X = np.array([[3, 4], [2, 2], [4, 4], [1, 4], [2, 1], [4, 3], [4, 1]], dtype=float)
y = np.array(['red'] * 4 + ['blue'] * 3)
m = SVC(kernel='linear', C=1e6).fit(X, y)

print(m.classes_)
print(m.n_support_)
print(sorted(m.support_.tolist()))
print(m.coef_.round(2), m.intercept_.round(2))
print(m.predict([[3, 1], [1, 1]]))
print(m.decision_function([[3, 2]]).round(2))'''

CODE['B4'] = '''import numpy as np

x  = np.array([1.0, 2.0])
W1 = np.array([[0.5, -1.0], [1.0, 0.5], [-0.5, 1.0]])      # shape (3, 2)
b1 = np.array([0.0, -1.0, 0.5])
W2 = np.array([[1.0, 0.5, -1.0], [-1.0, 2.0, 1.0]])        # shape (2, 3)
b2 = np.array([0.0, 0.5])

u = W1 @ x + b1
h = np.maximum(0, u)
z = W2 @ h + b2
p = np.exp(z - z.max()); p /= p.sum()
y = np.array([1, 0])                                       # one-hot label
loss = -np.sum(y * np.log(p))

dz  = p - y
dW2 = np.outer(dz, h)
dh  = W2.T @ dz
du  = dh * (u > 0)
dW1 = np.outer(du, x)

print(u, h, z)
print(p.round(3), round(loss, 3), np.argmax(p))
print(dW2.round(3) + 0.0)
print(dW1.round(3) + 0.0)
print(W1.size + b1.size + W2.size + b2.size)'''

CODE['B5'] = '''import numpy as np
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage, fcluster

D = np.array([[0, 2, 6, 10, 9],
              [2, 0, 5,  9, 8],
              [6, 5, 0,  4, 5],
              [10, 9, 4, 0, 3],
              [9, 8, 5,  3, 0]], dtype=float)
Z = linkage(squareform(D), method='average')
print(Z.round(2))
print(fcluster(Z, t=2, criterion='maxclust'))
print(fcluster(Z, t=3.0, criterion='distance'))'''

CODE['B6'] = '''import numpy as np

X = np.array([[1, 1], [-1, -1], [2, -2], [-2, 2]], dtype=float)
Xc = X - X.mean(axis=0)
S = Xc.T @ Xc / (len(X) - 1)
vals, vecs = np.linalg.eigh(S)
order = np.argsort(vals)[::-1]
vals, vecs = vals[order], vecs[:, order]

print(vals.round(3))
print((vals / vals.sum()).round(3))
scores = Xc @ vecs[:, 0]
print(np.abs(scores).round(3))
recon = np.outer(scores, vecs[:, 0])
print(round(float(np.sum((Xc - recon) ** 2)), 3))'''

CODE['B7'] = '''import numpy as np
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

m = DiscreteBayesianNetwork([('Pollution', 'Cancer'), ('Smoker', 'Cancer'),
                             ('Cancer', 'Xray'), ('Cancer', 'Dyspnoea')])
m.add_cpds(
    TabularCPD('Pollution', 2, [[0.9], [0.1]], state_names={'Pollution': ['low', 'high']}),
    TabularCPD('Smoker', 2, [[0.3], [0.7]], state_names={'Smoker': ['T', 'F']}),
    TabularCPD('Cancer', 2, [[0.03, 0.05, 0.001, 0.02], [0.97, 0.95, 0.999, 0.98]],
               evidence=['Smoker', 'Pollution'], evidence_card=[2, 2],
               state_names={'Cancer': ['T', 'F'], 'Smoker': ['T', 'F'], 'Pollution': ['low', 'high']}),
    TabularCPD('Xray', 2, [[0.9, 0.2], [0.1, 0.8]], evidence=['Cancer'], evidence_card=[2],
               state_names={'Xray': ['pos', 'neg'], 'Cancer': ['T', 'F']}),
    TabularCPD('Dyspnoea', 2, [[0.65, 0.3], [0.35, 0.7]], evidence=['Cancer'], evidence_card=[2],
               state_names={'Dyspnoea': ['T', 'F'], 'Cancer': ['T', 'F']}),
)
ve = VariableElimination(m)
q1 = ve.query(['Cancer'], evidence={'Smoker': 'T', 'Pollution': 'high'}, show_progress=False)
q2 = ve.query(['Cancer'], evidence={'Smoker': 'T', 'Pollution': 'high', 'Xray': 'pos', 'Dyspnoea': 'T'}, show_progress=False)
q3 = ve.query(['Cancer'], evidence={'Xray': 'pos'}, show_progress=False)
q4 = ve.query(['Xray', 'Dyspnoea'], evidence={'Cancer': 'T'}, show_progress=False)
print(q1.state_names['Cancer'], np.round(q1.values, 4))
print(np.round(q2.values, 4))
print(np.round(q3.values, 4))
print(np.round(q4.values, 4))
print(m.is_dconnected('Xray', 'Dyspnoea'), m.is_dconnected('Xray', 'Dyspnoea', observed=['Cancer']))'''

CODE['B8'] = '''import itertools
import numpy as np

emit  = np.array([[4, 1], [2, 3], [1, 5]], dtype=float)    # emit[t, label],  label 0 = O, 1 = P
trans = np.array([[2, 1], [1, 3]], dtype=float)            # trans[prev, cur]

def score(y):
    s = np.prod([emit[t, y[t]] for t in range(3)])
    s *= np.prod([trans[y[t - 1], y[t]] for t in range(1, 3)])
    return s

scores = {y: score(y) for y in itertools.product([0, 1], repeat=3)}
Z = sum(scores.values())
best = max(scores, key=scores.get)

print(len(scores), Z)
print(best, scores[best], round(scores[best] / Z, 4))
print(round(sum(v for y, v in scores.items() if y[1] == 1) / Z, 4))'''

CODE['B9'] = '''import numpy as np

pA   = np.array([0.6, 0.4])
pB_A = np.array([[0.7, 0.3], [0.2, 0.8]])      # rows: A, columns: B
pC_B = np.array([[0.9, 0.1], [0.4, 0.6]])      # rows: B, columns: C
pD_C = np.array([[0.5, 0.5], [0.1, 0.9]])      # rows: C, columns: D

tau1 = pA @ pB_A
tau2 = tau1 @ pC_B
pD   = tau2 @ pD_C
print(tau1, tau2, pD)

m = np.einsum('a,ab,bc,c->a', pA, pB_A, pC_B, pD_C[:, 1])
print(m.round(3), m.sum().round(3))
print((m / m.sum()).round(4))'''

CODE['B10'] = '''import numpy as np

P_G = {(0, 0): [.30, .40, .30], (0, 1): [.05, .25, .70],    # key = (I, D); entries over G = 0, 1, 2
       (1, 0): [.90, .08, .02], (1, 1): [.50, .30, .20]}
P_S1 = {0: 0.05, 1: 0.80}                                   # P(S = 1 | I)
P_L1 = {0: 0.90, 1: 0.60, 2: 0.01}                          # P(L = 1 | G)

def draw(probs, u):                 # first state k with u <= cumulative probability
    return int(np.argmax(u <= np.cumsum(probs)))

def forward_sample(u):              # order D, I, G, S, L
    d = draw([0.6, 0.4], u[0])
    i = draw([0.7, 0.3], u[1])
    g = draw(P_G[(i, d)], u[2])
    s = draw([1 - P_S1[i], P_S1[i]], u[3])
    l = draw([1 - P_L1[g], P_L1[g]], u[4])
    return d, i, g, s, l

U = [[0.31, 0.18, 0.60, 0.92, 0.45],
     [0.75, 0.55, 0.20, 0.10, 0.95],
     [0.10, 0.90, 0.50, 0.60, 0.05],
     [0.80, 0.20, 0.40, 0.77, 0.15]]
samples = [forward_sample(u) for u in U]
kept = [s for s in samples if s[3] == 1 and s[4] == 0]      # evidence S = 1, L = 0

for s in samples: print(s)
print(kept)
print(len(kept) / len(samples))'''

CODE['B11'] = '''import numpy as np

PD, PI = np.array([0.6, 0.4]), np.array([0.7, 0.3])
PG  = {(0, 0): [.30, .40, .30], (0, 1): [.05, .25, .70], (1, 0): [.90, .08, .02], (1, 1): [.50, .30, .20]}  # key (i, d)
PS1 = np.array([0.05, 0.80])            # P(S = 1 | I)
PL0 = np.array([0.10, 0.40, 0.99])      # P(L = 0 | G)

def draw(p, u): return int(np.argmax(u <= np.cumsum(p)))
def cond_D(g, i): w = np.array([PG[(i, d)][g] * PD[d] for d in (0, 1)]);                 return w / w.sum()
def cond_I(g, d): w = np.array([PG[(i, d)][g] * PS1[i] * PI[i] for i in (0, 1)]);        return w / w.sum()
def cond_G(d, i): w = np.array([PL0[g] * PG[(i, d)][g] for g in range(3)]);              return w / w.sum()

d, i, g = 0, 0, 1                        # evidence S = 1, L = 0 is held fixed
for u in [(0.80, 0.50, 0.70), (0.30, 0.20, 0.95)]:
    p = cond_D(g, i); d = draw(p, u[0]); print(p.round(3), d)
    p = cond_I(g, d); i = draw(p, u[1]); print(p.round(3), i)
    p = cond_G(d, i); g = draw(p, u[2]); print(p.round(3), g)
    print((d, i, g))'''

CODE['B12'] = '''import numpy as np

sigmoid = lambda t: 1 / (1 + np.exp(-t))
W = np.array([[ 1.0, -2.0,  0.5,  0.0],
              [-1.0,  1.5,  0.0,  2.0],
              [ 2.0,  0.0, -1.0, -0.5]])        # 3 visible x 4 hidden
a = np.array([0.0, -0.5, 0.5])                  # visible biases
b = np.array([-1.0, 0.0, 0.5, -0.5])            # hidden biases

v    = np.array([0, 1, 1])
p_h  = sigmoid(b + v @ W);    h  = (np.array([0.70, 0.10, 0.45, 0.20]) < p_h).astype(int)
p_v  = sigmoid(a + W @ h);    v2 = (np.array([0.05, 0.99, 0.30]) < p_v).astype(int)
p_h2 = sigmoid(b + v2 @ W)
dW   = np.outer(v, p_h) - np.outer(v2, p_h2)

print(p_h.round(3), h)
print(p_v.round(3), v2)
print(p_h2.round(3))
print(dW.round(3))'''

CODE['B13a'] = '''import itertools

V = ['X', 'Y', 'Z', 'W']
alpha = 0.05
table = {(('X', 'Y'), ()): 0.70, (('W', 'X'), ('Z',)): 0.60, (('W', 'Y'), ('Z',)): 0.50}   # every other test: p = 0.0005

def pvalue(a, b, S):
    return table.get((tuple(sorted((a, b))), tuple(sorted(S))), 0.0005)

edges = {frozenset(e) for e in itertools.combinations(V, 2)}
sepset = {}
for size in range(3):
    for e in sorted(edges, key=lambda e: sorted(e)):
        if e not in edges: continue
        a, b = sorted(e)
        cand = sorted(v for v in V if v not in e and (frozenset((a, v)) in edges or frozenset((b, v)) in edges))
        for S in itertools.combinations(cand, size):
            if pvalue(a, b, S) > alpha:
                edges.discard(e); sepset[(a, b)] = S
                break

print(sorted(map(sorted, edges)))
print(sepset)
colliders = []
for z in V:
    nb = sorted(v for v in V if frozenset((v, z)) in edges)
    for a, b in itertools.combinations(nb, 2):
        if frozenset((a, b)) not in edges and z not in sepset[(a, b)]:
            colliders.append((a, z, b))
print(colliders)'''

CODE['B13b'] = '''import pandas as pd
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.parameter_estimator import DiscreteMLE, DiscreteBayesianEstimator

df = pd.DataFrame({'A': [0, 0, 0, 0, 1, 1, 1, 1],
                   'B': [0, 0, 0, 1, 1, 1, 1, 1]})
m1 = DiscreteBayesianNetwork([('A', 'B')])
m1.fit(df, estimator=DiscreteMLE())
print(m1.get_cpds('B').values.round(3))

m2 = DiscreteBayesianNetwork([('A', 'B')])
m2.fit(df, estimator=DiscreteBayesianEstimator(prior_type='K2'))
print(m2.get_cpds('B').values.round(3))'''
