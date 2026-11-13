# -*- coding: utf-8 -*-
"""Builds deliverables/FIT5149_Cheat_Sheet.html  (render with: node render_pdf.js <html> <pdf>).
Explanations: Vietnamese with English technical terms.  Code: English.  Limit: 5 A4 pages."""
import html, os, textwrap

esc = html.escape
W = []          # list of (week_title, [blocks])


def week(title, *blocks):
    W.append((title, blocks))


def code(s, width=64):
    """Code block: trailing comments that would wrap are moved to their own line above the code."""
    out = []
    for line in s.strip('\n').split('\n'):
        if '#' in line and len(line) > width:
            i = line.index('#')
            head, cm = line[:i].rstrip(), line[i + 1:].strip()
            ind = ' ' * (len(line) - len(line.lstrip()))
            out += textwrap.wrap(cm, width=width - len(ind) - 2, initial_indent=ind + '# ', subsequent_indent=ind + '# ')
            if head.strip():
                out.append(head)
        else:
            out.append(line)
    return '<pre>' + esc('\n'.join(out)) + '</pre>'


def ul(*items):
    return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


def p(s):
    return f'<p>{s}</p>'


# =============================================================== WEEK 1
week('W1 · EDA & preprocessing (Ames housing, linear regression)',
     code('''
df.info(); df.describe(); df.isna().sum()           # dtypes / thống kê / số NaN mỗi cột
df[c].fillna(df[c].mean())                          # numeric -> mean (median nếu lệch/outlier)
df[c].fillna(df[c].mode()[0])                       # categorical; mode() trả Series ĐÃ SẮP XẾP (hoà -> [0] = nhỏ nhất/alphabet)
X = pd.get_dummies(df, drop_first=True)             # k mức -> k-1 cột (tránh dummy-variable trap); tên cột Type_B
df.corr(); X.corrwith(y)                            # |r| cao giữa 2 feature => đa cộng tuyến; chọn feature tương quan với y
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=0)
sc = StandardScaler(); Ztr = sc.fit_transform(Xtr); Zte = sc.transform(Xte)   # fit CHỈ trên train (tránh leakage)
s = cross_val_score(LinearRegression(), X, y, cv=5, scoring='neg_mean_squared_error')
rmse = np.sqrt(-s); rmse.mean(), rmse.std()         # báo cáo mean ± std qua các fold'''),
     ul('<b>ddof</b>: pandas <code>.std()</code> chia <i>n−1</i>; <code>np.std</code>, <code>StandardScaler</code> chia <i>n</i> (ddof=0). Ví dụ 3 giá trị 3,4,5: np.std=0.8165, ddof=1 → 1.0.',
        '<code>neg_mean_squared_error</code>: sklearn "càng lớn càng tốt" ⇒ trả giá trị <b>âm</b>; luôn đổi dấu <code>-s</code> rồi √. Mean của RMSE từng fold ≤ √(mean MSE) (Jensen), hai số <b>không bằng nhau</b>.',
        'MSE = mean(e²); RMSE cùng đơn vị y; R² = 1 − RSS/TSS. Cột có NaN là float. Outlier: |z|&gt;3 hoặc IQR; target lệch → <code>np.log</code>. Scale không đổi dự đoán của OLS nhưng đổi hệ số.'))

# =============================================================== WEEK 2
week('W2 · Model selection, regularisation, logistic regression, resampling',
     ul('<b>Subset selection</b>: best subset = 2<sup>p</sup> mô hình; forward/backward stepwise = 1 + p(p+1)/2. RSS/R² luôn giảm/tăng khi thêm biến ⇒ chọn <i>kích thước</i> bằng CV hoặc C<sub>p</sub>/AIC/BIC (nhỏ nhất), adj-R² (lớn nhất). <code>SequentialFeatureSelector(LinearRegression(), k_features=5, forward=True, scoring=..., cv=5).fit(X,y)</code> (mlxtend).',
        '<b>Ridge</b> <code>Ridge(alpha)</code>: min ‖y−Xw‖² + α‖w‖² (co hệ số, <u>không bao giờ = 0</u>). <b>Lasso</b> <code>Lasso(alpha)</code>: min <sup>1</sup>⁄<sub>2n</sub>‖y−Xw‖² + α‖w‖₁ (một số hệ số <u>đúng bằng 0</u> ⇒ feature selection). α↑ ⇒ variance↓, bias↑. Phải <b>standardise</b> trước.',
        'Khi XᵀX = nI: Lasso ŵ<sub>j</sub> = sign(β̂<sub>j</sub>)·max(|β̂<sub>j</sub>|−α, 0) (soft-threshold); Ridge ŵ<sub>j</sub> = β̂<sub>j</sub>·n/(n+α) (co đều).'),
     code('''
lcv = LassoCV(cv=5, alphas=np.logspace(-3, 1, 50)).fit(X, y)    # lcv.alpha_, lcv.coef_, lcv.mse_path_ (n_alphas x n_folds)
np.nonzero(lcv.coef_)[0]                                       # chỉ số biến được giữ
res = sm.GLM(y, sm.add_constant(X), family=sm.families.Binomial()).fit()   # logistic: res.params, res.summary()
prob = res.predict(sm.add_constant(X)); pred = (prob > 0.5).astype(int)     # predict() = XÁC SUẤT; ngưỡng ">" là strict
err = np.mean(pred != y); cm = confusion_matrix(y, pred)                    # cm = [[TN, FP], [FN, TP]]: HÀNG = true, CỘT = pred
b = resample(df)                                                            # bootstrap: lấy mẫu CÓ hoàn lại, kích thước n
se = np.std([boot_fn(resample(df)) for _ in range(B)]); np.percentile(est, [2.5, 97.5])'''),
     ul('Logistic: log-odds = β₀+β·x tuyến tính; p = 1/(1+e<sup>−(β₀+β·x)</sup>). precision = TP/(TP+FP); recall = TP/(TP+FN); specificity = TN/(TN+FP). Hạ ngưỡng ⇒ recall↑, precision↓. Dữ liệu mất cân bằng (≈3% default): luôn đoán "No" đã có error ≈ 3% ⇒ cần so với baseline.',
        '<b>Validation set</b>: 1 lần chia, kết quả đổi theo split. <b>K-fold</b> (K=5/10) cân bằng bias–variance. <b>LOOCV</b> K=n, ít bias nhưng đắt/variance cao. <b>Bootstrap</b> SE = độ lệch chuẩn của ước lượng qua B mẫu; ~63.2% quan sát khác nhau trong mỗi mẫu.'))

