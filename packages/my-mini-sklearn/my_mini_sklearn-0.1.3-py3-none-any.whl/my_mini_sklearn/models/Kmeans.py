import numpy as np

import matplotlib.pyplot as plt

class KMeans:
    """
    KMeans 聚类算法实现类。
    """
    def __init__(self, n_clusters=3, max_iters=300, tol=1e-4):
        """
        初始化 KMeans 模型。

        参数：
        - n_clusters: 聚类的数量（即 K 值）。
        - max_iters: 最大迭代次数。
        - tol: 收敛阈值，当中心点变化小于此值时停止迭代。
        """
        self.n_clusters = n_clusters
        self.max_iters = max_iters
        self.tol = tol
        self.centroids = None  # 聚类中心

    def fit(self, X):
        """
        训练 KMeans 模型。

        参数：
        - X: 数据矩阵，形状为 (n_samples, n_features)。
        """
        n_samples, n_features = X.shape

        # 随机初始化聚类中心
        np.random.seed(42)
        random_indices = np.random.choice(n_samples, self.n_clusters, replace=False)
        self.centroids = X[random_indices]

        for i in range(self.max_iters):
            # 1. 分配每个样本到最近的聚类中心
            clusters = self._assign_clusters(X)

            # 2. 计算新的聚类中心
            new_centroids = np.array([X[clusters == k].mean(axis=0) for k in range(self.n_clusters)])

            # 3. 检查收敛条件
            if np.all(np.linalg.norm(self.centroids - new_centroids, axis=1) < self.tol):
                break

            self.centroids = new_centroids

    def predict(self, X):
        """
        使用训练好的 KMeans 模型预测样本所属的聚类。

        参数：
        - X: 数据矩阵，形状为 (n_samples, n_features)。

        返回：
        - 每个样本所属的聚类索引，形状为 (n_samples,)。
        """
        return self._assign_clusters(X)

    def _assign_clusters(self, X):
        """
        将每个样本分配到最近的聚类中心。

        参数：
        - X: 数据矩阵，形状为 (n_samples, n_features)。

        返回：
        - 每个样本所属的聚类索引，形状为 (n_samples,)。
        """
        distances = np.linalg.norm(X[:, np.newaxis] - self.centroids, axis=2)
        return np.argmin(distances, axis=1)

# 示例：使用 KMeans 进行聚类
if __name__ == "__main__":
    from sklearn.datasets import make_blobs
    # 创建示例数据
    X, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.6, random_state=0)

    # 初始化模型
    kmeans = KMeans(n_clusters=4, max_iters=300, tol=1e-4)

    # 训练模型
    kmeans.fit(X)

    # 预测聚类
    clusters = kmeans.predict(X)
    print("聚类中心:\n", kmeans.centroids)
    print("样本的聚类索引:\n", clusters)

    # 可视化结果
    plt.scatter(X[:, 0], X[:, 1], c=clusters, cmap='viridis', marker='o')
    plt.scatter(kmeans.centroids[:, 0], kmeans.centroids[:, 1], s=300, c='red', marker='x')
    plt.title("KMeans Clustering")
    plt.show()
