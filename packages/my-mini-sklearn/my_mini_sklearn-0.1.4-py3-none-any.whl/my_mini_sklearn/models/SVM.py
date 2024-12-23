import numpy as np

class SVM:
    """
    支持向量机（SVM）实现类，支持线性不可分的软间隔情况，并可通过核函数扩展到非线性问题。

    该类实现了支持向量机（SVM）算法，适用于线性不可分问题。SVM的目标是通过最大化间隔来找到最佳分隔超平面，同时考虑到误分类的惩罚。支持核方法的使用，使得SVM能够解决非线性可分的问题。

    方法：
    - linear_kernel(x1, x2): 线性核函数
    - polynomial_kernel(x1, x2, degree): 多项式核函数
    - rbf_kernel(x1, x2, gamma): 径向基核函数（RBF）
    - fit(X, y): 训练模型，通过梯度下降法优化软间隔
    - predict(X): 使用训练好的模型进行预测
    """

    def __init__(self, kernel=None, learning_rate=0.001, lambda_param=0.01, n_iters=1000, C=1.0):
        """
        初始化 SVM 模型

        参数：
        - kernel: 核函数，用于非线性映射，默认 None 表示线性核
        - learning_rate: 学习率，用于梯度下降优化
        - lambda_param: 正则化参数，用于控制模型复杂度
        - n_iters: 最大迭代次数
        - C: 惩罚参数，用于平衡间隔最大化与误分类惩罚
        """
        self.kernel = kernel if kernel is not None else self.linear_kernel  # 默认线性核
        self.learning_rate = learning_rate
        self.lambda_param = lambda_param
        self.n_iters = n_iters
        self.C = C
        self.w = None  # 权重向量
        self.b = None  # 偏置项
        self.alpha = None  # 拉格朗日乘子（用于核方法）

    @staticmethod
    def linear_kernel(x1, x2):
        """线性核函数"""
        return np.dot(x1, x2)

    @staticmethod
    def polynomial_kernel(x1, x2, degree=3):
        """多项式核函数"""
        return (1 + np.dot(x1, x2)) ** degree

    @staticmethod
    def rbf_kernel(x1, x2, gamma=0.5):
        """径向基核函数 (RBF)"""
        return np.exp(-gamma * np.linalg.norm(x1 - x2) ** 2)

    def fit(self, X, y):
        """
        训练 SVM 模型，使用梯度下降法优化软间隔。

        参数：
        - X: 特征矩阵，形状为 (n_samples, n_features)
        - y: 标签向量，形状为 (n_samples,)
          标签值必须为 -1 或 1
        """
        n_samples, n_features = X.shape

        # 初始化权重和偏置
        self.w = np.zeros(n_features)
        self.b = 0

        # 梯度下降优化
        for _ in range(self.n_iters):
            for idx, x_i in enumerate(X):
                # 核函数计算决策值
                if callable(self.kernel):
                    decision = y[idx] * (np.dot(self.w, x_i) - self.b)
                else:
                    decision = y[idx] * (self.kernel(x_i, x_i) - self.b)

                condition = decision >= 1

                if condition:
                    # 正例：没有违反间隔条件
                    dw = self.lambda_param * self.w
                    db = 0
                else:
                    # 反例：违反间隔条件，添加软间隔惩罚
                    dw = self.lambda_param * self.w - self.C * y[idx] * x_i
                    db = -self.C * y[idx]

                # 更新权重和偏置
                self.w -= self.learning_rate * dw
                self.b -= self.learning_rate * db

    def predict(self, X):
        """
        使用训练好的 SVM 模型进行预测

        参数：
        - X: 特征矩阵，形状为 (n_samples, n_features)

        返回：
        - 预测标签，形状为 (n_samples,)，值为 -1 或 1
        """
        if callable(self.kernel):
            decision_function = np.dot(X, self.w) - self.b
        else:
            decision_function = [self.kernel(x, self.w) - self.b for x in X]
        return np.sign(decision_function)

# 示例：使用线性不可分数据进行训练和预测
if __name__ == "__main__":
    # 创建线性不可分的示例数据
    X = np.array([[1, 2], [2, 3], [3, 3], [2, 1], [3, 2], [1, 1], [2, 2.5], [3, 1.5]])
    y = np.array([1, 1, 1, -1, -1, -1, 1, -1])

    # 初始化 SVM 模型，使用径向基核（RBF）
    svm = SVM(kernel=SVM.rbf_kernel, learning_rate=0.001, lambda_param=0.01, n_iters=1000, C=1.0)

    # 训练模型
    svm.fit(X, y)

    # 输出权重和偏置
    print("权重向量 (w):", svm.w)
    print("偏置项 (b):", svm.b)

    # 测试预测
    predictions = svm.predict(X)
    print("预测结果:", predictions)

    # 比较真实值与预测值
    print("真实标签:", y)