# =============================================================== WEEK 3
week('W3 · Non-linear methods (polynomials, splines)',
     code('''
PolynomialFeatures(degree=2).fit_transform([[2, 3]])      # [[1, 2, 3, 4, 6, 9]] = [1, a, b, a², ab, b²]; #cột = C(p+d, d)
PolynomialFeatures(2, include_bias=False, interaction_only=True).fit_transform([[2, 3]])   # [[2, 3, 6]] (bỏ a², b²)
dmatrix("bs(x, knots=(5, 7), degree=3)", {"x": x})        # patsy: cột = degree + K  (+1 intercept) -> shape (n, 6)
dmatrix("bs(x, df=6, degree=3)", {"x": x})                # df = degree + K  => K = 3 knots (quantile); shape (n, 7) gồm intercept
smf.ols("y ~ bs(x, knots=(5, 7), degree=0)", df).fit()    # degree=0: hằng số từng đoạn; params = [mean đoạn 1, Δ đoạn 2, Δ đoạn 3]
ns(x, df=4)                                               # natural spline (ISLP/patsy): tuyến tính ngoài biên
cross_val_score(LinearRegression(), Xpoly, y, cv=5, scoring='neg_mean_squared_error')'''),
     ul('<b>Polynomial</b>: bậc d lớn ⇒ dao động mạnh ở biên (variance cao); chọn d bằng CV. <b>Step function</b>: <code>pd.cut</code>, hệ số = chênh lệch so với vùng cơ sở.',
        '<b>Regression spline</b>: cubic từng đoạn, liên tục f, f′, f″ tại K knots ⇒ 4(K+1) − 3K = <b>K+4</b> tham số (gồm intercept). <b>Natural spline</b>: tuyến tính ngoài hai boundary knot ⇒ variance thấp ở biên. Knots đặt theo quantile của x.',
        '<b>Smoothing spline</b>: min Σ(y−g(x))² + λ∫g″(t)²dt. λ→0: nội suy (overfit); λ→∞: đường thẳng. Chọn λ bằng LOOCV; <i>effective df</i> = trace(S<sub>λ</sub>). <b>GAM</b>: f = β₀ + Σ f<sub>j</sub>(x<sub>j</sub>) — phi tuyến nhưng cộng tính, diễn giải được.'))

# =============================================================== WEEK 4
week('W4 · Support vector machines',
     ul('Siêu phẳng w·x+b=0, phân loại theo dấu. Margin: khoảng cách tới điểm gần nhất = 1/‖w‖; <b>bề rộng toàn phần = 2/‖w‖</b> khi y(w·x+b)≥1 (dấu "=" tại support vector). Hard-margin chỉ khi tách được. Soft-margin: min ½‖w‖² + CΣξ<sub>i</sub>; hinge loss max(0, 1 − y·f(x)).',
        'sklearn: <b>C lớn</b> ⇒ ít vi phạm, margin hẹp, ÍT support vector, bias thấp/variance cao (ngược với "budget C" của ISLR). <b>Chỉ support vector</b> (trên/trong margin hoặc phân sai) quyết định ranh giới; dời điểm khác không đổi mô hình.',
        'Kernel: linear x·x′; poly (γx·x′+r)<sup>d</sup>; <b>RBF</b> exp(−γ‖x−x′‖²): γ lớn ⇒ cục bộ, dễ overfit; γ nhỏ ⇒ gần tuyến tính. Luôn <b>scale</b> feature trước SVM.'),
     code('''
m = SVC(kernel='linear', C=1e6).fit(X, y)          # C rất lớn ~ hard margin
m.classes_                                         # thứ tự alphabet, vd ['blue' 'red']; decision_function > 0  <=>  classes_[1]
m.n_support_      # số SV THEO TỪNG CLASS (theo classes_);  m.support_ = chỉ số (0-based);  m.support_vectors_
m.coef_, m.intercept_                              # chỉ kernel linear; w = coef_[0]; bề rộng margin = 2/np.linalg.norm(w)
m.decision_function([[3, 2]])                      # w·x+b ; +1/-1 = nằm đúng trên biên margin
m.score(X, y)                                      # accuracy; gọi trên dữ liệu train => TRAIN accuracy
GridSearchCV(SVC(), {'C': [.1, 1, 10], 'gamma': [.01, .1, 1]}, cv=5).fit(X, y).best_params_
make_pipeline(StandardScaler(), SVC(kernel='rbf'))
TfidfVectorizer().fit_transform(texts)             # tf-idf = tf·idf; CountVectorizer = bag-of-words; fit CHỈ trên train
classification_report(yte, pred); ConfusionMatrixDisplay.from_predictions(yte, pred)'''),
     ul('Multi-class <code>SVC</code> dùng one-vs-one: K(K−1)/2 bộ phân loại. Đo trên dữ liệu mất cân bằng: dùng stratified CV, F1/Cohen κ thay vì accuracy.'))

