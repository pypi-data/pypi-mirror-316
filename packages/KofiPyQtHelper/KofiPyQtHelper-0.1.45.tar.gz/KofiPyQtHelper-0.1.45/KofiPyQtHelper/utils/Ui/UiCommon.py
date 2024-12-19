#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-07-11 15:22:09
LastEditors  : Kofi
LastEditTime : 2023-07-11 15:22:09
Description  : 
"""

from PyQt5.QtWidgets import QLayout
from loguru import logger


class UiCommand:
    def setMargin(self, info, box: QLayout):
        # 默认边距值
        default_margins = (5, 5, 5, 5)

        # 获取边距信息
        margins = info.get("margins", default_margins)

        # 根据不同的参数长度设置内容边距
        try:
            if len(margins) == 4:
                box.setContentsMargins(*margins)
            elif len(margins) == 3:
                box.setContentsMargins(margins[1], margins[0], margins[1], margins[2])
            elif len(margins) == 2:
                box.setContentsMargins(margins[1], margins[0], *margins)
            elif len(margins) == 1:
                margin = margins[0]
                box.setContentsMargins(margin, margin, margin, margin)
            else:
                raise ValueError("Invalid margins length: {}".format(len(margins)))
        except Exception as e:
            logger.exception("{}-设置边框出现问题: {}".format(info, e))
