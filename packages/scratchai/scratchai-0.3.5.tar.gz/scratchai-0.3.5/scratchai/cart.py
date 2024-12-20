import numpy as np
from collections import Counter

# static helpers functions
def _to_numeric(array):
    try:
        return array.astype('float')
    except:
        return array
    
def _most_common(array):
    count = Counter(array)
    return count.most_common(1)[0][0]

# Tree metrics functions
def entropy(y):
    _, counts = np.unique(y, return_counts = True)
    p = counts / len(y)
    return abs(-np.sum(p * np.log2(p)))

# Tree nodes
class _DecisionNode:
    def __init__(self, feature = None, value = None, left = None, right = None):
        self.feature = feature
        self.value = value
        self.left = left
        self.right = right
        
class _LeafNode:
    def __init__(self, value = None):
        self.value = value

# Incomplete - Todo: provide doc strings for both tree classes methods.
class DecisionTreeClassifier:
    def __init__(self, max_depth = 50, min_samples_split = 5):
        # thr root node of th three
        self.root = None
        
        # the tree parameters
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        
        # performance settings
        self.thresh_batch = 64
        self.process_batch = 128
        
        # features data types
        self.dtypes = []
        
    def _init_dtypes(self, X):
        for i in range(X.shape[1]):
            cur_column = _to_numeric(X[:, i])
            if (isinstance(cur_column.dtype, np.dtypes.Int64DType) or 
                isinstance(cur_column.dtype, np.dtypes.Float64DType)):
                self.dtypes.append('numeric')
            else:
                self.dtypes.append('categorical')
                
    def fit(self, X, y):
        """fit the decision tree model to the data

        Args:
            X (array): the features array
            y (array): the target array
        """
        # initialize the features data types and grow the three
        self._init_dtypes(X)
        self.root = self._grow_tree(X, y)
        
    def _grow_tree(self, X, y, depth = 0):
        n_samples, n_labels = X.shape[0], len(np.unique(y))
        
        # Checks Three criteria :
        # 1 - if the maximum depth exceeded
        # 2 - if the number of samples is insuffisant for split
        # 3 - if there no further slit needed
        # and returns a leaf node if one of them is True.
        if depth >= self.max_depth or n_samples <= self.min_samples_split or n_labels == 1:
            leaf_val = _most_common(y)
            return _LeafNode(value = leaf_val)
        
        # finds the best split
        split_feature, split_val = self._best_split(X, y)
        split_column = _to_numeric(X[:, split_feature])
        
        # split the data
        left_mask = split_column >= split_val if self.dtypes[split_feature] == 'numeric' else split_column == split_val
        right_mask = ~left_mask
        
        X_left, X_right = X[left_mask], X[right_mask]
        y_left, y_right = y[left_mask], y[right_mask]
        
        parent_node = _DecisionNode(split_feature, split_val)
        parent_node.left = self._grow_tree(X_left, y_left)
        parent_node.right = self._grow_tree(X_right, y_right)
        
        return parent_node
        
    def _best_split(self, X, y):
        n_features = X.shape[1]
        split_gain = 0
        split_feature, split_val = None, None
        
        for feature in range(n_features):
            cur_column = _to_numeric(X[:, feature])
            
            if self.dtypes[feature] == 'numeric':
                # process the sampled data using min batches
                for start in range(0, len(cur_column), self.process_batch):
                    end = min(start + self.process_batch, len(cur_column))
                    X_sample = cur_column[start:end]
                    y_sample = y[start:end]
                    
                    uniques = np.unique(X_sample)
                    thresholds = (uniques[:-1] + uniques[1:]) / 2
                    
                    for start in range(0, len(thresholds), self.thresh_batch):
                        end = min(start + self.thresh_batch, len(thresholds))
                        thresh_sample = thresholds[start:end]
                        
                        # calculate the information gain for all thresholds in thresh_sample
                        gains, thresh_sample = self._information_gains(X_sample, y_sample, thresh_sample, 'numeric')
                        
                        if len(gains) == 0 or len(thresh_sample) == 0:
                            continue
                        
                        max_gain = np.argmax(gains)
                        if gains[max_gain] > split_gain:
                            split_gain = gains[max_gain]
                            split_feature, split_val = feature, thresh_sample[max_gain]
                        
            else:
                for start in range(0, len(cur_column), self.process_batch):
                    end = min(start + self.process_batch, len(cur_column))
                    X_sample = cur_column[start:end]
                    y_sample = y[start:end]
                    
                    uniques = np.unique(X_sample)
                    
                    for start in range(0, len(uniques), self.thresh_batch):
                        end = min(start + self.thresh_batch, len(uniques))
                        uniques_batch = uniques[start:end]
                        
                        # caclulate the infromation gain for all unique values of feature
                        gains, uniques_batch = self._information_gains(X_sample, y_sample, uniques, 'categorical')
                        
                        if len(gains) == 0 or len(uniques_batch) == 0:
                            continue
                        
                        max_gain = np.argmax(gains)
                        if gains[max_gain] > split_gain:
                            split_gain = gains[max_gain]
                            split_feature, split_val = feature, uniques_batch[max_gain]
                        
        
        return split_feature, split_val
    
    def _information_gains(self, X, y, thresholds, feature_dtype):
        masks = X[None ,:] >= thresholds[:, None] if feature_dtype == 'numeric' else X[None ,:] == thresholds[:, None]
        
        left_counts = np.sum(masks, axis = 1)
        right_counts = np.sum(~masks, axis = 1)
        
        valid_thresholds = (left_counts > 0) & (right_counts > 0)
        thresholds = thresholds[valid_thresholds]
        masks = masks[valid_thresholds]
        
        gains = []
        for mask in masks:
            left_entropy = entropy(y[mask])
            right_entropy = entropy(y[~mask])
            
            w = np.sum(mask) / len(y)
            gain = entropy(y) - (w * left_entropy + (1 - w) * right_entropy)
            gains.append(gain)
            
        return np.array(gains), thresholds
        
                
    def _split(self, feature, value, column):
        left_indices = column >= value if self.dtypes[feature] == 'numeric' else column == value
        right_indices = column < value if self.dtypes[feature] == 'numeric' else column != value
        return left_indices, right_indices
    
    def predict(self, X):
        """predict the target values for the given data X

        Args:
            X (array): the features array

        Returns:
            array: the preicted values from X
        """
        return np.array([self._traverse_tree(row, self.root) for row in X])
    
    def _traverse_tree(self, X, node):
        if isinstance(node, _LeafNode):
            return node.value
        
        if self.dtypes[node.feature] == 'numeric':
            if float(X[node.feature]) >= node.value:
                return self._traverse_tree(X, node.left)
            return self._traverse_tree(X, node.right)
        else:
            if X[node.feature] == node.value:
                return self._traverse_tree(X, node.left)
            return self._traverse_tree(X, node.right)
        
