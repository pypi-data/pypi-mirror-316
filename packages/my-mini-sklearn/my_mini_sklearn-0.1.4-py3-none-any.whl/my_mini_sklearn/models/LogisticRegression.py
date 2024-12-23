import numpy as np

class LogisticRegression:
    """
    逻辑回归实现类，使用梯度下降进行优化。

    该类实现了逻辑回归模型，使用梯度下降法进行优化，以最小化交叉熵损失函数。逻辑回归常用于二分类任务，其核心思想是利用 Sigmoid 函数将线性模型的输出映射到概率值，并使用梯度下降进行优化。

    方法：
    - fit(X, y): 训练逻辑回归模型。
    - sigmoid(z): Sigmoid 激活函数。
    - predict_proba(X): 计算预测的概率。
    - predict(X): 进行标签预测。
    """

    def __init__(self, learning_rate=0.01, n_iters=1000):
        """
        初始化逻辑回归模型。

        参数：
        - learning_rate (float): 学习率，用于控制每次更新的步长。
        - n_iters (int): 最大迭代次数，指定优化过程中梯度下降的步数。
        """
        self.learning_rate = learning_rate
        self.n_iters = n_iters
        self.weights = None  # 权重向量
        self.bias = None  # 偏置项

    def sigmoid(self, z):
        """
        Sigmoid 激活函数。

        参数：
        - z: 输入值（线性组合的结果）。

        返回：
        - Sigmoid 函数的输出，值范围在 (0, 1) 之间。
        """
        return 1 / (1 + np.exp(-z))

    def fit(self, X, y):
        """
        训练逻辑回归模型，使用梯度下降法优化损失函数。

        参数：
        - X (numpy.ndarray): 特征矩阵，形状为 (n_samples, n_features)。
        - y (numpy.ndarray): 标签向量，形状为 (n_samples,)。
        """
        n_samples, n_features = X.shape

        # 初始化权重和偏置
        self.weights = np.zeros(n_features)
        self.bias = 0

        # 梯度下降优化
        for _ in range(self.n_iters):
            # 计算模型的线性输出 (X * w + b)
            model = np.dot(X, self.weights) + self.bias
            # 计算 Sigmoid 激活后的预测概率
            predictions = self.sigmoid(model)

            # 计算梯度
            dw = (1 / n_samples) * np.dot(X.T, (predictions - y))  # 权重的梯度
            db = (1 / n_samples) * np.sum(predictions - y)  # 偏置的梯度

            # 更新权重和偏置
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def predict_proba(self, X):
        """
        计算预测的概率。

        参数：
        - X (numpy.ndarray): 特征矩阵，形状为 (n_samples, n_features)。

        返回：
        - 概率向量，形状为 (n_samples,)。
        """
        model = np.dot(X, self.weights) + self.bias
        return self.sigmoid(model)

    def predict(self, X):
        """
        使用训练好的模型进行预测，输出二分类标签。

        参数：
        - X (numpy.ndarray): 特征矩阵，形状为 (n_samples, n_features)。

        返回：
        - 预测标签，形状为 (n_samples,)，值为 0 或 1。
        """
        probabilities = self.predict_proba(X)
        return [1 if p > 0.5 else 0 for p in probabilities]


# 示例：使用逻辑回归进行训练和预测
if __name__ == "__main__":
    # 创建示例数据
    X = np.array([[0.1, 1.1], [2.0, 1.9], [1.1, 3.3], [1.5, 0.7], [1.2, 2.2], [1.4, 1.0]])
    y = np.array([0, 1, 1, 0, 1, 0])

    # 初始化逻辑回归模型
    lr = LogisticRegression(learning_rate=0.1, n_iters=1000)

    # 训练模型
    lr.fit(X, y)

    # 输出权重和偏置
    print("权重 (weights):", lr.weights)
    print("偏置 (bias):", lr.bias)

    # 测试预测
    predictions = lr.predict(X)
    print("预测结果:", predictions)

    # 比较真实值与预测值
    print("真实标签:", y)
