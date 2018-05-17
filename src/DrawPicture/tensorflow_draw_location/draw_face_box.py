#!/usr/bin/env python
# coding: utf-8
"""
   @author: kenwood
   @time: 18-5-11 上午10:49
"""
import numpy as np
from src.DrawPicture.tensorflow_draw_location.utils import visualization_utils_color as vis_util


def draw_box(image, boxes):
    vis_util.draw_bounding_boxes_on_image_array(image, boxes)
    return image