# =============================================================== WEEK 5
week('W5 · Neural networks: MLP, CNN, attention/Transformer, LLM',
     ul('Layer: <b>A = g(XW + b)</b>; X(8,10)·W(10,4) → (8,4). <b>nn.Linear(in,out)</b> có in·out + out tham số. ReLU = max(0,u), đạo hàm 1[u&gt;0]. Output: regression = tuyến tính; binary = sigmoid; K lớp = softmax (trừ max để ổn định). Loss: MSE; BCE; <b>CE = −log p<sub>đúng</sub></b>; hinge cho SVM.',
        'Backprop (softmax+CE, 1 mẫu): dz = p − y; dW₂ = dz·hᵀ; dh = W₂ᵀdz; du = dh ⊙ 1[u&gt;0]; dW₁ = du·xᵀ. Unit có u≤0 ⇒ gradient 0 ("dead"). Cập nhật: w ← w − lr·∂L/∂w.'),
     code('''
loss = nn.CrossEntropyLoss()(logits, target)       # logits THÔ (chưa softmax) + chỉ số lớp; softmax 2 lần = sai
opt.zero_grad(); loss.backward(); opt.step()       # backward() chỉ TÍNH grad và CỘNG DỒN vào .grad; step() mới cập nhật
model.train() / model.eval();  with torch.no_grad(): ...      # dropout/BN khác nhau; no_grad khi suy luận
nn.Conv2d(3, 16, kernel_size=5, stride=2, padding=2)    # H_out = floor((H + 2p - k)/s) + 1 ; params = 16*(3*5*5) + 16 = 1216
nn.MaxPool2d(2)  # (H,W)->(H/2,W/2) ;  nn.AdaptiveAvgPool2d(1) -> (B,C,1,1) ;  nn.Flatten() -> (B, C*H*W)
nn.Embedding(V, d)                                  # params V*d ; token id -> vector
attn = torch.softmax(Q @ K.transpose(-2, -1) / math.sqrt(d_k), dim=-1) @ V      # mỗi HÀNG attn sum = 1
scores.masked_fill(mask == 0, float('-inf'))        # causal mask: vị trí bị chặn có trọng số 0 sau softmax'''),
     ul('<b>CNN</b>: weight sharing + local connectivity + pooling (translation invariance). Số tham số conv không phụ thuộc kích thước ảnh. "same" padding: p=(k−1)/2 với stride 1.',
        '<b>Attention</b> = softmax(QKᵀ/√d<sub>k</sub>)V; chia √d<sub>k</sub> làm scores <i>nhỏ đi</i> để softmax không bão hoà. Multi-head: h đầu, mỗi đầu d/h chiều rồi concat + W<sub>o</sub>. Positional encoding (sin/cos) vì attention không biết thứ tự. Block: self-attention → residual + LayerNorm → MLP → residual + LayerNorm. Chi phí O(N²d).',
        '<b>ViT</b>: patchify ảnh H×W×C với patch P ⇒ N=(H/P)(W/P) token, mỗi token P²C chiều → Linear → +positional encoding → các block → head. CNN có inductive bias (locality) ⇒ tốt khi ít dữ liệu; ViT cần nhiều dữ liệu. <b>LLM</b>: BPE tokenisation (subword) → embedding → decoder-only Transformer (causal mask) pretrain dự đoán token kế tiếp → alignment (instruction tuning/RLHF).'))

# =============================================================== WEEK 6
week('W6 · Clustering: K-means, hierarchical, clustering learned representations',
     code('''
km = KMeans(n_clusters=2, n_init=10, random_state=0).fit(X)     # km.labels_, km.cluster_centers_, km.inertia_, km.predict(Xnew)
d = pdist(X)                    # vector rút gọn độ dài n(n-1)/2 ;  squareform(d) <-> ma trận vuông n×n
Z = linkage(d, method='single')  # 'single' | 'complete' | 'average' | 'ward'.  linkage(squareform-matrix) = BUG (bị coi là n quan sát p=n đặc trưng)
Z[i] = [idx_a, idx_b, height, size]                            # cụm mới thứ i có id n+i ; height không giảm (single/complete/average/ward)
fcluster(Z, t=2, criterion='maxclust'); fcluster(Z, t=3.0, criterion='distance'); dendrogram(Z)
feat = resnet18(weights=...); feat.fc = nn.Identity()          # 512-d embedding -> normalize -> KMeans
adjusted_rand_score(true_labels, km.labels_); pd.crosstab(true, km.labels_)   # ARI: 1 = khớp, ≈0 = ngẫu nhiên'''),
     ul('<b>K-means</b> (Lloyd): lặp (a) tính centroid = mean của cụm, (b) gán điểm về centroid gần nhất. Mục tiêu <b>inertia</b> = Σ‖x−μ<sub>k</sub>‖² giảm sau mỗi bước nhưng chỉ tới <b>local optimum</b> ⇒ <code>n_init</code> chạy nhiều khởi tạo, không đảm bảo global. Inertia luôn giảm khi K tăng (K=n ⇒ 0) ⇒ chọn K bằng elbow/silhouette. <b>Scale</b> biến trước khi tính khoảng cách. Điểm mới → gán về centroid gần nhất.',
        '<b>Linkage</b>: <i>single</i> = min khoảng cách giữa 2 cụm (chaining, cụm dài); <i>complete</i> = max (cụm gọn); <i>average</i> = trung bình mọi cặp (d(AB,C) = (|A|d(A,C)+|B|d(B,C))/(|A|+|B|)); <i>ward</i> = tối thiểu tăng within-cluster variance. Thuật toán: gộp cặp có dissimilarity nhỏ nhất, cập nhật ma trận, lặp; vẽ dendrogram, chiều cao = mức dissimilarity khi gộp; cắt ở độ cao h hoặc K cụm.',
        'Cách làm tay (đề mẫu Oct-2023): liệt kê ma trận sau mỗi bước, vd single: d((B,C),A) = min(d(A,B),d(A,C)). Cụm học từ <b>representation</b> (embedding CNN) tốt hơn pixel thô; ViT lab: so sánh CNN vs MiniViT, optimiser SGD vs Adam, đếm tham số, patchify.'))

