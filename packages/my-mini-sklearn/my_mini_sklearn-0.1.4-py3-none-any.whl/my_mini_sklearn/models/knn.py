import numpy as np
from collections import Counter
from matplotlib import pyplot as plt


class KNearestNeighbors:
    """
    K-Nearest Neighbors (KNN) 分类算法实现类。使用矩阵化计算进行预测。
    """

    def __init__(self, k=3):
        """
        初始化 KNN 模型。

        参数：
        - k (int): 使用的邻居数量，默认为 3。
        """
        self.k = k

    def fit(self, X, y):
        """
        训练 KNN 模型，存储训练数据。

        参数：
        - X (numpy.ndarray): 特征数据，形状为 (n_samples, n_features)。
        - y (numpy.ndarray): 标签数据，形状为 (n_samples,)。
        """
        self.X_train = X  # 存储训练特征数据
        self.y_train = y  # 存储训练标签数据

    def predict(self, X):
        """
        使用 KNN 进行批量预测。

        参数：
        - X (numpy.ndarray): 待预测的数据，形状为 (n_samples, n_features)。

        返回：
        - numpy.ndarray: 预测标签，形状为 (n_samples,)。
        """
        # 计算所有测试样本与训练样本之间的距离矩阵
        distances = np.linalg.norm(X[:, np.newaxis] - self.X_train, axis=2)

        # 找到每个测试样本的 k 个最近邻
        k_indices = np.argsort(distances, axis=1)[:, :self.k]

        # 获取每个样本的 k 个邻居标签
        k_nearest_labels = self.y_train[k_indices]

        # 进行投票，并返回每个样本的预测标签
        predictions = np.array([Counter(labels).most_common(1)[0][0] for labels in k_nearest_labels])

        return predictions

    def score(self, X, y):
        """
        计算模型的准确率。

        参数：
        - X (numpy.ndarray): 测试数据，形状为 (n_samples, n_features)。
        - y (numpy.ndarray): 测试标签，形状为 (n_samples,)。

        返回：
        - float: 准确率，0 到 1 之间。
        """
        y_pred = self.predict(X)
        return np.mean(y_pred == y)  # 返回预测标签与真实标签相等的比例


# 示例：使用优化后的 KNN 进行分类
if __name__ == "__main__":
    from sklearn.datasets import make_classification

    # 创建示例数据
    X, y = make_classification(n_samples=100, n_features=2, n_classes=2, random_state=42)

    # 初始化 KNN 模型，选择邻居数为 3
    knn = KNearestNeighbors(k=3)

    # 训练模型
    knn.fit(X, y)

    # 预测新数据
    predictions = knn.predict(X)

    # 输出预测结果
    print("预测标签:", predictions)

    # 计算准确率
    accuracy = knn.score(X, y)
    print(f"模型准确率: {accuracy * 100:.2f}%")

    # 可视化数据和预测结果
    plt.scatter(X[:, 0], X[:, 1], c=predictions, cmap='viridis', marker='o')
    plt.title("KNN Classification Results")
    plt.show()
