# -*- coding: utf-8 -*-
"""FIT5149 written-exam solutions cheat sheet: 10 A4 sides (5 sheets double-sided), 8pt, English.
Sources: Mock paper answers, sample exams (clustering, BN, MN, inference).
Numbers marked 'verified' were recomputed with Python (scipy / numpy / networkx).
Build:  python3 build_solutions_sheet.py && node render_pdf.js deliverables/FIT5149_Solutions_CheatSheet.html deliverables/FIT5149_Solutions_CheatSheet.pdf
"""
import os, sys

B = []  # body chunks


def add(x):
    B.append(x)


def H(t, color='#1f3a5f'):
    add(f'<h2 style="background:{color}">{t}</h2>')


def Q(src, t):
    add(f'<div class="q"><b>QUESTION</b> <span class="src">[{src}]</span> {t}</div>')


def LG(t):
    add(f'<div class="b lg"><b>SOLUTION LOGIC ▸</b> {t}</div>')


def FM(t):
    add(f'<div class="b fm"><b>FORMULAS ▸</b> {t}</div>')


def TK(t):
    add(f'<div class="b tk"><b>KEY TAKEAWAY ▸</b> {t}</div>')


def TP(t):
    add(f'<div class="b tp"><b>TRAP ▸</b> {t}</div>')


def P(t):
    add(f'<p>{t}</p>')


def UL(*items):
    add('<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>')


def T(rows, head=True, cls='t'):
    s = f'<table class="{cls}">'
    for i, r in enumerate(rows):
        tag = 'th' if (head and i == 0) else 'td'
        s += '<tr>' + ''.join(f'<{tag}>{c}</{tag}>' for c in r) + '</tr>'
    add(s + '</table>')


OK = '<span class="ok">✓</span>'
NO = '<span class="no">✗</span>'

# =====================================================================================================
add('<div class="title">FIT5149 · WRITTEN-EXAM SOLUTIONS CHEAT SHEET &nbsp;|&nbsp; Mock paper + 4 sample papers, condensed by question type &nbsp;|&nbsp; '
    'Format: <b>QUESTION → SOLUTION LOGIC → WORKED SOLUTION → FORMULAS → TAKEAWAY / TRAP</b> &nbsp;|&nbsp; ✓/✗ in option lists = correct/incorrect; “recomputed” = numbers re-verified in Python</div>')

H('0 · EXAM FORMAT & HOW MARKS ARE EARNED')
T([['Mock paper section', 'Marks', 'Where in this sheet'],
   ['1 Multiple choice: 13 questions × 2, <i>select ALL correct options</i> (one or more)', '26', 'MCQ items placed inside §1–§9'],
   ['2 Hierarchical clustering (single linkage, dendrogram, cut)', '12', '§1.2'],
   ['3 Non-linear regression (cubic spline constraints, truncated power basis)', '12', '§2.2'],
   ['4 Neural networks (forward pass, #parameters, gradient step, dead ReLU)', '15', '§3.2'],
   ['5 BN, Naive Bayes, PC algorithm, forward sampling', '19', '§4, §5, §6'],
   ['6 Markov networks & CRF (factor graph, variable elimination, Z)', '16', '§8, §9'],
   ['Sample papers: clustering (Oct 2023, 9) · BN (13) · MN (14) · exact &amp; approximate inference (22)', '—', '§1, §4, §6, §7, §8']])
UL('<b>Rules:</b> closed book; calculator allowed; unlimited working sheets; notes = 5 × A4 double-sided, physical only. Week-12 slides: <i>no code to write in the exam, but you must analyse results of code</i> (shapes, probabilities, p-values, orderings).',
   '<b>Mark pattern seen in every marking scheme:</b> 1 mark per formula/definition, 1 per numerical table or entry, 1 for the final value, 1 for the named rule or interpretation. <b>Follow-through credit</b> is given after an arithmetic slip → always show every intermediate table/vector.',
   '<b>Name the rule</b> (explaining away, collider, moralisation, Hammersley–Clifford, Meek rule 1, separating set, soft-threshold…) — naming it is usually worth a mark on its own.',
   '<b>MCQ method:</b> test every option independently; most distractors are (i) an over-strong word (“always”, “guarantees”, “proves”, “must”), (ii) a swapped definition (rows/cols, min/max, L1/L2), (iii) a true fact attached to a wrong conclusion. Write the selected letters only; no partial credit is stated, so decide each option firmly.')

# =====================================================================================================
H('1 · CLUSTERING: K-MEANS AND HIERARCHICAL', '#1f3a5f')
add('<h3>1.1 K-means (Mock MCQ 1 and MCQ 7)</h3>')
Q('Mock MCQ1', 'Standard K-means, squared Euclidean distance, fixed K, no empty cluster. Which are correct?')
T([['Option', 'Verdict', 'Why'],
   ['A. Setting each centroid to the mean of its assigned points minimises the objective for those fixed assignments', OK,
    'For fixed assignments Σ<sub>i∈C</sub>‖x<sub>i</sub>−c‖² is minimised at c = mean (this is step 2a of Lloyd’s algorithm).'],
   ['B. Two successive iterations with identical assignments <i>prove</i> a global optimum', NO,
    'Convergence means a <b>local</b> optimum (a fixed point). Global optimum is NP-hard; result depends on initialisation.'],
   ['C. Multiplying one feature by 100 leaves all assignments unchanged for any dataset', NO,
    'That feature then dominates the Euclidean distance → assignments change. K-means is scale-dependent ⇒ standardise.'],
   ['D. Several initialisations, keep the smallest objective, helps avoid a poor local solution', OK,
    'Standard remedy (<code>n_init</code>); improves the result but gives no global guarantee.']])
P('<b>Answer A, D.</b>')
Q('Mock MCQ7', 'W = Σ<sub>k</sub>Σ<sub>i∈C<sub>k</sub></sub>‖x<sub>i</sub>−μ<sub>k</sub>‖², μ<sub>k</sub> = cluster mean. Which are correct? (A) ×3 on every coordinate, partition fixed, centroids recomputed ⇒ W×9. (B) The partition with smallest W matches any external labels. (C) Objective requires equal-size clusters. (D) Moving a centroid away from the cluster mean cannot reduce that cluster’s SSE.')
P(f'<b>Answer A, D.</b> A {OK} squared distances scale by 3² = 9. B {NO} K-means never uses labels; minimum W says nothing about external classes. C {NO} no size constraint. D {OK} the mean is the unique minimiser: Σ‖x−c‖² = Σ‖x−μ‖² + |C|·‖μ−c‖² ≥ Σ‖x−μ‖².')
FM('<b>Objective</b> min Σ<sub>k</sub> W(C<sub>k</sub>), W(C<sub>k</sub>) = (1/|C<sub>k</sub>|)Σ<sub>i,i′∈C<sub>k</sub></sub>‖x<sub>i</sub>−x<sub>i′</sub>‖² = 2Σ<sub>i∈C<sub>k</sub></sub>‖x<sub>i</sub>−μ<sub>k</sub>‖². '
   '<b>Lloyd:</b> (a) μ<sub>k</sub> = mean of C<sub>k</sub>; (b) assign each x to nearest μ<sub>k</sub>; repeat until assignments stop changing. The objective is non-increasing at every step (both steps can only reduce it) ⇒ converges, but only to a local minimum. '
   'Scaling all data by s multiplies W by s². Inertia always falls as K grows (K = n ⇒ 0) ⇒ choose K by elbow / silhouette / CV, never by smallest inertia.')
TK('Say “local optimum + initialisation-dependent + scale-dependent + label-free + no equal-size constraint”. These five facts decide almost every K-means option.')

add('<h3>1.2 Agglomerative hierarchical clustering (Mock Q2 — 12 marks; Sample Oct-2023 — 9 marks)</h3>')
Q('Mock Q2', 'Five observations with the dissimilarity matrix below. (1) <b>Single linkage</b>: write each step (which clusters merge, merge height, updated dissimilarities) and sketch the dendrogram with leaf labels and fusion heights [10]. (2) Cut to get exactly two clusters [2].')
T([['', 'A', 'B', 'C', 'D', 'E'], ['A', '0', '0.6', '1.0', '1.9', '3.1'], ['B', '0.6', '0', '0.4', '1.3', '2.5'],
   ['C', '1.0', '0.4', '0', '0.9', '2.1'], ['D', '1.9', '1.3', '0.9', '0', '1.2'], ['E', '3.1', '2.5', '2.1', '1.2', '0']])
LG('<b>(1)</b> Start with n singletons. <b>Repeat n−1 times:</b> (a) scan <i>all</i> off-diagonal entries of the <i>current</i> matrix, take the minimum, merge that pair at height = that value; '
   '(b) recompute the new cluster’s dissimilarity to every other cluster with the linkage rule (single = <b>min</b> over member pairs) and write the new smaller matrix; (c) the new matrix is what you scan next. '
   '<b>(2)</b> A horizontal cut at height h gives the branches it crosses. For K clusters cut between the (n−K)-th and (n−K+1)-th merge height.')
P('<b>Step 1</b> min = 0.4 ⇒ merge <b>B,C @ 0.4</b>. d(BC,A) = min(0.6,1.0) = <b>0.6</b>; d(BC,D) = min(1.3,0.9) = <b>0.9</b>; d(BC,E) = min(2.5,2.1) = <b>2.1</b>; unchanged: d(A,D) = 1.9, d(A,E) = 3.1, d(D,E) = 1.2. '
  '<b>Step 2</b> min = 0.6 ⇒ <b>BC+A @ 0.6</b> → ABC. d(ABC,D) = min(1.9,1.3,0.9) = <b>0.9</b>; d(ABC,E) = min(3.1,2.5,2.1) = <b>2.1</b>; d(D,E) = 1.2. '
  '<b>Step 3</b> min = 0.9 ⇒ <b>ABC+D @ 0.9</b> → ABCD; d(ABCD,E) = min(3.1,2.5,2.1,1.2) = <b>1.2</b>. <b>Step 4</b> merge <b>ABCD+E @ 1.2</b>.')
P('<b>Dendrogram</b> (one valid leaf order B, C, A, D, E; any rotation accepted): U-shaped joins at heights 0.4 (B,C), 0.6 (+A), 0.9 (+D), 1.2 (+E) — the staircase / <i>chaining</i> shape typical of single linkage. '
  '<b>(2) Cut</b> at h = 1.0 (above 0.9, below 1.2): <b>{A,B,C,D}</b> and <b>{E}</b>. Marking: 1 per merge+height (4), 2 for the updated matrices, 4 for the dendrogram (nesting 2, heights 1, five labelled leaves 1), 1 per cluster (2).')
Q('Sample Oct-2023 (9 marks)', 'Same task, single linkage, A..E with d(A,B)=0.5, d(A,C)=0.7, d(A,D)=1.4, d(A,E)=2.4, d(B,C)=0.2, d(B,D)=0.9, d(B,E)=1.9, d(C,D)=0.7, d(C,E)=1.7, d(D,E)=1.0.')
P('Min 0.2 ⇒ <b>B,C @ 0.2</b>; d(BC,A) = min(0.5,0.7) = 0.5, d(BC,D) = min(0.9,0.7) = 0.7, d(BC,E) = min(1.9,1.7) = 1.7. Min 0.5 ⇒ <b>A+BC @ 0.5</b>; d(ABC,D) = min(0.7,1.4) = 0.7, d(ABC,E) = min(1.7,2.4) = 1.7, d(D,E) = 1.0. '
  'Min 0.7 ⇒ <b>ABC+D @ 0.7</b>; d(ABCD,E) = min(1.7,1.0) = 1.0. Final merge <b>@ 1.0</b>. Marking: 0.5 per merge, 0.5 per dissimilarity update, 0.5 per new matrix; dendrogram with heights 0.2 / 0.5 / 0.7 / 1.0.')
FM('<b>Linkage:</b> single d(S,T) = min<sub>i∈S,j∈T</sub> d(i,j); complete = max; average = (1/|S||T|)Σ<sub>i,j</sub> d(i,j); centroid = distance of means; Ward = smallest increase in within-cluster SS. '
   '<b>Lance–Williams shortcut after merging i,j:</b> single d(k,ij) = min(d<sub>ki</sub>,d<sub>kj</sub>); complete = max(d<sub>ki</sub>,d<sub>kj</sub>); average = (n<sub>i</sub>d<sub>ki</sub>+n<sub>j</sub>d<sub>kj</sub>)/(n<sub>i</sub>+n<sub>j</sub>). '
   'n−1 merges for n points; heights are non-decreasing for single/complete/average/Ward (centroid linkage can invert). SciPy: <code>linkage(Z)</code> rows [a, b, height, size]; condensed input of length n(n−1)/2.')
P('<b>✓ Extension (same Mock matrix, recomputed):</b> <b>Complete</b>: BC@0.4 → d(BC,A)=max(0.6,1.0)=1.0 → <b>A+BC@1.0</b> → D,E@1.2 (d(D,E)=1.2 &lt; d(ABC,D)=1.9) → final @ <b>3.1</b>; 2-cluster cut = <b>{A,B,C},{D,E}</b>. '
  '<b>Average</b>: BC@0.4; d(BC,A)=0.8 → A+BC@0.8; d(ABC,D)=(1.9+1.3+0.9)/3=1.37, d(ABC,E)=2.57, D,E@1.2; final @ (11.8/6) = 1.967; cut = {A,B,C},{D,E}. '
  '<b>Single gives {A,B,C,D},{E}</b> — the choice of linkage changes the partition.')
TK('Always (1) restate the current matrix, (2) circle the minimum, (3) record the height, (4) recompute only the row/column of the new cluster, (5) state the cut rule. Single linkage ⇒ chaining (long straggly clusters, outliers join last); complete ⇒ compact clusters; average ⇒ in between.')
TP('Do not recompute unchanged entries wrongly, do not merge using the <i>original</i> matrix, and do not forget leaf labels / fusion heights on the sketch (4 of 10 marks).')

add('<h3>1.3 Complete and average linkage, step by step (same Mock matrix; ✓ recomputed with SciPy)</h3>')
T([['Step', 'Complete linkage (max)', 'Average linkage (mean of all pairs)'],
   ['1', 'min 0.4 ⇒ <b>B,C @ 0.4</b>. d(BC,A)=max(0.6,1.0)=1.0; d(BC,D)=max(1.3,0.9)=1.3; d(BC,E)=max(2.5,2.1)=2.5; A–D 1.9, A–E 3.1, D–E 1.2',
    'min 0.4 ⇒ <b>B,C @ 0.4</b>. d(BC,A)=(0.6+1.0)/2=0.8; d(BC,D)=(1.3+0.9)/2=1.1; d(BC,E)=(2.5+2.1)/2=2.3; A–D 1.9, A–E 3.1, D–E 1.2'],
   ['2', 'min 1.0 ⇒ <b>A+BC @ 1.0</b>. d(ABC,D)=max(1.9,1.3,0.9)=1.9; d(ABC,E)=max(3.1,2.5,2.1)=3.1; D–E 1.2',
    'min 0.8 ⇒ <b>A+BC @ 0.8</b>. d(ABC,D)=(1.9+1.3+0.9)/3=1.37; d(ABC,E)=(3.1+2.5+2.1)/3=2.57; D–E 1.2'],
   ['3', 'min 1.2 ⇒ <b>D+E @ 1.2</b>; d(ABC,DE)=max(1.9,3.1)=3.1', 'min 1.2 ⇒ <b>D+E @ 1.2</b>; d(ABC,DE)=(1.9+1.3+0.9+3.1+2.5+2.1)/6 = 1.97'],
   ['4', 'merge ABC+DE <b>@ 3.1</b> ⇒ 2-cluster cut {A,B,C},{D,E}', 'merge ABC+DE <b>@ 1.97</b> ⇒ 2-cluster cut {A,B,C},{D,E}']])