# =============================================================== WEEK 7
week('W7 · Dimension reduction: PCA, PCR, t-SNE',
     code('''
pca = PCA(n_components=2).fit(Xs)        # Xs = StandardScaler().fit_transform(X)   (PCA phụ thuộc scale!)
pca.components_            # (k, p): MỖI HÀNG = 1 PC (loading, ‖φ‖=1) ;  pca.explained_variance_ = eigenvalue λ (ddof=n-1)
pca.explained_variance_ratio_.cumsum()   # PVE tích luỹ ;  PCA(n_components=0.95) -> số PC nhỏ nhất đạt ≥ 95% phương sai
Z = pca.transform(Xs)  == (Xs - pca.mean_) @ pca.components_.T      # score ;  pca.inverse_transform(Z) = tái tạo
pcr = Pipeline([('sc', StandardScaler()), ('pca', PCA(n_components=M)), ('lr', LinearRegression())])  # PCR; chọn M bằng CV
TSNE(n_components=2, perplexity=30, random_state=0).fit_transform(X)   # KHÔNG có .transform cho điểm mới
S = Xc.T @ Xc / (n-1); vals, vecs = np.linalg.eigh(S)                 # eigh trả eigenvalue TĂNG dần -> phải sắp giảm dần'''),
     ul('<b>Curse of dimensionality</b>: số vùng tăng mũ theo p; khi p≳n OLS khớp hoàn hảo train (R²→1, test tệ). PCA: PC₁ = hướng phương sai lớn nhất, các PC trực giao; λ<sub>m</sub>/Σλ = PVE; tổng bình phương sai số tái tạo khi bỏ PC = (n−1)·Σλ<sub>bỏ</sub>. Dấu eigenvector tuỳ ý. Hai cột không tương quan ⇒ PC trùng trục (tỉ lệ = tỉ lệ phương sai).',
        '<b>PCR</b> = PCA (unsupervised) rồi hồi quy trên M score; không bảo đảm các PC dự đoán tốt y. <b>TruncatedSVD</b>: không centre, dùng cho ma trận thưa (bag-of-words).',
        '<b>t-SNE</b>: giữ láng giềng cục bộ (P Gaussian ở chiều cao, Q Student-t ở chiều thấp, tối thiểu KL(P‖Q)); <i>perplexity</i> ≈ số láng giềng hiệu dụng (5–50); ngẫu nhiên ⇒ đặt random_state; khoảng cách giữa cụm & kích thước cụm <u>không</u> có ý nghĩa; thường PCA→50 chiều trước. PCA tuyến tính, giữ cấu trúc toàn cục, có transform.'))

# =============================================================== WEEK 8
week('W8 · Bayesian networks (pgmpy)',
     code('''
bn = DiscreteBayesianNetwork([('D','G'), ('I','G'), ('I','S'), ('G','L')])
TabularCPD('G', 3, values, evidence=['I','D'], evidence_card=[2,2], state_names={...})
#   values.shape = (card(G), prod card(parents)) ; mỗi CỘT tổng = 1 ; BIẾN evidence CUỐI đổi nhanh nhất:
#   cột = (I0,D0), (I0,D1), (I1,D0), (I1,D1) khi evidence=['I','D']
bn.add_cpds(c1, c2, ...); bn.check_model()          # True nếu CPD khớp graph (cardinality, cột tổng 1) else ValueError
bn.is_dconnected('D','I'); bn.is_dconnected('D','I', observed=['L'])      # d-connected? (True = KHÔNG bị chặn)
bn.get_markov_blanket('G'); bn.local_independencies('G'); bn.get_independencies()
bn.get_parents('G'); bn.get_children('G'); bn.get_roots(); bn.get_leaves(); bn.get_immoralities()
bn.simulate(100)  # forward sample ;  bn.fit(df, estimator=...)  # học tham số'''),
     ul('<b>Factorisation</b>: P(X₁..X<sub>n</sub>) = Π P(X<sub>i</sub> | Pa(X<sub>i</sub>)). Student: P(d,i,g,s,l)=P(d)P(i)P(g|i,d)P(s|i)P(l|g). <b>#tham số độc lập</b> = Σ<sub>i</sub> (|X<sub>i</sub>|−1)·Π|Pa<sub>i</sub>| (G 3 trạng thái, 2 cha nhị phân: 2×4 = 8, <u>không phải</u> 12); bảng joint đầy đủ: Π|X<sub>i</sub>| − 1.',
        '<b>d-separation</b> (path giữa A,B): <i>chain</i> A→M→B và <i>fork</i> A←M→B: <b>bị chặn khi M được quan sát</b>; <i>collider</i> A→M←B: bị chặn khi M <b>và mọi hậu duệ của M</b> KHÔNG được quan sát (quan sát M hoặc hậu duệ ⇒ mở = <i>explaining away</i>). Hai nút d-separated ⇔ <u>mọi</u> path bị chặn; chỉ cần <u>một</u> path mở ⇒ d-connected. D-sep ⇒ độc lập có điều kiện.',
        '<b>Markov blanket</b> = cha + con + cha khác của các con. Loại lập luận: causal (top-down), evidential (bottom-up), intercausal. Học tham số từ đếm; thiết kế BN từ mô tả: nguyên nhân → hệ quả, mediator, confounder (C→T, C→Y). Deep BN (pomegranate): encoder NN biến input thô (ảnh) thành biến rời rạc làm nút trong BN; dữ liệu thiếu dùng <code>MaskedTensor</code>.'))

