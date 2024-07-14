"""
模型权重文件，请自行下载，然后修改configs.json中的参数
"""

import shutil
import subprocess
import sys
import numpy as np
import sherpa_onnx

from utils import ConfigLoader, assert_file_exists


def create_recognizer():
    recognizer = sherpa_onnx.OnlineRecognizer.from_transducer(
        tokens=configs.tokens,
        encoder=configs.encoder,
        decoder=configs.decoder,
        joiner=configs.joiner,
        num_threads=1,
        sample_rate=16000,
        feature_dim=80,
        decoding_method="greedy_search",
        enable_endpoint_detection=True,
        rule1_min_trailing_silence=2.4,
        rule2_min_trailing_silence=1.2,
        rule3_min_utterance_length=300,  # it essentially disables this rule
        hotwords_file=configs.hotwords_file,
        hotwords_score=1.5,  # 默认
    )
    return recognizer


def main():

    assert_file_exists(configs.encoder)
    assert_file_exists(configs.decoder)
    assert_file_exists(configs.joiner)
    assert_file_exists(configs.tokens)

    recognizer = create_recognizer()

    ffmpeg_cmd = [
        "ffmpeg",
        "-i",
        configs.rtmp_url,
        "-f",
        "s16le",
        "-acodec",
        "pcm_s16le",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-",
    ]

    process = subprocess.Popen(
        ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
    )

    frames_per_read = 1600  # 0.1 second

    stream = recognizer.create_stream()

    last_result = ""

    print("Started!")

    seg_id = 1
    temp_string = ""
    while True:
        # *2 because int16_t has two bytes
        data = process.stdout.read(frames_per_read * 2)
        if not data:
            break

        samples = np.frombuffer(data, dtype=np.int16)
        samples = samples.astype(np.float32) / 32768
        stream.accept_waveform(16000, samples)

        while recognizer.is_ready(stream):
            recognizer.decode_stream(stream)

        is_endpoint = recognizer.is_endpoint(stream)

        result = recognizer.get_result(stream)

        # if result and (last_result != result):

        if not result or last_result == result:
            continue

        if last_result in result:
            X = result[len(last_result) :]
        else:
            X = result
        
        if seg_id % configs.tokenization_time == 0:
            print(temp_string) # 此处将结果发送给分词工具
            temp_string = ""
        
        temp_string += X
        seg_id += 1
            
        last_result = result

        if is_endpoint:
            recognizer.reset(stream)


if __name__ == "__main__":

    configs = ConfigLoader(
        configs_items=(
            "decoder",
            "encoder",
            "joiner",
            "tokens",
            "rtmp_url",
            "hotwords_file",
            "tokenization_time"
        )
    )
    

    if shutil.which("ffmpeg") is None:
        sys.exit("安装FFMPEG")
    main()
