import numpy as np
import matplotlib.pyplot as plt


# 准确率计算
def accuracy_score(y_true, y_pred):
    """
    计算准确率
    :param y_true: 真实标签
    :param y_pred: 预测标签
    :return: 准确率
    """
    return np.mean(np.array(y_true) == np.array(y_pred))


# 混淆矩阵
def confusion_matrix(y_true, y_pred):
    """
    计算混淆矩阵
    :param y_true: 真实标签
    :param y_pred: 预测标签
    :return: 混淆矩阵（二维数组）
    """
    unique_classes = np.unique(y_true)
    matrix = np.zeros((len(unique_classes), len(unique_classes)), dtype=int)
    class_map = {cls: idx for idx, cls in enumerate(unique_classes)}

    for true, pred in zip(y_true, y_pred):
        matrix[class_map[true], class_map[pred]] += 1

    return matrix


# 精确率、召回率、F1-score
def precision_recall_f1(y_true, y_pred):
    """
    计算每个类别的精确率、召回率和F1-score
    :param y_true: 真实标签
    :param y_pred: 预测标签
    :return: 精确率、召回率和F1-score
    """
    matrix = confusion_matrix(y_true, y_pred)
    precision = np.diag(matrix) / np.sum(matrix, axis=0)
    recall = np.diag(matrix) / np.sum(matrix, axis=1)
    f1_score = 2 * (precision * recall) / (precision + recall)

    return precision, recall, f1_score


# 手动绘制ROC曲线
def plot_roc_curve(y_true, y_scores, classes):
    """
    手动计算并绘制ROC曲线
    :param y_true: 真实标签
    :param y_scores: 预测的概率（每个类别的概率）
    :param classes: 类别标签
    """
    fpr = []
    tpr = []
    thresholds = np.arange(0.0, 1.1, 0.01)  # 从0到1的阈值

    # 获取每个类别的FPR和TPR
    for threshold in thresholds:
        # 根据当前阈值将预测概率转换为预测标签
        y_pred = (y_scores >= threshold).astype(int)

        # 计算TPR和FPR
        tp = np.sum((y_true == 1) & (y_pred == 1))  # True Positive
        fp = np.sum((y_true == 0) & (y_pred == 1))  # False Positive
        tn = np.sum((y_true == 0) & (y_pred == 0))  # True Negative
        fn = np.sum((y_true == 1) & (y_pred == 0))  # False Negative

        tpr_value = tp / (tp + fn)  # True Positive Rate (Recall)
        fpr_value = fp / (fp + tn)  # False Positive Rate

        tpr.append(tpr_value)
        fpr.append(fpr_value)

    # 计算AUC
    auc_value = np.trapz(tpr, fpr)

    # 绘制ROC曲线
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % auc_value)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.show()

    return auc_value


# AUC计算
def roc_auc_score(y_true, y_scores):
    """
    手动计算AUC分数
    :param y_true: 真实标签
    :param y_scores: 预测的概率（每个类别的概率）
    :return: AUC分数
    """
    fpr = []
    tpr = []
    thresholds = np.arange(0.0, 1.1, 0.01)  # 从0到1的阈值

    # 获取每个类别的FPR和TPR
    for threshold in thresholds:
        # 根据当前阈值将预测概率转换为预测标签
        y_pred = (y_scores >= threshold).astype(int)

        # 计算TPR和FPR
        tp = np.sum((y_true == 1) & (y_pred == 1))  # True Positive
        fp = np.sum((y_true == 0) & (y_pred == 1))  # False Positive
        tn = np.sum((y_true == 0) & (y_pred == 0))  # True Negative
        fn = np.sum((y_true == 1) & (y_pred == 0))  # False Negative

        tpr_value = tp / (tp + fn)  # True Positive Rate (Recall)
        fpr_value = fp / (fp + tn)  # False Positive Rate

        tpr.append(tpr_value)
        fpr.append(fpr_value)

    # 计算AUC
    auc_value = np.trapz(tpr, fpr)
    return auc_value