P('<b>Oct-2023 matrix, other linkages ✓:</b> complete heights 0.2, 0.7 (A+BC), 1.0 (D+E), 2.4; average heights 0.2, 0.6 (A+BC), 1.0, 1.75. '
  '<b>Tie warning:</b> for average linkage after A+BC@0.6 both d(ABC,D) = (1.4+0.9+0.7)/3 = 1.0 and d(D,E) = 1.0 tie — SciPy merges ABC+D (final height 1.75) whereas D+E first would give a final height of 1.5. If a tie occurs in the exam, <b>state your tie-break rule</b>; the printed single-linkage questions are built to have no ties.')
UL('<b>Reading a dendrogram:</b> the vertical axis is the dissimilarity at which two clusters fuse; horizontal order of leaves is arbitrary (rotation at any fusion). Two leaves are close <i>only if they fuse low</i>, never because they are neighbours on the x-axis. The cophenetic distance of two points = height of the fusion that first joins them.',
   '<b>Cutting:</b> height h ⇒ clusters = subtrees below the cut; “exactly K clusters” ⇒ any h between the merge heights number n−K and n−K+1. Mock: n = 5, K = 2 ⇒ any 0.9 &lt; h &lt; 1.2.',
   '<b>Properties:</b> hierarchical clustering needs no K in advance, is deterministic (no random start) and gives all K at once, but costs O(n²) memory/time and merges are never undone; K-means needs K, is random-start dependent, but is O(nKp) per iteration and scales to large n.')
add('<h3>1.4 Lloyd’s algorithm by hand (practice; ✓ recomputed)</h3>')
Q('Practice', 'x = {1, 2, 4, 9, 10, 12}, K = 2, initial centres μ₁ = 1, μ₂ = 2. Run K-means until the assignments stop changing and report SSE after each iteration.')
P('<b>Iteration 1:</b> assign by nearest centre: 1 → μ₁ (|1−1| = 0 &lt; 1); 2, 4, 9, 10, 12 → μ₂ (nearer to 2 than to 1) ⇒ C₁ = {1}, C₂ = {2,4,9,10,12}. Update: μ₁ = 1, μ₂ = 37/5 = 7.4; SSE = 0 + (5.4²+3.4²+1.6²+2.6²+4.6²) = <b>71.2</b>. '
  '<b>Iteration 2:</b> distances to (1, 7.4): 2 → μ₁ (1 &lt; 5.4); 4 → μ₁ (3 &lt; 3.4); 9, 10, 12 → μ₂ ⇒ C₁ = {1,2,4}, C₂ = {9,10,12}; μ₁ = 7/3 = 2.33, μ₂ = 31/3 = 10.33; SSE = (1.33²+0.33²+1.67²) + (1.33²+0.33²+1.67²) = <b>9.33</b>. '
  '<b>Iteration 3:</b> same assignments ⇒ stop (a local, here also global, optimum). SSE decreased 71.2 → 9.33 → 9.33, as guaranteed. A different start (μ₁ = 1, μ₂ = 12) reaches the same partition in one iteration; with other data a bad start can give a worse local optimum — hence <code>n_init</code>.')

# =====================================================================================================
H('2 · REGULARISATION AND REGRESSION SPLINES', '#2e6a4f')
add('<h3>2.1 Lasso vs Ridge (Mock MCQ 2)</h3>')
Q('Mock MCQ2', 'Many predictors, several irrelevant, standardised; Lasso and Ridge with finite λ > 0 and unpenalised intercept. (A) Ridge is more suitable for obtaining exact zeros. (B) An L1 penalty can use only a subset of predictors. (C) An L2 penalty discourages large coefficients without generally forcing exact zeros. (D) Penalising NN weights by L1/L2 requires the input–output relationship to be linear.')
P(f'<b>Answer B, C.</b> A {NO} Lasso (L1) gives exact zeros; Ridge only shrinks. B {OK}. C {OK}. D {NO} L1/L2 weight penalties (weight decay) regularise <i>non-linear</i> neural networks too.')
FM('<b>Ridge</b> min Σ(y−ŷ)² + λΣβ<sub>j</sub>² (closed form β̂ = (XᵀX+λI)<sup>−1</sup>Xᵀy); <b>Lasso</b> min Σ(y−ŷ)² + λΣ|β<sub>j</sub>| (no closed form). Equivalent constrained forms: Σβ² ≤ s (disc) vs Σ|β| ≤ s (diamond with <i>corners on the axes</i> ⇒ exact zeros). '
   'λ ↑ ⇒ bias ↑, variance ↓; λ = 0 ⇒ OLS; λ → ∞ ⇒ all β → 0. Orthonormal design (XᵀX = I): Ridge β̂<sub>j</sub> = β̂<sub>j</sub><sup>OLS</sup>/(1+λ); Lasso β̂<sub>j</sub> = sign(β̂<sub>j</sub><sup>OLS</sup>)·max(|β̂<sub>j</sub><sup>OLS</sup>|−λ/2, 0) (soft-threshold). Standardise first; never penalise the intercept; choose λ by CV.')
add('<h3>2.2 Cubic regression splines (Mock MCQ 3 and Q3 — 12 marks)</h3>')
Q('Mock MCQ3', 'Standard cubic regression spline for demand vs temperature, fixed knots, usual continuity constraints. (A) Fitted function and first two derivatives agree on both sides of every interior knot. (B) More distinct interior knots give a richer class of functions. (C) Each segment must interpolate every training point in it. (D) With knots and basis fixed, the model is linear in its coefficients although non-linear in temperature.')
P(f'<b>Answer A, B, D.</b> A {OK} C² continuity. B {OK} spline space dimension = K+4 grows with K. C {NO} regression splines <i>fit</i> (least squares), they do not interpolate. D {OK} f(x) = Σβ<sub>j</sub>b<sub>j</sub>(x) ⇒ ordinary least squares on basis columns.')
Q('Mock Q3 (12)', 'g(x) = p(x) = a₀+a₁x+a₂x²+a₃x³ for x ≤ 2 and q(x) = b₀+b₁x+b₂x²+b₃x³ for x &gt; 2; g must have continuous value, first and second derivative at the knot x = 2. '
  '(1) p(2), q(2) and the continuity constraint. (2) p′(2), q′(2), constraint. (3) p″(2), q″(2), constraint. (4) With δ = b₃−a₃, express b₂, b₁, b₀. (5) Write g in the basis {1, x, x², x³, (x−2)³₊} and justify. (6) q‴(2)−p‴(2), meaning of δ, degrees of freedom.')
LG('Write the three equalities at x = 2, then <b>solve from the highest derivative down</b>: second-derivative equality gives b₂, then first-derivative gives b₁, then value gives b₀. '
   '<b>Shortcut:</b> r(x) = q(x)−p(x) is a cubic with r(2) = r′(2) = r″(2) = 0, i.e. a triple root at 2 ⇒ r(x) = δ(x−2)³ with δ = b₃−a₃ (use the hint (x−2)³ = x³−6x²+12x−8).')
T([['Part', 'Working', 'Result'],
   ['(1) value', 'p(2) = a₀+2a₁+4a₂+8a₃; q(2) = b₀+2b₁+4b₂+8b₃', 'b₀+2b₁+4b₂+8b₃ = a₀+2a₁+4a₂+8a₃'],
   ['(2) 1st deriv.', 'p′ = a₁+2a₂x+3a₃x² ⇒ p′(2) = a₁+4a₂+12a₃; q′(2) = b₁+4b₂+12b₃', 'b₁+4b₂+12b₃ = a₁+4a₂+12a₃'],
   ['(3) 2nd deriv.', 'p″ = 2a₂+6a₃x ⇒ p″(2) = 2a₂+12a₃; q″(2) = 2b₂+12b₃', '2b₂+12b₃ = 2a₂+12a₃'],
   ['(4) solve', '2(b₂−a₂)+12δ = 0; (b₁−a₁)+4(−6δ)+12δ = 0; (b₀−a₀)+2(12δ)+4(−6δ)+8δ = 0', '<b>b₂ = a₂−6δ, b₁ = a₁+12δ, b₀ = a₀−8δ</b>'],
   ['(5) basis', 'q = p + δ(x³−6x²+12x−8) = p + δ(x−2)³', '<b>g(x) = a₀+a₁x+a₂x²+a₃x³ + δ(x−2)³₊</b> (x ≤ 2: truncated term 0 ⇒ p; x &gt; 2: p+δ(x−2)³ = q)'],
   ['(6) jump', 'p‴(2) = 6a₃; q‴(2) = 6b₃ = 6(a₃+δ)', '<b>q‴−p‴ = 6δ</b>; δ = 0 ⇒ g is one cubic; <b>5 free coefficients</b> (a₀..a₃, δ) vs 4 for one cubic']])
P('δ controls only the <b>third-derivative jump</b>: cubic behaviour may change at the knot while value, slope and curvature stay continuous. Counting: 2 pieces × 4 coefficients = 8, minus 3 independent constraints = <b>5</b>. Marking: 1+1 per part (evaluations / constraint), part 4 = 1 for b₂ with working + 0.5 each for b₁, b₀, part 5 = 1 expression + 1 justification, part 6 = 1 for jump &amp; interpretation incl. δ = 0, 1 for 5 vs 4.')
FM('<b>Truncated power basis</b> for a cubic spline with knots ξ₁..ξ<sub>K</sub>: {1, x, x², x³, (x−ξ₁)³₊, …, (x−ξ<sub>K</sub>)³₊}, (x−ξ)³₊ = (x−ξ)³ for x &gt; ξ else 0 ⇒ <b>K+4 parameters</b> = 4(K+1) − 3K. '
   'Degree-d piecewise polynomial with C<sup>d−1</sup> continuity: K+d+1 parameters. <b>Natural cubic spline</b> adds linearity beyond the boundary knots (f″ = f‴ = 0 at both ends ⇒ 4 extra constraints): K+4−4 = K parameters, lower variance near the boundary. '
   'Smoothing spline: min Σ(y−g)² + λ∫g″(t)²dt (λ→0 interpolates, λ→∞ linear). Fit by OLS on basis columns; choose K and knot placement (quantiles) by CV.')
TK('Spline questions are algebra on three equalities: <b>compute one-sided values → equate → solve downward → recognise δ(x−2)³₊</b>. The free-parameter count is always (#pieces × coefficients) − (#knots × #constraints).')

add('<h3>2.3 Numerical drills: Lasso/Ridge, model selection, degrees of freedom (✓ recomputed)</h3>')
Q('Practice', 'Orthogonal design XᵀX = nI with n = 8, noiseless y = Xβ, β = (4, −3, 2, 1, 0.5). Predict the scikit-learn estimates: Lasso (objective (1/2n)‖y−Xw‖² + α‖w‖₁) for α = 0.5, 1.5, 3.5 and Ridge (‖y−Xw‖² + α‖w‖²) for α = 8.')
P('Because XᵀX/n = I the Lasso problem separates by coefficient ⇒ <b>soft-threshold</b> ŵ<sub>j</sub> = sign(β<sub>j</sub>)·max(|β<sub>j</sub>|−α, 0): α = 0.5 → (3.5, −2.5, 1.5, 0.5, <b>0</b>); α = 1.5 → (2.5, −1.5, 0.5, <b>0, 0</b>); α = 3.5 → (0.5, <b>0, 0, 0, 0</b>). '
  'Ridge: ŵ = (XᵀX+αI)<sup>−1</sup>Xᵀy = β·n/(n+α) = β·8/16 = (2, −1.5, 1, 0.5, 0.25) — <b>no exact zeros</b>, every coefficient shrunk by the same factor; Ridge never zeroes a non-zero coefficient for finite α.')
FM('<b>Model-selection criteria</b> (d predictors, σ̂² = error-variance estimate): C<sub>p</sub> = (RSS+2dσ̂²)/n; AIC ∝ (RSS+2dσ̂²)/(nσ̂²); BIC = (RSS+log(n)·dσ̂²)/n; adjusted R² = 1 − [RSS/(n−d−1)]/[TSS/(n−1)]. Choose the <i>smallest</i> C<sub>p</sub>/AIC/BIC but the <i>largest</i> adjusted R². '
   'RSS and R² always improve as variables are added ⇒ useless for choosing the model size. <b>Search cost:</b> best subset 2<sup>p</sup> models; forward/backward stepwise 1 + p(p+1)/2. CV: K-fold with K = 5 or 10 balances bias and variance; LOOCV has low bias, high cost. One-standard-error rule: pick the simplest model within 1 SE of the best CV error.')
T([['Model for K interior knots', 'Free parameters (incl. intercept)', 'Counting argument'],
   ['Piecewise constant (step function)', 'K+1', 'K+1 regions, no continuity'], ['Continuous piecewise linear', 'K+2', '2(K+1) − K (continuity of f)'],
   ['Quadratic spline (C¹)', 'K+3', '3(K+1) − 2K'], ['<b>Cubic spline (C²)</b>', '<b>K+4</b>', '4(K+1) − 3K'],
   ['Natural cubic spline', 'K', 'cubic spline minus 4 boundary constraints (f″ = f‴ = 0 at both ends)'],
   ['Polynomial regression degree d', 'd+1', 'one polynomial, no knots']])
P('<b>Software link:</b> <code>bs(x, knots=(k₁,…,k<sub>K</sub>), degree=3)</code> creates K+3 columns (+1 for the intercept = K+4); <code>bs(x, df=6, degree=3)</code> ⇒ K = df−degree = 3 interior knots at quantiles ⇒ 7 columns with intercept; <code>degree=0</code> ⇒ K+1 indicator columns (piecewise constant). '
  '<b>Bias–variance:</b> more knots / higher degree / smaller λ ⇒ lower bias, higher variance; choose by CV. Splines are <b>linear in β</b> (OLS applies) and non-linear in x; GAMs add one smooth f<sub>j</sub>(x<sub>j</sub>) per predictor (additive, interpretable).')

