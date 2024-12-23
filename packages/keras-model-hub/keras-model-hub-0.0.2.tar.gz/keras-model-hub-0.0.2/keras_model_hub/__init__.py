try:
    from keras.models import Model
    from keras.layers import Layer, Dense, Conv1D, MaxPooling1D, GlobalMaxPooling1D, concatenate, Reshape
except ImportError:
    from tensorflow.python.keras.model import Model
    from tensorflow.python.keras.layers import Layer, Dense, Conv1D, MaxPooling1D, GlobalMaxPooling1D, concatenate, Reshape

__all__ = ['TextCNN', 'TextCNNLayer', 'TextCNNModel', 'TextCNN2D', 'TextCNN2DModel']


class TextCNN(Layer):
    """
    TextCNN 层类，继承自 Layer。
    该层主要用于文本分类等自然语言处理任务，通过不同大小的卷积核捕捉文本中的不同长度的特征，
    并使用最大池化操作保留最显著的特征。

    参数:
    - units: int, 输出单元的数量。
    - filters: int, 卷积核的数量。
    - kernel_sizes: tuple, 卷积核的大小，默认为 (2, 3, 4)，表示有三种不同大小的卷积核。
    - **kwargs: 其他传递给 Layer 类的参数。
    """
    def __init__(self, units: int, filters: int = 32, kernel_sizes=(2, 3, 4), activation='softmax', **kwargs):
        super().__init__(**kwargs)
        # 初始化卷积层列表，为每个 kernel_size 创建一个 Conv1D 层
        self.convs = [Conv1D(filters=filters, kernel_size=k, strides=1, padding='same') for k in kernel_sizes]
        # 初始化全局最大池化层，用于提取每个卷积层输出的重要特征
        self.pooling = GlobalMaxPooling1D()
        self.fc = Dense(units, activation=activation)
    
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
        out = concatenate(out, axis=-1)
        return self.fc(out)
    

class TextCNNLayer(Layer):
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
        self.pooling = MaxPooling1D()
    
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
    

class TextCNNModel(Model):
    """
    TextCNN 层类，继承自 Layer。
    该层主要用于文本分类等自然语言处理任务，通过不同大小的卷积核捕捉文本中的不同长度的特征，
    并使用最大池化操作保留最显著的特征。

    参数:
    - units: int, 输出单元的数量。
    - filters: int, 卷积核的数量。
    - kernel_sizes: tuple, 卷积核的大小，默认为 (2, 3, 4)，表示有三种不同大小的卷积核。
    - activation: Any, 激活函数的名称，默认为 'softmax'。
    - **kwargs: 其他传递给 Layer 类的参数。
    """
    def __init__(self, units: int, filters: int = 32, kernel_sizes=(2, 3, 4), activation='softmax', **kwargs):
        super().__init__(**kwargs)
        self.model = TextCNN(units, filters, kernel_sizes, activation)
    
    def call(self, inputs):
        """
        TextCNN 的调用方法，执行前向传播。

        参数:
        - inputs: 输入张量，通常是文本数据的词嵌入表示。

        返回:
        - 输出张量，是所有卷积核输出的连接，代表输入文本的高级特征。
        """
        return self.model(inputs)


class TextCNN2D(Layer):
    """
    TextCNN 层类，继承自 Layer。
    该层主要用于文本分类等自然语言处理任务，通过不同大小的卷积核捕捉文本中的不同长度的特征，
    并使用最大池化操作保留最显著的特征。

    参数:
    - embed_dim: int, 词嵌入的维度。
    - units: int, 输出单元的数量。
    - filters: int, 卷积核的数量。
    - kernel_sizes: tuple, 卷积核的大小，默认为 (2, 3, 4)，表示有三种不同大小的卷积核。
    - **kwargs: 其他传递给 Layer 类的参数。
    """
    def __init__(self, embed_dim: int, units: int, hidden_size: int = 128, filters: int = 32, kernel_sizes=(2, 3, 4), activation='softmax', **kwargs):
        super().__init__(**kwargs)
        self.linear = Dense(hidden_size, activation='relu')
        self.reshape = Reshape((-1, embed_dim))
        # 初始化卷积层列表，为每个 kernel_size 创建一个 Conv1D 层
        self.convs = [Conv1D(filters=filters, kernel_size=k, strides=1, padding='same') for k in kernel_sizes]
        # 初始化全局最大池化层，用于提取每个卷积层输出的重要特征
        self.pooling = GlobalMaxPooling1D()
        self.fc = Dense(units, activation=activation)
    
    def call(self, inputs):
        """
        TextCNN 的调用方法，执行前向传播。

        参数:
        - inputs: 输入张量，通常是文本数据的词嵌入表示。

        返回:
        - 输出张量，是所有卷积核输出的连接，代表输入文本的高级特征。
        """
        out = self.linear(inputs)
        out = self.reshape(out)
        # 对每个卷积层的输出应用最大池化，然后将所有结果拼接成一个向量输出
        out = [self.pooling(conv(out)) for conv in self.convs]
        out = concatenate(out, axis=-1)
        return self.fc(out)


class TextCNN2DModel(Model):
    """
    TextCNN 层类，继承自 Layer。
    该层主要用于文本分类等自然语言处理任务，通过不同大小的卷积核捕捉文本中的不同长度的特征，
    并使用最大池化操作保留最显著的特征。

    参数:
    - embed_dim: int, 词嵌入的维度。
    - units: int, 输出单元的数量。
    - filters: int, 卷积核的数量。
    - kernel_sizes: tuple, 卷积核的大小，默认为 (2, 3, 4)，表示有三种不同大小的卷积核。
    - **kwargs: 其他传递给 Layer 类的参数。
    """
    def __init__(self, embed_dim: int, units: int, hidden_size: int = 128, filters: int = 32, kernel_sizes=(2, 3, 4), activation='softmax', **kwargs):
        super().__init__(**kwargs)
        self.model = TextCNN2D(embed_dim, units, hidden_size, filters, kernel_sizes, activation=activation)
    
    def call(self, inputs):
        """
        TextCNN 的调用方法，执行前向传播。

        参数:
        - inputs: 输入张量，通常是文本数据的词嵌入表示。

        返回:
        - 输出张量，是所有卷积核输出的连接，代表输入文本的高级特征。
        """
        return self.model(inputs)
