# -*- coding: utf-8 -*-
"""Question text + answer key. Code is looked up in snippets.CODE, outputs in outputs.json.
Question language: English (as in the real exam). Justifications: Vietnamese with English terms."""

T, F = True, False

MCQ = [
# ---------------------------------------------------------------- W1
dict(id='A1', week='Week 1 · EDA & preprocessing', code='A1',
 stem='The code below is run. Which statements about what it prints are correct?',
 options=[
  ("The first printed line is [50.0, 60.0, 65.0, 80.0, 70.0].", T,
   "Area có 4 giá trị hợp lệ (50, 60, 80, 70) nên mean = 260/4 = <b>65</b>; ô NaN được thay bằng 65.0 (float vì cột có NaN)."),
  ("The missing Type is imputed with 'B', because B appears last in the data.", F,
   "A và B xuất hiện 2 lần mỗi loại (hoà). <code>mode()</code> trả về <b>cả hai</b> giá trị đã sắp xếp, ['A','B'], nên <code>[0]</code> = 'A'. In ra ['A','B','A','A','B']."),
  ("X has shape (5, 3) because both categories A and B receive an indicator column.", F,
   "<code>drop_first=True</code> bỏ dummy đầu tiên (Type_A) ⇒ chỉ còn Area và Type_B ⇒ shape <b>(5, 2)</b>. (Bỏ một mức để tránh dummy-variable trap/đa cộng tuyến hoàn hảo với intercept.)"),
  ("The column list printed is ['Area', 'Type_B'].", T,
   "Đúng như giải thích ở trên; cột dummy mang tên <code>Type_B</code>."),
  ("The last line prints 11.18 first and 10.0 second.", T,
   "Dữ liệu sau impute: 50, 60, 65, 80, 70, tổng bình phương lệch = 500. pandas <code>.std()</code> dùng <b>ddof=1</b>: √(500/4)=11.18; numpy <code>np.std</code> dùng <b>ddof=0</b>: √(500/5)=10.0."),
 ], key_note="Đáp án: A, D, E"),

# ---------------------------------------------------------------- W1-2
dict(id='A2', week='Week 1–2 · Model evaluation (cross-validation)', code='A2',
 stem='<code>neg_mse</code> holds the scores returned by <code>cross_val_score(..., scoring="neg_mean_squared_error")</code> for three folds. Which statements about the printed output are correct?',
 options=[
  ("The mean of the per-fold RMSEs (4.0) is smaller than the RMSE computed from the mean MSE (4.0825).", T,
   "Per-fold RMSE = 3, 4, 5 ⇒ mean = 4.0. Mean MSE = (9+16+25)/3 = 16.67 ⇒ √ = 4.0825. Vì √ là hàm lõm (Jensen) nên mean(√MSE) ≤ √mean(MSE); hai cách <b>không</b> bằng nhau."),
  ("Averaging the per-fold RMSEs always gives the same number as taking the square root of the averaged MSE.", F,
   "Chỉ bằng nhau khi mọi fold có MSE như nhau. Ở đây 4.0 ≠ 4.0825."),
  ("<code>rmse.std()</code> prints 0.8165 because NumPy's default is ddof=0 (divide by n).", T,
   "Độ lệch bình phương quanh mean 4: 1+0+1 = 2; 2/3 = 0.667 ⇒ √ = 0.8165."),
  ("<code>rmse.std(ddof=1)</code> prints 1.0, the sample standard deviation (divide by n−1).", T,
   "2/(3−1) = 1 ⇒ √1 = 1.0."),
  ("The prefix <code>neg_</code> means that the model's prediction errors are negative.", F,
   "scikit-learn quy ước 'score càng lớn càng tốt'; metric là loss (MSE) nên bị <b>đổi dấu</b>. Vì vậy code của môn luôn viết <code>-cross_val_score(...)</code> để lấy lại giá trị dương."),
 ], key_note="Đáp án: A, C, D"),

# ---------------------------------------------------------------- W2
dict(id='A3', week='Week 2 · Classification metrics', code='A3',
 stem='A logistic-regression model produced the probabilities in <code>prob</code>. Which statements are correct?',
 options=[
  ("<code>cm[0, 1] = 2</code> counts observations whose true class is 0 but which were predicted as 1.", T,
   "<code>confusion_matrix(y_true, pred)</code>: hàng = <b>true</b>, cột = <b>predicted</b>. cm[0,1] là true=0, pred=1 (false positive): các điểm 0.55 và 0.60."),
  ("The rows of the confusion matrix correspond to the predicted classes.", F,
   "Hàng là nhãn thật, cột là nhãn dự đoán (đúng như notebook Week 2: 'C_ij = số quan sát thuộc nhóm i được dự đoán vào nhóm j')."),
  ("The printed error rate is 0.4.", T,
   "Sai = 2 (FP) + 2 (FN) = 4 trong 10 ⇒ 0.4 (cũng chính là cm[0,1]+cm[1,0] chia 10)."),
  ("The observation with probability exactly 0.50 is classified as class 1 by the first rule.", F,
   "Luật là <code>prob &gt; 0.5</code> (strict) ⇒ 0.50 bị xếp vào class 0. Đó là lý do pred = [0 0 0 0 1 1 0 0 1 1]."),
  ("Replacing <code>&gt;</code> by <code>&gt;=</code> raises the recall of class 1 to 0.75.", T,
   "Điểm 0.50 (true = 1) chuyển thành dự đoán 1 ⇒ TP từ 2 lên 3 ⇒ recall = 3/4 = 0.75 (dòng in cuối)."),
 ], key_note="Đáp án: A, C, E"),

# ---------------------------------------------------------------- W3
dict(id='A4', week='Week 3 · Non-linear methods (polynomials & splines)', code='A4',
 stem='Which statements about the printed output are correct?',
 options=[
  ("The first printed array is [[1. 2. 3. 4. 6. 9.]].", T,
   "Với [a,b]=[2,3], degree 2 (có bias): 1, a, b, a², ab, b² = 1, 2, 3, 4, 6, 9."),
  ("With <code>interaction_only=True, include_bias=False</code> the output is [[2. 3. 4. 9.]].", F,
   "<code>interaction_only</code> bỏ các luỹ thừa (a², b²) và giữ tích chéo: [a, b, ab] = [[2. 3. 6.]]."),
  ("<code>bs(x, df=6, degree=3)</code> gives 7 columns because <code>dmatrix</code> adds an intercept column to the 6 basis functions.", T,
   "<code>df</code> = số hàm cơ sở (không tính intercept) = 6; patsy thêm cột hằng ⇒ (11, 7)."),
  ("<code>bs(x, knots=(3, 6), degree=3)</code> gives 6 columns: an intercept plus degree + #knots = 5 basis functions.", T,
   "df = degree + số knots (khi không include_intercept) = 3 + 2 = 5, cộng intercept = 6 ⇒ (11, 6)."),
  ("A cubic regression spline with two knots needs 12 free coefficients, so the design matrix would have 12 columns.", F,
   "3 đoạn cubic × 4 hệ số = 12 trước ràng buộc; 3 ràng buộc liên tục (hàm, đạo hàm 1, đạo hàm 2) × 2 knots = 6 ràng buộc ⇒ 12 − 6 = <b>6</b> bậc tự do."),
 ], key_note="Đáp án: A, C, D"),

# ---------------------------------------------------------------- W4
dict(id='A5', week='Week 4 · Support vector machines', code='A5', show_output=True,
 stem='The code was run and printed the three lines shown. Which statements are supported by the code and its output?',
 options=[
  ("For C = 0.001 the classifier uses 176 support vectors in total.", T,
   "<code>n_support_</code> = số support vector <b>theo từng class</b> = [88, 88] ⇒ 176 trên tổng 200 điểm (gần như mọi điểm nằm trong/ trên margin)."),
  ("Increasing C from 0.001 to 100 reduces the number of support vectors, while the training accuracy barely changes.", T,
   "88+88 → 29+28 → 24+24; accuracy 0.92 / 0.915 / 0.92."),
  ("With C = 100 no training point violates the margin, because the two classes are separable.", F,
   "Accuracy = 0.92 &lt; 1 ⇒ dữ liệu <b>không</b> tách tuyến tính (hai blob chồng lên nhau, std = 1.5). Vẫn còn điểm vi phạm margin/bị phân sai dù C lớn."),
  ("C penalises margin violations: a small C tolerates many violations, producing a wider margin.", T,
   "C là hệ số phạt slack; C nhỏ ⇒ chấp nhận nhiều vi phạm ⇒ margin rộng ⇒ nhiều support vector."),
  ("<code>m.score(X, y)</code> reports the test accuracy.", F,
   "Nó được gọi trên chính (X, y) dùng để fit ⇒ là <b>training</b> accuracy."),
 ], key_note="Đáp án: A, B, D"),

# ---------------------------------------------------------------- W5
dict(id='A6', week='Week 5 · Neural networks (CNN shapes)', code='A6',
 stem='Which statements are correct?',
 options=[
  ("<code>h.shape</code> is (8, 16, 32, 32) because ⌊(64 + 2·2 − 5)/2⌋ + 1 = 32.", T,
   "H_out = ⌊(H_in + 2p − k)/s⌋ + 1 = ⌊63/2⌋ + 1 = 31 + 1 = 32; số kênh = 16 filters."),
  ("With stride 1 instead of 2, the output of <code>conv</code> would be (8, 16, 64, 64).", T,
   "(64 + 4 − 5)/1 + 1 = 64: padding 2 với kernel 5 là 'same padding'."),
  ("The last printed value is 1200 because a <code>Conv2d</code> layer has no bias term by default.", F,
   "<code>bias=True</code> theo mặc định: 16 × (3·5·5) = 1200 weights <b>+ 16 biases = 1216</b> (giá trị in ra)."),
  ("<code>nn.Flatten()(p)</code> has 4096 features, so a following <code>nn.Linear(4096, 10)</code> would add 40,970 parameters.", T,
   "16·16·16 = 4096 (shape (8, 4096)); Linear: 4096·10 + 10 = 40 970."),
  ("<code>gap(p)</code> keeps the 16 × 16 spatial grid, so its shape is (8, 16, 16, 16).", F,
   "<code>AdaptiveAvgPool2d(1)</code> trung bình mỗi kênh về 1×1 ⇒ (8, 16, 1, 1)."),
 ], key_note="Đáp án: A, B, D"),

dict(id='A7', week='Week 5 · Neural networks (training mechanics)', code='A7',
 stem='Which statements are correct?',
 options=[
  ("The first printed line is <code>tensor([72.])</code>, because gradients accumulate across the two <code>backward()</code> calls.", T,
   "loss = 9w² ⇒ dloss/dw = 18w = 36 tại w = 2. PyTorch <b>cộng dồn</b> vào <code>.grad</code>: 36 + 36 = 72. Đây là lý do cần <code>optimizer.zero_grad()</code> mỗi iteration."),
  ("After <code>w.grad.zero_()</code> a single backward pass gives 36.", T,
   "Reset về 0 rồi cộng 36 ⇒ tensor([36.])."),
  ("<code>loss.backward()</code> updates <code>w</code> to <code>w − lr·grad</code>.", F,
   "<code>backward()</code> chỉ <b>tính</b> gradient. Việc cập nhật tham số do <code>optimizer.step()</code> thực hiện."),
  ("<code>CrossEntropyLoss</code> expects raw logits; for logits [2, 0] and target 0 it prints 0.127 = log(1 + e<sup>−2</sup>).", T,
   "CE = −log softmax(logits)[0] = −log(e²/(e²+1)) = log(1 + e<sup>−2</sup>) = 0.127."),
  ("Feeding <code>torch.softmax(logits)</code> into <code>CrossEntropyLoss</code> is harmless; it returns the same loss.", F,
   "CrossEntropyLoss đã gồm log-softmax; áp softmax 2 lần làm logits bị nén về [0.88, 0.12] ⇒ loss = 0.383 ≠ 0.127 (sai và gradient yếu đi)."),
 ], key_note="Đáp án: A, B, D"),

dict(id='A8', week='Week 5 · Transformers (attention)', code='A8',
 stem='Which statements are correct?',
 options=[
  ("Every row of the attention-weight matrix <code>w</code> sums to 1.", T,
   "softmax theo <code>dim=-1</code> chuẩn hoá từng hàng ⇒ in ra tensor([1., 1.])."),
  ("<code>w @ V</code> returns <code>V</code> unchanged.", F,
   "V = I nên <code>w @ V = w</code> = [[0.67, 0.33], [0.33, 0.67]], không phải V = I. Mỗi hàng output là trung bình có trọng số của các hàng V."),
  ("In <code>w2</code>, row 1 is [1, 0] because the blocked position receives −∞ before the softmax.", T,
   "<code>masked_fill(mask == 0, -inf)</code> ⇒ e<sup>−∞</sup> = 0 ⇒ toàn bộ xác suất dồn vào vị trí cho phép (kiểu causal mask)."),
  ("Dividing by √d<sub>k</sub> makes the scores larger, which sharpens the softmax.", F,
   "Chia cho √d<sub>k</sub> làm scores <b>nhỏ đi</b> (1 → 0.707) để softmax không bão hoà khi d<sub>k</sub> lớn. Không scale thì hàng 1 sẽ là [0.731, 0.269] thay vì [0.67, 0.33]."),
  ("Row 2 of <code>w2</code> is identical to row 2 of <code>w</code>, because position 2 may attend to both positions.", T,
   "mask hàng 2 = [1, 1] ⇒ không chặn gì ⇒ [0.33, 0.67] như cũ."),
 ], key_note="Đáp án: A, C, E"),

# ---------------------------------------------------------------- W6
dict(id='A9', week='Week 6 · K-means clustering', code='A9',
 stem='Which statements about the printed output are correct?',
 options=[
  ("The two cluster centres are 2 and 11.", T,
   "Hai nhóm {1,2,3} và {10,11,12}; centroid = mean ⇒ 2 và 11."),
  ("<code>inertia_</code> = 4.0 is the sum of squared distances of the points to their own centre.", T,
   "(1−2)²+(2−2)²+(3−2)² = 2, tương tự nhóm 2 = 2 ⇒ 4.0."),
  ("The new point x = 6 is assigned to the cluster whose centre is 11.", F,
   "|6−2| = 4 &lt; |6−11| = 5 ⇒ gán vào cụm tâm 2, cùng cụm với <code>X[0]</code>, vì thế dòng in ra là [ True ]."),
  ("With K = 3 the inertia drops to 2.5, so inertia alone can never be used to pick K.", T,
   "K = 3: {1,2,3} → 2, {10,11} → 0.5, {12} → 0 ⇒ 2.5. Inertia luôn giảm khi K tăng (K = n ⇒ 0) nên phải dùng elbow/silhouette, không chọn K nhỏ nhất theo inertia."),
  ("Using <code>n_init=10</code> guarantees that the globally optimal partition is found.", F,
   "K-means chỉ hội tụ tới <b>local optimum</b>; n_init chạy nhiều lần khởi tạo và giữ nghiệm tốt nhất, giảm rủi ro nhưng không đảm bảo."),
 ], key_note="Đáp án: A, B, D"),

dict(id='A10', week='Week 6 · Hierarchical clustering (scipy)', code='A10',
 stem='Which statements about the printed output are correct?',
 options=[
  ("<code>linkage</code> receives the condensed distance vector (10 = 5·4/2 entries), which is the correct input type.", T,
   "<code>pdist</code> trả về vector rút gọn độ dài n(n−1)/2 = 10; đây là định dạng dissimilarity mà <code>linkage</code> chấp nhận (hoặc truyền thẳng ma trận quan sát X)."),
  ("Passing <code>squareform(d)</code> (a 5 × 5 matrix) to <code>linkage</code> would give the same <code>Z</code>.", F,
   "Ma trận vuông bị hiểu là <b>5 quan sát với 5 đặc trưng</b> (cụm hoá các hàng của ma trận khoảng cách) ⇒ kết quả khác, kèm ClusterWarning. Đây chính là bug trong bài Week 7 của môn."),
  ("In the single-linkage tree the last merge joins observation 4 (x = 12) to the other four points at height 5.", T,
   "Hàng cuối của Z: [4, 7, 5, 5] ⇒ obs 4 hợp với cụm 7 ở độ cao 5 (khoảng cách nhỏ nhất 12−7 = 5), cụm mới có 5 phần tử."),
  ("The final merge height of complete linkage is 12, the largest distance between a point of {0, 1, 3} and a point of {7, 12}.", T,
   "<code>Zc[:, 2] = [1, 3, 5, 12]</code>. Complete linkage dùng khoảng cách <b>lớn nhất</b> giữa hai cụm: 12 − 0 = 12."),
  ("Cutting both trees into two clusters gives the same partition.", F,
   "Single: [1 1 1 1 2] (điểm 12 đứng riêng, hiệu ứng chaining); complete: [1 1 1 2 2] ({7, 12} thành một cụm)."),
 ], key_note="Đáp án: A, C, D"),

# ---------------------------------------------------------------- W7
dict(id='A11', week='Week 7 · Dimension reduction (PCA & t-SNE)', code='A11',
 stem='Which statements about the printed output are correct?',
 options=[
  ("The first principal component explains 80% of the variance, because the variance of column 1 (8/3) is four times that of column 2 (2/3).", T,
   "Cột 1 chứa ±2 (tổng bình phương 8, chia n−1 = 3), cột 2 chứa ±1 (tổng 2). Hai cột không tương quan nên các PC trùng trục toạ độ ⇒ tỉ lệ 0.8 / 0.2."),
  ("After <code>StandardScaler</code> the two components explain 50% each.", T,
   "Sau chuẩn hoá hai cột có cùng phương sai, vẫn không tương quan ⇒ [0.5, 0.5]. PCA <b>phụ thuộc scale</b>, vì vậy phải scale khi các biến khác đơn vị."),
  ("<code>PCA(n_components=0.75)</code> keeps one component.", T,
   "Với số thực trong (0,1), sklearn giữ số PC nhỏ nhất sao cho cumulative explained variance ≥ 0.75; PC1 đã có 0.8 ⇒ 1."),
  ("The fitted <code>TSNE</code> object can project new observations through <code>transform</code>.", F,
   "In ra False: t-SNE chỉ có <code>fit_transform</code> (không có phép chiếu cố định cho điểm mới); PCA mới có <code>transform</code>."),
  ("<code>pca.components_</code> has one row per principal component and one column per original feature.", T,
   "Shape (n_components, n_features); ở đây (2, 2) nên cả hai chiều trùng nhau, nhưng quy ước là hàng = PC (loading vector)."),
 ], key_note="Đáp án: A, B, C, E"),

# ---------------------------------------------------------------- W8
dict(id='A12', week='Week 8 · Bayesian networks (d-separation)', code='A12',
 stem='The network is the Student network: D → G ← I, I → S, G → L. Which statements are correct?',
 options=[
  ("<code>D</code> and <code>I</code> are d-connected when nothing is observed (first printed value).", F,
   "In ra False: đường D → G ← I có G là <b>collider</b> chưa quan sát ⇒ bị chặn ⇒ D ⟂ I."),
  ("Observing <code>L</code> makes <code>D</code> and <code>I</code> d-connected again.", T,
   "L là hậu duệ của collider G; quan sát hậu duệ của collider cũng 'mở' đường (explaining away) ⇒ True."),
  ("<code>D</code> and <code>S</code> are d-connected given <code>G</code>.", T,
   "Đường D → G ← I → S: G là collider và được quan sát ⇒ mở; I là non-collider chưa quan sát ⇒ không chặn ⇒ True."),
  ("<code>L</code> and <code>S</code> are d-connected given <code>G</code>.", F,
   "Đường duy nhất L ← G ← I → S đi qua G (chuỗi, không phải collider) mà G đã quan sát ⇒ bị chặn ⇒ False."),
  ("The Markov blanket of <code>G</code> is {D, I, L}.", T,
   "Markov blanket = cha (D, I) + con (L) + cha khác của các con (L không có cha nào khác) ⇒ ['D','I','L']."),
 ], key_note="Đáp án: B, C, E"),

dict(id='A13', week='Week 8 · Bayesian networks (CPDs & factorisation)', code='A13',
 stem='Which statements are correct?',
 options=[
  ("<code>check_model()</code> printing True means the CPDs are consistent with the graph (correct cardinalities, columns sum to 1).", T,
   "pgmpy kiểm tra mỗi CPD có đúng biến cha như cạnh trong graph, và mỗi cột tổng bằng 1; sai thì ném ValueError."),
  ("0.0399 equals P(D=hard)·P(I=low)·P(G=B | I=low, D=hard)·P(S=weak | I=low)·P(L=strong | G=B).", T,
   "0.4 × 0.7 × 0.25 × 0.95 × 0.6 = 0.0399 (chain rule theo cấu trúc mạng). Cột thứ 2 của bảng G là (I=low, D=hard) vì <code>evidence=['I','D']</code> và biến cuối (D) đổi nhanh nhất ⇒ [0.05, 0.25, 0.70]."),
  ("The network has 15 independent parameters, against 47 for an unrestricted joint table.", T,
   "D: 1; I: 1; G: (3−1)·4 = 8; S: (2−1)·2 = 2; L: (2−1)·3 = 3 ⇒ 15. Bảng joint 2·2·3·2·2 = 48 ô ⇒ 47 tham số tự do. Đây là lợi ích của factorisation."),
  ("The CPD of G contributes 12 free parameters (3 states × 4 parent configurations).", F,
   "12 là số <b>ô</b> của bảng; do mỗi cột phải có tổng 1 nên chỉ có (3−1)×4 = <b>8</b> tham số tự do."),
  ("The two numbers 15 and 47 are equal as long as the CPDs are valid probabilities.", F,
   "15 ≠ 47; chúng chỉ bằng nhau nếu đồ thị đầy đủ (không có độc lập có điều kiện)."),
 ], key_note="Đáp án: A, B, C"),

# ---------------------------------------------------------------- W9
dict(id='A14', week='Week 9 · Markov networks (factors)', code='A14',
 stem='Which statements about the printed output are correct?',
 options=[
  ("<code>psi = phi1 * phi2</code> has scope ['A', 'B', 'C'] and 8 entries.", T,
   "Tích factor: ψ(a,b,c) = φ₁(a,b)·φ₂(b,c), scope là hợp của hai scope, shape (2,2,2)."),
  ("<code>tau</code> was obtained by summing out A.", F,
   "<code>tau.scope()</code> = ['A','C'] ⇒ biến bị <b>marginalize là B</b>."),
  ("24.0 is the partition function Z of the Markov network A − B − C with these two factors.", T,
   "Z = Σ<sub>a,b,c</sub> φ₁φ₂ = 7+5+5+7 = 24; giá trị chưa chuẩn hoá nên không phải xác suất."),
  ("After <code>tau.normalize()</code> the entry for (A=0, C=0) equals 7/12.", F,
   "Chuẩn hoá chia cho tổng 24: 7/24 = 0.292 (in ra [[0.292 0.208],[0.208 0.292]])."),
  ("The last line shows φ₁(A=0, B=0) and φ₁(A=0, B=1).", T,
   "<code>reduce([('A',0)])</code> cố định A = 0 và giữ lại bảng theo B: [φ₁(0,0), φ₁(0,1)] = [3, 1]."),
 ], key_note="Đáp án: A, C, E"),

# ---------------------------------------------------------------- W10
dict(id='A15', week='Week 10 · Exact inference (variable elimination)', code='A15',
 stem='The factors are the scopes of the factors of a Markov network. Which statements about the printed output are correct?',
 options=[
  ("With order A, B, C, D, E the largest intermediate factor has 3 variables; with B, D, A, C, E it has 4.", T,
   "Order 1: ψ có scope {A,B}, {B,C,D}, {C,D}, {D,E}, {E} ⇒ [2,3,2,2,1]. Order 2: {A,B,C,D}, {A,C,D,E}, ... ⇒ [4,4,3,2,1]."),
  ("The cost of variable elimination grows exponentially with the size of the largest intermediate scope, so order A, B, C, D, E is cheaper.", T,
   "Bảng ψ có k<sup>|scope|</sup> ô (k = số trạng thái). 3 &lt; 4 biến ⇒ thứ tự thứ nhất rẻ hơn."),
  ("The marginal probability computed by variable elimination depends on the elimination order.", F,
   "Kết quả <b>không đổi</b> (phép cộng/nhân có tính hoán vị và kết hợp); chỉ chi phí thay đổi."),
  ("Finding the elimination order with the smallest induced width is easy (polynomial time).", F,
   "Tìm thứ tự tối ưu là NP-khó ⇒ dùng heuristic (MinFill, MinNeighbors, MinWeight… như notebook Week 10)."),
  ("In order A, B, C, D, E eliminating B creates a new factor over {C, D}.", T,
   "Loại B: gộp {B} (từ bước A), {B,C}, {B,D} ⇒ scope {B,C,D} (3 biến); sau khi sum-out còn τ(C,D)."),
 ], key_note="Đáp án: A, B, E"),

# ---------------------------------------------------------------- W12
dict(id='A16', week='Week 12 · Structure learning (I-equivalence)', code='A16',
 stem='Which statements about the code and its output are correct?',
 options=[
  ("G1 (X → Y → Z) and G2 (Z → Y → X) are I-equivalent.", T,
   "Cùng skeleton X − Y − Z và đều 0 immorality ⇒ I-equivalent (cùng X ⟂ Z | Y)."),
  ("G3 (X → Y ← Z) is not I-equivalent to G1, because it has an immorality (v-structure) that G1 does not have.", T,
   "G3 có 1 immorality X → Y ← Z với X, Z không kề nhau (X ⟂ Z nhưng X ⟂̸ Z | Y)."),
  ("G1 and G4 (X ← Y → Z) are I-equivalent.", T,
   "Common cause: cùng skeleton và 0 immorality ⇒ True (dòng in cuối: True False True)."),
  ("Two DAGs with the same skeleton are always I-equivalent.", F,
   "Định lý: I-equivalent ⇔ cùng skeleton <b>và</b> cùng tập immorality. G1 và G3 có cùng skeleton nhưng khác immorality."),
  ("All four graphs imply X ⟂ Z | Y.", F,
   "G3 thì ngược lại: conditioning vào collider Y làm X và Z <b>phụ thuộc</b>."),
 ], key_note="Đáp án: A, B, C"),
]