# =====================================================================================================
H('3 · NEURAL NETWORKS, CNN, DEC, PCA / t-SNE', '#6a2e5f')
add('<h3>3.1 Conceptual MCQs (Mock MCQ 4, 5, 6)</h3>')
Q('Mock MCQ4', 'Autoencoder pre-trained on unlabelled sensor data, then standard Deep Embedded Clustering (DEC) with loss KL(P‖Q), P periodically recomputed from soft assignments Q. (A) Lower DEC loss ⇒ lower reconstruction error. (B) P must be built from manual class labels. (C) DEC loss can move both embeddings and cluster centres. (D) The P update strengthens confident assignments, so clustering refines the representation without labels.')
P(f'<b>Answer C, D.</b> A {NO} the clustering loss does not guarantee better reconstruction. B {NO} P is derived from Q itself (self-training). C {OK} encoder weights and centres are trained jointly. D {OK}.')
FM('<b>DEC:</b> soft assignment (Student-t) q<sub>ij</sub> ∝ (1+‖z<sub>i</sub>−μ<sub>j</sub>‖²/α)<sup>−(α+1)/2</sup>; target p<sub>ij</sub> = (q<sub>ij</sub>²/f<sub>j</sub>)/Σ<sub>j′</sub>(q<sub>ij′</sub>²/f<sub>j′</sub>), f<sub>j</sub> = Σ<sub>i</sub>q<sub>ij</sub> (squaring = <i>confidence sharpening</i>; dividing by f<sub>j</sub> = cluster-frequency normalisation); loss KL(P‖Q) = Σ<sub>ij</sub>p<sub>ij</sub>log(p<sub>ij</sub>/q<sub>ij</sub>). No labels needed.')
Q('Mock MCQ5', '30 centred features, first two principal components kept; separate standard non-parametric t-SNE. (A) PCA keeps exactly two of the original columns. (B) Centring alone makes PCA unit-invariant. (C) A new observation can be projected using the training mean and fitted loadings. (D) PCA features can feed clustering, but dropped components may remove cluster-distinguishing information. (E) Fitted t-SNE gives a fixed projection matrix for new data.')
P(f'<b>Answer C, D.</b> A {NO} PCs are <i>linear combinations</i> of all columns. B {NO} centring does not equalise variances; PCA is scale-dependent ⇒ standardise when units differ. C {OK} z<sub>new</sub> = Vᵀ(x−x̄). D {OK} high variance ≠ cluster separation. E {NO} t-SNE has no <code>transform</code> (non-parametric embedding).')
FM('<b>PCA:</b> S = XcᵀXc/(n−1) = VΛVᵀ; loadings = eigenvectors (unit length); scores Z = XcV; PVE<sub>m</sub> = λ<sub>m</sub>/Σλ; reconstruction X̂ = Z<sub>k</sub>V<sub>k</sub>ᵀ + x̄. <b>t-SNE:</b> Gaussian similarities p<sub>ij</sub> in high-D, Student-t q<sub>ij</sub> in 2-D, minimise KL(P‖Q); perplexity ≈ effective neighbours; non-convex ⇒ seed matters; global distances / cluster sizes not interpretable.')
Q('Mock MCQ6', 'CNN on greyscale images with 3×3 kernels; considering stride changes and replacing Flatten by global average pooling (GAP). (A) The same kernel parameters are reused at different spatial positions. (B) A separately learned 3×3 kernel is needed for every position. (C) Stride 2 can give a smaller feature map. (D) Without a fully connected layer, classification becomes impossible after GAP.')
P(f'<b>Answer A, C.</b> A {OK} weight sharing. B {NO} that would be a locally-connected layer. C {OK}. D {NO} use one feature map per class → GAP → softmax (as in all-convolutional nets).')
FM('<b>Conv output size</b> ⌊(n + 2p − k)/s⌋ + 1 per spatial dim; params = C<sub>out</sub>(C<sub>in</sub>k²+1); <b>Linear</b> params = in·out + out; GAP: (B,C,H,W) → (B,C). Pooling gives translation invariance and a regularising effect.')

add('<h3>3.2 Feed-forward network: forward pass, parameter count, gradient step (Mock Q4 — 15 marks)</h3>')
Q('Mock Q4', 'Crop yield from standardised soil moisture z<sub>M</sub> and sunlight z<sub>S</sub> (standardisation uses <i>training</i>-set mean/SD only; 240/80/80 train/val/test). Network: 2 inputs, 3 ReLU hidden units, 1 identity output. '
  'u = W⁽¹⁾x+b⁽¹⁾, h = ReLU(u), ŷ = W⁽²⁾h+b⁽²⁾ with W⁽¹⁾ = [[1.2,−0.2],[−1.0,0.4],[0.2,0.6]], b⁽¹⁾ = (−0.3,−0.2,0.1), W⁽²⁾ = (−2.0,−1.5,0.8), b⁽²⁾ = 5. '
  '(1) For z<sub>S</sub> = 0.5 predict yield at z<sub>M</sub> = −1 and +1 [6]. (2) Count trainable parameters [2]. (3) One observation x = (1,0.5), y = 4.88, L = ½(ŷ−y)², η = 0.1: gradients for W⁽²⁾, b⁽²⁾, one output-layer step, and are the second hidden unit’s incoming gradients zero? [7]')
LG('<b>Forward:</b> matrix–vector product, add bias, apply ReLU elementwise, then output layer. <b>Count:</b> Σ (inputs×outputs + biases) per layer. <b>Backprop:</b> start at the loss: e = ŷ−y; output-layer gradients = e × (what feeds the weight); only then propagate δ = Wᵀe through the ReLU derivative 1[u&gt;0]. <b>Step:</b> θ ← θ − η∇. State explicitly that gradients are evaluated at the <i>current</i> parameters.')
T([['Case', 'u = W⁽¹⁾x + b⁽¹⁾', 'h = ReLU(u)', 'ŷ = W⁽²⁾h + b⁽²⁾'],
   ['x = (−1, 0.5)', '(1.2(−1)−0.2(0.5)−0.3, −1.0(−1)+0.4(0.5)−0.2, 0.2(−1)+0.6(0.5)+0.1) = (−1.6, 1.0, 0.2)', '(0, 1.0, 0.2)', '−2(0)−1.5(1.0)+0.8(0.2)+5 = <b>3.66</b>'],
   ['x = (1, 0.5)', '(1.2−0.1−0.3, −1.0+0.2−0.2, 0.2+0.3+0.1) = (0.8, −1.0, 0.6)', '(0.8, 0, 0.6)', '−2(0.8)−1.5(0)+0.8(0.6)+5 = <b>3.88</b>']])
P('<b>(2) Parameters</b> = 2×3 + 3 + 3×1 + 1 = 6+3+3+1 = <b>13</b> (weights 9, biases 4). '
  '<b>(3) Output layer:</b> e = ŷ−y = 3.88−4.88 = −1, ∂L/∂ŷ = e; ∂L/∂W⁽²⁾ = e·hᵀ = (−0.8, 0, −0.6); ∂L/∂b⁽²⁾ = e = −1. '
  '<b>Update (η = 0.1):</b> W⁽²⁾ ← (−2.0,−1.5,0.8) − 0.1(−0.8,0,−0.6) = <b>(−1.92, −1.5, 0.86)</b>; b⁽²⁾ ← 5 − 0.1(−1) = <b>5.1</b>. '
  '<b>Dead unit:</b> yes — u₂ = −1.0 &lt; 0 ⇒ ReLU′(u₂) = 0 ⇒ ∂L/∂u₂ = e·W⁽²⁾<sub>1,2</sub>·ReLU′(u₂) = 0 ⇒ ∂L/∂W⁽¹⁾<sub>2,j</sub> = 0 (j = 1,2) and ∂L/∂b⁽¹⁾<sub>2</sub> = 0, <i>for this observation at the current parameters</i>; other observations may activate the unit. '
  'Marking: 3 per forward case (u, ReLU, ŷ); 1+1 for count; 3 for gradients (e, ∂W, ∂b); 2 for update; 2 for the ReLU argument.')
P('<b>✓ Extension (full backprop, recomputed):</b> δh = e·W⁽²⁾ᵀ = (2, 1.5, −0.8); δu = δh ⊙ 1[u&gt;0] = (2, 0, −0.8); ∂L/∂W⁽¹⁾ = δu xᵀ = [[2,1],[0,0],[−0.8,−0.4]]; ∂L/∂b⁽¹⁾ = (2,0,−0.8). '
  'Output-layer-only step: new ŷ = 4.08, loss 0.50 → <b>0.32</b>; updating <i>all</i> parameters: W⁽¹⁾ = [[1.0,−0.3],[−1.0,0.4],[0.28,0.64]], b⁽¹⁾ = (−0.5,−0.2,0.18), ŷ = 5.10, loss → <b>0.024</b> (second row unchanged: dead unit).')
FM('<b>Loss/derivatives:</b> squared error L = ½(ŷ−y)² ⇒ ∂L/∂ŷ = ŷ−y. Cross-entropy with softmax: ∂L/∂z = p − y. <b>Chain rule:</b> ∂L/∂W⁽ˡ⁾ = δ⁽ˡ⁾(a⁽ˡ⁻¹⁾)ᵀ; δ⁽ˡ⁾ = (W⁽ˡ⁺¹⁾ᵀδ⁽ˡ⁺¹⁾) ⊙ g′(u⁽ˡ⁾). ReLU′(u) = 1[u&gt;0]; sigmoid′ = σ(1−σ). '
   'Vanishing/exploding gradients grow with depth; regularisation = weight decay λ‖W‖², dropout, early stopping on the <i>validation</i> set; the <i>test</i> set is used once at the end; standardise with training statistics only (no leakage).')
TK('Show u → h → ŷ as three explicit vectors, then e, then each gradient with its formula. A zero ReLU derivative kills <b>every</b> incoming gradient of that hidden unit (weights and bias), but only for that observation.')

add('<h3>3.3 Numerical drills: softmax / cross-entropy, shapes, attention, PCA (✓ recomputed)</h3>')
T([['Topic', 'Worked numbers'],
   ['Softmax + CE', 'logits z = (2, 0), true class 0: p = (e²,1)/(e²+1) = (0.881, 0.119); L = −ln 0.881 = <b>0.127</b>; ∂L/∂z = p − y = (−0.119, +0.119). Logits (−1.5, 4.5), true class 0: p = (0.002, 0.998), L = ln(1+e⁶) = <b>6.002</b>, ∂L/∂z = (−0.998, 0.998); argmax = class 1 ⇒ misclassified. Softmax applied twice before CE (wrong) turns logits (2,0) into probabilities (0.88,0.12) and loss 0.383.'],
   ['Binary output', 'σ(z) = 1/(1+e<sup>−z</sup>): σ(0) = 0.5, σ(1) = 0.731, σ(2) = 0.881, σ(3) = 0.953; BCE = −[y ln p + (1−y)ln(1−p)]; ∂L/∂z = p − y again.'],
   ['Conv/pool shapes', 'input (8,3,64,64); <code>Conv2d(3,16,k=5,s=2,p=2)</code> ⇒ ⌊(64+4−5)/2⌋+1 = 32 ⇒ (8,16,32,32); params 16·(3·25)+16 = <b>1216</b>; <code>MaxPool2d(2)</code> ⇒ (8,16,16,16); Flatten ⇒ (8,4096); <code>Linear(4096,10)</code> ⇒ 4096·10+10 = <b>40 970</b> params; GAP ⇒ (8,16,1,1). “Same” padding: p = (k−1)/2 at stride 1.'],
   ['Self-attention', 'Attention(Q,K,V) = softmax(QKᵀ/√d<sub>k</sub>)V. With Q = K = V = I₂: scores/√2 = [[0.707,0],[0,0.707]] ⇒ weights [[0.670,0.330],[0.330,0.670]] (rows sum to 1); output = weights·V = the weights. Causal mask sets future scores to −∞ before softmax ⇒ row 1 = (1,0). Dividing by √d<sub>k</sub> keeps scores small so the softmax does not saturate. Multi-head: h heads of size d/h, concatenated then W<sub>o</sub>; sinusoidal positional encoding because attention is permutation-invariant. Block = self-attention → residual+LayerNorm → MLP → residual+LayerNorm; cost O(N²d).'],
   ['PCA by hand', 'X = {(1,1),(−1,−1),(2,−2),(−2,2)}, mean 0, S = XᵀX/3 = [[10/3,−2],[−2,10/3]] ⇒ eigenvalues 10/3 ± 2 = <b>5.333, 1.333</b>; PC₁ = (1,−1)/√2 (PVE 0.8), PC₂ = (1,1)/√2 (PVE 0.2). |PC₁ scores| = (0, 0, 2.828, 2.828); reconstruction error with one PC = (n−1)λ₂ = 3·1.333 = <b>4.0</b>. If the columns were uncorrelated with variances 8/3 and 2/3, the PCs would be the axes and PVE = (0.8, 0.2). <code>eigh</code> returns eigenvalues in <i>ascending</i> order — sort descending.'],
   ['Overfitting', 'Train/validation/test: tune on validation, report once on test; standardise with <b>training</b> mean/SD only. Remedies: weight decay (L2), dropout, early stopping, data augmentation, smaller network. Deep MLPs suffer vanishing/exploding gradients (ReLU, normalisation, residual connections help); fully connected layers ignore spatial structure and overfit ⇒ CNN.']])
T([['', 'PCA', 't-SNE'],
   ['Map', 'linear, orthogonal projection', 'non-linear embedding minimising KL(P‖Q)'], ['New points', 'transform with training mean + loadings', 'no transform (re-fit)'],
   ['Preserves', 'global variance structure', 'local neighbourhoods; global distances / cluster sizes are not meaningful'], ['Randomness / tuning', 'deterministic (up to sign)', 'seed, perplexity (5–50), iterations'],
   ['Typical use', 'preprocessing, PCR, compression', 'visualisation in 2-D / 3-D (often after PCA to 50 dims)']])
UL('<b>Output / loss pairs:</b> regression → identity + squared error; binary → sigmoid + binary cross-entropy; K classes → softmax + cross-entropy (<code>CrossEntropyLoss</code> expects raw logits and a class index); margin classifiers → hinge loss max(0, 1−y·f(x)).',
   '<b>Activations:</b> ReLU max(0,u), derivative 1[u&gt;0] (units with u ≤ 0 pass no gradient); sigmoid σ(u), derivative σ(1−σ) ≤ 0.25 (saturates ⇒ vanishing gradients); tanh; softmax e<sup>z<sub>k</sub></sup>/Σ<sub>j</sub>e<sup>z<sub>j</sub></sup> (shift by max for stability).')

# =====================================================================================================
H('4 · BAYESIAN NETWORKS: MODELLING, d-SEPARATION, QUERIES, EXPLAINING AWAY, NAIVE BAYES', '#7a2e2e')
add('<h3>4.1 Dr Johnson (Sample BN — 13 marks; same scenario in the Week 11-12 inference sample)</h3>')
Q('Sample BN', 'T ∈ {A,B} treatment, Y ∈ {0,1} success; C = duration of negative thinking (short/long) influences <b>both</b> the treatment given and the outcome; M = isolation (mild/severe) is influenced by the treatment, affects success, and the treatment may also affect success directly. '
  'Success counts — A: C=short 160/1000, C=long 38/100, M=mild 90/200, M=severe 108/900; B: C=short 5/50, C=long 126/600, M=mild 105/150, M=severe 26/500. '
  '(a) DAG [5]. (b) Factorise joint [2]. (c) Are C, M d-separated with nothing observed? List paths; does T observed change this? [2] (d) C = long: (i) P(Y=1|C=long) [2], (ii) P(T=A|C=long,Y=1) [2].')
