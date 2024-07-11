# :rofl: Welcome to Listener

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

`pycorrector`用于错别字纠正，`opencc`用于繁体字到简体字转换，`jieba`用于分词。

## `zmq_mock_client.py`

ZeroMQ客户端，用于模拟提供卡片数据，在使用运用中，flet客户端，即`main.py`作为一个单独进程运行，而语音转录作为另一个单独进程运行，两者通过ZeroMQ消息队列通信。


# Problems

音频转录文字还没有解决，拟采用`whisper_live`，后端服务运行正常，client时好时坏，但直接运行音频文件而不是流式则一切正常。

[whisper_live 参考链接](https://github.com/collabora/WhisperLive)

现有另一解决方案`FunASR`，提供流式输入，但原生不提供RTSP。

[FunASR 参考链接](https://github.com/modelscope/FunASR)

还有诸多加钱解决方案，调用API，例如[百度](https://ai.baidu.com/ai-doc/SPEECH/qlcirqhz0)，[讯飞](https://www.xfyun.cn/doc/asr/rtasr/API.html)等等。