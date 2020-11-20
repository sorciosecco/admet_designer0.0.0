# ENSEMBLE METHODS BASED ON DECISION TREES

# Two averaging algorithms based on randomized decision trees: the RandomForest algorithm and the Extra-Trees method.
# Both algorithms are perturb-and-combine techniques specifically designed for trees.
# This means a diverse set of classifiers is created by introducing randomness in the classifier construction.
# The prediction of the ensemble is given as the averaged prediction of the individual classifiers.
# -----------------------------------------------------------------------------------------------------------------------
# RANDOM FOREST (RF)
# In random forests, each tree in the ensemble is built from a sample drawn with replacement (i.e., a bootstrap sample)
# from the training set. In addition, when splitting a node during the construction of the tree, the chosen split
# is no longer the best split among all features. Instead, the split that is picked is the best split among a random
# subset of the features. As a result of this randomness, the bias of the forest usually slightly increases (with
# respect to the bias of a single non-random tree) but, due to averaging, its variance also decreases, usually more than
# compensating for the increase in bias, hence yielding an overall better model.
# -----------------------------------------------------------------------------------------------------------------------
# In contrast to the original publication, the scikit-learn implementation combines classifiers by averaging their
# probabilistic prediction, instead of letting each classifier vote for a single class.
# -----------------------------------------------------------------------------------------------------------------------
# EXTRA-TREE (ET)
# In extremely randomized trees, randomness goes one step further in the way splits are computed. As in random forests,
# a random subset of candidate features is used, but instead of looking for the most discriminative thresholds,
# thresholds are drawn at random for each candidate feature and the best of these randomly-generated thresholds is
# picked as the splitting rule. This usually allows to reduce the variance of the model a bit more, at the expense
# of a slightly greater increase in bias.
# -----------------------------------------------------------------------------------------------------------------------
# ADA BOOST (AB)
# An AdaBoost classifier is a meta-estimator that begins by fitting a classifier on the original dataset and then fits 
# additional copies of the classifier on the same dataset but where the weights of incorrectly classified instances are 
# adjusted such that subsequent classifiers focus more on difficult cases.
# -----------------------------------------------------------------------------------------------------------------------
# GRADIENT BOOSTING (GB)
# GB builds an additive model in a forward stage-wise fashion; it allows for the optimization of arbitrary
# differentiable loss functions. In each stage n_classes_ regression trees are fit on the negative gradient of the
# binomial or multinomial deviance loss function. Binary classification is a special case where only a single regression
# tree is induced.
# -----------------------------------------------------------------------------------------------------------------------
# PARAMETERS (see details for the methods below)
# Good results are often achieved when setting max_depth=None in combination with min_samples_split=1
# (i.e., when fully developing the trees). Bear in mind though that these values are usually not optimal,
# and might result in models that consume a lot of ram. The best parameter values should always be cross-validated.
# In addition, note that in random forests, bootstrap samples are used by default (bootstrap=True) while the default
# strategy for extra-trees is to use the whole dataset (bootstrap=False).
# When using bootstrap sampling the generalization error can be estimated on the left out or out-of-bag samples.
# This can be enabled by setting oob_score=True.
# -----------------------------------------------------------------------------------------------------------------------

# OTHER METHODS

# -----------------------------------------------------------------------------------------------------------------------
# LINEAR DISCRIMINANT ANALYSIS (LDA)
# A classifier with a linear decision boundary, generated by fitting class conditional densities to the data and using
# Bayes' rule. The model fits a Gaussian density to each class, assuming that all classes share the same covariance
# matrix. The fitted model can also be used to reduce the dimensionality of the input by projecting it to the most
# discriminative directions.
# -----------------------------------------------------------------------------------------------------------------------
# SUPPORT VECTOR MACHINES (SVM)
# The implementation is based on libsvm. The fit time scales at least quadratically with the number of samples and may
# be impractical beyond tens of thousands of samples. The multiclass support is handled according to a one-vs-one scheme.
# -----------------------------------------------------------------------------------------------------------------------

# PARAMETERS BY ALGORITHM

##### (RF, ETC, AB, GB)

### The number of trees in the forest. The larger the better, but also the longer it will take to compute. In addition, note that results will stop getting significantly better beyond a critical number of trees.

n_estimators=10

##### (RF, ETC, GB)

### The number of features to consider when looking for the best split:
#   If int, then consider max_features features at each split.
#   If float, then max_features is a percentage and int(max_features * n_features) features are considered at each split.
#   If "sqrt", then max_features=sqrt(n_features) (same as "auto").
#   If "log2", then max_features=log2(n_features).
#   If None, then max_features=n_features.
### Note: the search for a split does not stop until at least one valid partition of the node samples is found, even if it requires to effectively inspect more than max_features features.
# It is the size of the random subsets of features to consider when splitting a node. The lower the greater the reduction of variance, but also the greater the increase in bias. Empirical good default values are:
#   max_features=n_features for regression problems
#   max_features=sqrt(n_features) for classification tasks (where n_features is the number of features in the data)

#max_features='sqrt'
max_features='log2'
#max_features=None
#max_features=0.0

### The maximum depth of the tree. If None, then nodes are expanded until all leaves are pure or until all leaves contain less than min_samples_split samples. Ignored if max_leaf_nodes is not None.

max_depth=4
#max_depth=None

