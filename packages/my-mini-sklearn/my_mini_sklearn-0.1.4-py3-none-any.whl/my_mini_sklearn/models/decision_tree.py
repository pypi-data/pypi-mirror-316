import numpy as np
from collections import Counter


class DecisionTreeClassifier:
    """
    一个简单的决策树分类器，使用信息增益（ID3算法）作为分裂标准，支持最大深度限制。

    方法：
    - fit(X, y): 将决策树模型拟合到训练数据。
    - predict(X): 使用训练好的模型进行预测。
    - score(X, y): 计算模型的准确率。
    - _entropy(y): 计算标签的熵。
    - _information_gain(X_column, y, threshold): 计算给定阈值的特征的信息增益。
    - _best_split(X, y): 寻找最佳分割特征和阈值。
    - _build_tree(X, y, depth): 递归构建决策树。
    - _predict_single(x, tree): 对单个样本进行预测。
    """

    def __init__(self, max_depth=None):
        """
        初始化决策树分类器。

        参数:
        max_depth (int): 树的最大深度，默认为 None 表示没有限制。
        """
        self.max_depth = max_depth  # 设置树的最大深度
        self.tree = None  # 初始化树为空

    def fit(self, X, y):
        """
        训练决策树模型。

        参数:
        X (numpy.ndarray): 特征数据，形状为 (n_samples, n_features)。
        y (numpy.ndarray): 标签数据，形状为 (n_samples,)。
        """
        self.tree = self._build_tree(X, y)  # 使用 _build_tree 方法构建决策树

    def predict(self, X):
        """
        使用决策树进行预测。

        参数:
        X (numpy.ndarray): 待预测的数据，形状为 (n_samples, n_features)。

        返回:
        numpy.ndarray: 预测标签，形状为 (n_samples,)。
        """
        return np.array([self._predict_single(x, self.tree) for x in X])  # 对每个样本进行预测

    def _entropy(self, y):
        """
        计算信息熵。

        参数:
        y (numpy.ndarray): 标签数据。

        返回:
        float: 信息熵。
        """
        # 计算标签的唯一值及其出现频率
        unique, counts = np.unique(y, return_counts=True)

        # 计算每个标签的概率
        probabilities = counts / len(y)

        # 计算信息熵（忽略概率为0的项）
        entropy = -np.sum(probabilities * np.log2(probabilities, where=(probabilities > 0)))

        return entropy

    def _information_gain(self, X_column, y, threshold):
        """
        计算信息增益。

        参数:
        X_column (numpy.ndarray): 特征列。
        y (numpy.ndarray): 标签数据。
        threshold (float): 阈值。

        返回:
        float: 信息增益。
        """
        # 分割数据
        left_indices = X_column <= threshold  # 左子集
        right_indices = X_column > threshold  # 右子集
        left_y, right_y = y[left_indices], y[right_indices]

        # 计算信息增益
        if len(left_y) == 0 or len(right_y) == 0:  # 若某一子集为空，信息增益为0
            return 0

        parent_entropy = self._entropy(y)  # 计算父节点的熵
        n = len(y)
        n_left, n_right = len(left_y), len(right_y)
        child_entropy = (n_left / n) * self._entropy(left_y) + (n_right / n) * self._entropy(right_y)  # 计算子节点的熵

        info_gain = parent_entropy - child_entropy  # 信息增益等于父节点熵与子节点熵之差
        return info_gain

    def _best_split(self, X, y):
        """
        找到最佳分割特征和阈值。

        参数:
        X (numpy.ndarray): 特征数据。
        y (numpy.ndarray): 标签数据。

        返回:
        tuple: (最佳特征索引，最佳阈值，最大信息增益)。
        """
        best_gain = -1  # 初始化最优信息增益
        split_index, split_threshold = None, None  # 初始化最优特征索引和阈值

        # 遍历每个特征列，寻找最佳分割
        for i in range(X.shape[1]):
            X_column = X[:, i]  # 获取第 i 列特征
            thresholds = np.unique(X_column)  # 获取该特征的所有唯一值作为分割阈值

            # 遍历所有阈值，计算信息增益
            for threshold in thresholds:
                gain = self._information_gain(X_column, y, threshold)
                if gain > best_gain:  # 若当前信息增益更大，则更新最优信息增益及对应阈值
                    best_gain = gain
                    split_index = i
                    split_threshold = threshold

        return split_index, split_threshold, best_gain

    def _build_tree(self, X, y, depth=0):
        """
        递归地构建决策树。

        参数:
        X (numpy.ndarray): 特征数据。
        y (numpy.ndarray): 标签数据。
        depth (int): 当前树的深度。

        返回:
        dict: 表示决策树的节点。
        """
        num_samples, num_features = X.shape
        num_labels = len(np.unique(y))  # 获取标签的种类数

        # 停止条件
        if depth == self.max_depth or num_labels == 1 or num_samples == 0:
            leaf_value = Counter(y).most_common(1)[0][0]  # 若达到停止条件，则返回最常见的标签作为叶节点
            return leaf_value

        # 找到最佳分割
        split_index, split_threshold, best_gain = self._best_split(X, y)

        if best_gain == 0:  # 若信息增益为0，则返回最常见的标签
            leaf_value = Counter(y).most_common(1)[0][0]
            return leaf_value

        # 构建子树
        left_indices = X[:, split_index] <= split_threshold  # 左子集索引
        right_indices = X[:, split_index] > split_threshold  # 右子集索引
        left_subtree = self._build_tree(X[left_indices], y[left_indices], depth + 1)  # 递归构建左子树
        right_subtree = self._build_tree(X[right_indices], y[right_indices], depth + 1)  # 递归构建右子树
        return {
            "feature_index": split_index,  # 当前节点的特征索引
            "threshold": split_threshold,  # 当前节点的分割阈值
            "left": left_subtree,  # 左子树
            "right": right_subtree  # 右子树
        }

    def _predict_single(self, x, tree):
        """
        对单个样本进行预测。

        参数:
        x (numpy.ndarray): 单个样本。
        tree (dict): 决策树。

        返回:
        int: 预测的标签。
        """
        if not isinstance(tree, dict):  # 若树节点是叶节点，则返回叶节点的标签
            return tree

        feature_index = tree["feature_index"]  # 当前节点的特征索引
        threshold = tree["threshold"]  # 当前节点的分割阈值

        # 根据样本特征值与阈值进行分支
        if x[feature_index] <= threshold:
            return self._predict_single(x, tree["left"])  # 向左子树递归预测
        else:
            return self._predict_single(x, tree["right"])  # 向右子树递归预测

    def score(self, X, y):
        """
        计算模型的准确率。

        参数:
        X (numpy.ndarray): 测试数据。
        y (numpy.ndarray): 测试标签。

        返回:
        float: 准确率。
        """
        y_pred = self.predict(X)  # 预测标签
        return np.mean(y_pred == y)  # 计算预测的准确率


if __name__ == '__main__':
    # 测试代码
    X = np.array([[1, 2], [3, 4], [5, 6]])  # 特征数据
    y = np.array([0, 1, 1])  # 标签数据

    model = DecisionTreeClassifier(max_depth=2)  # 初始化决策树模型，最大深度为2
    model.fit(X, y)  # 拟合模型

    predictions = model.predict(X)  # 进行预测

    print(f"Predictions: {predictions}")  # 输出预测结果
    print(f"Accuracy: {model.score(X, y)}")  # 输出模型准确率
