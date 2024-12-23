import numpy as np


class SoftmaxClassifier:
    """
    基于 Softmax 的多类分类器。

    该类实现了基于 Softmax 的多类分类算法。Softmax 分类器通过最大化每个类别的预测概率来进行多类分类。它可以通过交叉熵损失函数和梯度下降方法进行训练。

    方法：
    - softmax(z): 计算 softmax 函数，用于将原始的预测值（logits）转换为概率。
    - compute_loss(y_pred, y_true): 计算交叉熵损失，衡量预测值与真实标签之间的差异。
    - forward(X): 前向传播，计算模型的输出。
    - backward(X, y_true, y_pred): 反向传播，计算梯度。
    - train(X_train, y_train): 训练模型，使用梯度下降更新模型参数。
    - predict(X): 根据训练后的模型进行预测，返回预测的类别索引。
    """

    def __init__(self, input_dim, num_classes, learning_rate=0.01, num_epochs=1000):
        """
        初始化 Softmax 分类器。

        参数：
        - input_dim: 输入特征的维度。
        - num_classes: 类别的数量。
        - learning_rate: 学习率，控制模型参数更新的速度。
        - num_epochs: 训练的迭代次数，表示模型在训练集上训练的次数。
        """
        self.input_dim = input_dim
        self.num_classes = num_classes
        self.learning_rate = learning_rate
        self.num_epochs = num_epochs

        # 初始化权重和偏置
        self.W = np.random.randn(input_dim, num_classes) * 0.01  # 权重
        self.b = np.zeros((1, num_classes))  # 偏置

    def softmax(self, z):
        """
        计算 softmax 函数。

        参数：
        - z: 输入矩阵，形状为 (n_samples, num_classes)，表示每个样本在每个类别上的得分。

        返回：
        - softmax 输出，形状为 (n_samples, num_classes)，表示每个样本属于每个类别的概率。
        """
        exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))  # 稳定性优化，防止溢出
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)  # 归一化，得到概率分布

    def compute_loss(self, y_pred, y_true):
        """
        计算交叉熵损失。

        参数：
        - y_pred: 预测值，形状为 (n_samples, num_classes)，表示每个样本在各个类别上的预测概率。
        - y_true: 真实标签，形状为 (n_samples, num_classes)，是 one-hot 编码表示的类别标签。

        返回：
        - 损失值，表示模型预测结果与真实标签之间的差距。
        """
        m = y_true.shape[0]  # 样本数
        log_likelihood = -np.log(y_pred[range(m), np.argmax(y_true, axis=1)])  # 取正确类别的预测概率
        loss = np.sum(log_likelihood) / m  # 平均损失
        return loss

    def forward(self, X):
        """
        前向传播，计算预测值。

        参数：
        - X: 输入数据，形状为 (n_samples, input_dim)，每一行是一个样本，每一列是一个特征。

        返回：
        - 预测值，形状为 (n_samples, num_classes)，表示每个样本在各个类别上的预测概率。
        """
        z = np.dot(X, self.W) + self.b  # 线性变换：W * X + b
        return self.softmax(z)  # 使用 softmax 将线性输出转化为概率

    def backward(self, X, y_true, y_pred):
        """
        反向传播，计算梯度。

        参数：
        - X: 输入数据，形状为 (n_samples, input_dim)，每一行是一个样本，每一列是一个特征。
        - y_true: 真实标签，形状为 (n_samples, num_classes)，one-hot 编码。
        - y_pred: 预测值，形状为 (n_samples, num_classes)，每个样本的类别概率。

        返回：
        - 梯度：返回对权重和偏置的梯度，用于更新模型参数。
        """
        m = X.shape[0]  # 样本数
        # 计算梯度
        dZ = y_pred - y_true  # 计算损失函数对 z 的梯度
        dW = np.dot(X.T, dZ) / m  # 权重梯度
        db = np.sum(dZ, axis=0, keepdims=True) / m  # 偏置梯度
        return dW, db

    def train(self, X_train, y_train):
        """
        训练 Softmax 分类器。

        参数：
        - X_train: 训练数据，形状为 (n_samples, input_dim)，每一行是一个样本，每一列是一个特征。
        - y_train: 真实标签，形状为 (n_samples, num_classes)，one-hot 编码。

        该方法使用梯度下降法通过多次迭代（`num_epochs`）更新权重和偏置，最小化交叉熵损失。
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

            # 每 100 次输出一次损失
            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Loss: {loss}")

    def predict(self, X):
        """
        预测输入数据的类别。

        参数：
        - X: 输入数据，形状为 (n_samples, input_dim)，每一行是一个样本，每一列是一个特征。

        返回：
        - 预测类别的索引，形状为 (n_samples,)，表示每个样本的预测类别。
        """
        y_pred = self.forward(X)  # 获取每个样本的类别概率
        return np.argmax(y_pred, axis=1)  # 选择概率最大的类别作为预测结果


# 使用示例：
if __name__ == "__main__":
    # 创建示例数据（假设我们有 4 个特征，3 类）
    X_train = np.random.randn(1000, 4)  # 1000 个样本，4 个特征
    y_train = np.zeros((1000, 3))  # 1000 个样本，3 类的 one-hot 标签

    # 假设前 300 个样本属于类别 0，接下来的 400 个样本属于类别 1，其余的属于类别 2
    y_train[:300, 0] = 1
    y_train[300:700, 1] = 1
    y_train[700:, 2] = 1

    # 初始化并训练模型
    model = SoftmaxClassifier(input_dim=4, num_classes=3, learning_rate=0.1, num_epochs=1000)
    model.train(X_train, y_train)

    # 测试预测
    predictions = model.predict(X_train)
    print("预测类别:", predictions[:10])  # 输出前 10 个预测结果