### Grow trees with max_leaf_nodes in best-first fashion. Best nodes are defined as relative reduction in impurity. If None then unlimited number of leaf nodes. If not None then max_depth will be ignored.

max_leaf_nodes=15
#max_leaf_nodes=None

##### (RF, ETC, SVM)

### class_weight : dict, list of dicts, "balanced", "balanced_subsample" or None.
### Weights associated with classes in the form {class_label: weight}. If not given, all classes are supposed to have weight one. For multi-output problems, a list of dicts can be provided in the same order as the columns of y.
#   The "balanced" mode uses the values of y to automatically adjust weights inversely proportional to class frequencies in the input data as n_samples / (n_classes * np.bincount(y)).
#   The "balanced_subsample" mode is the same as "balanced" except that weights are computed based on the bootstrap sample for every tree grown. For multi-output, the weights of each column of y will be multiplied. Note that these weights will be multiplied with sample_weight (passed through the fit method) if sample_weight is specified.

#class_weight=None
class_weight='balanced'
#class_weight='balanced_subsample'

##### (RF, ETC)

### The function to measure the quality of a split. Supported criteria are "gini" for the Gini impurity and "entropy" for the information gain.

#criterion_rf='gini'
criterion_rf='entropy'

##### (AB)

### If SAMME.R then use the SAMME.R real boosting algorithm. base_estimator must support calculation of class probabilities. If SAMME then use the SAMME discrete boosting algorithm. The SAMME.R algorithm typically converges faster than SAMME, achieving a lower test error with fewer boosting iterations.

algorithm_ab='SAMME.R'
#algorithm_ab='SAMME'

##### (GB)

### loss function to be optimized. "deviance" refers to deviance (= logistic regression) for classification with probabilistic outputs. For loss "exponential" gradient boosting recovers the AdaBoost algorithm.

#loss='deviance'
loss='exponential'

### The function to measure the quality of a split. Supported criteria are:
#   "friedman_mse" for the mean squared error with improvement score by Friedman
#   "mse" for mean squared error
#   "mae" for the mean absolute error.
### The default value of "friedman_mse" is generally the best as it can provide a better approximation in some cases.

criterion_gb='friedman_mse'
#criterion_gb='mse'
#criterion_gb='mae'

##### (LDA, MLP)

### Possible values are:
#   "svd": Singular value decomposition (default). Does not compute the covariance matrix, therefore this solver is recommended for data with a large number of features.
#   "lsqr": Least squares solution, can be combined with shrinkage.
#   "eigen": Eigenvalue decomposition, can be combined with shrinkage.

#solver='svd'
#solver='lsqr'
solver='eigen'

##### (LDA)

### Possible values are:
#   None: no shrinkage (default).
#   "auto": automatic shrinkage using the Ledoit-Wolf lemma.
#   float between 0 and 1: fixed shrinkage parameter.
### Note that shrinkage works only with "lsqr" and "eigen" solvers.

#shrinkage=None
#shrinkage='auto'
shrinkage=0.09

##### (SVM)

### Penalty parameter C of the error term.

C=1

### Degree of the polynomial kernel function "poly". Ignored by all other kernels.

degree=2

### Kernel coefficient for "rbf", "poly" and "sigmoid".
#   default is "auto" which uses 1 / n_features
#   if gamma="scale" is passed then it uses 1 / (n_features * X.var()) as value of gamma.

#gamma='auto'
#gamma='scale'
gamma=0.011

### Specifies the kernel type to be used in the algorithm. It must be one of "linear", "poly", "rbf", "sigmoid", "precomputed" or a callable. If none is given, "rbf" will be used. If a callable is given it is used to pre-compute the kernel matrix from data matrices; that matrix should be an array of shape (n_samples, n_samples).

#kernel='linear'
kernel='rbf'
#kernel='poly'
#kernel='sigmoid'

##### (kNN, rNN)

### Number of neighbors to use by default for kneighbors queries.

n_neighbors=4

### Radius to use by default for kneighbors queries.

radius=1.0

### Weight function used in prediction. Possible values:
#   "uniform" : uniform weights. All points in each neighborhood are weighted equally.
#   "distance" : weight points by the inverse of their distance. in this case, closer neighbors of a query point will have a greater influence than neighbors which are further away.
#   [callable] : a user-defined function which accepts an array of distances, and returns an array of the same shape containing the weights.

weights='uniform'
#weights='distance'

### Algorithm used to compute the nearest neighbors:
#   "ball_tree" will use BallTree
#   "kd_tree" will use KDTree
#   "brute" will use a brute-force search.
#   "auto" will attempt to decide the most appropriate algorithm based on the values passed to fit method.

#algorithm_knn='auto'

### Leaf size passed to BallTree or KDTree. This can affect the speed of the construction and query, as well as the memory required to store the tree. The optimal value depends on the nature of the problem.

#leaf_size=30

### Power parameter for the Minkowski metric. When p = 1, this is equivalent to using manhattan_distance (l1), and euclidean_distance (l2) for p = 2. For arbitrary p, minkowski_distance (l_p) is used.

#p=1
p=2

### The distance metric to use for the tree. The default metric is minkowski, and with p=2 is equivalent to the standard Euclidean metric. See the documentation of the DistanceMetric class for a list of available metrics.

#metric='minkowski'

##### MLP
max_iter=1000
hidden_layer_sizes=(200,50)
