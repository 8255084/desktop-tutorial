# Python In-built packages
from pathlib import Path
import PIL

# External packages
import streamlit as st
from ultralytics import RTDETR

# Local Modules
import settings
import helper

# Setting page layout
st.set_page_config(
    page_title="肇事动物检测系统",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.title("肇事动物检测系统")
st.caption("使用改进的RT-DETR模型对肇事动物图片进行检测")

# Sidebar
st.sidebar.header("模型配置")

# Model Options
model_type = st.sidebar.radio(
    "请选择任务类型", ['目标检测'])

confidence = 0.4

# Selecting Detection Or Segmentation
if model_type == '目标检测':
    model_path = Path(settings.DETECTION_MODEL)

# Load Pre-trained ML Model
try:
    model=RTDETR('weights/best.pt')
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

st.sidebar.header("图片配置")
source_radio = st.sidebar.radio(
    "请选择资源类型", settings.SOURCES_LIST)

source_img = None
# If image is selected
if source_radio == settings.IMAGE:
    source_img = st.sidebar.file_uploader(
        "请上传一张图片...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    col1, col2 = st.columns(2)

    with col1:
        try:
            if source_img is None:
                default_image_path = str(settings.DEFAULT_IMAGE)
                default_image = PIL.Image.open(default_image_path)
                st.image(default_image_path, caption="默认图片",
                         use_column_width=True)
            else:
                uploaded_image = PIL.Image.open(source_img)
                st.image(source_img, caption="上传的图片",
                         use_column_width=True)
        except Exception as ex:
            st.error("打开图片时发生错误.")
            st.error(ex)

    with col2:
        if source_img is None:
            default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
            default_detected_image = PIL.Image.open(
                default_detected_image_path)
            st.image(default_detected_image_path, caption='检测结果',
                     use_column_width=True)
        else:
                model=RTDETR('weights/best.pt')
                res = model.predict(uploaded_image,
                                    conf=confidence
                                    )
                boxes = res[0].boxes
                res_plotted = res[0].plot()[:, :, ::-1]
                st.image(res_plotted, caption='检测结果',
                         use_column_width=True)

else:
    st.error("请上传有效的类型!")
