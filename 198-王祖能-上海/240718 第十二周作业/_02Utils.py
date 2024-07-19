'''
定义数据预处理的工具函数
'''
import matplotlib.image as mpimg
import numpy as np
import tensorflow as tf
# from tensorflow.python.ops import array_ops  # 未使用


def load_img(path):  # 按短边大小的正方形截取图片中心位置
    img = mpimg.imread(path)  # 读取rgb图片
    short_edge = min(img.shape[0], img.shape[1])
    delta_x = int((img.shape[1] - short_edge)/2)
    delta_y = int((img.shape[0] - short_edge)/2)
    crop_img = img[delta_y:short_edge+delta_y, delta_x:short_edge+delta_x]
    return crop_img


def resize_img(img, size, method=tf.image.ResizeMethod.BILINEAR, align_corner=False):
    with tf.name_scope('resize_img'):
        # 像操作系统文件夹，不同的顶层文件夹下，可以有同名文件夹。不同的命名空间下，可以有名字相同的变量。
        # tf.name_scope 主要结合 tf.Variable() 来使用，方便参数命名管理。
        img = tf.expand_dims(img, axis=0)  # 在某个维度前增加一个维度
        ''' 
        't2' is a tensor of shape [2, 3, 5]
        tf.shape(tf.expand_dims(t2, 0))  # [1, 2, 3, 5]
        tf.shape(tf.expand_dims(t2, 3))  # [2, 3, 5, 1]
        '''
        img = tf.image.resize_images(img, size, method, align_corner)
        '''
        method图片形状调整方法：ResizeMethod.BILINEAR：双线性插值，ResizeMethod.NEAREST_NEIGHBOR：最临近插值，ResizeMethod.BICUBIC：双三次插值，ResizeMethod.AREA：区域插值
        align_corners布尔型，为True时，输入与输出的四个角像素点中心对齐，保留四个角
        '''
        img = tf.reshape(img, tf.stack([-1, size[0], size[1], 3]))  # 张量堆叠成[-1, h, w, 3]传入reshape
        return img


def print_prob(prob, file_path):
    synset = [L.strip() for L in open(file_path).readlines()]  # 打开文件后按行读取，strip字符串方法，去除前导和尾随空白字符。
    pred = np.argsort(prob)[::-1]  # 将概率从大到小排列序号的结果存入pred
    top1 = synset[pred[0]]  # 概率最大的那个序号，回溯到标签信息的对应为止
    print('top1:', top1, prob[pred[0]])  # 输出最大标签，和概率
    top5 = [(synset[pred[i]], prob[pred[i]]) for i in range(5)]
    print('top5:', top5)
    return top1