LG('<b>(a)</b> One node per variable; for every “X influences Y” sentence draw X → Y. Sentence-by-sentence: C influences T ⇒ C→T; C influences outcome ⇒ C→Y; T influences isolation ⇒ T→M; isolation affects success ⇒ M→Y; T may affect success directly ⇒ T→Y. Roots (C) get priors; Pa(Y) = {C,T,M}. '
   '<b>(b)</b> Product of P(node | parents). <b>(c)</b> enumerate <i>every</i> undirected path, classify each interior node (chain / fork / collider), decide blocked/active; one active path ⇒ d-connected. '
   '<b>(d)</b> Keep only variables in the query; M is not mentioned ⇒ marginalised out (its CPD sums to 1); condition on evidence; use counts from the table.')
P('<b>(a) DAG:</b> C→T, C→Y, T→Y, T→M, M→Y (M is a <i>mediator</i> on T→M→Y). <b>(b)</b> <b>P(Y,C,M,T) = P(C) P(T|C) P(M|T) P(Y|C,T,M)</b>.')
T([['Path C … M', 'Structure', 'Status (nothing observed)', 'Given T'],
   ['C → T → M', 'chain through T', '<b>active</b> (T unobserved)', 'blocked (observed chain node)'],
   ['C → Y ← T → M', 'collider at Y (+ fork T)', 'blocked (Y unobserved)', 'blocked (Y unobserved collider)'],
   ['C → Y ← M', 'collider at Y', 'blocked', 'blocked']])
P('<b>(c)</b> One active path ⇒ <b>C and M are NOT d-separated</b> (d-connected). Observing T blocks the chain ⇒ <b>C ⊥ M | T</b>. Observing Y (or a descendant of Y) would <i>open</i> the collider paths. '
  '<b>(d)(i)</b> Among 700 long-duration patients: 100 got A, 600 got B ⇒ P(T=A|long) = 1/7, P(T=B|long) = 6/7; success rates 0.38 (A) and 0.21 (B). P(Y=1|long) = Σ<sub>t</sub> P(Y=1|t,long)P(t|long) = 0.38·(1/7)+0.21·(6/7) = (38+126)/700 = <b>164/700 ≈ 0.234</b>. '
  '<b>(ii) Bayes:</b> P(A|long,Y=1) = 0.38·(1/7)/0.234 = 38/164 ≈ <b>0.232</b> — A has the higher success rate (38% vs 21%) but a successful long-duration patient most likely got B because B is given 6× as often: the <i>prior</i> P(T|C) outweighs the likelihood ratio 0.38/0.21 ≈ 1.8. '
  '(M is summed out because each table rate already equals Σ<sub>m</sub>P(Y|C,T,m)P(m|T).)')
P('<b>✓ Extra insight from the table (Simpson’s paradox):</b> overall success A = 198/1100 = <b>18.0%</b> but B = 131/650 = <b>20.2%</b>, although A is better within both C = short (16% vs 10%) and C = long (38% vs 21%). The confounder C drives who gets which treatment (B is given mostly to long-duration patients), so the pooled comparison misleads ⇒ condition on / adjust for C.')
add('<h3>4.2 Week 11-12 sample: DAG and factorisation without M→Y</h3>')
P('Same story but Y depends only on C and T: edges <b>C→T, C→Y, T→Y, T→M</b>; <b>P(C,T,M,Y) = P(C) P(T|C) P(M|T) P(Y|C,T)</b> (5 + 2 marks). Only Y has two parents (C, T) and they are already adjacent (C→T) ⇒ no immorality ⇒ moral graph = skeleton (used in §7).')
add('<h3>4.3 Explaining away and Naive Bayes (Mock Q5 parts 1–2)</h3>')
Q('Mock Q5 (1)-(2)', 'Monitoring system: I intrusion (class, P=0.06), B backup running (P=0.25), H high traffic, A alert. G<sub>BN</sub>: I→H←B, H→A. P(H=1|I,B): (1,1)=0.92, (1,0)=0.75, (0,1)=0.45, (0,0)=0.04; P(A=1|H=1)=0.85, P(A=1|H=0)=0.03. G<sub>NB</sub>: I is the only parent of B, H, A. '
  '(1) Factorise under both models [4]. (2) In G<sub>BN</sub>, after observing H=1, A=0, learning B=1 lowers P(intrusion). Name the phenomenon and explain with the graph; explain why a Naive Bayes model with P(B|I) = 0.25 for both classes cannot do this [3].')
P('<b>(1) G<sub>BN</sub>:</b> P(I,B,H,A) = P(I) P(B) P(H|I,B) P(A|H). <b>G<sub>NB</sub>:</b> P(I,B,H,A) = P(I) P(B|I) P(H|I) P(A|I) (2 marks each: correct parent sets + complete product incl. all root priors). '
  '<b>(2) Explaining away</b> (intercausal reasoning): H is a <b>collider</b> on I → H ← B; observing H (or a descendant such as A) opens the otherwise blocked path, making the two causes dependent. A backup is an alternative explanation for high traffic, so it reduces the evidence for intrusion. Given H, A adds nothing about the roots (H blocks the chain H→A). '
  '<b>Naive Bayes:</b> posterior odds = prior odds × ∏<sub>k</sub> P(f<sub>k</sub>|I=1)/P(f<sub>k</sub>|I=0); the factor for B=1 is 0.25/0.25 = 1 whatever H, A are ⇒ B can never become informative “only after” other features are observed — NB cannot represent explaining away (features are independent given the class).')
P('<b>✓ Numbers (recomputed by enumeration):</b> P(H=1) = 0.1815; P(I=1|H=1) = P(I=1|H=1,A=0) = <b>0.262</b> (A irrelevant given H); adding B=1: P(I=1|H=1,A=0,B=1) = <b>0.115</b>; with B=0: <b>0.545</b>. Marginally P(I=1|B=1) = 0.06 = P(I=1) (I ⊥ B).')
FM('<b>Factorisation</b> P(X<sub>1..n</sub>) = ∏P(X<sub>i</sub>|Pa<sub>i</sub>). <b>Free parameters</b> = Σ<sub>i</sub>(|X<sub>i</sub>|−1)∏<sub>p∈Pa<sub>i</sub></sub>|X<sub>p</sub>|. <b>d-separation:</b> chain A→M→B and fork A←M→B blocked iff M observed; collider A→M←B blocked iff M <i>and all descendants of M</i> unobserved. '
   'Local Markov: X ⊥ NonDesc(X) | Pa(X). Markov blanket = parents + children + co-parents. <b>Bayes:</b> P(a|b) = P(b|a)P(a)/ΣP(b|a′)P(a′). Marginalise: P(Y|e) = Σ<sub>other</sub>P(Y,other,e)/P(e). <b>Naive Bayes:</b> P(C|f) ∝ P(C)∏P(f<sub>k</sub>|C).')
TK('Text → DAG by sentences (cause → effect); factorise by parents; d-separation by <i>listing every path</i>; a collider is blocked by default and opened by observing it or a descendant (explaining away); common cause/chain are open by default and closed by observing the middle node.')
TP('Do not forget descendants of a collider; do not claim d-separation after finding one blocked path (all must be blocked); do not mistake “A better in every subgroup” for “A better overall”.')

add('<h3>4.4 d-separation drill on the Student network (✓ checked with pgmpy)</h3>')
P('Edges <b>D→G, I→G, I→S, G→L</b> (G has parents D, I; D, I roots). Parameters: D 1 + I 1 + G (3−1)·4 = 8 + S 2 + L 3 = <b>15</b> vs 2·2·3·2·2 − 1 = <b>47</b> for the unrestricted joint. Joint = P(d)P(i)P(g|i,d)P(s|i)P(l|g), e.g. 0.4·0.7·0.25·0.95·0.6 = 0.0399.')
T([['Query', 'Observed', 'Result', 'Reason'],
   ['D, I', '∅', '<b>separated</b>', 'D→G←I: collider G unobserved'], ['D, I', 'G (or L)', '<b>connected</b>', 'collider (or its descendant) observed ⇒ explaining away'],
   ['D, S', '∅ / I', 'separated / separated', 'collider G blocks; given I the fork I is observed'], ['D, S', 'G', '<b>connected</b>', 'D→G←I→S: G observed opens, I unobserved passes'],
   ['L, S', '∅', '<b>connected</b>', 'L←G←I→S is open'], ['L, S', 'G or I', 'separated', 'chain/fork node observed'], ['D, L', '∅ / G', 'connected / separated', 'D→G→L chain'],
   ['S, L', 'G', 'separated', 'only path S←I→G→L is blocked at G']])
P('<b>Markov blankets:</b> MB(G) = {D, I, L}; MB(I) = {G, S, D} (children G, S + co-parent D); MB(D) = {G, I}. <b>Three kinds of reasoning:</b> <i>causal</i> (top-down, e.g. P(L | I)), <i>evidential</i> (bottom-up, P(I | L)), <i>intercausal</i> (between causes of a common effect, explaining away).')
add('<h3>4.5 Inference by hand on the Cancer network (pgmpy example network used in Weeks 8–12; ✓ recomputed) and parameter learning</h3>')
P('Edges Pollution→Cancer, Smoker→Cancer, Cancer→Xray, Cancer→Dyspnoea. P(Pollution=high) = 0.1, P(Smoker=T) = 0.3; P(Cancer=T | S,Pol): (T,low) 0.03, (T,high) 0.05, (F,low) 0.001, (F,high) 0.02; P(Xray=pos | C=T) = 0.9, | C=F 0.2; P(Dysp=T | C=T) = 0.65, | C=F 0.3.')
UL('<b>Evidence on all other nodes:</b> P(C=T | S=T, Pol=high, X=pos, D=T) ∝ 0.05·0.9·0.65 = 0.02925; P(C=F | …) ∝ 0.95·0.2·0.3 = 0.0570 ⇒ normalise 0.02925/0.08625 = <b>0.339</b> (factors not containing C cancel).',
   '<b>Marginal:</b> P(C=T) = Σ<sub>s,pol</sub>P(s)P(pol)P(C=T|s,pol) = 0.3·0.9·0.03 + 0.3·0.1·0.05 + 0.7·0.9·0.001 + 0.7·0.1·0.02 = <b>0.01163</b>. <b>Evidential:</b> P(C=T | Xray=pos) = 0.01163·0.9/(0.01163·0.9 + 0.98837·0.2) = <b>0.0503</b> (4.3× the prior but still small: low prior + 20% false-positive rate).',
   '<b>Independence:</b> given Cancer, Xray ⊥ Dyspnoea (common cause observed ⇒ blocked); unconditionally they are dependent. With Cancer = T: P(X=pos,D=T) = 0.9·0.65 = 0.585.',
   '<b>Parameter learning from counts:</b> MLE θ(x|pa) = N(x,pa)/N(pa). Data A = (0,0,0,0,1,1,1,1), B = (0,0,0,1,1,1,1,1): P(B|A=0) = (0.75, 0.25), P(B|A=1) = (0, 1) — a zero ⇒ log-likelihood −∞ for (A=1,B=0). With a K2 (+1 pseudo-count) prior: P(B|A=0) = (4/6, 2/6), P(B|A=1) = (1/6, 5/6). BDeu = Dirichlet prior with equivalent sample size spread over the cells.')

# =====================================================================================================
H('5 · PC ALGORITHM AND I-EQUIVALENCE', '#2e5a6a')
add('<h3>5.1 PC step by step (Mock Q5 parts 3–4 — 8 marks)</h3>')
Q('Mock Q5 (3)-(4)', 'PC on observations of I, B, H, A, α = 0.05; remove an edge when p &gt; α. Tests: I⊥B p=0.640; I⊥A 0.009; I⊥A|H 0.420; I⊥A|B 0.006; B⊥A|H 0.580; B⊥A|I 0.018; every other test reached has p &lt; 0.001. '
  '(3) Skeleton phase: for each removed edge give |S| and the separating set; draw the skeleton [4]. (4) Orient: find unshielded collider(s), apply orientation rules, draw result, explain the H–A edge [4].')
LG('<b>Skeleton:</b> start from the complete undirected graph. For |S| = 0, 1, 2, … test every still-adjacent pair X,Y given every subset S (size |S|) of their current neighbours; the first time p &gt; α remove the edge and <b>record Sep(X,Y) = S</b>; stop when no conditioning set of that size exists. '
   '<b>Colliders:</b> for each unshielded triple X–Z–Y (X, Y non-adjacent) orient X→Z←Y iff <b>Z ∉ Sep(X,Y)</b>. <b>Propagate</b> with Meek rules until nothing changes. Output = CPDAG.')
T([['Removed edge', '|S|', 'Evidence', 'Sep'], ['I − B', '0', 'I⊥B p = 0.640 &gt; 0.05', '∅'], ['I − A', '1', 'I⊥A|H p = 0.420 (but I⊥A p = 0.009 and I⊥A|B p = 0.006 keep it earlier)', '{H}'],
   ['B − A', '1', 'B⊥A|H p = 0.580 (B⊥A|I p = 0.018 &lt; 0.05 keeps it)', '{H}']])
P('<b>Skeleton:</b> I–H, B–H, H–A (3 edges). <b>(4)</b> Unshielded triple I–H–B with H ∉ Sep(I,B) = ∅ ⇒ collider <b>I → H ← B</b>. Triples I–H–A and B–H–A are <i>not</i> colliders (H ∈ Sep). Now I → H – A with I, A non-adjacent ⇒ orient <b>H → A</b> (Meek rule 1: otherwise a new unshielded collider I→H←A would appear). Result is fully directed: <b>I→H←B, H→A</b>. Marking: collider 1 + separator justification 1; H→A and rule 1; final graph 1.')
P('<b>Sensitivity remark ✓:</b> with α = 0.01 the test B⊥A|I (p = 0.018) would also remove B–A, so Sep(B,A) could be {I} or {H} depending on the order of tests (PC is order-dependent for finite samples; “stable PC” fixes this) — a different Sep set changes which triples are colliders.')
Q('Mock MCQ12', 'PC under causal sufficiency, Markov + faithfulness, perfect CI tests. (A) Unshielded R–S–T, R,T non-adjacent, S not in their separating set ⇒ R→S←T. (B) Every remaining skeleton edge is oriented in its unique true direction. (C) With “remove edge if p &gt; α”, changing α from 0.05 to 0.01 makes a test with p = 0.03 favour removal. (D) PC starts from the empty graph and adds edges.')
P(f'<b>Answer A, C.</b> A {OK}. B {NO} only a CPDAG (Markov equivalence class) is identifiable; chains and forks stay undirected. C {OK} 0.03 &lt; 0.05 (dependent, keep) but 0.03 &gt; 0.01 (independent, remove). D {NO} starts from the <i>complete</i> undirected graph and removes edges.')
add('<h3>5.2 I-equivalence of DAGs (Mock MCQ 13)</h3>')
Q('Mock MCQ13', 'Reference DAG on U,V,W,T,X,Y,Z with edges U→W, V→W, V→T, W→X, W→Y, X→Y, Y→Z, T→Z. Which candidates are Markov equivalent? A reverses X→Y to Y→X; B reverses W→X to X→W; C reverses T→Z to Z→T; D deletes W→Y.')
P(f'<b>Answer A only ✓.</b> Reference unshielded colliders: <b>U→W←V</b> and <b>Y→Z←T</b>. A {OK} W→X and Y→X are into X, but W–Y is adjacent (triangle W,X,Y) ⇒ shielded, no new immorality. B {NO} X→W←U and X→W←V are new unshielded colliders. C {NO} moves the collider from Z to T (V→T←Z). D {NO} different skeleton.')
FM('<b>I-equivalent ⇔ same skeleton AND same immoralities</b> (v-structures X→Z←Y with X, Y <i>non-adjacent</i>; a collider whose parents are adjacent is “shielded” and does not count). An edge X→Y is <i>covered</i> if Pa(Y) = Pa(X) ∪ {X}: reversing a covered edge preserves the equivalence class (here Pa(X) = {W}, Pa(Y) = {W,X}). '
   'X→Y→Z, X←Y←Z, X←Y→Z are equivalent; X→Y←Z is alone in its class. PC returns the CPDAG (same skeleton, same immoralities, every compelled edge directed). <b>Meek rules:</b> R1 a→b–c, a,c non-adjacent ⇒ b→c; R2 a→b→c and a–c ⇒ a→c (avoid cycle); R3 a–b, a–c, a–d, c→b, d→b with c,d non-adjacent ⇒ a→b. Complexity O(n<sup>d+2</sup>).')