# ============================================================== SHORT ANSWER
SA = [
dict(id='B1', week='Week 2 · Regularisation (Lasso vs Ridge)', marks=6, code='B1',
 stem='The 8×5 matrix <code>X</code> consists of five mutually orthogonal ±1 columns, so XᵀX = 8I. The data contain no noise. State the exact output of the code, using the facts that scikit-learn minimises (1/2n)‖y − Xw‖² + α‖w‖₁ for Lasso and ‖y − Xw‖² + α‖w‖² for Ridge.',
 parts=[
  ("(a) What is printed on the first line (OLS)? Why?", 1),
  ("(b) Give the three Lasso coefficient vectors printed for α = 0.5, 1.5, 3.5, showing the formula you use.", 2),
  ("(c) Give the Ridge vector for α = 8 and state how many coefficients are exactly zero in each of the four fitted models (three Lasso, one Ridge).", 2),
  ("(d) Would Ridge with a very large α set the last coefficient exactly to zero? Explain.", 1),
 ],
 sol="""
<p><b>(a)</b> Dữ liệu không nhiễu và y = Xβ ⇒ OLS khôi phục đúng β = <code>[ 4. -3. 2. 1. 0.5]</code>. (1 điểm)</p>
<p><b>(b)</b> Vì XᵀX/n = I (n = 8) nên bài toán Lasso <b>tách theo từng hệ số</b>: ŵ<sub>j</sub> = sign(β<sub>j</sub>)·max(|β<sub>j</sub>| − α, 0) (soft-thresholding). (1 điểm công thức + 1 điểm kết quả)</p>
<table><tr><th>α</th><th>ŵ</th><th># zeros</th></tr>
<tr><td>0.5</td><td>[3.5, −2.5, 1.5, 0.5, 0]</td><td>1 (|0.5| − 0.5 = 0)</td></tr>
<tr><td>1.5</td><td>[2.5, −1.5, 0.5, 0, 0]</td><td>2</td></tr>
<tr><td>3.5</td><td>[0.5, 0, 0, 0, 0]</td><td>4 (chỉ |4| &gt; 3.5)</td></tr></table>
<p><b>(c)</b> Ridge: ŵ = (XᵀX + αI)<sup>−1</sup>Xᵀy = β·8/(8+α) = 0.5β ⇒ <code>[ 2. -1.5 1. 0.5 0.25]</code>, <b>0 hệ số bằng 0</b>. (1 điểm giá trị + 1 điểm số lượng zeros: 1, 2, 4 cho Lasso và 0 cho Ridge)</p>
<p><b>(d)</b> Không. Ridge chỉ <b>co đều</b> mọi hệ số theo hệ số 8/(8+α) &gt; 0 với mọi α hữu hạn, nên hệ số khác 0 vẫn khác 0 (chỉ tiến dần về 0 khi α → ∞). Chỉ phạt L1 (có điểm gãy tại 0) mới cho nghiệm thưa chính xác ⇒ Lasso dùng để chọn biến. (1 điểm)</p>"""),

dict(id='B2', week='Week 3 · Regression splines (degree 0)', marks=4, code='B2',
 stem='<code>bs(x, knots=(5, 7), degree=0)</code> builds a piecewise-constant basis. Predict the output of the code. No point of <code>df</code> lies exactly at a knot.',
 parts=[
  ("(a) How many columns does the design matrix have and what do they encode?", 1),
  ("(b) What is printed on the first line (the fitted coefficients)?", 1),
  ("(c) What are the second and third lines?", 1),
  ("(d) Compute the value printed on the last line.", 1),
 ],
 sol="""
<p><b>(a)</b> 3 cột: intercept + 2 chỉ báo vùng. 2 knots chia trục x thành 3 vùng {x&lt;5}, {5≤x&lt;7}, {x≥7}; patsy bỏ chỉ báo của vùng đầu vì đã có intercept (tránh đa cộng tuyến hoàn hảo). Do đó df_model = 3 − 1 = 2. (1 điểm)</p>
<p><b>(b)</b> Với hàm bậc 0, OLS cho <b>trung bình theo vùng</b>:
vùng 1 (x = 1,2,3,4): y = 2,4,3,3 ⇒ 3.0; vùng 2 (6, 6.5): 8, 9 ⇒ 8.5; vùng 3 (8, 9, 10): 5, 7, 6 ⇒ 6.0.
Hệ số: intercept = 3.0 (vùng cơ sở), tiếp theo là <i>chênh lệch</i> so với vùng cơ sở: 8.5 − 3 = 5.5 và 6 − 3 = 3.0 ⇒ <code>[3.0, 5.5, 3.0]</code>. (1 điểm)</p>
<p><b>(c)</b> x = 2.5 ∈ vùng 1 ⇒ 3.0; x = 6.2 ∈ vùng 2 ⇒ 8.5; x = 9.5 ∈ vùng 3 ⇒ 6.0 ⇒ <code>[3.0, 8.5, 6.0]</code>. Dòng tiếp theo là <code>m.df_model = 2.0</code>. (1 điểm)</p>
<p><b>(d)</b> RSS = tổng bình phương sai lệch khỏi mean từng vùng: vùng 1: (−1)²+1²+0+0 = 2; vùng 2: 0.5²+0.5² = 0.5; vùng 3: (−1)²+1²+0 = 2 ⇒ <b>4.5</b>. (1 điểm)</p>"""),

dict(id='B3', week='Week 4 · Support vector machine', marks=5, code='B3',
 stem='The seven observations are those of the Week 4 sample question (4 red, 3 blue). <code>C = 1e6</code> makes the fit effectively a hard-margin classifier. Predict the output.',
 parts=[
  ("(a) What does <code>classes_</code> print, and which class has a positive decision function?", 1),
  ("(b) Give <code>n_support_</code> and the sorted <code>support_</code> list, and identify the support vectors.", 1),
  ("(c) Give <code>coef_</code> and <code>intercept_</code>, write the separating hyperplane, and state the margin width.", 2),
  ("(d) Give the two predicted classes and the decision-function value of the point (3, 2).", 1),
 ],
 sol="""
<p><b>(a)</b> <code>['blue' 'red']</code> (sắp xếp theo alphabet). <code>decision_function &gt; 0</code> ứng với <code>classes_[1]</code> = <b>red</b>; &lt; 0 ứng với blue. (1 điểm)</p>
<p><b>(b)</b> <code>n_support_ = [2 2]</code> (2 blue, 2 red). Chỉ số (0-based) <code>[1, 2, 4, 5]</code> ⇒ các quan sát 2, 3, 5, 6 trong đề: (2,2), (4,4) màu đỏ và (2,1), (4,3) màu xanh. Các điểm (3,4), (1,4), (4,1) nằm xa margin ⇒ dịch chuyển nhẹ không đổi siêu phẳng (đúng như ý Q2(f) của đề mẫu). (1 điểm)</p>
<p><b>(c)</b> Trên support vector: w·x + b = +1 (đỏ) và −1 (xanh). Giải: w = (−2, 2), b = 1 ⇒ <code>[[-2. 2.]] [1.]</code>. Siêu phẳng −2X₁ + 2X₂ + 1 = 0 ⇔ X₁ − X₂ − 0.5 = 0 (đường X₂ = X₁ − 0.5). Margin (độ rộng toàn phần) = 2/‖w‖ = 2/(2√2) = 0.707. Kiểm tra: (2,2): −4+4+1 = +1 ✓; (2,1): −4+2+1 = −1 ✓; (4,3): −8+6+1 = −1 ✓. (2 điểm)</p>
<p><b>(d)</b> (3,1): −6+2+1 = −3 &lt; 0 ⇒ blue; (1,1): −2+2+1 = +1 &gt; 0 ⇒ red ⇒ <code>['blue' 'red']</code>. (3,2): −6+4+1 = <b>−1.0</b> — nằm đúng trên ranh giới margin phía blue. (1 điểm)</p>"""),

dict(id='B4', week='Week 5 · Neural network forward & backward pass', marks=7, code='B4',
 stem='A network with 2 inputs, 3 ReLU hidden units and 2 softmax outputs is trained on one example with the cross-entropy loss. Predict every printed line (rounded as shown).',
 parts=[
  ("(a) First line: u, h, z.", 2),
  ("(b) Second line: probabilities, loss, predicted class; is the example classified correctly?", 2),
  ("(c) The two gradient matrices dW2 and dW1. Which row of dW1 is zero and why?", 2),
  ("(d) The last line (number of parameters).", 1),
 ],
 sol="""
<p><b>(a)</b> u = W₁x + b₁: u₁ = 0.5·1 − 1·2 + 0 = −1.5; u₂ = 1·1 + 0.5·2 − 1 = 1.0; u₃ = −0.5 + 2 + 0.5 = 2.0 ⇒ <code>[-1.5 1. 2.]</code>.
h = ReLU(u) = <code>[0. 1. 2.]</code>. z = W₂h + b₂: z₁ = 0 + 0.5 − 2 + 0 = −1.5; z₂ = 0 + 2 + 2 + 0.5 = 4.5 ⇒ <code>[-1.5 4.5]</code>. (2 điểm)</p>
<p><b>(b)</b> softmax: p = [1/(1+e⁶), e⁶/(1+e⁶)] = <code>[0.002 0.998]</code> (0.00247, 0.99753). Nhãn y = [1, 0] ⇒ loss = −ln(0.00247) = ln(1+e⁶) = <b>6.002</b>. <code>argmax(p) = 1</code> trong khi nhãn thật là lớp 0 ⇒ <b>phân loại sai</b> (loss lớn). (2 điểm)</p>
<p><b>(c)</b> Gradient tại logits: dz = p − y = [−0.9975, +0.9975].
dW₂ = dz hᵀ = [[0, −0.998, −1.995], [0, 0.998, 1.995]] (cột đầu = 0 vì h₁ = 0).
Lan truyền ngược: dh = W₂ᵀdz = [−1.995, 1.496, 1.995]; du = dh ⊙ 1[u &gt; 0] = [0, 1.496, 1.995] (ReLU'(−1.5) = 0).
dW₁ = du xᵀ = [[0, 0], [1.496, 2.993], [1.995, 3.990]]. <b>Hàng 1 của dW₁ bằng 0</b> vì unit 1 có u₁ = −1.5 &lt; 0 ⇒ ReLU đạo hàm 0 ('dead' với mẫu này) nên các trọng số vào unit đó không nhận gradient. (2 điểm)</p>
<p><b>(d)</b> W₁ (3×2) = 6, b₁ = 3, W₂ (2×3) = 6, b₂ = 2 ⇒ <b>17</b>. (1 điểm)</p>"""),

dict(id='B5', week='Week 6 · Hierarchical clustering (average linkage)', marks=5, code='B5',
 stem='Perform the computation by hand and predict the output.',
 parts=[
  ("(a) Reproduce the four rows of Z (children, height, size). Show the updated dissimilarities you use.", 3),
  ("(b) Give the partition printed by <code>fcluster(Z, t=2, criterion='maxclust')</code>.", 1),
  ("(c) Give the partition printed with <code>t=3.0, criterion='distance'</code>.", 1),
 ],
 sol="""
<p><b>(a)</b> Average linkage: d(A,B) = trung bình mọi cặp giữa hai cụm.</p>
<ul><li>Gần nhất: d(0,1) = 2 ⇒ hợp {0,1} (id 5), height 2, size 2. Hàng 1: <code>[0, 1, 2, 2]</code>.</li>
<li>d(5,2) = (6+5)/2 = 5.5; d(5,3) = (10+9)/2 = 9.5; d(5,4) = (9+8)/2 = 8.5. Các cặp còn lại: d(2,3) = 4, d(2,4) = 5, <b>d(3,4) = 3</b> ⇒ hợp {3,4} (id 6) ở height 3. Hàng 2: <code>[3, 4, 3, 2]</code>.</li>
<li>d(5,6) = (10+9+9+8)/4 = 9; d(2,6) = (4+5)/2 = <b>4.5</b>; d(5,2) = 5.5 ⇒ hợp {2} với {3,4} (id 7) ở 4.5. Hàng 3: <code>[2, 6, 4.5, 3]</code>.</li>
<li>d(5,7) = (6+10+9+5+9+8)/6 = 47/6 = 7.83 ⇒ hàng 4: <code>[5, 7, 7.83, 5]</code>.</li></ul>
<p>(0.5 điểm mỗi bước hợp + 1 điểm cho các khoảng cách cập nhật)</p>
<p><b>(b)</b> Cắt thành 2 cụm = bỏ phép hợp cuối ⇒ {0,1} và {2,3,4}: <code>[1 1 2 2 2]</code>. (1 điểm)</p>
<p><b>(c)</b> Chỉ giữ các phép hợp có height ≤ 3: (0,1)@2 và (3,4)@3 ⇒ 3 cụm {0,1}, {2}, {3,4}: <code>[1 1 3 2 2]</code> (số nhãn tuỳ ý, cần đúng cách chia). (1 điểm)</p>
<p><i>Lưu ý:</i> code dùng <code>squareform(D)</code> để đưa ma trận vuông về dạng condensed; nếu đưa thẳng D vào <code>linkage</code> thì D bị coi là dữ liệu 5 chiều và kết quả sai.</p>"""),

dict(id='B6', week='Week 7 · PCA from first principles', marks=4, code='B6',
 stem='Predict the output of the code.',
 parts=[
  ("(a) The eigenvalues printed on the first line.", 1),
  ("(b) The explained-variance ratios.", 1),
  ("(c) The absolute scores on PC1.", 1),
  ("(d) The reconstruction error on the last line. How is it related to the eigenvalues? What would change if the lines that sort <code>vals</code> were deleted?", 1),
 ],
 sol="""
<p>Xc = X (mean 0). S = XᵀX/3 = [[10/3, −2], [−2, 10/3]].</p>
<p><b>(a)</b> Eigenvalue = 10/3 ± 2 ⇒ <code>[5.333 1.333]</code> (eigenvector (1,−1)/√2 và (1,1)/√2). (1 điểm)</p>
<p><b>(b)</b> 5.333/6.667 = 0.8 và 0.2 ⇒ <code>[0.8 0.2]</code>. (1 điểm)</p>
<p><b>(c)</b> Score trên PC1 = (x₁ − x₂)/√2: (1,1) → 0; (−1,−1) → 0; (2,−2) → 4/√2 = 2.828; (−2,2) → −2.828 ⇒ |scores| = <code>[0. 0. 2.828 2.828]</code>. (1 điểm)</p>
<p><b>(d)</b> Sai số tái tạo 1 PC = phần phương sai của PC2 = (n−1)·λ₂ = 3 × 1.333 = <b>4.0</b> (tổng bình phương score PC2: 1.414²·2 = 4).
Nếu bỏ phần sắp xếp, vì <code>np.linalg.eigh</code> trả eigenvalue theo thứ tự <b>tăng dần</b>, <code>vecs[:, 0]</code> sẽ là PC2 ⇒ scores = [1.414, 1.414, 0, 0] và sai số tái tạo = 3·5.333 = 16. (1 điểm)</p>"""),

dict(id='B7', week='Week 8 · Bayesian network inference (pgmpy)', marks=6, code='B7',
 stem='The network is the "cancer" network: Pollution, Smoker → Cancer → Xray, Dyspnoea. State orders: Pollution [low, high]; Smoker, Cancer and Dyspnoea [T, F]; Xray [pos, neg]. Predict the printed output.',
 parts=[
  ("(a) Line 1 (q1): P(Cancer | Smoker=T, Pollution=high).", 1),
  ("(b) Line 2 (q2): show the Bayes calculation.", 2),
  ("(c) Line 3 (q3): P(Cancer | Xray=pos). Compare with the prior P(Cancer=T) and comment.", 1),
  ("(d) Line 4 (q4): the 2×2 table, and the independence it reveals.", 1),
  ("(e) The last line (two booleans) and its meaning.", 1),
 ],
 sol="""
<p><b>(a)</b> Cancer có cha là Smoker, Pollution; bảng CPD: P(Cancer=T | S=T, P=high) = <b>0.05</b> ⇒ <code>['T','F'] [0.05 0.95]</code>. (1 điểm)</p>
<p><b>(b)</b> Evidence gồm tất cả các nút ngoài Cancer ⇒ theo Bayes, các nhân tử không chứa Cancer triệt tiêu:
P(C=T | e) ∝ P(C=T | S=T,P=high)·P(Xray=pos | C=T)·P(Dysp=T | C=T) = 0.05 × 0.9 × 0.65 = 0.02925;
P(C=F | e) ∝ 0.95 × 0.2 × 0.3 = 0.0570. Chuẩn hoá: 0.02925/0.08625 = <b>0.3391</b> ⇒ <code>[0.3391 0.6609]</code>. (2 điểm)</p>
<p><b>(c)</b> Prior: P(C=T) = Σ P(S)P(P)P(C|S,P) = 0.3·0.9·0.03 + 0.3·0.1·0.05 + 0.7·0.9·0.001 + 0.7·0.1·0.02 = 0.01163.
Posterior: 0.01163·0.9 / (0.01163·0.9 + 0.98837·0.2) = 0.010467/0.208141 = <b>0.0503</b> ⇒ <code>[0.0503 0.9497]</code>. X-quang dương làm xác suất ung thư tăng ~4.3 lần (0.0116 → 0.0503) nhưng vẫn thấp vì prior rất nhỏ và X-quang có false-positive 20%. (1 điểm)</p>
<p><b>(d)</b> Cho Cancer = T, Xray ⟂ Dyspnoea (hai con của cùng một cha, common cause) nên bảng = tích hai CPD: hàng Xray [pos, neg] × cột Dysp [T, F]: 0.9·0.65 = 0.585; 0.9·0.35 = 0.315; 0.1·0.65 = 0.065; 0.1·0.35 = 0.035 ⇒ <code>[[0.585 0.315] [0.065 0.035]]</code>. (1 điểm)</p>
<p><b>(e)</b> <code>True False</code>: Xray và Dyspnoea d-connected khi chưa quan sát gì (đường Xray ← Cancer → Dyspnoea mở), nhưng bị chặn khi Cancer được quan sát (non-collider đã quan sát) ⇒ Xray ⟂ Dyspnoea | Cancer. (1 điểm)</p>"""),

dict(id='B8', week='Week 9 · Conditional random field (brute force vs variable elimination)', marks=6, code='B8',
 stem='A three-token linear-chain CRF with labels {O, P} defines score(y) = ∏ₜ emit[t, yₜ] · ∏ₜ trans[yₜ₋₁, yₜ]. Predict the output of the code.',
 parts=[
  ("(a) What is the first number on line 1, and what does Z equal?", 2),
  ("(b) Give the best label sequence, its score and its probability (line 2).", 1),
  ("(c) What is printed on line 3? Say which probability it is.", 1),
  ("(d) Show that Z can be obtained by sum-product variable elimination in the order Y3, Y2, and compare the cost with brute force.", 2),
 ],
 sol="""
<p><b>(a)</b> 2³ = <b>8</b> chuỗi nhãn. Điểm từng chuỗi (O=0, P=1):
(0,0,0)=32, (0,0,1)=80, (0,1,0)=12, <b>(0,1,1)=180</b>, (1,0,0)=4, (1,0,1)=10, (1,1,0)=9, (1,1,1)=135 ⇒ Z = <b>462</b> (hằng chuẩn hoá). (2 điểm)</p>
<p><b>(b)</b> Điểm cao nhất là (0,1,1) = O,P,P với 180 ⇒ <code>(0, 1, 1) 180.0 0.3896</code> (= 180/462). Đây là MAP assignment (Viterbi cho cùng kết quả). (1 điểm)</p>
<p><b>(c)</b> P(Y₂ = P | x) = (12 + 180 + 9 + 135)/462 = 336/462 = <b>0.7273</b> (marginal của nhãn token giữa). (1 điểm)</p>
<p><b>(d)</b> Loại Y₃: τ₃(y₂) = Σ<sub>y₃</sub> trans(y₂,y₃)·emit₃(y₃) = [2·1 + 1·5, 1·1 + 3·5] = [7, 16].
Loại Y₂: τ₂(y₁) = Σ<sub>y₂</sub> trans(y₁,y₂)·emit₂(y₂)·τ₃(y₂) = [2·2·7 + 1·3·16, 1·2·7 + 3·3·16] = [76, 158].
Z = Σ<sub>y₁</sub> emit₁(y₁)·τ₂(y₁) = 4·76 + 1·158 = <b>462</b> ✓.
Brute force: K<sup>T</sup> = 8 số hạng (tăng mũ theo độ dài câu); variable elimination trên chuỗi: O(T·K²) = 3·4, tuyến tính theo T. (2 điểm)</p>"""),

dict(id='B9', week='Week 10 · Variable elimination on a chain', marks=5, code='B9',
 stem='A chain A → B → C → D has binary variables. Predict every printed line.',
 parts=[
  ("(a) Line 1: tau1, tau2 and pD. State what each vector represents.", 2),
  ("(b) Lines 2 and 3: the vector <code>m</code>, the sum, and the posterior P(A | D=1).", 2),
  ("(c) Count the scalar multiplications needed for the three vector–matrix products versus enumerating all joint entries; what is the general complexity for a chain of n variables with k states?", 1),
 ],
 sol="""
<p><b>(a)</b> tau1(b) = Σₐ P(a)P(b|a) = <b>P(B)</b> = [0.6·0.7+0.4·0.2, 0.6·0.3+0.4·0.8] = [0.5, 0.5].
tau2(c) = Σ_b P(b)P(c|b) = <b>P(C)</b> = [0.5·0.9+0.5·0.4, 0.5·0.1+0.5·0.6] = [0.65, 0.35].
pD(d) = Σ_c P(c)P(d|c) = <b>P(D)</b> = [0.65·0.5+0.35·0.1, 0.65·0.5+0.35·0.9] = [0.36, 0.64]. (2 điểm)</p>
<p><b>(b)</b> <code>m</code> = unnormalised P(A, D=1): đẩy vector cột D=1 = [0.5, 0.9] ngược lên:
Σ_c P(c|b)·[0.5,0.9] = [0.9·0.5+0.1·0.9, 0.4·0.5+0.6·0.9] = [0.54, 0.74];
Σ_b P(b|a)·(...) = [0.7·0.54+0.3·0.74, 0.2·0.54+0.8·0.74] = [0.60, 0.70]; nhân P(a) ⇒ <code>m = [0.36 0.28]</code>.
Tổng = <b>0.64 = P(D=1)</b> (khớp pD[1]) ⇒ P(A | D=1) = [0.36, 0.28]/0.64 = <code>[0.5625 0.4375]</code>. (2 điểm)</p>
<p><b>(c)</b> Mỗi phép vector × ma trận 2×2: 4 phép nhân ⇒ 3 × 4 = 12. Liệt kê bảng joint: 2⁴ = 16 ô, mỗi ô 3 phép nhân = 48. Tổng quát chuỗi n biến: O(n·k²) so với O(kⁿ): tiết kiệm nhờ <b>distributive law</b> (đẩy phép tổng vào trong). (1 điểm)</p>"""),

dict(id='B10', week='Week 11 · Forward sampling and rejection sampling', marks=5, code='B10',
 stem='The uniform draws are supplied in <code>U</code>, one row per sample; each variable uses the next number of its row. <code>draw</code> returns the first state k with u ≤ cumulative probability. Predict the output.',
 parts=[
  ("(a) Give the four printed samples and show how the first one is generated.", 2),
  ("(b) What are the last two lines?", 1),
  ("(c) Compute exactly P(S = 1, L = 0). What is the expected number of accepted samples out of 1000 forward samples, and why is this approach inefficient when the evidence is rare?", 2),
 ],
 sol="""
<p><b>(a)</b> Mẫu 1 (u = 0.31, 0.18, 0.60, 0.92, 0.45): D: cum [0.6, 1] ⇒ 0.31 ≤ 0.6 ⇒ <b>d = 0</b>; I: 0.18 ≤ 0.7 ⇒ <b>i = 0</b>; G | (I=0, D=0) = [.30, .40, .30], cum [.30, .70, 1] ⇒ 0.60 ∈ (0.30, 0.70] ⇒ <b>g = 1</b>; S | I=0: [0.95, 0.05], cum [0.95, 1] ⇒ 0.92 ≤ 0.95 ⇒ <b>s = 0</b>; L | G=1: P(L=1) = 0.6 ⇒ [0.4, 0.6], cum [0.4, 1] ⇒ 0.45 > 0.4 ⇒ <b>l = 1</b>.
Kết quả 4 mẫu: <code>(0,0,1,0,1)</code>, <code>(1,0,1,0,1)</code>, <code>(0,1,0,1,0)</code>, <code>(1,0,2,0,0)</code>. (2 điểm)</p>
<p><b>(b)</b> Chỉ mẫu 3 có S = 1 và L = 0 ⇒ <code>kept = [(0, 1, 0, 1, 0)]</code>, tỉ lệ chấp nhận <b>0.25</b> (1/4). (1 điểm)</p>
<p><b>(c)</b> P(s¹,l⁰) = Σ_i P(i)P(s¹|i) Σ_g P(l⁰|g) Σ_d P(d)P(g|i,d).
i = 0: P(g) = [0.2, 0.34, 0.46] ⇒ Σ_g P(l⁰|g)P(g) = 0.1·0.2 + 0.4·0.34 + 0.99·0.46 = 0.6114.
i = 1: P(g) = [0.74, 0.168, 0.092] ⇒ 0.074 + 0.0672 + 0.09108 = 0.23228.
⇒ 0.7·0.05·0.6114 + 0.3·0.8·0.23228 = 0.0214 + 0.0557 = <b>0.0771</b>. Kỳ vọng 1000 × 0.0771 ≈ <b>77</b> mẫu được giữ; 92% công sức bị bỏ. Evidence càng hiếm (ví dụ P(e) = 0.001 ⇒ 10 trên 10 000 mẫu) thì rejection càng lãng phí và ước lượng càng nhiễu ⇒ dùng Gibbs sampling (hoặc likelihood weighting) để <i>giữ cố định</i> evidence. (2 điểm)</p>"""),

dict(id='B11', week='Week 11 · Gibbs sampling with evidence', marks=5, code='B11',
 stem='Gibbs sampling is run in the Student network with evidence S = 1 and L = 0 held fixed. The state is (D, I, G) and each variable is resampled in the order D, I, G. Predict the output.',
 parts=[
  ("(a) The first sweep (lines 1–4): show the first two conditional distributions you computed by hand.", 2),
  ("(b) The final state after the second sweep.", 1),
  ("(c) Why are S and L never resampled, and why does <code>cond_D</code> not involve S or L?", 1),
  ("(d) After thousands of sweeps, what would the fraction of sweeps with I = 1 estimate? Name two practical issues.", 1),
 ],
 sol="""
<p><b>(a)</b> Trạng thái đầu (d,i,g) = (0,0,1).
<b>P(D | g=1, i=0)</b> ∝ P(g=1 | i=0, D)·P(D) = [0.40·0.6, 0.25·0.4] = [0.24, 0.10] ⇒ [0.706, 0.294]; u = 0.80 &gt; 0.706 ⇒ <b>d = 1</b>.
<b>P(I | g=1, d=1, s=1)</b> ∝ P(g | I, d=1)·P(s=1 | I)·P(I) = [0.25·0.05·0.7, 0.30·0.80·0.3] = [0.00875, 0.072] ⇒ [0.108, 0.892]; u = 0.50 ⇒ <b>i = 1</b>.
<b>P(G | l=0, d=1, i=1)</b> ∝ P(l=0 | G)·P(G | i=1, d=1) = [0.1·0.5, 0.4·0.3, 0.99·0.2] = [0.05, 0.12, 0.198] ⇒ [0.136, 0.326, 0.538]; u = 0.70 ⇒ <b>g = 2</b>.
Sweep 1 kết thúc ở (1,1,2). (2 điểm)</p>
<p><b>(b)</b> Sweep 2: P(D | g=2, i=1) = [0.13, 0.87], u = 0.30 ⇒ d = 1; P(I | g=2, d=1) = [0.338, 0.662], u = 0.20 ⇒ <b>i = 0</b>; P(G | d=1, i=0) = [0.006, 0.125, 0.868], u = 0.95 ⇒ g = 2. Trạng thái: <code>(1, 0, 2)</code>. (1 điểm)</p>
<p><b>(c)</b> S, L là <b>evidence</b> nên được gán cố định (ta lấy mẫu P(X | E = e), X = {D, I, G}). Trong <code>cond_D</code> chỉ còn các nhân tử chứa D: P(D) và P(G | I, D) (Markov blanket của D: con G và cha khác của G là I); các nhân tử P(I), P(S|I), P(L|G) không phụ thuộc D nên <b>triệt tiêu khi chuẩn hoá</b>. (1 điểm)</p>
<p><b>(d)</b> Ước lượng <b>P(I = 1 | S = 1, L = 0) ≈ 0.7226</b> (giá trị đúng tính bằng enumeration; một lần chạy 60 000 sweeps cho 0.722). Hai vấn đề thực tế: (1) <b>burn-in</b> — bỏ các mẫu đầu vì còn phụ thuộc vào khởi tạo; (2) các mẫu liên tiếp <b>tự tương quan</b> (autocorrelation ≈ 0.2 cho I) nên số mẫu hiệu dụng nhỏ hơn số sweep. (1 điểm)</p>"""),

dict(id='B12', week='Week 11 · Restricted Boltzmann machine (one Gibbs step and CD-1)', marks=5, code='B12',
 stem='A binary RBM has 3 visible and 4 hidden units. A unit is set to 1 when its uniform draw is smaller than its activation probability. The hidden draws are (0.70, 0.10, 0.45, 0.20) and the visible draws are (0.05, 0.99, 0.30). Predict the output.',
 parts=[
  ("(a) Line 1: P(h = 1 | v) and the sampled h.", 2),
  ("(b) Line 2: P(v = 1 | h) and the reconstruction v′.", 1),
  ("(c) Lines 3–4: the new hidden probabilities and the contrastive-divergence update dW.", 1),
  ("(d) Which statements in the code correspond to one step of block Gibbs sampling? Why can all hidden units be sampled at the same time?", 1),
 ],
 sol="""
<p><b>(a)</b> Với v = (0,1,1): pre-activation = b + vW = b + (hàng 2 + hàng 3 của W) = (−1,0,0.5,−0.5) + (1, 1.5, −1, 1.5) = (0, 1.5, −0.5, 1.0).
σ(·) = <code>[0.5 0.818 0.378 0.731]</code>. Với u = (0.70, 0.10, 0.45, 0.20), so sánh u &lt; p: 0.70 &lt; 0.5? Không ⇒ 0; 0.10 &lt; 0.818 ⇒ 1; 0.45 &lt; 0.378? Không ⇒ 0; 0.20 &lt; 0.731 ⇒ 1 ⇒ h = <code>[0 1 0 1]</code>. (2 điểm)</p>
<p><b>(b)</b> a + Wh = (0,−0.5,0.5) + (cột 2 + cột 4 của W = (−2+0, 1.5+2, 0−0.5) = (−2, 3.5, −0.5)) = (−2, 3, 0) ⇒ σ = <code>[0.119 0.953 0.5]</code>. u = (0.05, 0.99, 0.30): 0.05 &lt; 0.119 ⇒ 1; 0.99 &lt; 0.953? Không ⇒ 0; 0.30 &lt; 0.5 ⇒ 1 ⇒ v′ = <code>[1 0 1]</code> (khác v ban đầu). (1 điểm)</p>
<p><b>(c)</b> P(h | v′) với v′ = (1,0,1): b + (hàng 1 + hàng 3) = (−1,0,0.5,−0.5) + (3,−2,−0.5,−0.5) = (2,−2,0,−1) ⇒ σ = <code>[0.881 0.119 0.5 0.269]</code>.
dW = v·p_hᵀ − v′·p_h2ᵀ (positive phase − negative phase) = <code>[[-0.881 -0.119 -0.5 -0.269], [0.5 0.818 0.378 0.731], [-0.381 0.698 -0.122 0.462]]</code>.
Hàng 2 dương vì visible 2 bằng 1 ở dữ liệu nhưng 0 ở reconstruction: CD tăng w₂ⱼ để mô hình 'thấy' pattern dữ liệu; hàng 1 âm vì mô hình tái tạo v₁ = 1 trong khi dữ liệu có v₁ = 0. (1 điểm)</p>
<p><b>(d)</b> Một bước block Gibbs là 3 dòng: <code>p_h → h</code> (sample hidden | v), <code>p_v → v2</code> (sample visible | h) và (cho CD-1) <code>p_h2</code>. Vì không có cạnh giữa các unit cùng tầng nên P(H | v) = ∏ⱼ P(Hⱼ | v) và P(V | h) = ∏ᵢ P(Vᵢ | h): các unit trong một tầng <b>độc lập có điều kiện</b> ⇒ lấy mẫu cả tầng song song bằng cách so sánh từng xác suất với một Uniform(0,1) độc lập. (1 điểm)</p>"""),

dict(id='B13', week='Week 12 · Learning structure (PC) and parameters', marks=5, code='B13a', code2='B13b',
 stem='Part 1 runs the skeleton phase of the PC algorithm with a p-value "oracle" (α = 0.05; every test not in <code>table</code> has p = 0.0005 and therefore rejects independence). Part 2 estimates parameters from data.',
 parts=[
  ("(a) Part 1: give the three printed lines.", 1),
  ("(b) Orient the skeleton: identify the collider, then apply Meek's rule to the remaining edge, and give the final directed graph.", 2),
  ("(c) Part 2: give the two printed CPD tables and explain the danger of the first one when predicting an instance with A = 1, B = 0.", 2),
 ],
 sol="""
<p><b>(a)</b> Size 0: chỉ cặp (X,Y) có p = 0.70 &gt; 0.05 ⇒ xoá cạnh X–Y, sepset = ∅. Size 1: (W,X) cho Z: p = 0.60 ⇒ xoá, sepset {Z}; (W,Y) cho Z: p = 0.50 ⇒ xoá, sepset {Z}; các cạnh còn lại có p = 0.0005 ⇒ giữ. In ra:
<code>[['W','Z'], ['X','Z'], ['Y','Z']]</code>, <code>{('X','Y'): (), ('W','X'): ('Z',), ('W','Y'): ('Z',)}</code>, <code>[('X','Z','Y')]</code>. (1 điểm)</p>
<p><b>(b)</b> Unshielded triple X – Z – Y: X, Y không kề nhau và Z <b>∉ sepset(X,Y) = ∅</b> ⇒ collider <b>X → Z ← Y</b>. Hai triple còn lại (X–Z–W, Y–Z–W) có Z ∈ sepset ⇒ không phải collider. Cạnh Z – W: X → Z và X không kề W ⇒ nếu Z ← W thì tạo ra v-structure X → Z ← W mà dữ liệu không ủng hộ (sepset(X,W) chứa Z) ⇒ <b>Meek rule 1</b> định hướng <b>Z → W</b>. Đồ thị cuối: X → Z, Y → Z, Z → W. (2 điểm)</p>
<p><b>(c)</b> Đếm: A = 0: (B=0: 3, B=1: 1) ⇒ [0.75, 0.25]; A = 1: (B=0: 0, B=1: 4) ⇒ [0, 1]. MLE in <code>[[0.75 0.] [0.25 1.]]</code> (hàng = B, cột = A). Prior K2 cộng 1 pseudo-count mỗi ô: A=0 ⇒ (4,2)/6 = [0.667, 0.333]; A=1 ⇒ (1,5)/6 = [0.167, 0.833] ⇒ <code>[[0.667 0.167] [0.333 0.833]]</code>.
Nguy cơ của MLE: P(B=0 | A=1) = 0 ⇒ mẫu A = 1, B = 0 có likelihood 0 (log-likelihood −∞), mô hình quá tin vào dữ liệu hiếm; smoothing (Laplace/K2/BDeu) tránh xác suất 0. (2 điểm)</p>"""),
]
