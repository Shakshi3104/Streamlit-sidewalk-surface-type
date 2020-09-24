import os
import pandas as pd
import numpy as np

from pathlib import Path
import pickle


class PathManager:
    def __init__(self, work_dir="materials/"):

        self.data_path = work_dir + "cache/"
        self.result_path = work_dir + "result/"


class SidewalkSurfaceType:
    def __init__(self, path_manager: PathManager = PathManager()):
        self.path_manager = path_manager
        self.data = None
        self.target = None
        self.label_list = ["asphalt", "gravel", "lawn", "grass", "sand", "mat"]
        self.subject = None
        self.subject_group_list = None

    def __call__(self, *args, **kwargs):
        x, y, z = self.fit()
        return x, y, z

    def fit(self):
        if self.data is None or self.target is None:
            data_, target_, subject_group_list_ = self.__load_from_cache_csv()
            self.data = data_.values.reshape(-1, 256, 3)
            self.target = target_
            self.subject_group_list = subject_group_list_

        return self.data, self.target, self.subject_group_list

    def __load_from_cache_csv(self):
        filepath = self.path_manager.data_path + "roads_raw.csv"
        print("load from cache csv: ", filepath)

        label_list = ["road", "rock", "lawn", "grass", "sand", "mat"]

        df = pd.read_csv(filepath, engine="python", encoding="utf-8")
        # session_group_list = df["session_group_list"].values.tolist()
        subject_group_list = df["subject_group_list"].values.tolist()
        target = [label_list.index(x) for x in df["label"]]
        target = np.array(target)
        data = df.copy()
        del data["session_group_list"]
        del data["subject_group_list"]
        del data["label"]
        del data["Subject"]

        return data, target, subject_group_list


if __name__ == "__main__":
    data, target, _ = SidewalkSurfaceType()()