TK('PC = (1) skeleton with growing |S| and recorded Sep sets, (2) colliders iff middle ∉ Sep, (3) Meek propagation. Test I-equivalence by comparing <b>skeleton + immoralities</b> only; arrows elsewhere may flip.')
TP('“Same skeleton” alone is not enough; p-value &gt; α means <i>independent</i> (edge removed) — do not invert the rule when α changes; with perfect tests PC still recovers only the CPDAG.')

add('<h3>5.3 PC on the Cancer network (Week 12 slides) and a second hand example (✓)</h3>')
Q('Week 12 slide', 'Cancer network, 10⁶ samples, χ² tests, α = 0.01. p-values: Pollution⊥Smoker 0.035 (|S|=0); Pollution⊥Xray|Cancer 0.668, Pollution⊥Dysp|Cancer 0.216, Smoker⊥Xray|Cancer 0.440, Smoker⊥Dysp|Cancer 0.123, Xray⊥Dysp|Cancer 0.249; every other order-0 / order-1 test &lt; 0.001. Run PC.')
P('<b>Skeleton:</b> remove Pollution–Smoker (p = 0.035 &gt; 0.01, Sep = ∅); remove Pollution–Xray, Pollution–Dysp, Smoker–Xray, Smoker–Dysp, Xray–Dysp (each with Sep = {Cancer}) ⇒ skeleton Cancer–Pollution, Cancer–Smoker, Cancer–Xray, Cancer–Dysp (4 of 10 edges); order 2 accepts nothing. '
  '<b>Orient:</b> Pollution–Cancer–Smoker is unshielded and Cancer ∉ Sep(Pollution,Smoker) = ∅ ⇒ <b>Pollution→Cancer←Smoker</b>; Cancer–Xray and Cancer–Dysp: Pollution→Cancer–Xray with Pollution, Xray non-adjacent ⇒ Meek R1 ⇒ <b>Cancer→Xray, Cancer→Dysp</b> ⇒ the true DAG. '
  '<b>At α = 0.05</b> the first test (0.035 &lt; 0.05) is “dependent”, the spurious Pollution–Smoker edge survives, no collider is found and the result changes: the significance level matters.')
P('<b>Second example (4 variables):</b> p(X⊥Y) = 0.70 ⇒ remove X–Y, Sep = ∅; p(W⊥X|Z) = 0.60, p(W⊥Y|Z) = 0.50 ⇒ remove W–X, W–Y, Sep = {Z}; skeleton W–Z, X–Z, Y–Z. Unshielded triples: X–Z–Y with Z ∉ ∅ ⇒ collider <b>X→Z←Y</b>; X–Z–W and Y–Z–W have Z ∈ Sep ⇒ not colliders. Meek R1: X→Z–W, X and W non-adjacent ⇒ <b>Z→W</b>. Final: X→Z, Y→Z, Z→W.')
UL('<b>Independence tests:</b> χ² for categorical data (statistic Σ(O−E)²/E), mutual information (G-test), partial correlation (Pearson) for continuous data, Pillai trace for ordinal/high-dimensional; H₀ = “independent”: p ≥ α ⇒ do not reject ⇒ treat as independent; tests are noisy with little data and errors propagate.',
   '<b>Score-based alternative (hill climbing):</b> greedy add / delete / reverse one edge, accept the move that most improves a decomposable score — BIC = log L − (d/2)·log N (penalises complexity), K2, BDeu — until no improvement; can stick in local optima. <b>Constraint-based (PC)</b> uses CI tests, outputs a CPDAG; both identify the structure only up to Markov equivalence from observational data.',
   '<b>Assumptions for PC’s guarantees:</b> causal Markov, faithfulness, causal sufficiency (no hidden common causes), reliable CI tests. Complexity O(n<sup>d+2</sup>) for maximum degree d.')

# =====================================================================================================
H('6 · SAMPLING IN BAYESIAN NETWORKS', '#6a5a2e')
add('<h3>6.1 Forward (ancestral) sampling (Mock Q5 part 5 — 4 marks; Week 11-12 sample part c — 4 marks)</h3>')
Q('Mock Q5 (5)', 'Using G<sub>BN</sub>, sample one complete particle in the order I, B, H, A with u₁ = 0.31, u₂ = 0.18, u₃ = 0.40, u₄ = 0.91 (set variable to 1 if u ≤ p, else 0); give another valid order.')
T([['Variable', 'P(state 1)', 'u', 'u ≤ p ?', 'State'], ['I', 'P(I=1) = 0.06', '0.31', 'no', '0'], ['B', 'P(B=1) = 0.25', '0.18', 'yes', '1'],
   ['H', 'P(H=1 | I=0, B=1) = 0.45', '0.40', 'yes', '1'], ['A', 'P(A=1 | H=1) = 0.85', '0.91', 'no', '0']])
P('<b>Sample (I,B,H,A) = (0,1,1,0).</b> Another valid order: <b>B, I, H, A</b> (parents before children; I and B are both roots). ✓ <i>Note:</i> with the same four random numbers in order B, I, H, A the particle becomes (0,0,0,0) — different numbers meet different variables — so always say which u goes with which variable. Marking: roots 1, H probability &amp; sample 1, A probability &amp; sample 1, alternative order 1.')
Q('Week 11-12 sample (c)', 'List the steps of forward sampling for the network C→T, C→Y, T→Y, T→M. Is the order unique? [4]')
P('1. sample c ~ P(C); 2. sample t ~ P(T | c); 3. sample m ~ P(M | t); 4. sample y ~ P(Y | c, t); return (c,t,m,y). <b>Order is not unique:</b> any <b>topological order</b> works (each variable after all its parents); C first, T second, but M and Y have no ancestor relation so steps 3 and 4 can swap.')
FM('<b>Discrete draw:</b> u ~ U(0,1); choose the first state k with u ≤ cumulative probability (binary: 1 iff u ≤ p). <b>Forward sampling</b> gives i.i.d. samples of the joint; estimate P(q) ≈ count/N, E[f] ≈ (1/N)Σf(x<sup>(s)</sup>), error ∝ 1/√N. '
   '<b>Rejection sampling (BN):</b> forward-sample, discard particles inconsistent with the evidence; acceptance rate ≈ P(e) ⇒ wasteful when evidence is rare. <b>Likelihood weighting:</b> clamp evidence, weight each sample by ∏P(e<sub>i</sub>|pa). '
   '<b>Rejection sampling (continuous):</b> proposal q with k·q(z) ≥ p̃(z) ∀z; draw z₀ ~ q, u₀ ~ U(0, kq(z₀)); accept iff u₀ &lt; p̃(z₀); acceptance rate = ∫p̃ / k (q normalised); too small a k distorts the target. '
   '<b>Gibbs sampling (MCMC):</b> evidence fixed; repeatedly resample X<sub>i</sub> ~ P(X<sub>i</sub> | Markov blanket) ∝ product of the factors containing X<sub>i</sub>; samples are correlated ⇒ burn-in, thinning, many sweeps; stationary distribution = P(X|e).')
TK('Write a table: variable → probability used (with its parents’ values) → u → compare → state. Then name the order rule: <b>any topological order</b>.')

add('<h3>6.2 Worked Gibbs sweep with evidence (Student network, S = 1 and L = 0 fixed; ✓ recomputed)</h3>')
P('CPDs: P(D) = (0.6,0.4); P(I) = (0.7,0.3); P(G|I,D): (I0,D0) = (.30,.40,.30), (I0,D1) = (.05,.25,.70), (I1,D0) = (.90,.08,.02), (I1,D1) = (.50,.30,.20); P(S=1|I) = (0.05, 0.80); P(L=0|G) = (0.10, 0.40, 0.99). State (d,i,g) = (0,0,1), sweep order D, I, G.')
T([['Resample', 'Conditional ∝ (only factors containing the variable)', 'Normalised', 'u → value'],
   ['D', 'P(g=1|i=0,D)·P(D) = (0.40·0.6, 0.25·0.4) = (0.24, 0.10)', '(0.706, 0.294)', 'u = 0.80 &gt; 0.706 ⇒ d = 1'],
   ['I', 'P(g=1|I,d=1)·P(S=1|I)·P(I) = (0.25·0.05·0.7, 0.30·0.80·0.3) = (0.00875, 0.072)', '(0.108, 0.892)', 'u = 0.50 ⇒ i = 1'],
   ['G', 'P(L=0|G)·P(G|i=1,d=1) = (0.1·0.5, 0.4·0.3, 0.99·0.2) = (0.05, 0.12, 0.198)', '(0.136, 0.326, 0.538)', 'u = 0.70 ⇒ g = 2']])
P('After sweep 1 the state is (1,1,2). Evidence nodes are <b>never resampled</b>; D’s conditional contains only P(D) and P(G|I,D) (its Markov blanket factors) — P(I), P(S|I), P(L|G) are constant in D and cancel on normalisation. '
  'The fraction of sweeps with I = 1 estimates P(I=1 | S=1, L=0) = <b>0.7226</b> (exact, by enumeration); consecutive states are autocorrelated (lag-1 ≈ 0.2 for I) ⇒ discard burn-in and use many sweeps.')
add('<h3>6.3 Rejection sampling and the sampling toolbox (✓)</h3>')
P('<b>Continuous rejection example:</b> target p̃(z) = 4z(1−z) on [0,1], q = Uniform(0,1), k = 1. Draws z₀ = (0.10, 0.50, 0.85, 0.30, 0.95, 0.65, 0.20, 0.40), u = (0.50, 0.90, 0.10, 0.80, 0.30, 0.45, 0.35, 0.99): p̃(z₀) = (0.36, 1.00, 0.51, 0.84, 0.19, 0.91, 0.64, 0.96) ⇒ accept iff u &lt; p̃ ⇒ (0,1,1,1,0,1,1,0); kept z = (0.5, 0.85, 0.3, 0.65, 0.2), empirical rate 5/8 = 0.625, theoretical ∫p̃/k = 2/3 (k = 2 would halve it to 1/3; k = 0.5 violates kq ≥ p̃ and under-samples the mode). Target density = 6z(1−z), Beta(2,2), mean 0.5. '
  '<b>Inverse-CDF sampling:</b> for p(z) = 2z on [0,1], F(z) = z² ⇒ z = √u; discrete: first k with u ≤ cum<sub>k</sub> (p = (0.1,0.3,0.4,0.2) ⇒ cum = (0.1,0.4,0.8,1.0), u = 0.55 ⇒ the third category, index 2).')
T([['Method', 'Evidence handling', 'Samples', 'Weakness'],
   ['Forward / ancestral', 'none (prior samples)', 'i.i.d. from P(X)', 'cannot condition'],
   ['Rejection', 'discard inconsistent particles', 'i.i.d. from P(X|e)', 'acceptance ≈ P(e); hopeless for rare/many evidence'],
   ['Likelihood weighting', 'clamp evidence, weight by ∏P(e|pa)', 'weighted i.i.d.', 'weights degenerate when evidence is unlikely / deep'],
   ['Gibbs (MCMC)', 'clamp evidence, resample X<sub>i</sub> | MB(X<sub>i</sub>)', 'correlated, asymptotically P(X|e)', 'burn-in, autocorrelation, slow mixing with deterministic CPDs']])

# =====================================================================================================
H('7 · BN → MARKOV NETWORK → FACTOR GRAPH, AND VARIABLE ELIMINATION (SUM-PRODUCT)', '#2e6a5a')
add('<h3>7.1 Moralisation, factor graph, Gibbs distribution, symbolic variable elimination (Week 11-12 sample — 13 marks)</h3>')
Q('Week 11-12 sample (d)-(f)', 'For the BN C→T, C→Y, T→Y, T→M: (d) transform it to a Markov network and explain the idea [4]; (e) draw the factor graph with one factor per CPD and write the Gibbs distribution [4]; (f) derive P(Y | M = mild) symbolically with sum-product variable elimination, order C, T, using φ(X,Z) for initial factors and φ(X)[Z=z] for factors reduced by evidence [3].')
LG('<b>(d) Moralise:</b> (1) for every node connect all pairs of its parents (“marry the parents”); (2) drop all directions. Guarantees every CPD scope P(X|Pa(X)) is a clique. <b>(e)</b> factor nodes = CPDs, each linked to the variables in its scope; φ = the CPD itself ⇒ Z = 1. '
   '<b>(f)</b> VE recipe: (i) list initial factors; (ii) <b>reduce</b> every factor mentioning evidence; (iii) for each variable in the elimination order: multiply all factors containing it into ψ, sum it out to get τ, put τ back; (iv) multiply what is left; (v) <b>normalise</b> by Σ<sub>y</sub>.')
P('<b>(d)</b> Edges C−T, C−Y, T−Y, T−M. Only Y has more than one parent (C, T), already adjacent through C→T ⇒ no immorality, no new edge; just remove directions. '
  '<b>(e)</b> Factor nodes and neighbours: φ(C)–{C}; φ(C,T)–{C,T}; φ(C,T,Y)–{C,T,Y}; φ(T,M)–{T,M}. <b>P(C,T,M,Y) = (1/Z) φ(C) φ(C,T) φ(T,M) φ(C,T,Y)</b> with φ(C) = P(C), φ(C,T) = P(T|C), φ(T,M) = P(M|T), φ(C,T,Y) = P(Y|C,T); since every factor is a CPD, <b>Z = 1</b>.')
P('<b>(f) Order C, T, evidence M = mild.</b> 1. Eliminate C: ψ₁(C,T,Y) = φ(C)·φ(C,T)·φ(C,T,Y); τ₁(T,Y) = Σ<sub>C</sub> ψ₁(C,T,Y). '
  '2. Reduce the factor with evidence and eliminate T: ψ₂(T,Y)[M=mild] = τ₁(T,Y)·φ(T,M)[M=mild]; τ₂(Y)[M=mild] = Σ<sub>T</sub> ψ₂(T,Y)[M=mild]. '
  '3. τ₂(Y)[M=mild] = P(Y, M=mild) is unnormalised ⇒ <b>P(Y | M=mild) = τ₂(Y)[M=mild] / Σ<sub>y</sub> τ₂(y)[M=mild]</b>.')
