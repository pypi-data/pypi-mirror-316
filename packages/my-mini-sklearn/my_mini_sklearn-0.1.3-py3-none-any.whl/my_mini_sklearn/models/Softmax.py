import numpy as np


class SoftmaxClassifier:
    """
    基于 Softmax 的多类分类器。
    """

    def __init__(self, input_dim, num_classes, learning_rate=0.01, num_epochs=1000):
        """
        初始化 Softmax 分类器。

        参数：
        - input_dim: 输入特征的维度。
        - num_classes: 类别的数量。
        - learning_rate: 学习率。
        - num_epochs: 训练的迭代次数。
        """
        self.input_dim = input_dim
        self.num_classes = num_classes
        self.learning_rate = learning_rate
        self.num_epochs = num_epochs

        # 初始化权重和偏置
        self.W = np.random.randn(input_dim, num_classes) * 0.01
        self.b = np.zeros((1, num_classes))

    def softmax(self, z):
        """
        计算 softmax 函数。

        参数：
        - z: 输入矩阵，形状为 (n_samples, num_classes)。

        返回：
        - softmax 输出，形状为 (n_samples, num_classes)。
        """
        exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))  # 稳定性优化
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)

    def compute_loss(self, y_pred, y_true):
        """
        计算交叉熵损失。

        参数：
        - y_pred: 预测值，形状为 (n_samples, num_classes)。
        - y_true: 真实标签，形状为 (n_samples, num_classes)（one-hot 编码）。

        返回：
        - 损失值。
        """
        m = y_true.shape[0]
        log_likelihood = -np.log(y_pred[range(m), np.argmax(y_true, axis=1)])
        loss = np.sum(log_likelihood) / m
        return loss

    def forward(self, X):
        """
        前向传播，计算预测值。

        参数：
        - X: 输入数据，形状为 (n_samples, input_dim)。

        返回：
        - 预测值，形状为 (n_samples, num_classes)。
        """
        z = np.dot(X, self.W) + self.b
        return self.softmax(z)

    def backward(self, X, y_true, y_pred):
        """
        反向传播，计算梯度。

        参数：
        - X: 输入数据，形状为 (n_samples, input_dim)。
        - y_true: 真实标签，形状为 (n_samples, num_classes)。
        - y_pred: 预测值，形状为 (n_samples, num_classes)。

        返回：
        - 梯度：权重梯度和偏置梯度。
        """
        m = X.shape[0]
        # 计算梯度
        dZ = y_pred - y_true
        dW = np.dot(X.T, dZ) / m
        db = np.sum(dZ, axis=0, keepdims=True) / m
        return dW, db

    def train(self, X_train, y_train):
        """
        训练 Softmax 分类器。

        参数：
        - X_train: 训练数据，形状为 (n_samples, input_dim)。
        - y_train: 真实标签，形状为 (n_samples, num_classes)（one-hot 编码）。
        """
        for epoch in range(self.num_epochs):
            # 前向传播
            y_pred = self.forward(X_train)

            # 计算损失
            loss = self.compute_loss(y_pred, y_train)

            # 反向传播
            dW, db = self.backward(X_train, y_train, y_pred)

            # 更新权重和偏置
            self.W -= self.learning_rate * dW
            self.b -= self.learning_rate * db

            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Loss: {loss}")

    def predict(self, X):
        """
        预测输入数据的类别。

        参数：
        - X: 输入数据，形状为 (n_samples, input_dim)。

        返回：
        - 预测类别的索引，形状为 (n_samples,)。
        """
        y_pred = self.forward(X)
        return np.argmax(y_pred, axis=1)


# 使用示例：
if __name__ == "__main__":
    # 创建示例数据（假设我们有 4 个特征，3 类）
    X_train = np.random.randn(1000, 4)  # 100 个样本，4 个特征
    y_train = np.zeros((1000, 3))  # 100 个样本，3 类的 one-hot 标签

    # 假设前 50 个样本属于类别 0，接下来的 30 个样本属于类别 1，其余的属于类别 2
    y_train[:300, 0] = 1
    y_train[300:700, 1] = 1
    y_train[700:, 2] = 1

    # 初始化并训练模型
    model = SoftmaxClassifier(input_dim=4, num_classes=3, learning_rate=0.1, num_epochs=1000)
    model.train(X_train, y_train)

    # 测试预测
    predictions = model.predict(X_train)

