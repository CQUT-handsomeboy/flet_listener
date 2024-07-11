import jieba

jieba.enable_paddle()

import os
import json
from opencc import OpenCC

from pycorrector import MacBertCorrector


def participle_words(text: str, mode="precise") -> list:
    """
    分词
    """
    match mode:
        case "precise":
            # 精准模式
            seg_list = jieba.cut(text, cut_all=False)
        case "paddle":
            # paddl模式
            seg_list = jieba.cut(text, use_paddle=True)
            pass
        case "full":
            # 全模式
            seg_list = jieba.cut(text, cut_all=True)
            pass
        case "search_engine":
            # 搜索引擎模式
            seg_list = jieba.cut_for_search(text)
            pass
        case "news":
            # 新闻模式
            seg_list = jieba.cut(text)
            pass

    return seg_list


def chinese_traditional_to_simplified(traditional_text: str) -> str:
    """
    中文繁体到简体
    """
    cc = OpenCC("t2s")
    simplified_text = cc.convert(traditional_text)
    return simplified_text


def correct(text: str):
    """
    错别字纠正
    """
    m = MacBertCorrector()
    error_sentences = [
        text,
    ]
    batch_res = m.correct_batch(error_sentences)
    return batch_res[0]


class ConfigLoader:
    def __init__(
        self,
        configs_filename: str = "configs.json",
        configs_items: tuple = ("rtsp_url", "zeromq_port"),
    ):
        self.configs_items = configs_items
        self.configs_filename = configs_filename

        self.load_configs()

    def load_configs(self):
        assert os.path.exists(
            self.configs_filename
        ), f"配置文件{self.configs_filename}不存在"

        with open(self.configs_filename, "r", encoding="utf-8") as f:
            self.configs = json.load(f)

        for arg in self.configs_items:
            assert arg in self.configs, f"配置文件缺少必要项{arg}"