Q('Mock MCQ8', 'BN A→B→C and a separate MN A–B–C with positive pairwise potentials ψ₁(A,B), ψ₂(B,C). (A) The MN joint is always ψ₁ψ₂ with no normalisation. (B) The BN joint is P(A)P(B|A)P(C|B). (C) Each MN potential must sum to one before the joint is defined. (D) For the MN, Z = Σ<sub>a,b,c</sub>ψ₁(a,b)ψ₂(b,c) normalises the joint.')
P(f'<b>Answer B, D.</b> A {NO} needs 1/Z. C {NO} potentials are non-negative compatibility scores, not probabilities. BN CPDs are locally normalised; MN products are normalised globally by Z.')
FM('<b>Gibbs distribution</b> P(x) = (1/Z)∏<sub>c</sub>φ<sub>c</sub>(x<sub>c</sub>), Z = Σ<sub>x</sub>∏φ<sub>c</sub>. <b>VE:</b> τ(x<sub>S</sub>) = Σ<sub>z</sub>∏<sub>φ∋z</sub>φ; elimination of a variable creates a factor over its current neighbours; cost ∝ Σ k<sup>|scope(ψ)|</sup> (induced width); order does not change the answer, only the cost (best order is NP-hard ⇒ heuristics MinFill / MinNeighbors / MinWeight). '
   '<b>Marginal / conditional / MAP:</b> P(Q|e) = τ(Q,e)/Σ<sub>q</sub>τ(q,e); MAP uses <i>max-product</i> (replace Σ by max, then back-track). <b>BN→MN</b> loses the independencies encoded by immoralities; the factor graph is bipartite (variables ↔ factors).')
TK('Moralisation = “marry parents + drop arrows”; factor-graph from a BN = one factor per CPD ⇒ Z = 1; VE = reduce → (multiply, sum-out) per variable → multiply remainder → normalise. Always mark unnormalised results as P(Y, e).')

add('<h3>7.2 Factor operations and variable elimination with numbers (✓ recomputed)</h3>')
P('<b>Factor product / marginalise / reduce:</b> φ₁(A,B) = [[3,1],[1,3]] (rows A), φ₂(B,C) = [[2,1],[1,2]] (rows B). ψ(a,b,c) = φ₁(a,b)φ₂(b,c): (000) 6, (001) 3, (010) 1, (011) 2, (100) 2, (101) 1, (110) 3, (111) 6 — scope {A,B,C}, 8 entries. '
  'τ(A,C) = Σ<sub>B</sub>ψ = [[7,5],[5,7]]; <b>Z = 24</b> (sum of all entries); normalised τ = [[7,5],[5,7]]/24 = [[0.292,0.208],[0.208,0.292]]. Reduce φ₁[A=0] keeps the row (3,1) over B. A factor is <i>not</i> a probability until divided by Z.')
P('<b>Chain A→B→C→D:</b> P(A) = (0.6,0.4); P(B|A) rows (0.7,0.3),(0.2,0.8); P(C|B) rows (0.9,0.1),(0.4,0.6); P(D|C) rows (0.5,0.5),(0.1,0.9). Forward elimination = vector×matrix: τ₁ = P(B) = (0.5,0.5); τ₂ = P(C) = (0.65,0.35); P(D) = (0.36,0.64). '
  'Evidence D = 1: push the column (0.5,0.9) backwards: Σ<sub>c</sub>P(c|b)(0.5,0.9) = (0.54,0.74); Σ<sub>b</sub>P(b|a)(…) = (0.60,0.70); times P(a) ⇒ P(A,D=1) = (0.36,0.28), sum 0.64 = P(D=1) ✓ ⇒ <b>P(A|D=1) = (0.5625, 0.4375)</b>. Cost: 3 vector–matrix products = 12 multiplications vs 16 joint entries × 3 = 48; in general O(n·k²) vs O(kⁿ) thanks to the distributive law.')
P('<b>Elimination order matters for cost, not result:</b> Markov network with factors {A,B}, {B,C}, {C,D}, {B,D}, {D,E}. Order A,B,C,D,E creates ψ scopes of sizes (2,3,2,2,1) ⇒ largest table 3 variables; order B,D,A,C,E gives (4,4,3,2,1) ⇒ largest 4 variables (k⁴ vs k³ entries). Heuristics: MinFill, MinNeighbors, MinWeight. <b>Moralisation example:</b> a collider A→C←B gains the edge A–B; a chain or fork needs no new edge.')

# =====================================================================================================
H('8 · MARKOV NETWORKS: GRAPH DESIGN, INDEPENDENCE, FACTOR DESIGN', '#5a2e6a')
add('<h3>8.1 Friends network (Sample MN — 14 marks)</h3>')
Q('Sample MN', 'Alice, Bob, Carol, Dave, Emma (binary: attends event). Influence is symmetric. Alice–Bob influence each other; Bob, Carol, Dave form a close trio (each influences the other two); Emma is not influenced by Alice but relies on Bob and Dave. (a) Draw the Markov network [5]. (b) Give ≥ 2 conditional independencies with justification [4]. (c) Design factors, write the joint, explain the principles [5].')
LG('<b>(a)</b> One node per person; one undirected edge per “influences” relation; a trio = triangle; add nothing else. <b>(b)</b> Use <i>graph separation</i>: X ⊥ Y | Z iff removing Z disconnects X from Y. Easiest source: Markov blanket = neighbours. <b>(c)</b> Find maximal cliques; one factor per maximal clique (every factor scope must be a clique); write (1/Z)∏φ; define Z.')
P('<b>(a) Edges (6):</b> A–B, B–C, B–D, C–D, B–E, D–E. No A–C/A–D/A–E, no C–E. <b>(b)</b> <b>A ⊥ {C,D,E} | B</b> (Bob is Alice’s only neighbour = her Markov blanket, every path passes through B); <b>C ⊥ {A,E} | {B,D}</b> (blanket of Carol); <b>E ⊥ {A,C} | {B,D}</b>. '
  'The graph is connected ⇒ <b>no marginal independencies</b>: A ⊥ E (without conditioning) is wrong. A false statement: <b>C ⊥ E | B</b> fails because of the path C–D–E. Sub-statements follow by decomposition (A ⊥ D | B etc.). '
  '<b>(c) Maximal cliques:</b> {A,B}, {B,C,D}, {B,D,E}. <b>Design 1:</b> P(A,B,C,D,E) = (1/Z) φ₁(A,B) φ₂(B,C,D) φ₃(B,D,E), Z = Σ<sub>a,b,c,d,e</sub> φ₁φ₂φ₃. Each φ is a non-negative table over 2<sup>k</sup> assignments (k = |scope|); e.g. φ₁ large on (0,0),(1,1), small on (1,0),(0,1) encodes strong Alice–Bob agreement. '
  '<b>Design 2</b> adds sub-clique factors φ₄(B,C), φ₅(A), φ₆(C), φ₇(D): more interpretable but <i>same family</i> of distributions (absorbed into maximal-clique factors).')
P('<b>Principles (2 marks):</b> a Gibbs distribution factorises over the graph iff each factor’s scope is a clique ⇒ it satisfies the separation-based independencies; by the <b>Hammersley–Clifford theorem</b> every strictly positive distribution satisfying them is a product of clique factors ⇒ one factor per maximal clique is fully general; Z (partition function) normalises. '
  'Pairwise-only factors are valid but cannot express the three-way interactions in the two triangles. <b>Marking:</b> (a) 1 per node set / A–B / triangle / Emma edges / no spurious edges, −1 for directed edges; (b) 1 per independence + 1 per separation justification; (c) 1 cliques, 2 joint, 2 explanation; a factor like φ(A,E) or φ(C,E) (non-clique scope) loses the 2 joint marks. ✓ Parameter count: 4 + 8 + 8 = 20 table entries vs 2⁵ = 32 for the full joint.')
add('<h3>8.2 Graph-separation MCQs (Mock MCQ 9 and MCQ 11)</h3>')
Q('Mock MCQ9', 'P(U,V,W,X,Y) = (1/Z)ψ₁(U,V)ψ₂(U,W)ψ₃(V,W)ψ₄(W,X)ψ₅(W,Y)ψ₆(X,Y); H connects variables that share a factor. (A) MB(U) = {V,W}. (B) The maximal cliques are exactly the six factor scopes. (C) U ⊥ X | W. (D) V ⊥ Y | X.')
P(f'<b>Answer A, C ✓.</b> H = two triangles {{U,V,W}} and {{W,X,Y}} meeting at W. A {OK} neighbours of U. B {NO} maximal cliques are the two triangles {{U,V,W}}, {{W,X,Y}}. C {OK} removing W separates U from X. D {NO} the path V–W–Y stays open given X.')
Q('Mock MCQ11', 'Undirected I-map with edges A–B, C–D, E–F, G–H (rungs), A–C, C–E, E–G (left chain), B–D, D–F, F–H (right chain) and the arc B–F. Which independences are implied by separation? (A) A ⊥ H | D,E (B) C ⊥ H | E,F (C) A ⊥ F | B,D (D) B ⊥ G | C,F.')
P(f'<b>Answer B, D ✓.</b> A {NO} path A–B–F–H survives after removing D,E. B {OK} removing E,F separates {{A,B,C,D}} from {{G,H}}. C {NO} path A–C–E–F survives. D {OK} removing C,F separates {{A,B,D}} from {{E,G,H}}. An I-map need not encode every independence of P — ask only what separation <i>implies</i>.')
FM('<b>Separation test:</b> delete the conditioning nodes (and their edges), ask whether any path remains between X and Y; none ⇒ X ⊥ Y | Z. <b>Local Markov:</b> X ⊥ rest | neighbours(X). <b>Pairwise:</b> non-adjacent X,Y: X ⊥ Y | all others. <b>Clique:</b> every pair adjacent; <b>maximal</b> = cannot add a vertex. Edge set of H = pairs co-occurring in some factor. '
   'Factor over a non-clique is illegal; sub-clique factors are redundant. Entries per factor = ∏ cardinalities of its scope.')
TK('Build H from factor scopes, list <b>maximal</b> cliques (not all factors), then answer every independence by “delete Z, look for a path”. The answer to a “marginal independence” question in a connected graph is always no.')

add('<h3>8.3 The “misconception” network and BN vs MN (Week 9 slides)</h3>')
P('<b>Four-cycle example:</b> Alice–Bob, Bob–Charles, Charles–Debbie, Debbie–Alice meet in pairs. Separation gives <b>A ⊥ C | {B,D}</b> and <b>B ⊥ D | {A,C}</b> and nothing else. No Bayesian network encodes exactly these independencies (any DAG on the cycle either creates an immorality — which forces an extra edge in its moral graph — or has a directed cycle), so Markov networks represent some independence structures BNs cannot (and vice-versa: the collider X→Z←Y has no exact MN).')
T([['', 'Bayesian network', 'Markov network'],
   ['Graph', 'directed acyclic', 'undirected (cycles allowed)'], ['Factors', 'CPDs P(X|Pa(X)), locally normalised', 'non-negative potentials on cliques'],
   ['Normalisation', 'none needed (Z = 1)', 'partition function Z = Σ∏φ'], ['Independence test', 'd-separation (collider rules)', 'graph separation (delete Z, look for a path)'],
   ['Natural for', 'causal / generative stories, asymmetric influence', 'symmetric interactions (friends, pixels, label chains)'],
   ['Conversion', 'moralise ⇒ MN (loses immoralities)', 'chordal MNs can be turned into BNs']])
UL('<b>Three Markov properties:</b> pairwise (non-adjacent X,Y: X ⊥ Y | rest); local (X ⊥ others | neighbours(X)); global (separation). They coincide for strictly positive distributions (Hammersley–Clifford).',
   '<b>I-map:</b> I(H) ⊆ I(P) — every independence read off the graph holds in P, but P may have more; a <b>P-map</b> has I(H) = I(P) exactly.',
   '<b>Why design with cliques:</b> a factor over {A,E} would imply an A–E edge and break the A ⊥ E | B reading — factor scopes must be cliques of the graph.')

# =====================================================================================================
H('9 · LINEAR-CHAIN CRF: FACTOR GRAPH, PARTITION FUNCTION, MAP', '#7a4a2e')
add('<h3>9.1 CRF concepts (Mock MCQ 10) and the person-name tagger (Mock Q6 — 16 marks)</h3>')
Q('Mock MCQ10', 'Linear-chain CRF, labels Y₁..Y₄, input x: P(y|x) = (1/Z(x)) φ₁(y₁,x)∏<sub>t=2..4</sub>φ<sub>t</sub>(y<sub>t−1</sub>,y<sub>t</sub>,x). (A) Replacing sums by maxima in the forward recursion computes Z(x). (B) Z(x) is the sum of the unnormalised score over all label sequences with x fixed. (C) The observed inputs must also be summed out. (D) A sum-product forward pass gives α₄(y₄); then Z(x) = Σ<sub>y₄</sub>α₄(y₄). (E) Z is a penalty discouraging large weights.')
P(f'<b>Answer B, D.</b> A {NO} max-product gives the best-sequence <i>score</i> (MAP), not Z. B {OK}. C {NO} x is conditioned on, never summed out (CRF is discriminative: models P(y|x), not P(x)). D {OK} the last label must still be summed. E {NO} Z normalises; regularisation is a separate term.')
Q('Mock Q6', 'Tagger for names in x = “meet Ada Lovelace”, labels {O,P}. Emission potentials φ<sub>t</sub>(y): t=1 (O 5, P 1); t=2 (O 3, P 2); t=3 (O 1, P 4). Shared transition potential φ<sub>tr</sub>(y<sub>t−1</sub>,y<sub>t</sub>) (rows = previous): O→O 3, O→P 1, P→O 1, P→P 4. '
  'P(y|x) = (1/Z(x))∏φ<sub>t</sub>(y<sub>t</sub>)∏<sub>t=2,3</sub>φ<sub>tr</sub>(y<sub>t−1</sub>,y<sub>t</sub>). (1) Draw the factor graph and state one conditional independence [5]. (2) Compute Z(x) by sum-product VE in order Y₃ then Y₂, giving ψ<sub>i</sub> and τ<sub>i</sub> with all entries [11].')
LG('<b>(1)</b> 3 circles (Y₁–Y₃), 3 unary squares φ₁,φ₂,φ₃ each attached to its Y<sub>t</sub>, 2 pairwise squares φ<sub>tr</sub>(Y₁,Y₂), φ<sub>tr</sub>(Y₂,Y₃). The chain structure gives Y₁ ⊥ Y₃ | Y₂, X. '
   '<b>(2)</b> Eliminate Y₃ first: multiply <i>only</i> the factors containing Y₃, ψ₃(y₂,y₃) = φ<sub>tr</sub>(y₂,y₃)φ₃(y₃), then τ₃(y₂) = Σ<sub>y₃</sub>ψ₃. Then Y₂: ψ₂(y₁,y₂) = φ<sub>tr</sub>(y₁,y₂)φ₂(y₂)τ₃(y₂), τ₂(y₁) = Σ<sub>y₂</sub>ψ₂. Finally Z = Σ<sub>y₁</sub>φ₁(y₁)τ₂(y₁).')
