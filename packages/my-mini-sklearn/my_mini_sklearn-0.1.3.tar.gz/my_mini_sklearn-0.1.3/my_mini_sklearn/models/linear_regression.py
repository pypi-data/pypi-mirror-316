import numpy as np


class LinearRegression:
    """
    一个使用最小二乘法的简单线性回归模型，支持岭回归（L2 正则化）。

    方法：
    - fit(X, y): 将模型拟合到训练数据。
    - predict(X): 使用训练好的模型进行预测。
    - score(X, y): 计算模型的 R-squared 得分。
    - get_params(), set_params(): 用于获取和设置模型的参数。

    属性：
    - coef_ : ndarray，形状为 (n_features,)，模型的系数。
    - intercept_ : float，模型的截距。
    """

    def __init__(self, alpha=0.0, fit_intercept=True):
        """
        初始化线性回归模型，支持正则化。

        参数：
        - alpha : float，默认值为0，正则化参数（岭回归的系数）。
        - fit_intercept : bool，默认值为 True，是否计算截距。
        """
        self.alpha = alpha  # 正则化参数
        self.fit_intercept = fit_intercept
        self.coef_ = None  # 模型的系数
        self.intercept_ = None  # 模型的截距

    def fit(self, X, y):
        """
        使用最小二乘法拟合线性回归模型，并支持岭回归。

        参数：
        - X : ndarray，形状为 (n_samples, n_features)，训练数据的输入特征。
        - y : ndarray，形状为 (n_samples,)，训练数据的目标值。

        返回：
        - self : 返回模型本身。
        """
        # 输入数据检查
        X, y = self._check_input(X, y)

        # 在 X 中加入一列全为 1 的数据，用于截距项
        if self.fit_intercept:
            X_b = np.c_[np.ones((X.shape[0], 1)), X]  # 加一列1
        else:
            X_b = X

        if self.alpha > 0:
            # 带正则化的正规方程：(X^T * X + alpha * I)^(-1) * X^T * y
            I = np.eye(X_b.shape[1])  # 单位矩阵
            if self.fit_intercept:
                I[0, 0] = 0  # 不对截距项正则化
            theta_best = np.linalg.inv(X_b.T.dot(X_b) + self.alpha * I).dot(X_b.T).dot(y)
        else:
            # 无正则化，使用普通最小二乘法
            theta_best = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)

        # 存储截距和系数
        if self.fit_intercept:
            self.intercept_ = theta_best[0]
            self.coef_ = theta_best[1:]
        else:
            self.intercept_ = 0
            self.coef_ = theta_best

        return self

    def predict(self, X):
        """
        使用训练好的线性回归模型进行预测。

        参数：
        - X : ndarray，形状为 (n_samples, n_features)，测试数据的输入特征。

        返回：
        - y_pred : ndarray，形状为 (n_samples,)，预测的目标值。
        """
        X, _ = self._check_input(X)  # 检查输入数据
        return X.dot(self.coef_) + self.intercept_

    def score(self, X, y):
        """
        计算 R-squared 得分，用于评估模型性能。

        参数：
        - X : ndarray，形状为 (n_samples, n_features)，测试数据的输入特征。
        - y : ndarray，形状为 (n_samples,)，真实的目标值。

        返回：
        - score : float，R-squared 得分，表示模型解释数据的能力。
        """
        y_pred = self.predict(X)
        total_variance = ((y - y.mean()) ** 2).sum()  # 总方差
        residual_variance = ((y - y_pred) ** 2).sum()  # 残差方差
        return 1 - residual_variance / total_variance

    def _check_input(self, X, y=None):
        """
        检查输入数据的有效性，确保 X 和 y 是 numpy 数组。

        参数：
        - X : ndarray，输入特征数据。
        - y : ndarray，可选参数，目标值数据。

        返回：
        - (X, y) : 经过检查后的 numpy 数组格式的数据。
        """
        X = np.asarray(X)
        if X.ndim != 2:
            raise ValueError("X should be a 2D array.")

        if y is not None:
            y = np.asarray(y)
            if y.ndim != 1:
                raise ValueError("y should be a 1D array.")
            if X.shape[0] != y.shape[0]:
                raise ValueError("X and y must have the same number of samples.")

        return X, y

    def get_params(self, deep=True):
        """
        获取模型的参数。
        """
        return {"alpha": self.alpha, "fit_intercept": self.fit_intercept}

    def set_params(self, **params):
        """
        设置模型的参数。
        """
        for key, value in params.items():
            setattr(self, key, value)
        return self