# =============================================================== WEEK 9
week('W9 · Markov networks, factor graphs, CRF',
     code('''
mn = DiscreteMarkovNetwork(); mn.add_edges_from([('A','B'), ('B','C')])
f1 = DiscreteFactor(['A','B'], [2,2], [3,1,1,3])     # values (A0B0, A0B1, A1B0, A1B1): biến ĐẦU đổi chậm nhất
mn.add_factors(f1, f2); psi = f1 * f2                 # tích factor: scope = hợp, 3 biến -> 8 ô
psi.marginalize(['B'], inplace=False); f1.reduce([('A',0)], inplace=False); tau.normalize()   # sum-out / điều kiện hoá / chuẩn hoá
sorted(psi.scope())      # THỨ TỰ scope() của pgmpy không ổn định -> luôn tự sort khi so sánh
BeliefPropagation(mn).query(['C'], evidence={'A':0}); mn.get_local_independencies(); bn.to_markov_model(); mn.to_factor_graph()
crf = CRF(n_tags, batch_first=True)
nll = -crf(emissions, tags, mask=mask, reduction='mean')    # crf(...) trả LOG-LIKELIHOOD ⇒ loss = âm của nó
crf.decode(emissions, mask=mask)       # Viterbi: list các chuỗi tag tốt nhất ;  crf.transitions[i, j] = điểm chuyển tag i -> j'''),
     ul('<b>Gibbs distribution</b>: P(x) = (1/Z) Π<sub>c</sub> φ<sub>c</sub>(x<sub>c</sub>), φ ≥ 0 trên <i>clique</i>; <b>Z = Σ<sub>x</sub> Πφ</b> (partition function; vd Z=24 ⇒ chia 24 mới ra xác suất). Factor là điểm tương thích, <u>không</u> phải xác suất. Hammersley–Clifford: P&gt;0 thoả các độc lập của đồ thị ⇔ phân rã theo clique cực đại.',
        '<b>Độc lập trong MN</b> = <i>graph separation</i>: X⊥Y|Z nếu Z chặn mọi path; Markov blanket = hàng xóm. Đồ thị liên thông ⇒ không có độc lập biên (A⊥E không suy ra được). <b>BN → MN</b> = <i>moralisation</i> (nối các cha chung của một con, bỏ hướng); factor = CPD ⇒ Z=1. <b>Factor graph</b>: đồ thị hai phía biến–factor.',
        '<b>Linear-chain CRF</b>: P(y|x) = (1/Z(x))·exp(Σ<sub>t</sub> emit(t,y<sub>t</sub>) + Σ<sub>t</sub> trans(y<sub>t−1</sub>,y<sub>t</sub>)); Z(x) tính bằng forward algorithm O(T·K²) thay vì liệt kê K<sup>T</sup> chuỗi; decode bằng Viterbi (MAP). Softmax per-token chọn nhãn độc lập ⇒ có thể ra chuỗi BIO không hợp lệ (O → I-X); CRF học <b>transition</b> (so learned với empirical; ô không hợp lệ rất âm) ⇒ nhất quán cấp chuỗi. Metric: token accuracy dễ cao giả; dùng span F1 / Macro F1.'))

# =============================================================== WEEK 10
week('W10 · Exact inference: variable elimination, MAP',
     code('''
ve = VariableElimination(bn)
ve.query(['Cancer'], evidence={'Smoker':'T'}, elimination_order='MinFill', show_progress=False)   # DiscreteFactor đã CHUẨN HOÁ
q.values, q.state_names                              # values thứ tự theo state_names;  joint=True (mặc định) -> bảng joint các biến query
ve.map_query(['Cancer'], evidence={...})             # {'Cancer': 'F'}  MAP assignment (dict)
BeliefPropagation(bn).query([...]); bn.to_markov_model().to_factor_graph()'''),
     ul('<b>Queries</b>: marginal P(X); conditional P(Q|e) = P(Q,e)/P(e); <b>MAP</b> = argmax<sub>q</sub> P(q|e) (sum-product → <i>max-product</i>: thay Σ bằng max, rồi truy ngược).',
        '<b>Variable elimination</b>: (1) chuyển BN→MN→factor graph, mỗi CPD là một factor; (2) <b>reduce</b> các factor chứa evidence (giữ ô khớp); (3) chọn thứ tự loại biến (biến evidence/query không bị loại); (4) với mỗi biến Z theo thứ tự: ψ = Π (mọi factor chứa Z), τ = Σ<sub>Z</sub> ψ, thay vào danh sách; (5) nhân các factor còn lại, <b>chuẩn hoá</b> → P(Q|e). Chain A→B→C→D: τ₁ = pA·P(B|A) = P(B), ... ⇒ n·k² thay cho kⁿ.',
        '<b>Chi phí</b> ∝ Σ k<sup>|scope(ψ)|</sup>, scope = biến loại + hàng xóm hiện tại ⇒ lớn nhất = <i>induced width</i>+1. Kết quả <u>không đổi</u> theo thứ tự, chỉ chi phí đổi; tìm thứ tự tối ưu là NP-khó ⇒ heuristic <b>MinFill</b> (ít cạnh bù nhất), <b>MinNeighbors</b>, <b>MinWeight</b>, <b>WeightedMinFill</b>. Cây/chuỗi ⇒ width nhỏ ⇒ chính xác & rẻ; lưới/đồ thị dày ⇒ cần xấp xỉ (sampling). Belief propagation (junction tree) tính mọi marginal một lượt.'))