T([['ψ₃(y₂,y₃)', 'y₃=O', 'y₃=P', 'τ₃(y₂)'], ['y₂=O', '3·1 = 3', '1·4 = 4', '<b>7</b>'], ['y₂=P', '1·1 = 1', '4·4 = 16', '<b>17</b>']])
T([['ψ₂(y₁,y₂)', 'y₂=O', 'y₂=P', 'τ₂(y₁)'], ['y₁=O', '3·3·7 = 63', '1·2·17 = 34', '<b>97</b>'], ['y₁=P', '1·3·7 = 21', '4·2·17 = 136', '<b>157</b>']])
P('<b>Z(x) = φ₁(O)τ₂(O) + φ₁(P)τ₂(P) = 5·97 + 1·157 = 485 + 157 = 642.</b> Marking: 4 for eliminating Y₃ (definition, products, sum, (7,17)); 4 for Y₂ ((97,157)); 3 for retaining φ₁, summing Y₁ with 5·97 and 1·157, final 642; 5 for the factor graph (nodes 1, unary factors 1, pairwise factors 1, labels 1, CI 1).')
P('<b>✓ Extensions (recomputed):</b> brute force over 2³ = 8 sequences — OOO 135, <b>OOP 180</b>, OPO 10, OPP 160, POO 9, POP 12, PPO 8, PPP 128 ⇒ Σ = 642 ✓. '
  '<b>MAP (Viterbi / max-product):</b> δ₁ = (5,1); δ₂(O) = max(5·3, 1·1)·3 = 45, δ₂(P) = max(5·1, 1·4)·2 = 10 (back-pointers O, O); δ₃(O) = max(45·3, 10·1)·1 = 135, δ₃(P) = max(45·1, 10·4)·4 = 180 (back-pointers O, O) ⇒ best sequence <b>O,O,P</b> (“meet Ada” = O, “Lovelace” = P) with score 180, probability 180/642 = <b>0.280</b>. '
  '<b>Marginals:</b> P(Y₁=P) = 0.245, P(Y₂=P) = 306/642 = 0.477, P(Y₃=P) = 0.748. <b>Forward check:</b> α₁ = (5,1); α₂ = (48,18); α₃ = (162,480); Z = 162+480 = 642 ✓.')
FM('<b>Linear-chain CRF:</b> P(y|x) = (1/Z(x))∏<sub>t</sub>φ<sub>t</sub>(y<sub>t</sub>)∏<sub>t≥2</sub>φ<sub>tr</sub>(y<sub>t−1</sub>,y<sub>t</sub>); in log space score(y) = Σ<sub>t</sub>emit<sub>t</sub>(y<sub>t</sub>) + Σ<sub>t</sub>trans(y<sub>t−1</sub>,y<sub>t</sub>). <b>Z(x) = Σ<sub>y</sub>∏φ</b> by the forward algorithm α<sub>t</sub>(y<sub>t</sub>) = φ<sub>t</sub>(y<sub>t</sub>)Σ<sub>y<sub>t−1</sub></sub>α<sub>t−1</sub>(y<sub>t−1</sub>)φ<sub>tr</sub>(y<sub>t−1</sub>,y<sub>t</sub>): cost O(T·K²) vs K<sup>T</sup> sequences. '
   '<b>MAP</b> = Viterbi (same recursion with max, keep arg-max pointers); marginals P(y<sub>t</sub>|x) = α<sub>t</sub>β<sub>t</sub>/Z. Training: maximise log P(y|x) = score(y) − log Z(x) (loss = −log-likelihood; <code>torchcrf</code> returns the log-likelihood, <code>decode</code> = Viterbi, <code>transitions[i,j]</code> = score i→j). '
   'A per-token softmax tagger decides each label independently ⇒ may output invalid BIO sequences; the CRF learns transition scores so the sequence is globally consistent.')
TK('CRF questions are variable elimination on a chain: <b>eliminate from one end, write ψ then τ as tables, multiply in the unary factor you retained, sum the last variable</b>. Z = Σ over labels only; x is fixed. Sum-product = Z/marginals; max-product = MAP.')

add('<h3>9.2 CRF in practice and model comparison</h3>')
T([['', 'Per-token softmax tagger', 'HMM (generative)', 'Linear-chain CRF'],
   ['Models', 'P(y<sub>t</sub>|x) independently per token', 'P(x,y) = ∏P(y<sub>t</sub>|y<sub>t−1</sub>)P(x<sub>t</sub>|y<sub>t</sub>)', 'P(y|x) = (1/Z(x))exp(Σ emission + Σ transition)'],
   ['Label dependence', 'none ⇒ may output invalid BIO (O → I-PER)', 'first-order Markov labels', 'learned transition scores ⇒ globally consistent sequence'],
   ['Normalisation', 'per token (softmax)', 'locally normalised', 'per sequence, Z(x) over K<sup>T</sup> sequences via forward algorithm'],
   ['Decoding', 'argmax per token', 'Viterbi', 'Viterbi (max-product)'],
   ['Inputs', 'any features of x', 'must model P(x)', 'any overlapping features of x, never modelled']])
UL('<b>pytorch-crf workflow:</b> a neural encoder produces <i>emission scores</i> (T × K); <code>crf = CRF(K, batch_first=True)</code>; loss = −crf(emissions, tags, mask=mask, reduction="mean") (log-likelihood = score(y) − log Z); prediction = <code>crf.decode(emissions, mask)</code>; the learned <code>crf.transitions[i][j]</code> is the score of moving from tag i to tag j — compare it with the <i>empirical</i> transition counts (large negative entries for invalid moves such as O → I-X).',
   '<b>Metrics:</b> token accuracy is inflated by the majority tag O; report span/entity F1 or macro-F1; CRF mainly improves span F1 and the transition structure rather than token accuracy.',
   '<b>Sum-product vs max-product on a chain:</b> forward α gives Z; adding backward β gives marginals P(y<sub>t</sub>=k|x) = α<sub>t</sub>(k)β<sub>t</sub>(k)/Z; replacing Σ by max gives the best sequence score (Mock: 180 for O,O,P, probability 180/642 = 0.28 — note the MAP sequence has probability far below 1).')

# =====================================================================================================
H('10 · MASTER FORMULA SHEET, TRUE/FALSE BANK AND ANSWER TEMPLATES', '#1f3a5f')
T([['Topic', 'Must-know formula / rule'],
   ['K-means', 'W = ΣΣ‖x−μ<sub>k</sub>‖²; Lloyd = assign + mean; local optimum; scale-dependent; scaling by s ⇒ W·s²'],
   ['Hierarchical', 'single = min, complete = max, average = mean of all pairs; n−1 merges; cut between merge n−K and n−K+1 for K clusters'],
   ['Ridge / Lasso', 'RSS + λΣβ² (shrinks) vs RSS + λΣ|β| (exact zeros, selection); λ↑ ⇒ bias↑ variance↓; standardise; intercept not penalised'],
   ['Cubic spline', 'K knots ⇒ K+4 parameters; basis {1,x,x²,x³,(x−ξ<sub>k</sub>)³₊}; q−p = δ(x−ξ)³; third-derivative jump 6δ; natural spline: K'],
   ['Neural net', 'u = Wx+b, h = ReLU(u), ŷ = W₂h+b₂; params = Σ(in·out+out); e = ŷ−y; ∇W₂ = e hᵀ; δu = (W₂ᵀe)⊙1[u&gt;0]; ∇W₁ = δu xᵀ; θ ← θ−η∇'],
   ['CNN', 'out = ⌊(n+2p−k)/s⌋+1; params = C<sub>out</sub>(C<sub>in</sub>k²+1); shared kernels; GAP removes the FC layer'],
   ['PCA / t-SNE', 'S = XcᵀXc/(n−1); scores = Xc·V; PVE = λ/Σλ; z<sub>new</sub> = Vᵀ(x−x̄); t-SNE has no transform, minimises KL(P‖Q)'],
   ['Bayesian net', 'P = ∏P(X|Pa); params Σ(|X|−1)∏|Pa|; chain/fork blocked by observing the middle; collider opened by observing it or a descendant'],
   ['Naive Bayes', 'P(C|f) ∝ P(C)∏P(f<sub>k</sub>|C); features independent given class; no explaining away'],
   ['PC / I-equiv.', 'Skeleton with Sep sets; collider iff Z ∉ Sep; Meek R1–R3; I-equivalent ⇔ same skeleton + same immoralities; PC returns CPDAG'],
   ['Sampling', 'forward: topological order, u ≤ cumulative; rejection acceptance ≈ P(e); Gibbs: X<sub>i</sub> | Markov blanket, burn-in; rejection (continuous): kq ≥ p̃, rate = ∫p̃/k'],
   ['MN / VE', 'P = (1/Z)∏φ<sub>c</sub> over cliques; moralise = marry parents + drop arrows; VE: reduce → (ψ = ∏, τ = Σ) → multiply → normalise; cost k<sup>|scope|</sup>'],
   ['CRF', 'Z = Σ<sub>y</sub>∏φ via forward α; MAP = Viterbi; x never summed; O(TK²) vs K<sup>T</sup>']])
add('<h3>10.1 True / False bank distilled from the Mock distractors</h3>')
UL(f'{NO} “Stable cluster assignments prove the global optimum.” — only a local optimum.',
   f'{NO} “Rescaling one feature never changes K-means clusters.” — it changes distances.',
   f'{NO} “Ridge is best for exact sparsity.” — Lasso (L1).  {OK} “L2 shrinks without forcing zeros.”  {NO} “L1/L2 on NN weights needs a linear model.”',
   f'{OK} “A cubic spline’s value, f′ and f″ are continuous at interior knots.”  {NO} “Each spline segment must interpolate its data.”  {OK} “Spline model is linear in β for fixed knots.”',
   f'{OK} “DEC target P is derived from Q (no labels), sharpens confident assignments.”  {NO} “Lower DEC loss ⇒ lower reconstruction error.”',
   f'{NO} “PCA keeps 2 of the original columns.”  {NO} “Centring makes PCA unit-free.”  {OK} “PCA projects new points with the training mean and loadings.”  {NO} “t-SNE gives a projection matrix.”',
   f'{OK} “Convolution reuses the same kernel across positions; stride 2 shrinks the map.”  {NO} “One kernel per position.”  {NO} “GAP makes classification impossible.”',
   f'{OK} “BN joint = P(A)P(B|A)P(C|B).”  {NO} “MN joint needs no Z.”  {NO} “MN potentials must be probabilities.”  {OK} “Z = Σ∏ψ.”',
   f'{OK} “U ⊥ X | W by separation.”  {NO} “Maximal cliques = the six factor pairs.” (they are the two triangles)',
   f'{OK} “Z(x) = Σ over label sequences, x fixed (sum-product).”  {NO} “Max-product computes Z.”  {NO} “x must be summed out.”  {NO} “Z is a regulariser.”',
   f'{OK} “PC orients R→S←T iff S ∉ Sep(R,T).”  {NO} “Remaining edges are all oriented.”  {OK} “Lowering α from 0.05 to 0.01 can remove an edge”: with the rule “remove iff p &gt; α”, p = 0.03 is dependent (kept) at α = 0.05 but independent (removed) at α = 0.01.',
   f'{NO} “PC starts from the empty graph.” — complete graph, then removes.  {OK} “Markov equivalent ⇔ same skeleton and unshielded colliders.”')
add('<h3>10.2 Answer templates that collect marks</h3>')
UL('<b>Draw-a-DAG:</b> “X influences Y ⇒ X→Y”; list edges; state roots; give factorisation; (optionally) parameter count.',
   '<b>d-separation:</b> table with path | structure (chain/fork/collider) | observed nodes | blocked or active; conclude with the rule “one active path ⇒ d-connected”.',
   '<b>Probability query:</b> identify query / evidence / nuisance variables; write the sum; substitute numbers; simplify to a fraction; interpret (prior vs likelihood).',
   '<b>Algorithm trace (clustering / PC / VE):</b> Step k → what is chosen (minimum, edge, variable) → updated structure (matrix, Sep set, τ factor) → next minimum. Show every updated table.',
   '<b>Design question (MN factors):</b> graph → maximal cliques → one φ per clique → (1/Z)∏φ → define Z → principle (clique scope, Hammersley–Clifford) → example numbers (agree = large).',
   '<b>Calculation question:</b> formula first, numbers second, units/rounding last; label every intermediate vector; when unsure of a later part, state the assumption so follow-through marks apply.')
add('<h3>10.2 True / False bank from the sample papers (BN, MN, inference, clustering)</h3>')
UL(f'{NO} “With nothing observed C and M are d-separated.” — C→T→M is active; {OK} “C ⊥ M | T”.  {NO} “Observing Y keeps the collider paths blocked.” — it opens them.',
   f'{OK} “Observing the collider H (or its descendant A) opens I→H←B (explaining away).”  {OK} “Given H, A adds nothing about I or B.”',
   f'{OK} “P(T=A|C=long,Y=1) ≈ 0.232 although A has the higher success rate” (prior P(T|C) = 1/7 vs 6/7).  {NO} “A is better overall because it is better in every subgroup.” — Simpson’s paradox: pooled rates are A 18.0 % vs B 20.2 %.',
   f'{OK} “Forward-sampling order is not unique: any topological order.”  {NO} “C must be sampled last.”  {NO} “Variable elimination gives a different answer for a different order.”',
   f'{OK} “Moralising C→T, C→Y, T→Y, T→M adds no edge.”  {OK} “A factor graph from a BN with one factor per CPD has Z = 1.”  {OK} “τ₂(Y)[M=mild] = P(Y, M=mild) is unnormalised.”',
   f'{NO} “A ⊥ E in the friends network.” — connected graph, only A ⊥ E | B (or | {{B,D}}).  {NO} “C ⊥ E | B.” — the path C–D–E stays open.  {NO} “φ(A,E) is a valid factor.” — not a clique.',
   f'{OK} “Single linkage on the Mock matrix: heights 0.4, 0.6, 0.9, 1.2; two clusters {{A,B,C,D}}, {{E}}.”  {NO} “Complete linkage gives the same two-cluster cut.” — it gives {{A,B,C}}, {{D,E}}.',
   f'{OK} “A noise-free dissimilarity table with a tie needs a stated tie-break.”  {OK} “A dendrogram’s leaf order can be rotated.”  {NO} “Closer on the x-axis means more similar.”')

