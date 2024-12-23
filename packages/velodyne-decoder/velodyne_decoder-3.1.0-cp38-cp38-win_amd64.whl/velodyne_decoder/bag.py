# Copyright (c) 2021-2023, Martin Valgur
# SPDX-License-Identifier: BSD-3-Clause

import sys
from collections import namedtuple

import velodyne_decoder as vd

is_py2 = sys.version_info[0] == 2


def read_bag(
    bag_file,
    config=None,
    topics=None,
    as_pcl_structs=False,
    time_range=(None, None),
):
    """Decodes and yields all point clouds stored in a ROS bag file.

    `model` parameter must be set in the provided config.

    Parameters
    ----------
    bag_file : path or file handle
    config : Config, optional
    topics : str or list of str
    as_pcl_structs : bool
        If False, the returned NumPy arrays will be a contiguous array of floats (default).
        If True, the returned NumPy arrays will contain PCL-compatible structs with dtype
        {'names': ['x', 'y', 'z', 'intensity', 'ring', 'time'],
         'formats': ['<f4', '<f4', '<f4', '<f4', '<u2', '<f4'],
         'offsets': [0, 4, 8, 16, 20, 24], 'itemsize': 32}
    return_frame_id : bool
        If True, includes the frame_id of the messages in the returned tuple. Defaults to False.
    time_range : float, float or rospy.Time, rospy.Time
        Optionally only return scans from given time range.

    Yields
    ------
    timestamp: rospy.Time
    point_cloud : numpy.ndarray
    topic : str
    """
    if config is None:
        config = vd.Config()
    decoder = vd.ScanDecoder(config)
    Result = namedtuple("ResultTuple", ("stamp", "points", "topic", "frame_id"))
    msg_types = ["velodyne_msgs/VelodyneScan"]
    for topic, scan_msg, ros_time in vd.util.iter_bag(bag_file, topics, msg_types, time_range):
        if is_py2:
            for packet in scan_msg.packets:
                packet.data = bytearray(packet.data)
        stamp, points = decoder.decode_message(scan_msg, as_pcl_structs)
        yield Result(stamp, points, topic, scan_msg.header.frame_id)
