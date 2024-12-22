import numpy as np
from collections import defaultdict

class NaiveBayes:
    """
    朴素贝叶斯分类器实现类。
    """
    def __init__(self):
        """
        初始化 NaiveBayes 模型。
        """
        self.priors = {}  # 先验概率
        self.likelihoods = defaultdict(lambda: defaultdict(float))  # 条件概率
        self.classes = None  # 分类标签

    def fit(self, X, y):
        """
        训练朴素贝叶斯模型。

        参数：
        - X: 特征矩阵，形状为 (n_samples, n_features)
        - y: 标签向量，形状为 (n_samples,)
        """
        n_samples, n_features = X.shape
        self.classes = np.unique(y)

        # 计算先验概率
        for cls in self.classes:
            self.priors[cls] = np.sum(y == cls) / n_samples

        # 计算条件概率 P(x|y)
        for cls in self.classes:
            X_cls = X[y == cls]
            for feature_idx in range(n_features):
                feature_values, counts = np.unique(X_cls[:, feature_idx], return_counts=True)
                for value, count in zip(feature_values, counts):
                    self.likelihoods[feature_idx][(value, cls)] = count / X_cls.shape[0]

    def predict(self, X):
        """
        使用朴素贝叶斯模型进行预测。

        参数：
        - X: 特征矩阵，形状为 (n_samples, n_features)

        返回：
        - 预测标签，形状为 (n_samples,)
        """
        predictions = []

        for x in X:
            posteriors = {}

            for cls in self.classes:
                # 计算后验概率 P(y|x)
                posterior = np.log(self.priors[cls])
                for feature_idx, feature_value in enumerate(x):
                    likelihood = self.likelihoods[feature_idx].get((feature_value, cls), 1e-6)
                    posterior += np.log(likelihood)
                posteriors[cls] = posterior

            # 选择后验概率最大的分类
            predictions.append(max(posteriors, key=posteriors.get))

        return np.array(predictions)

# 示例：使用朴素贝叶斯进行分类
if __name__ == "__main__":
    # 创建示例数据
    X = np.array([
        [1, 0],
        [1, 1],
        [0, 0],
        [0, 1],
        [1, 0],
        [0, 0]
    ])
    y = np.array([1, 1, 0, 0, 1, 0])

    # 初始化模型
    nb = NaiveBayes()

    # 训练模型
    nb.fit(X, y)

    # 测试预测
    test_data = np.array([
        [1, 1],
        [0, 0]
    ])
    predictions = nb.predict(test_data)

    print("测试数据:", test_data)
    print("预测结果:", predictions)
