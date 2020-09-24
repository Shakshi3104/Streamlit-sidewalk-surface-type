import streamlit as st
import plotly.graph_objects as go

from utils import plotly_utils as pu, utils
from utils.data import PathManager

if __name__ == "__main__":

    """
    # Sidewalk Surface Type
    Estimation of Sidewalk Surface Type with a Smartphone
    ## Visualize Acceleration Data
    """
    path_manager = PathManager("materials/")
    sidewalk, data, metadata = utils.load_sidewalk_data(path_manager)

    subject_select = st.selectbox(
        "Subject", metadata["subject"].unique()
    )

    target_select = st.selectbox(
        "Target", sidewalk.label_list
    )

    st.write(f'### Subject: {subject_select}, Target: {target_select}')

    # 当該データを取得
    selected_data = utils.get_selected_data(sidewalk, data, metadata, subject_select, target_select)

    color = pu.seaborn_color_palette_2_plotly_rgb("Set2", 3)

    plot_data = [
        go.Scatter(x=selected_data.index,
                   y=selected_data["x"],
                   mode='lines',
                   name="x",
                   marker_color=color[0]),
        go.Scatter(x=selected_data.index,
                   y=selected_data["y"],
                   mode='lines',
                   name="y",
                   marker_color=color[1]),
        go.Scatter(x=selected_data.index,
                   y=selected_data["z"],
                   mode='lines',
                   name="z",
                   marker_color=color[2])
    ]

    layout = go.Layout(
        yaxis={"title": "Acceleration Data [G]"}
    )

    st.plotly_chart(go.Figure(data=plot_data, layout=layout))
    # st.line_chart(selected_data)

    if st.checkbox("Show Raw Data"):
        st.write(selected_data.T)

    """

    ## Estimation Performance
    ### Accuracy
    """
    accuracy, f_measure = utils.load_performance_data()
    fig = pu.plotly_boxplot(accuracy, x="Model", y="Accuracy", pallete="Set2",
                            title="Leave-One-Subject-Out Cross Validation",
                            showmeans=True, width=800, height=500)
    st.plotly_chart(fig)

    """
    ### F-measure
    """
    fig = pu.plotly_multi_boxplot(f_measure, x="Target", y="F-measure", hue="Model",
                                  pallet="Set2",
                                  title="F-measure per Target",
                                  showmeans=True, width=1000, height=500)
    st.plotly_chart(fig)

    """
    ### Confusion Matrix
    """
    model_select = st.selectbox(
        "Model", accuracy["Model"].unique()
    )

    conf_mat = utils.get_confusion_matrix(model_select)
    fig = pu.plotly_heatmap(conf_mat)
    st.plotly_chart(fig)

    if st.checkbox("Show Confusion Matrix via DataFrame"):
        st.write(conf_mat)
