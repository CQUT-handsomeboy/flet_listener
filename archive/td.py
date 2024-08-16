import pandas as pd

time_caption = {
    2: "各位评委大家好！",
    7: "我们的作品名称是智领未来，智眸教育追踪摄像系统。",
    14: "本作品主要针对教育场景，研发一款智能追踪摄像系统。",
    19: "在边缘计算设备上使用深度学习目标检测算法，",
    27: "实现摄像头对教师和学生进行检测，控制舵机完成实时追踪。",
    35: "同时将摄像头采集到的画面与麦克风采集的音频信息传输给客户端。",
    43: "该系统创新性地集成了边缘计算、流媒体传输、实时语音转文字等技术，",
    46: "提升了教学质量与互动体验。",
    53: "事实上，您现在看到的，正是我们软件的基本操作界面。",
    57: "现在向您介绍我们软件的基本功能。",
    67: "在客户端收到摄像头实时传输过来的音频时，会通过FunASR实时语音转录工具将结果存储为队列，",
    74: "输送给NLP工具进行分词，然后将结果放入我们的Redis数据库中查询释义，",
    82: "正如您看到的这样，我们的客户端已经展示出先前所提到所有术语的释义。",
    86: "接下来，我们将为您展示我们客户端的其他功能。",
}

time_entry = {
    18: (
        "边缘计算",
        "边缘运算（英语：），是一种分散式运算的架构，将应用程式、数据资料与服务的运算，由网路中心节点，移往网路逻辑上的边缘节点来处理。边缘运算将原本完全由中心节点处理大型服务加以分解，切割成更小与更容易管理的部份，分散到边缘节点去处理。边缘节点更接近于用户终端装置，可以加快资料的处理与传送速度，减少延迟。在这种架构下，资料的分析与知识的产生，更接近于数据资料的来源，因此更适合处理大数据。",
    ),
    19: (
        "深度学习",
        "又名人工神经网络，在机器学习和认知科学领域，是一种模仿生物神经网络（动物的中樞神經系統，特别是大脑）的结构和功能的数学模型或计算模型，用于对函数进行估计或近似。神经网络由大量的人工神经元联结进行计算。大多数情况下人工神经网络能在外界信息的基础上改变内部结构，是一种自适应系统，通俗地讲就是具备学习功能。现代神经网络是一种非线性统计性数据建模工具，神经网络通常是过一个基于数学统计学类型的学习方法（learning method）得以优化，所以也是数学统计学方法的一种实际应用，过统计学的标准数学方法我们能够得到大量的可以用函数来表达的局部结构空间，另一方面在人工智能学的人工感知领域，我们过数学统计学的应用可以来做人工感知方面的决定问题（也就是说过统计学的方法，人工神经网络能够类似人一样具有简单的决定能力和简单的判断能力），这种方法比起正式的逻辑学推理演算更具有优势。",
    ),
    21: (
        "目标检测",
        "目标检测（Object Detection）的任务是找出图像中所有感兴趣的目标（物体），确定它们的类别和位置，是计算机视觉领域的核心问题之一。由于各类物体有不同的外观、形状和姿态，加上成像时光照、遮挡等因素的干扰，目标检测一直是计算机视觉领域最具有挑战性的问题。",
    ),
    27: (
        "舵机",
        "舵机是指在自动驾驶仪中操纵飞机舵面（操纵面）转动的一种执行部件。分有：①电动舵机，由电动机、传动部件和离合器组成。接受自动驾驶仪的指令信号而工作，当人工驾驶飞机时，由于离合器保持脱开而传动部件不发生作用。②液压舵机，由液压作动器和旁通活门组成。当人工驾驶飞机时，旁通活门打开，由于作动器活塞两边的液压互相连通而不妨碍人工操纵。此外，还有电动液压舵机，简称“电液舵机”。",
    ),
    43: (
        "流媒体传输技术",
        "流媒体（streaming media）技术，是指将一连串的多媒体数据压缩后，经过互联网分段发送数据，在互联网上即时传输影音，以供用户观赏的一种技术。",
    ),
    44: (
        "实时语音转文字",
        "也被称为自动语音识别（Automatic Speech Recognition，ASR），其目标是将人类的语音中的词汇内容转换为计算机可读的输入，例如按键、二进制编码或者字符序列。与说话人识别及说话人确认不同，后者尝试识别或确认发出语音的说话人而非其中所包含的词汇内容。",
    ),
    67: (
        "FunASR",
        "FunASR是由阿里巴巴开源的基础语音识别工具包，提供多种功能，包括语音识别（ASR）、语音端点检测（VAD）、标点恢复、语言模型、说话人验证、说话人分离和多人对话语音识别等。FunASR提供了便捷的脚本和教程，支持预训练好的模型的推理与微调。",
    ),
    74: (
        "NLP",
        "自然语言处理是计算机科学和人工智能 （AI） 的一个子领域，它使用机器学习使计算机能够理解人类语言并与之交流。",
    ),
    75: (
        "Redis数据库",
        "Redis（Remote Dictionary Server）是一个使用ANSI C编写的支持网络、基于内存、分布式、可选持久性的键值对存储数据库。根据月度排行网站DB-Engines.com的数据，Redis是最流行的键值对存储数据库。",
    ),
}


captions_df = pd.DataFrame(list(time_caption.items()), columns=["Time (seconds)", "Content"])
entry_df = pd.DataFrame(list(time_entry.items()), columns=["Time (seconds)", "Content"])

VIDEO_LENGTH = 87


def limit(start, end):
    # 限幅
    if start > VIDEO_LENGTH:
        start = VIDEO_LENGTH
    if start < 0:
        start = 0
    if end > VIDEO_LENGTH:
        end = VIDEO_LENGTH
    if end < 0:
        end = 0
    return start, end


def caption_select(start_seconds, end_seconds):
    start_seconds, end_seconds = limit(start_seconds, end_seconds)
    s = captions_df[
        (captions_df["Time (seconds)"] >= start_seconds) & (captions_df["Time (seconds)"] <= end_seconds)
    ]
    if s.__len__():
        return s.iloc[0, 1]
    else:
        return ""
    
def entry_select(start_seconds, end_seconds):
    start_seconds, end_seconds = limit(start_seconds, end_seconds)
    s = entry_df[
        (entry_df["Time (seconds)"] >= start_seconds) & (entry_df["Time (seconds)"] <= end_seconds)
    ]
    if s.__len__():
        return s.iloc[0, 1]
    else:
        return None
