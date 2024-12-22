import numpy as np


class CrossValidation:
    """实现k折交叉验证的类"""

    def __init__(self, n_splits=5):
        """
        Parameters:
        - n_splits : int, 默认值为5，交叉验证的折数
        """
        self.n_splits = n_splits

    def split(self, X):
        """
        手动实现KFold分割。

        Parameters:
        - X : ndarray, 特征数据

        Returns:
        - folds : list of tuple, 每个元素为一个包含训练索引和测试索引的元组
        """
        n_samples = len(X)
        indices = np.arange(n_samples)
        np.random.shuffle(indices)  # 打乱数据顺序
        fold_sizes = n_samples // self.n_splits  # 每折的数据大小
        folds = []

        for i in range(self.n_splits):
            test_indices = indices[i * fold_sizes:(i + 1) * fold_sizes]
            train_indices = np.setdiff1d(indices, test_indices)
            folds.append((train_indices, test_indices))

        return folds

    def _accuracy_score(self, y_true, y_pred):
        """
        计算准确率
        :param y_true: 真实标签
        :param y_pred: 预测标签
        :return: 准确率
        """
        return np.mean(np.array(y_true) == np.array(y_pred))

    def _r2_score(self, y_true, y_pred):
        """
        计算R2分数
        :param y_true: 真实值
        :param y_pred: 预测值
        :return: R2分数
        """
        ss_total = np.sum((y_true - np.mean(y_true))**2)  # 总平方和
        ss_residual = np.sum((y_true - y_pred)**2)        # 残差平方和
        return 1 - ss_residual / ss_total

    def cross_val_score(self, model, X, y, scoring="accuracy"):
        """
        计算交叉验证的分数。

        Parameters:
        - model : 需要评估的模型
        - X : ndarray, 特征数据
        - y : ndarray, 目标数据
        - scoring : str, 评分标准，支持"accuracy"和"r2"

        Returns:
        - scores : list, 每折的得分
        """
        folds = self.split(X)
        scores = []

        for train_index, test_index in folds:
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]

            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            if scoring == "accuracy":
                score = self._accuracy_score(y_test, y_pred)
            elif scoring == "r2":
                score = self._r2_score(y_test, y_pred)
            else:
                raise ValueError(f"Unsupported scoring method: {scoring}")

            scores.append(score)

        return scores