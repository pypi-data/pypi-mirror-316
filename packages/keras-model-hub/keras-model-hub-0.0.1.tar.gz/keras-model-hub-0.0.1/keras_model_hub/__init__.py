from keras.layers import Layer, Conv1D, GlobalMaxPooling1D, concatenate

__all__ = ['TextCNN']


class TextCNN(Layer):
    """
    TextCNN 层类，继承自 Layer。
    该层主要用于文本分类等自然语言处理任务，通过不同大小的卷积核捕捉文本中的不同长度的特征，
    并使用最大池化操作保留最显著的特征。

    参数:
    - filters: int, 卷积核的数量。
    - kernel_sizes: tuple, 卷积核的大小，默认为 (2, 3, 4)，表示有三种不同大小的卷积核。
    - **kwargs: 其他传递给 Layer 类的参数。
    """
    def __init__(self, filters: int, kernel_sizes=(2, 3, 4), **kwargs):
        super().__init__(**kwargs)
        # 初始化卷积层列表，为每个 kernel_size 创建一个 Conv1D 层
        self.convs = [Conv1D(filters=filters, kernel_size=k, strides=1, padding='same') for k in kernel_sizes]
        # 初始化全局最大池化层，用于提取每个卷积层输出的重要特征
        self.pooling = GlobalMaxPooling1D()
    
    def call(self, inputs):
        """
        TextCNN 的调用方法，执行前向传播。

        参数:
        - inputs: 输入张量，通常是文本数据的词嵌入表示。

        返回:
        - 输出张量，是所有卷积核输出的连接，代表输入文本的高级特征。
        """
        # 对每个卷积层的输出应用最大池化，然后将所有结果拼接成一个向量输出
        out = [self.pooling(conv(inputs)) for conv in self.convs]
        return concatenate(out, axis=-1)
