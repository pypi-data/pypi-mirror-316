import numpy as np
from collections import defaultdict


class NaiveBayes:
    """
    朴素贝叶斯分类器实现类。

    该类实现了朴素贝叶斯分类算法，适用于离散特征。朴素贝叶斯分类器的核心思想是基于特征条件独立的假设，计算每个类别的后验概率并进行分类。通过训练，模型学习到先验概率和条件概率，然后通过贝叶斯定理进行分类。

    方法：
    - fit(X, y): 训练朴素贝叶斯模型，计算先验概率和条件概率。
    - predict(X): 使用训练好的模型进行预测，计算每个类别的后验概率，选择后验概率最大的类别。
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
        训练朴素贝叶斯模型，计算先验概率和条件概率。

        参数：
        - X: 特征矩阵，形状为 (n_samples, n_features)
        - y: 标签向量，形状为 (n_samples,)
        """
        n_samples, n_features = X.shape
        self.classes = np.unique(y)

        # 计算先验概率 P(y)
        for cls in self.classes:
            self.priors[cls] = np.sum(y == cls) / n_samples

        # 计算条件概率 P(x|y)
        for cls in self.classes:
            X_cls = X[y == cls]  # 当前类别的样本
            for feature_idx in range(n_features):
                feature_values, counts = np.unique(X_cls[:, feature_idx], return_counts=True)  # 特征值及其频次
                for value, count in zip(feature_values, counts):
                    self.likelihoods[feature_idx][(value, cls)] = count / X_cls.shape[0]  # 条件概率 P(x_i|y)

    def predict(self, X):
        """
        使用朴素贝叶斯模型进行预测，计算后验概率并选择最大值对应的类别。

        参数：
        - X: 特征矩阵，形状为 (n_samples, n_features)

        返回：
        - 预测标签，形状为 (n_samples,)
        """
        predictions = []

        for x in X:
            posteriors = {}

            for cls in self.classes:
                # 计算后验概率 P(y|x) = P(y) * P(x1|y) * P(x2|y) * ... * P(xn|y)
                posterior = np.log(self.priors[cls])  # 先验概率的对数
                for feature_idx, feature_value in enumerate(x):
                    # 如果特征值未在训练集中出现，则使用一个非常小的概率值
                    likelihood = self.likelihoods[feature_idx].get((feature_value, cls), 1e-6)
                    posterior += np.log(likelihood)  # 计算对数后的条件概率
                posteriors[cls] = posterior  # 存储每个类别的后验概率

            # 选择后验概率最大的类别
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