# =============================================================== WEEK 11
week('W11 · Approximate inference: sampling',
     code('''
cum = np.cumsum(p); k = np.argmax(u <= cum)          # lấy mẫu rời rạc: lớp ĐẦU TIÊN có u ≤ cumulative (xác suất)
# rejection (liên tục): z0~q ;  u0~U(0, k*q(z0)) ;  nhận z0 nếu u0 < p~(z0) ;  cần k*q(z) >= p~(z) mọi z ; acceptance = ∫p~ / k (q chuẩn hoá)
s = BayesianModelSampling(bn)
s.forward_sample(size=1000, seed=0)                  # ancestral: theo thứ tự topo, mỗi biến ~ P(X | cha đã lấy mẫu)
s.rejection_sample(evidence=[State('Smoker','T')], size=1000)     # forward + bỏ mẫu không khớp evidence
s.likelihood_weighted_sample(evidence=[...], size=1000)           # evidence cố định, mẫu có trọng số
ApproxInference(bn).query(['Cancer'], n_samples=10000, evidence={...})
GibbsSampling(model).sample(start_state=None, size=1000)          # pgmpy: không nhận evidence; notebook dùng pyAgrum gum.GibbsSampling'''),
     ul('<b>Forward sampling</b>: thứ tự <u>không duy nhất</u> (mọi thứ tự topological). <b>Rejection</b>: tỉ lệ nhận ≈ P(e) ⇒ lãng phí khi evidence hiếm. <b>Gibbs (MCMC)</b>: giữ evidence cố định; lặp, mỗi lần lấy lại một biến X<sub>i</sub> ~ P(X<sub>i</sub> | MB(X<sub>i</sub>)) ∝ Π factor chứa X<sub>i</sub> (các nhân tử không chứa X<sub>i</sub> triệt tiêu); mẫu <i>tự tương quan</i> ⇒ cần <b>burn-in</b>, nhiều sweep; hội tụ về phân phối dừng P(X|e). Ước lượng E[f] ≈ (1/N)Σf(x<sup>(s)</sup>); sai số Monte Carlo ∝ 1/√N.',
        'So sánh: forward/rejection cho mẫu <i>độc lập</i> nhưng bỏ phí; Gibbs không bỏ phí nhưng phụ thuộc, mixing chậm. <b>N-gram language model</b> là một BN (P(w<sub>t</sub> | w<sub>t−1</sub>, w<sub>t−2</sub>)): tham số bằng MLE từ đếm Counter; sinh câu bằng lấy mẫu từ kế tiếp; Gibbs resample từng vị trí.'))

# =============================================================== WEEK 12
week('W12 · Structure learning (PC algorithm), parameter estimation',
     code('''
chi_square(X, Y, Z, data, boolean=True)                # CI test (χ²): p ≥ α  => không bác bỏ H0 "độc lập" => X ⊥ Y | Z
PC(data).estimate(ci_test='chi_square', significance_level=0.05, return_type='dag')   # 'skeleton' | 'pdag' | 'dag'
HillClimbSearch(data).estimate(scoring_method='bic-d')  # score-based: thêm/xoá/đảo cạnh; 'bic-d' cần cột dtype category (int bị coi là liên tục)
bn.fit(df, estimator=DiscreteMLE())                      # MLE: θ(x|pa) = N(x,pa)/N(pa)  (đếm)
bn.fit(df, estimator=DiscreteBayesianEstimator(prior_type='K2'))   # +1 pseudo-count mỗi ô
DiscreteBayesianEstimator(prior_type='BDeu', equivalent_sample_size=5)   # mặc định BDeu, ESS=5'''),
     ul('<b>PC</b>: (1) <b>skeleton</b>: bắt đầu đồ thị đầy đủ; với |U|=0,1,2,...: xoá cạnh X−Y nếu có U (từ láng giềng) sao cho X⊥Y|U (p ≥ α) và ghi <i>sepset</i>(X,Y)=U; (2) <b>immorality</b>: với X−Z−Y, X,Y không kề: là collider X→Z←Y ⇔ <b>Z ∉ sepset(X,Y)</b>; (3) <b>Meek rules</b>: R1 a→b−c, a,c không kề ⇒ b→c (tránh immorality mới); R2 a→b→c, a−c ⇒ a→c (tránh chu trình); R3. Kết quả là <b>CPDAG</b>, không phải DAG. α nhỏ (0.01) giữ ít cạnh ngẫu nhiên hơn α=0.05; kiểm định nhạy với nhiễu/ít dữ liệu. Độ phức tạp O(n<sup>d+2</sup>).',
        '<b>I-equivalence</b>: hai DAG tương đương ⇔ <u>cùng skeleton VÀ cùng tập immoralities</u> (v-structure mà hai cha không kề nhau). X→Y→Z, X←Y←Z, X←Y→Z tương đương (X⊥Z|Y) ⇒ PC trả X−Y−Z; X→Y←Z (X⊥Z nhưng X⊥̸Z|Y) là duy nhất. Cùng skeleton chưa đủ. P-map duy nhất tới I-equivalence.',
        '<b>MLE</b> cho xác suất 0 với tổ hợp chưa gặp ⇒ log-likelihood −∞; prior Dirichlet (K2/BDeu) = làm mượt. Số mẫu nhỏ ⇒ ước lượng nhiễu. <b>Score</b> BIC = log L − (d/2)·log N (phạt độ phức tạp); phân rã theo nút ⇒ cập nhật cục bộ khi thêm/xoá cạnh.'))

