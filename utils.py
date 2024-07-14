import os
import json

def assert_file_exists(filename: str):
    """
    判断文件是否存在
    """
    assert os.path.exists(filename), f"文件{filename}不存在"


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

        assert_file_exists(self.configs_filename)

        with open(self.configs_filename, "r", encoding="utf-8") as f:
            self.__configs = json.load(f)

        for item in self.configs_items:
            assert item in self.__configs, f"配置文件缺少必要项{item}"

        for key, value in self.__configs.items():
            setattr(self, key, value)