add('<h3>10.3 Common mistakes that cost marks</h3>')
UL('<b>Clustering:</b> merging from the original matrix instead of the updated one; forgetting to list updated dissimilarities; no heights/leaf labels on the dendrogram; mixing up linkage (min vs max).',
   '<b>Splines:</b> equating polynomials instead of <i>derivatives</i>; wrong constant in p″(2) = 2a₂+12a₃; forgetting that the truncated term is 0 for x ≤ knot; counting K+3 instead of K+4 (or 5 vs 4 for one knot).',
   '<b>Neural nets:</b> applying ReLU to the output layer (identity here); forgetting biases in the parameter count; using ŷ−y with the wrong sign; claiming the second hidden unit’s gradient is non-zero when u₂ &lt; 0; updating with + instead of −.',
   '<b>Graphical models:</b> listing only one path in d-separation; ignoring descendants of colliders; confusing immoralities with shielded colliders; drawing edges for factors that are not cliques; calling unnormalised τ a probability; summing x out in a CRF.',
   '<b>PC:</b> reversing the p &gt; α rule; recording a separating set that was not actually used for the removal; orienting a collider when the middle node is in Sep; forgetting Meek R1 for the remaining edge.')

add('<h3>10.4 How the topics connect (concept map)</h3>')
P('<b>Model</b> → <b>inference</b> → <b>learning</b>: a Bayesian network (directed, CPDs) is turned into a Markov network by <i>moralisation</i> and into a <i>factor graph</i> with one factor per CPD; a CRF is a Markov network over labels conditioned on x. Exact inference = sum-product variable elimination (marginals, Z), max-product (MAP); on a chain it is the forward/Viterbi algorithm. '
  'Approximate inference = forward / rejection / likelihood-weighted / Gibbs sampling. Learning: parameters by MLE or Bayesian (K2/BDeu) estimation from counts; structure by PC (CI tests → CPDAG) or score-based search (BIC/K2/BDeu). Unsupervised methods (K-means, hierarchical, PCA, t-SNE, DEC) and supervised regularised/spline/neural models cover the non-graphical half of the paper.')
TK('Memorise the <b>shape</b> of each answer (steps, tables, named rule, interpretation). The numbers change between papers; the marking structure does not.')

# =====================================================================================================# =====================================================================================================
H('11 · QUESTION-TYPE DECISION GUIDE AND MARK ALLOCATION', '#10243f')
T([['If the question says …', 'Do this (solution logic)', 'Typical marks'],
   ['“Write the steps … sketch the dendrogram … cut for K clusters”', 'Matrix → circle min → merge + height → updated matrix (linkage rule) → repeat; sketch with leaf labels + heights; cut between merge n−K and n−K+1', '1/merge, 2 updates, 4 dendrogram, 1/cluster'],
   ['“Find p(ξ), q(ξ) … continuity constraint … express b₂,b₁,b₀ … basis … degrees of freedom”', 'Three equalities (value, f′, f″) → solve downward → q = p + δ(x−ξ)³ → truncated power basis → params = pieces·coeffs − constraints', '2 per part'],
   ['“Predict … hidden pre-activations … counts parameters … gradients … one step … ReLU”', 'u → ReLU → ŷ; Σ(in·out+out); e = ŷ−y; ∇W₂ = e hᵀ; ∇b₂ = e; θ − η∇; ReLU′ = 0 ⇒ zero incoming gradients', '3 / case; 2; 3 + 2 + 2'],
   ['“Create a DAG … factorise … d-separated? … paths … probability”', 'Sentence → edge; ∏P(X|Pa); enumerate paths with blocked/active; marginalise nuisance variables; Bayes + normalise', '5, 2, 2, 2+2'],
   ['“Name this phenomenon … explain using the graph”', 'Explaining away: collider observed ⇒ path opens ⇒ alternative cause lowers the other cause; Naive Bayes cannot (factor cancels)', '2 + 1'],
   ['“Carry out the skeleton phase … separating set … orient … rules”', 'Complete graph; |S| = 0,1,… ; p &gt; α ⇒ remove + Sep; collider iff middle ∉ Sep; Meek R1; draw CPDAG', '4 + 4'],
   ['“Generate one sample by forward sampling … other valid order”', 'Topological order; table variable | probability | u | state; second order with parents first', '1 + 1 + 1 + 1'],
   ['“Transform to a Markov network / factor graph / Gibbs distribution / P(Y|e) with VE”', 'Marry parents + drop arrows; one factor per CPD, Z = 1; reduce → ψ,τ per variable → multiply → normalise', '4, 4, 3'],
   ['“Draw the Markov network … conditional independencies … design the factors”', 'Edge per relation, trio = triangle; blanket / separation; maximal cliques → one φ each → (1/Z)∏φ, define Z; Hammersley–Clifford', '5, 4, 5'],
   ['“CRF factor graph … compute Z by sum-product in order Y₃, Y₂”', 'Circles + unary squares + pairwise squares; ψ → τ tables per eliminated label; Z = Σφ₁τ₂', '5 + 11 (4 + 4 + 3)'],
   ['“Which candidates are I-equivalent?” / “Which statements follow from separation?”', 'Compare skeleton + immoralities; delete the conditioning set and search for a path', '2 each (all-or-nothing)']])

# =====================================================================================================
H('12 · GLOSSARY: ONE-SENTENCE DEFINITIONS FOR “EXPLAIN / DEFINE” QUESTIONS', '#3a3a3a')
T([['Term', 'Definition'],
   ['Immorality / v-structure', 'X→Z←Y with X, Y <i>not</i> adjacent (an unshielded collider); if X–Y are adjacent the collider is “shielded” and is not an immorality.'],
   ['Moral graph / moralisation', 'Undirected graph obtained by marrying all parents of every node and dropping directions; each CPD scope becomes a clique.'],
   ['Markov blanket', 'BN: parents + children + co-parents of children; MN: the neighbours. Given its blanket a node is independent of everything else.'],
   ['d-separation', 'X and Y are d-separated by Z if every path between them is blocked (observed non-collider on it, or collider with it and all descendants unobserved); implies X ⊥ Y | Z.'],
   ['Explaining away', 'Two independent causes become dependent once their common effect (or a descendant) is observed; confirming one cause lowers the probability of the other.'],
   ['I-map / P-map / I-equivalence', 'I-map: independencies of the graph hold in P; P-map: graph independencies = those of P; I-equivalent graphs entail the same independencies (same skeleton + immoralities).'],
   ['CPDAG / PDAG', 'Partially directed graph representing a Markov equivalence class: compelled edges directed, reversible edges undirected; the output of PC.'],
   ['Separating set (Sep)', 'The conditioning set S with X ⊥ Y | S found when the edge X–Y was removed; used to decide colliders (middle node ∉ Sep).'],
   ['Clique / maximal clique', 'Clique: all pairs adjacent; maximal: no further vertex can be added. Markov-network factors live on cliques.'],
   ['Partition function Z', 'Normalising constant Z = Σ<sub>x</sub>∏φ<sub>c</sub>(x<sub>c</sub>) (CRF: Z(x) sums over labels only); not a regulariser.'],
   ['Factor graph', 'Bipartite graph with variable nodes and factor nodes; a factor is linked to the variables in its scope; makes the factorisation explicit.'],
   ['Sum-product / max-product', 'Message-passing / elimination with Σ (marginals, Z) or max (MAP); both exact on trees and chains.'],
   ['Induced width / elimination order', 'Size of the largest factor created minus one; governs cost k<sup>width+1</sup>; best order is NP-hard (use MinFill etc.).'],
   ['Burn-in / mixing', 'Initial Gibbs samples discarded because the chain has not reached the stationary distribution; mixing speed = how quickly correlation decays.'],
   ['Acceptance rate', 'Rejection sampling: fraction kept = ∫p̃/k; BN rejection: ≈ P(evidence).'],
   ['Local vs global optimum', 'K-means / hill climbing / neural-network training converge to local optima; restarts reduce the risk, never remove it.'],
   ['Bias–variance', 'Flexible models (many knots, small λ, deep nets, large K in K-means) have low bias, high variance; regularisation trades variance for bias; choose by validation/CV.'],
   ['Weight sharing', 'A convolution applies the same small kernel at every position ⇒ few parameters and translation equivariance.'],
   ['Data leakage', 'Using test/validation information (e.g. its mean, SD or labels) during fitting or preprocessing; standardise using training statistics only.']])

# =====================================================================================================H('13 · SUPPLEMENTARY FORMULAS FOR TOPICS NOT TESTED IN THE ANSWERS ABOVE (weeks 1–5)', '#2e6a4f')
T([['Topic', 'Formulas and facts'],
   ['Regression metrics', 'MSE = (1/n)Σ(y−ŷ)²; RMSE = √MSE (same unit as y); R² = 1 − RSS/TSS; mean of per-fold RMSEs ≠ √(mean MSE); sklearn’s <code>neg_mean_squared_error</code> is the negative of MSE.'],
   ['Classification metrics', 'Confusion matrix [[TN,FP],[FN,TP]] (rows = true); error = (FP+FN)/n; precision = TP/(TP+FP); recall = sensitivity = TP/(TP+FN); specificity = TN/(TN+FP); F1 = 2PR/(P+R); lowering the threshold raises recall and lowers precision; with ≈3 % positives “always No” already has ≈3 % error.'],
   ['Logistic regression', 'log[p/(1−p)] = β₀+β·x; p = 1/(1+e<sup>−(β₀+β·x)</sup>); coefficient = change in log-odds, e<sup>β</sup> = odds ratio; fitted by maximum likelihood; class = 1 iff p &gt; threshold (0.5 default, strict).'],
   ['Resampling', 'K-fold CV: average of K validation errors (K = 5/10); LOOCV: K = n; bootstrap: draw n with replacement, B repeats, SE(θ̂) = SD of the B estimates; ≈63.2 % distinct observations per bootstrap sample; validation-set approach varies with the random split.'],
   ['SVM', 'Hyperplane β₀+β·x = 0; margin width 2/‖β‖; soft margin min ½‖w‖²+CΣξ<sub>i</sub> (hinge loss); large C ⇒ narrow margin, few support vectors, low bias/high variance (sklearn); only support vectors matter; kernels linear / polynomial (γx·x′+r)<sup>d</sup> / RBF exp(−γ‖x−x′‖²) (large γ ⇒ local, overfits); scale features; one-vs-one for K classes ⇒ K(K−1)/2 classifiers; <code>decision_function</code> &gt; 0 ⇒ <code>classes_[1]</code>.'],
   ['Polynomial features', '<code>PolynomialFeatures(2)</code> on [a,b] ⇒ [1, a, b, a², ab, b²]; number of columns C(p+d, d) with bias; <code>interaction_only</code> drops pure powers.'],
   ['Preprocessing', 'Impute numeric with mean/median, categorical with mode (ties ⇒ first sorted value); <code>get_dummies(drop_first=True)</code> gives k−1 columns (avoids the dummy-variable trap); pandas std divides by n−1, NumPy / StandardScaler by n; fit scalers on the training fold only.'],
   ['Probability basics', 'P(A,B) = P(A)P(B|A); P(B) = Σ<sub>a</sub>P(B|a)P(a); Bayes P(A|B) = P(B|A)P(A)/P(B); A ⊥ B | C ⇔ P(A,B|C) = P(A|C)P(B|C); E[X] = Σ x P(x); marginalisation sums a variable out; conditioning = reduce to the evidence rows and renormalise.']])
UL('<b>Suggested order of attack (suggestion, based on the Mock mark distribution):</b> mechanical calculation sections first — hierarchical clustering 12, splines 12, neural network 15, CRF/Markov 16 (= 55 marks, each with a fixed recipe) — then BN/PC/sampling 19, then the 13 MCQs (26 marks) with every option judged independently; keep the last minutes to re-check signs, indices and normalisation (rows sum to 1, Z computed, probabilities ≤ 1).')
UL('<b>Permitted calculators (Mock cover):</b> online-calculator.com full-screen and tcsion.com scientific — practise e<sup>x</sup>, ln, √, fractions beforehand; keep exact fractions (164/700, 38/164) where possible.')

# =====================================================================================================
CSS = """
@page { size: A4; margin: 6mm 6.5mm 6mm 6.5mm; @bottom-center { content: counter(page) " / " counter(pages); font: 6pt Helvetica, Arial; color:#777; } }
:root { --lh: 1.29; --gap: 0.8mm; }
* { box-sizing: border-box; }
html, body { margin:0; padding:0; }
body { font: 8pt/var(--lh) "Helvetica Neue", Helvetica, Arial, "DejaVu Sans", sans-serif; color:#111; columns: 2; column-gap: 4mm; column-rule: 0.4px solid #bbb; column-fill: auto; }
.title { column-span: all; font-size: 8pt; font-weight: 700; padding: 1mm 1.6mm; background:#10243f; color:#fff; border-radius: 2px; margin-bottom: 1.2mm; }
h2 { font-size: 8pt; margin: 1.6mm 0 0.8mm; padding: 0.5mm 1.6mm; color:#fff; border-radius: 2px; font-weight: 700; break-after: avoid; }
h3 { font-size: 8pt; margin: 1.2mm 0 0.5mm; padding: 0 1mm; border-left: 2.4px solid #1f3a5f; background:#e8eef7; font-weight: 700; break-after: avoid; }
p { margin: 0 0 var(--gap); text-align: left; }
ul { margin: 0 0 var(--gap) 3.2mm; padding: 0; } li { margin: 0 0 0.35mm; }
.q { background:#fff8e1; border:0.4px solid #e6cf7a; border-radius:2px; padding: 0.4mm 1.2mm; margin: 0 0 var(--gap); }
.src { color:#7a5a00; font-weight:600; }
.b { padding: 0.4mm 1.4mm; margin: 0 0 var(--gap); border-radius: 2px; border-left: 2.4px solid; }
.lg { background:#e8f0fe; border-color:#1a56db; } .fm { background:#e9f7ee; border-color:#1e8f4e; }
.tk { background:#fff2cc; border-color:#d49a00; } .tp { background:#fde8e8; border-color:#c0392b; }
table.t { border-collapse: collapse; margin: 0 0 var(--gap); width: 100%; font-size: 8pt; }
table.t th, table.t td { border: 0.4px solid #9aa; padding: 0.1mm 0.9mm; text-align:left; vertical-align: top; }
table.t th { background:#e4e8ee; }
code { font: 8pt "DejaVu Sans Mono", Menlo, monospace; background:#eef0f3; padding:0 0.5px; border-radius:1.5px; }
.ok { color:#1e8f4e; font-weight:700; } .no { color:#c0392b; font-weight:700; }
tr { break-inside: auto; } table.t { break-inside: auto; }
"""


def render():
    return ('<!doctype html><html><head><meta charset="utf-8"><title>FIT5149 Solutions Cheat Sheet</title><style>'
            + CSS + '</style></head><body>' + ''.join(B) + '</body></html>')


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, 'deliverables')
    os.makedirs(out, exist_ok=True)
    html = render()
    # optional tuning from the command line:  --lh 1.3 --gap 1.0
    args = sys.argv[1:]
    for i, a in enumerate(args):
        if a == '--lh':
            html = html.replace('--lh: 1.29', f'--lh: {args[i+1]}')
        if a == '--gap':
            html = html.replace('--gap: 0.8mm', f'--gap: {args[i+1]}mm')
    open(os.path.join(out, 'FIT5149_Solutions_CheatSheet.html'), 'w').write(html)
    import re
    text = re.sub(r'<[^>]+>', '', html)
    print('ok; visible chars ~', len(text))
