[![SVG Banners](https://svg-banners.vercel.app/api?type=origin&text1=Welcome%20to%20Listener&text2=😂%20CQUT_handsomeboy&width=800&height=400)](https://github.com/Akshay090/svg-banners)

![Static Badge](https://img.shields.io/badge/License-AGPL3-green) ![Static Badge](https://img.shields.io/badge/Language-Python-red) ![Static Badge](https://img.shields.io/badge/Library-Flet-blue) ![Static Badge](https://img.shields.io/badge/Author-CQUT_handsomeboy-black)

# Quick Start

```shell
$ git clone https://github.com/CQUT-handsomeboy/listener.git
$ cd listener
$ pip install -r requirements.txt
```

# Explanations

## `main.py`

UI采用`flet`，消息队列`Zeromq`(`pyzmq`)收发卡片信息。

拉流视频采用`opencv`，音频采用`ffmpeg`，支持断点重连。

## `configs.json`

设置端口和拉流地址在设置文件`configs.json`中修改。

## `utils.py`

工具函数，加载配置文件，判断文件是否存在。

## `speech_recognition.py`

- 使用Sherpa ONNX库创建语音识别器。
- 通过FFMPEG处理音频流，将其转换为可识别的格式。
- 循环读取音频数据，进行语音识别并输出结果，将会进一步进行分词处理和语音段落检测。

## `participle_words.py`

根据传入的mode参数不同，使用不同的分词模式对文本进行分词。返回一个生成器对象。支持的分词模式有："precise"（精准模式）、"paddle"（paddl模式）、"full"（全模式）、"search_engine"（搜索引擎模式）和"news"（新闻模式）。默认模式为"precise"。使用jieba库的cut或cut_for_search方法进行分词。

## `zmq_mock_client.py`

ZeroMQ客户端，用于模拟提供卡片数据，在使用运用中，flet客户端，即`main.py`作为一个单独进程运行，而语音转录作为另一个单独进程运行，两者通过ZeroMQ消息队列通信。