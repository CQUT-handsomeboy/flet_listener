import flet as ft
import base64
import cv2
import numpy as np
import asyncio

# from icecream import ic
from threading import Thread
from time import sleep

import subprocess
import pyaudio


is_audio_playing = False

rtsp_url = "rtsp://localhost:8554/mystream"
cap = cv2.VideoCapture(rtsp_url)


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
            ],scroll=ft.ScrollMode.HIDDEN
        ),
        width=400,
        height=150,
        padding=10,
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

    async def add_cards():
        for i in range(10):
            column.controls.append(
                card(
                    "棋王",
                    "车开了一会儿，车厢开始平静下来。有水送过来，大家就掏出缸子要水。我旁边的人打了水，说：“谁的棋？收了放缸子。”他很可怜的样子，问：“下棋吗？”要放缸的人说：“反正没意思，来一盘吧。”他就很高兴，连忙码好棋子。对手说：“这横着算怎么回事儿？没法儿看。”他搓着手说：“凑合了，平常看棋的时候，棋盘不等于是横着的？你先走。”对手很老练地拿起棋子儿，嘴里叫着：“当头炮。”他跟着跳上马。对手马上把他的卒吃了，他也立刻用马吃了对方的炮。我看这种简单的开局没有大意思，又实在对象棋不感兴趣，就转了头。",
                )
            )
            page.update()
            await asyncio.sleep(3)

    page.run_task(add_cards)

    page.padding = 20
    page.theme_mode = ft.ThemeMode.DARK
    page.window_full_screen = True
    page.add(
        section,
    )


if __name__ == "__main__":
    try:
        ft.app(main)
    finally:
        cap.release()
        is_audio_playing = False
        if audio_play_thread.is_alive():
            audio_play_thread.join()