# =============================================================== WORKED PATTERNS
PATTERNS = ul(
    '<b>Số cần nhớ</b>: e<sup>−1</sup>=0.368, e<sup>−2</sup>=0.135, e<sup>1</sup>=2.718, e<sup>2</sup>=7.389, e<sup>6</sup>=403; σ(0)=0.5, σ(1)=0.731, σ(2)=0.881, σ(3)=0.953; ln2=0.693, ln3=1.099, ln10=2.303; √2=1.414, √3=1.732.',
    '<b>Softmax + CE</b>: z=[2,0] ⇒ p=[0.881,0.119], loss=−ln0.881=<b>0.127</b>; softmax 2 lần ⇒ p=[0.88,0.12] đưa vào CE ⇒ 0.383 (sai). z=[−1.5,4.5], nhãn lớp 0 ⇒ p=[0.002,0.998], loss=ln(1+e<sup>6</sup>)=6.002, argmax=1 ⇒ phân loại sai.',
    '<b>Bayes từ bảng đếm</b> (đề mẫu BN): P(Y=1|C=long)=Σ<sub>T</sub>P(Y=1|T,C)P(T|C)=0.38·(1/7)+0.21·(6/7)=164/700≈0.234; P(T=A|C=long,Y=1)=0.38·(1/7)/0.234≈0.232 (prior P(T|C) lấn át likelihood).',
    '<b>Single linkage tay</b> (đề mẫu Oct-2023): gộp cặp nhỏ nhất (B,C)@0.2; d((BC),A)=min(0.5,0.7)=0.5; d((BC),D)=min(0.9,0.7)=0.7 ⇒ gộp A@0.5, rồi D@0.7, cuối cùng E@1.0. Average linkage: lấy trung bình mọi cặp (vd (6+5)/2=5.5).',
    '<b>PCA 2×2</b>: S=[[a,b],[b,a]] ⇒ λ=a±b, eigenvector (1,±1)/√2; PVE₁=(a+|b|)/(2a). Hai cột không tương quan ⇒ PC trùng trục.',
    '<b>Lasso/Ridge tay</b> (XᵀX=nI, β̂=[4,−3,2,1,0.5], α=1.5): Lasso ⇒ [2.5,−1.5,0.5,0,0] (2 hệ số = 0); Ridge n=8,α=8 ⇒ β̂·8/16=[2,−1.5,1,0.5,0.25] (0 hệ số = 0).',
    '<b>SVM tay</b>: SV (2,2),(4,4)∈red; (2,1),(4,3)∈blue ⇒ w=(−2,2), b=1: f(x)=−2x₁+2x₂+1; margin=2/‖w‖=0.707; f(3,2)=−1 (nằm đúng biên phía blue).',
    '<b>Đếm tham số</b>: MLP 2→3→2: 2·3+3+3·2+2=17; Conv2d(3,16,5): 16·75+16=1216; Linear(4096,10): 40 970; BN (5 biến) với |D|=2,|I|=2,|G|=3,|S|=2,|L|=2: 1+1+8+2+3=15 vs joint 47.',
    '<b>CRF/VE</b>: Z (T=3, K=2) = 8 chuỗi ⇒ cộng 8 điểm; hoặc loại Y₃ rồi Y₂: τ₃(y₂)=Σtrans·emit₃, τ₂(y₁)=Σtrans·emit₂·τ₃, Z=Σemit₁·τ₂. Xác suất nhãn giữa = (tổng điểm các chuỗi có nhãn đó)/Z.',
    '<b>d-separation nhanh</b>: chain/fork: mở khi M <u>chưa</u> quan sát; collider: mở khi M <u>hoặc hậu duệ</u> được quan sát. Student (D→G←I, I→S, G→L): D,I d-separated; quan sát L ⇒ d-connected; D,S d-connected | G; L,S d-separated | G (chain bị chặn).',
    '<b>BN đề mẫu (Dr Johnson)</b>: C→T, C→Y, T→Y, T→M, M→Y ⇒ P(C)P(T|C)P(M|T)P(Y|C,T,M). C,M d-connected qua C→T→M; quan sát T ⇒ C⊥M|T (collider Y chưa quan sát chặn hai path còn lại). Moralise: cha của Y là {C,T,M}; C–T và T–M đã có cạnh, chỉ cần thêm <b>C–M</b>, rồi bỏ hướng.',
    '<b>MN đề mẫu (Alice…Emma)</b>: cạnh A–B, B–C, B–D, C–D, B–E, D–E; clique cực đại {A,B}, {B,C,D}, {B,D,E} ⇒ P=(1/Z)φ(A,B)φ(B,C,D)φ(B,D,E). A⊥{C,D,E}|B đúng; C⊥E|B <u>sai</u> (còn path C–D–E); C⊥{A,E}|{B,D} đúng.',
    '<b>PC tay</b> (α=0.05): p(X,Y)=0.70 ⇒ xoá X–Y, sepset=∅; p(W,X|Z)=0.60, p(W,Y|Z)=0.50 ⇒ xoá, sepset={Z}. Skeleton: W–Z, X–Z, Y–Z. X–Z–Y: Z∉∅ ⇒ collider X→Z←Y; Meek R1 ⇒ Z→W.',
    '<b>Rejection/forward sample</b>: so u với cumulative; nhận z₀ nếu u·k·q(z₀) &lt; p̃(z₀); acceptance lý thuyết = ∫p̃/k; rejection BN giữ ≈ N·P(e) mẫu.')

