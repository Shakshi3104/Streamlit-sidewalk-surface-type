import streamlit as st
import pandas as pd

from utils.data import SidewalkSurfaceType, PathManager


@st.cache
def load_sidewalk_data(manager: PathManager()):
    sidewalk = SidewalkSurfaceType()
    data, target, subject_group_list = sidewalk(manager)

    metadata = pd.DataFrame()
    metadata["target"] = target
    metadata["subject_id"] = subject_group_list

    subject_list = metadata["subject_id"].unique()
    subject_list = [chr(ord('A') + s) for s in range(len(subject_list))]
    metadata["subject"] = [subject_list[i] for i in subject_group_list]

    return sidewalk, data, metadata


def get_selected_data(sidewalk, data, metadata, subject_select, target_select):
    # 当該データを取得
    selected_metadata = metadata[metadata["subject"] == subject_select]
    selected_metadata = selected_metadata[selected_metadata["target"] == sidewalk.label_list.index(target_select)]
    # st.write(selected_metadata.index.values)

    index_select = st.slider('Index', 0, len(selected_metadata) - 1, len(selected_metadata) // 2)
    selected_index = selected_metadata.index.values[index_select]
    # st.write(selected_index)

    selected_data = pd.DataFrame(data[selected_index], columns=["x", "y", "z"])
    # st.write(selected_data)
    return selected_data


@st.cache
def load_performance_data():
    path = PathManager()
    
    accuracy = pd.read_csv(path.result_path + "subject_accuracy.csv", index_col=0)
    f_measure = pd.read_csv(path.result_path + "target_subject_f-measure.csv", index_col=0)
    f_measure.columns = ["Subject", "F-measure", "Target", "Model"]
    return accuracy, f_measure


def get_confusion_matrix(model):
    path = PathManager()

    cm_filepath = path.result_path + "{}_CM_all_subject.csv".format(model)

    conf_mat = pd.read_csv(cm_filepath, index_col=0)
    return conf_mat
