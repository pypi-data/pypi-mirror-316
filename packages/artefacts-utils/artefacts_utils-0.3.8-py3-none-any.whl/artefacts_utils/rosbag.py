import yaml
import os
import cv2
import subprocess

from rosbags.rosbag2 import Reader
from rosbags.typesys import Stores, get_typestore
from rosbags.image import message_to_cvimage
from launch.actions import ExecuteProcess
from pathlib import Path
from datetime import datetime
from .helpers import _extract_attribute_data
from artefacts_utils_rosbag_gpl.ros2bag2video import rosbag_to_mp4


def get_bag_recorder(topic_names, use_sim_time=False):
    """Create a rosbag2 recorder for a given list of topic names and return the node and the filepath"""
    yyyymmddhhmmss = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    rosbag_filepath = "rosbag2_" + yyyymmddhhmmss
    rosbag_cmd = (
        ["ros2", "bag", "record"]
        + topic_names
        + ["-o", rosbag_filepath, "--storage", "mcap"]
    )
    if use_sim_time:
        rosbag_cmd = rosbag_cmd + ["--use-sim-time"]
    bag_recorder = ExecuteProcess(cmd=rosbag_cmd, output="screen")
    return bag_recorder, rosbag_filepath


def extract_video(rosbag_filepath, topic_name, output_filepath, fps=20):
    rosbag_to_mp4(rosbag_filepath, topic_name, output_filepath, fps)


def convert_to_webm(video_name):
    """Convert a video to webm format using ffmpeg and save it under same name with .webm extension"""
    ffmpeg = [
        "ffmpeg",
        "-i",
        video_name,
        "-c:v",
        "libvpx-vp9",
        "-crf",
        "30",
        "-b:v",
        "0",
        "-y",
        video_name.split(".")[0] + ".webm",
    ]
    subprocess.run(ffmpeg)


def get_last_image_from_rosbag(rosbag_filepath, topic_name, output_dest):
    # Create a typestore and get the string class.
    typestore = get_typestore(Stores.LATEST)

    formatted_name = topic_name.replace("/", "_")
    filename = f"{output_dest}/{formatted_name}.last.png"
    for p in Path(output_dest).glob(f"{formatted_name}.last.png"):
        p.unlink()
    img = None
    # Create reader instance and open for reading.
    with Reader(rosbag_filepath) as reader:
        # Topic and msgtype information is available on .connections list.
        for connection in reader.connections:
            print(connection.topic, connection.msgtype)
        for connection, timestamp, rawdata in reader.messages():
            if connection.topic == topic_name:
                msg = typestore.deserialize_cdr(rawdata, connection.msgtype)
                img = message_to_cvimage(msg, "bgr8")
    if img is not None:
        cv2.imwrite(filename, img)
    return filename


def extract_image(flag, rosbag_filepath, camera_topic):
    if flag:
        output_dir = "output"
        try:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(e)
        try:
            get_last_image_from_rosbag(rosbag_filepath, camera_topic, output_dir)
        except Exception as e:
            print("error")
            print(e)


def get_final_message(rosbag_filepath, topic):
    typestore = get_typestore(Stores.LATEST)
    final_message = None
    topic_attributes = topic.split(".")
    
    with Reader(rosbag_filepath) as reader:
        for connection, timestamp, rawdata in reader.messages():
            if connection.topic == topic_attributes[0]:
                msg = typestore.deserialize_cdr(rawdata, connection.msgtype)
                final_message = _extract_attribute_data(msg, topic_attributes)

    return final_message