# =============================================================== FINAL CHECKLIST
CHECK = ul(
    '<b>Đọc đúng thứ được in</b>: shape vs giá trị, <code>.round()</code>, float/int, chuỗi hay mảng; đếm số dòng <code>print</code>.',
    '<b>Mặc định hay gây bẫy</b>: pandas std ddof=1 / numpy ddof=0; <code>neg_</code> scoring; confusion matrix hàng=true; ngưỡng <code>&gt;</code> strict; <code>mode()[0]</code> khi hoà; <code>drop_first</code>; <code>n_support_</code> theo class; TSNE không có <code>transform</code>; <code>bias=True</code> trong Conv/Linear; <code>eigh</code> sắp tăng dần.',
    '<b>Tự kiểm tra</b>: hàng softmax/CPD cộng = 1; số tham số = Σ cột·hàng + bias; xác suất ∈ [0,1]; chuẩn hoá bằng tổng; sanity check bằng trường hợp biên (K=n, α→∞, λ→0).',
    '<b>pgmpy</b>: <code>TabularCPD</code> cột theo evidence cuối đổi nhanh nhất; <code>DiscreteFactor</code> biến đầu đổi chậm nhất; <code>query</code> trả factor đã chuẩn hoá; thứ tự <code>scope()</code> không ổn định.',
    '<b>Hướng làm</b>: nhận diện hàm & tham số mặc định → tính tay một phần nhỏ → đối chiếu từng lựa chọn → kết luận kèm lý do (đề mẫu chấm cả lập luận).')

CSS = """
@page { size: A4; margin: 6.5mm 7mm 7mm 7mm; @bottom-right { content: "FIT5149 cheat sheet · " counter(page) "/" counter(pages); font: 7pt Helvetica, Arial; color:#777; } }
* { box-sizing: border-box; }
body { font: 8.5pt/1.3 "Helvetica Neue", Helvetica, Arial, sans-serif; color:#111; margin:0; }
h1 { font-size: 13pt; margin: 0 0 1.2mm; } .sub { font-size: 7.6pt; color:#555; margin-bottom: 1.5mm; }
.wk { break-inside: avoid; margin: 0 0 2.6mm; }
.grid { display: grid; grid-template-columns: minmax(0, 1.18fr) minmax(0, 1fr); column-gap: 3mm; align-items: start; }
.L { min-width: 0; } .R { min-width: 0; }
h2 { font-size: 9.3pt; margin: 0 0 1mm; padding: 0.6mm 1.6mm; background:#1f3a5f; color:#fff; border-radius: 2px; }
pre { background:#f3f4f6; border:0.5px solid #d3d6db; border-radius:2px; padding: 1mm 1.6mm; margin: 0 0 1mm; font: 6.55pt/1.26 Menlo, Consolas, "DejaVu Sans Mono", monospace; white-space: pre-wrap; word-break: break-word; }
code { font: 7.4pt "DejaVu Sans Mono", Menlo, monospace; background:#eef0f3; padding: 0 0.6px; border-radius: 1.5px; }
ul { margin: 0 0 0.8mm 3.4mm; padding: 0; } li { margin: 0 0 0.8mm; } p { margin: 0.6mm 0; }
.cols2 li { overflow-wrap: anywhere; } .cols2 { column-count: 2; column-gap: 4mm; } .cols2 ul { margin-left: 3.4mm; }
.final { break-inside: avoid; }
.final h2 { background:#7a2e2e; }
"""


def render():
    h = f'<!doctype html><html><head><meta charset="utf-8"><title>FIT5149 Cheat Sheet</title><style>{CSS}</style></head><body>'
    h += '<h1>FIT5149 · Code-reading cheat sheet (Weeks 1–12)</h1>'
    h += '<div class="sub">Dùng để đọc code và dự đoán output/kết quả trong bài thi. Code bằng tiếng Anh; giải thích tiếng Việt + thuật ngữ tiếng Anh. Thư viện: scikit-learn, statsmodels/patsy, SciPy, PyTorch, pgmpy, pytorch-crf.</div>'
    for title, blocks in W:
        L = ''.join(b for b in blocks if b.startswith('<pre>'))
        R = ''.join(b for b in blocks if not b.startswith('<pre>'))
        h += f'<div class="wk"><h2>{title}</h2><div class="grid"><div class="L">{L}</div><div class="R">{R}</div></div></div>'
    h += '<div class="wk"><h2 style="background:#2e6a4f">Mẫu tính tay &amp; số cần nhớ (hay gặp trong đề)</h2><div class="cols2">' + PATTERNS + '</div></div>'
    h += '<div class="wk final"><h2>Checklist khi đọc code trong phòng thi</h2>' + CHECK + '</div>'
    h += '</body></html>'
    return h


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, 'deliverables')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'FIT5149_Cheat_Sheet.html'), 'w').write(render())
    print('ok')