class DecisionTreeRegressor:
    def __init__(self, min_samples_split = 20, max_depth = 50):
        # Tree root
        self.root = None
        
        # Tree parameters
        self.min_samples_split = min_samples_split
        self.max_depth = max_depth
        
        # performance settings
        self.thresh_batch = 64
        self.process_batch = 128
        
        # features data types
        self.dtypes = []
        
    def _init_dtypes(self, X):
        for i in range(X.shape[1]):
            cur_column = _to_numeric(X[:, i])
            if (isinstance(cur_column.dtype, np.dtypes.Int64DType) or 
                isinstance(cur_column.dtype, np.dtypes.Float64DType)):
                self.dtypes.append('numeric')
            else:
                self.dtypes.append('categorical')
                
    def fit(self, X, y):
        """fit the decision tree model to the data

        Args:
            X (array): the features array
            y (array): the target array
        """
        # initialize the features data types and grow the three
        self._init_dtypes(X)
        self.root = self._grow_tree(X, y)
        
    def _grow_tree(self, X, y, depth = 0):
        n_samples, uniques = X.shape[0], len(np.unique(y))
        
        # Checks Three criteria :
        # 1 - if the maximum depth exceeded
        # 2 - if the number of samples is insuffisant for split
        # 3 - if there no further slit needed
        # and returns a leaf node if one of them is True.
        if depth >= self.max_depth or n_samples <= self.min_samples_split or uniques == 1:
            leaf_val = np.mean(y)
            return _LeafNode(value = leaf_val)
        
        split_feature, split_val = self._best_split(X, y)
        split_column = _to_numeric(X[:, split_feature])
        
        left_mask = split_column >= split_val if self.dtypes[split_feature] == 'numeric' else split_column == split_val
        right_mask = ~left_mask 
        
        X_left, X_right = X[left_mask], X[right_mask]
        y_left, y_right = y[left_mask], y[right_mask]
        
        left_node, right_node = self._grow_tree(X_left, y_left, depth + 1), self._grow_tree(X_right, y_right, depth + 1)
        return _DecisionNode(split_feature, split_val, left_node, right_node)
    
    
    def _best_split(self, X, y):
        n_features = X.shape[1]
        split_feature, split_val = None, None
        split_error = float('inf')
        
        for feature in range(n_features):
            cur_column = _to_numeric(X[:, feature])
            
            if self.dtypes[feature] == 'numeric':
                for start in range(0, len(cur_column), self.process_batch):
                    end = min(start + self.process_batch, len(cur_column))
                    x_sample = cur_column[start:end]
                    y_sample = y[start:end]
            
                    uniques = np.unique(x_sample)
                    thresholds = (uniques[1:] + uniques[:-1]) / 2
                    
                    for batch in range(0, len(thresholds), self.thresh_batch):
                        thresholds_batch = thresholds[batch: batch + self.thresh_batch]
                        
                        left_masks = x_sample[None ,:] >= thresholds_batch[:, None]
                        right_masks = ~left_masks
                        
                        left_means = np.sum(y_sample * left_masks, axis = 1) / np.sum(left_masks, axis = 1)
                        right_means = np.sum(y_sample * right_masks, axis = 1) / np.sum(right_masks, axis = 1)
                        
                        y_preds = left_means[:, None] * left_masks + right_means[:, None] * right_masks
                        errors = np.sum((y_preds - y_sample) ** 2, axis = 1)
                        min_error = np.argmin(errors)
                        
                        if errors[min_error] < split_error:
                            split_error = errors[min_error]
                            split_feature, split_val = feature, thresholds_batch[min_error]
            else:
                uniques = np.unique(cur_column)
                
                for start in range(0, len(cur_column), self.process_batch):
                    end = min(start + self.process_batch, len(cur_column))
                    x_sample = cur_column[start:end]
                    y_sample = y[start:end]
                
                    for batch in range(0, len(uniques), self.thresh_batch):
                        uniques_batch = uniques[batch: batch + self.thresh_batch]
                        
                        if len(uniques_batch) <= 1:
                            continue
                        
                        left_masks = x_sample[None ,:] == uniques_batch[:, None]
                        right_masks = ~left_masks

                        left_means = np.sum(y_sample * left_masks, axis = 1) / np.sum(left_masks, axis = 1)
                        right_means = np.sum(y_sample * right_masks, axis = 1) / np.sum(right_masks, axis = 1)
                                                
                        y_preds = left_means[:, None] * left_masks + right_means[:, None] * right_masks
                        errors = np.sum((y_preds - y_sample) ** 2, axis = 1)
                        min_error = np.argmin(errors)
                        
                        if errors[min_error] < split_error:
                            split_error = errors[min_error]
                            split_feature, split_val = feature, uniques_batch[min_error]
                        
        return split_feature, split_val
    
    def predict(self, X):
        """predict the target values for the given data X

        Args:
            X (array): the features array

        Returns:
            array: the preicted values from X
        """
        return np.array([self._traverse_tree(row, self.root) for row in X])
    
    def _traverse_tree(self, X, node):
        if isinstance(node, _LeafNode):
            return node.value
        
        if self.dtypes[node.feature] == 'numeric':
            if float(X[node.feature]) >= node.value:
                return self._traverse_tree(X, node.left)
            return self._traverse_tree(X, node.right)
        else:
            if X[node.feature] == node.value:
                return self._traverse_tree(X, node.left)
            return self._traverse_tree(X, node.right)
        