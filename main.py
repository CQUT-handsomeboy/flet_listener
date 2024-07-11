import flet as ft
import base64
import cv2
import numpy as np
import asyncio
import json
import os
import zmq

from icecream import ic
from threading import Thread
from time import sleep

import subprocess
import pyaudio

from utils import *

is_audio_playing = False


def play_audio():
    # 设置ffmpeg命令行参数以从RTSP流中提取音频
    ff_cmd = [
        "ffmpeg",
        "-i",
        rtsp_url,  # 请将此处的URL替换为实际的RTSP流地址
        "-acodec",
        "pcm_s16le",  # 使用pcm_s16le编码，这是pyaudio支持的格式之一
        "-f",
        "s16le",  # 设置输出格式为s16le
        "-ar",
        "44100",  # 设置采样率为44100Hz，这是常见的音频采样率
        "-ac",
        "1",  # 单声道输出
        "-",  # 输出到标准输出
    ]

    # 初始化PyAudio
    p = pyaudio.PyAudio()

    # 打开一个音频流用于播放
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)

    # 使用subprocess.Popen启动ffmpeg进程，通过管道读取音频数据
    ffmpeg_process = subprocess.Popen(
        ff_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
    )
    # 持续读取ffmpeg输出的数据并播放
    while is_audio_playing:
        data = ffmpeg_process.stdout.read(1024)
        if not data:
            break
        stream.write(data)

    # 清理工作
    stream.stop_stream()
    stream.close()
    p.terminate()

    # 确保ffmpeg进程也被正确终止
    ffmpeg_process.terminate()
    ffmpeg_process.wait()


audio_play_thread = Thread(target=play_audio)


class RTSP_VideoPlayer(ft.UserControl):
    def __init__(self):
        super().__init__()

    def did_mount(self):
        self.update_timer()

    def update_timer(self):
        global cap, is_audio_playing, audio_play_thread
        while True:
            ret, frame = cap.read()
            if ret:
                # 正确以后执行的代码
                if not audio_play_thread.is_alive():
                    is_audio_playing = True
                    audio_play_thread = Thread(target=play_audio)
                    audio_play_thread.start()

                decode_imb64 = self._npFrame2base64Img(frame)
                self.img.src_base64 = decode_imb64
                self.update()
                continue

            # 错误以后执行的代码
            cap.release()
            cap = cv2.VideoCapture(rtsp_url)
            sleep(1)

    def build(self):
        np_img = np.zeros((384, 512, 3))
        base64_img = self._npFrame2base64Img(np_img)
        self.img = ft.Image(
            src_base64=base64_img, border_radius=ft.border_radius.all(20)
        )
        return self.img

    def will_unmount(self):
        return super().will_unmount()

    def _npFrame2base64Img(self, frame: np.array):
        _, im_arr = cv2.imencode(".png", frame)
        im_b64 = base64.b64encode(im_arr)
        decode_imb64 = im_b64.decode("utf-8")
        return decode_imb64


card = lambda title, text: ft.Card(
    content=ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    title,
                    size=25,
                    weight=ft.FontWeight.W_500,
                    font_family="MiSans",
                ),
                ft.Text(text, size=15, font_family="MiSans"),
            ],
            scroll=ft.ScrollMode.HIDDEN,
        ),
        width=400,
        height=250,
        padding=25,
    ),
)


def main(page: ft.Page):
    column = ft.Column(
        [], scroll=ft.ScrollMode.ALWAYS, width=400, height=800, spacing=2
    )

    section = ft.Container(
        margin=ft.margin.only(bottom=40),
        content=ft.Row(
            [
                RTSP_VideoPlayer(),
                ft.Container(
                    padding=20,
                    margin=20,
                    border_radius=ft.border_radius.all(10),
                    content=column,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    def add_cards():
        while True:
            message = socket.recv()
            m = message.decode("utf-8")
            try:
                c = json.loads(m)
            except json.JSONDecodeError:
                socket.send_string("error")
                continue
            socket.send_string("successfully")
            column.controls.append(
                card(
                    c["title"],
                    c["text"],
                )
            )
            page.update()

    page.run_thread(add_cards)

    page.padding = 20
    page.theme_mode = ft.ThemeMode.DARK
    page.window_full_screen = True
    page.add(
        section,
    )


def run_server():
    server_process = subprocess.Popen(["python", "./run_server.py"], shell=True)
    server_process.wait()


if __name__ == "__main__":
    # 加载配置文件
    configs = ConfigLoader().configs
    rtsp_url = configs["rtsp_url"]
    zeromq_port = configs["zeromq_port"]

    cap = cv2.VideoCapture(rtsp_url)

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{zeromq_port}")

    # 运行whisper_live的后端服务器
    # server_proc = Process(target=run_server)
    # server_proc.start()

    try:
        ft.app(main)
    finally:
        app_running = False
        socket.close()
        cap.release()
        is_audio_playing = False
        if audio_play_thread.is_alive():
            audio_play_thread.join()
