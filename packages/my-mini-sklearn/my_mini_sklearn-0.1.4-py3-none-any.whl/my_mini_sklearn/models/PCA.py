import numpy as np


class PCA:
    """
    主成分分析（PCA）算法实现类。

    PCA（Principal Component Analysis）是一种常用的降维方法，用于将高维数据投影到低维空间，同时尽可能保留数据的方差。该实现基于协方差矩阵的特征值分解，通过选择特征值最大的特征向量来得到主成分。

    方法：
    - fit(X): 训练 PCA 模型，计算主成分。
    - transform(X): 使用训练好的 PCA 模型对数据进行降维。
    - fit_transform(X): 训练 PCA 模型并对数据进行降维，等效于调用 `fit` 和 `transform`。
    """

    def __init__(self, n_components):
        """
        初始化 PCA 模型。

        参数：
        - n_components: 降维后的主成分数量。指定保留的主成分数量，通常选择能解释数据大部分方差的成分数量。
        """
        self.n_components = n_components
        self.components = None  # 主成分矩阵
        self.mean = None  # 数据均值

    def fit(self, X):
        """
        训练 PCA 模型，计算主成分。

        参数：
        - X: 数据矩阵，形状为 (n_samples, n_features)，每一行是一个样本，每一列是一个特征。

        该方法通过计算数据的协方差矩阵，进行特征值分解，并选择最重要的主成分（特征向量）。
        """
        # 1. 计算数据的均值并中心化
        self.mean = np.mean(X, axis=0)
        X_centered = X - self.mean

        # 2. 计算协方差矩阵
        covariance_matrix = np.cov(X_centered, rowvar=False)

        # 3. 计算协方差矩阵的特征值和特征向量
        eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)

        # 4. 按特征值大小排序（从大到小）
        sorted_indices = np.argsort(eigenvalues)[::-1]
        eigenvectors = eigenvectors[:, sorted_indices]

        # 5. 选取前 n_components 个主成分
        self.components = eigenvectors[:, :self.n_components]

    def transform(self, X):
        """
        使用训练好的 PCA 模型对数据进行降维。

        参数：
        - X: 数据矩阵，形状为 (n_samples, n_features)，每一行是一个样本，每一列是一个特征。

        返回：
        - 降维后的数据，形状为 (n_samples, n_components)，表示每个样本在主成分空间中的投影。

        该方法通过将数据投影到主成分上，来实现数据的降维。
        """
        X_centered = X - self.mean
        return np.dot(X_centered, self.components)

    def fit_transform(self, X):
        """
        训练 PCA 模型并对数据进行降维。

        参数：
        - X: 数据矩阵，形状为 (n_samples, n_features)，每一行是一个样本，每一列是一个特征。

        返回：
        - 降维后的数据，形状为 (n_samples, n_components)，表示每个样本在主成分空间中的投影。

        该方法结合了 `fit` 和 `transform` 方法，首先训练模型再进行降维。
        """
        self.fit(X)
        return self.transform(X)


# 示例：使用 PCA 进行数据降维
if __name__ == "__main__":
    # 生成示例数据
    np.random.seed(42)
    X = np.random.rand(100, 5)  # 100 个样本，5 个特征

    # 初始化 PCA 模型
    pca = PCA(n_components=2)

    # 训练模型并进行降维
    X_reduced = pca.fit_transform(X)

    print("降维后的数据:\n", X_reduced)
    print("主成分矩阵:\n", pca.components)
