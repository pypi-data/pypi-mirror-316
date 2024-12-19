#!/usr/bin/env python
# coding=utf-8
"""
Author       : Kofi
Date         : 2022-08-10 10:24:51
LastEditors  : Kofi
LastEditTime : 2022-08-12 10:57:32
Description  : 组件创建
"""

import json, os
from loguru import logger
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget
from KofiPyQtHelper.utils.Command import Command
from KofiPyQtHelper.utils.Ui.LayoutHelper import LayoutHelper
from KofiPyQtHelper.utils.Ui.ComponentHelper import ComponentHelper


class UiHelper(Command, LayoutHelper, ComponentHelper):
    def __init__(self) -> None:
        self.class_ = self
        self.commands = {}
        self.variates = {}
        self.items = {}
        self.tables = {}
        self.trees = {}
        self.components = []
        self.load_layout_datas()
        self.gridInfo = {}
        Command.__init__(self)
        super(UiHelper, self).__init__()

    def load_layout_datas(self, category="", name="") -> None:
        """
        加载布局数据
        使用 self.category和self.name获取数据
        """
        category = self.category if category == "" else category
        name = self.name if name == "" else name
        path = os.path.abspath(
            "./config/interface/{0}/{1}.json".format(self.category, self.name)
        )
        self.layout_datas, self.button_datas, self.closeCommand = self.get_layout_data(
            path
        )

    def get_layout_data(self, path):
        try:
            with open(path, "r", encoding="UTF-8") as f:
                jsonData = json.load(f)
                if isinstance(jsonData, list):
                    return jsonData, None, None
                elif isinstance(jsonData, dict):
                    return (
                        jsonData.get("layout", jsonData),
                        jsonData.get("buttons", None),
                        jsonData.get("closeCommand", None),
                    )
                else:
                    # 如果json_data既不是列表也不是字典，记录一个错误
                    logger.error(
                        f"Unexpected JSON data format in {path}. Must be list or dict."
                    )
        except FileNotFoundError:
            logger.error(f"File not found: {path}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in file {path}: {e}")
        except OSError as e:
            # 其他与操作系统相关的I/O异常（例如文件权限问题）
            logger.error(f"OS error while opening file {path}: {e}")
        except Exception as e:
            # 捕获其他可能的异常并记录
            logger.exception(
                f"An unexpected error occurred while loading layout data: {e}"
            )

    def init(self, parent: QWidget, infos):
        # Helper function to get content from info
        def get_content(info):
            if "content" in info:
                return info["content"]
            if "contentJson" in info:
                category = info["contentJson"].get("category", "")
                name = info["contentJson"]["name"]
                path = os.path.join("config", "interface", category, f"{name}.json")
                return self.get_layout_data(os.path.abspath(path))[0]
            return None

        # Main loop to initialize components
        for info in infos:
            currentType = info["type"] if isinstance(info, dict) else info.type
            functionName = f"init{currentType.capitalize()}"
            try:
                init_function = getattr(self, functionName)
            except AttributeError as e:
                # Handle the error or log it if the init function is not found
                print(f"Initialization function '{functionName}' not found: {e}")
                continue  # Skip this info and continue with the next

            box = init_function(parent, info)
            content = get_content(info)

            if content is not None and box is not None:
                gridbox_conditions = currentType.capitalize() == "Gridbox" or (
                    currentType.capitalize() == "Groupbox"
                    and "layout" in info
                    and info["layout"].capitalize() == "Gridbox"
                )

                if gridbox_conditions:
                    self.initGridInfo(info, box)
                self.init(box, content)

    def initGridInfo(self, info, component):
        self.gridInfo[component] = {
            "columns": info["columns"],
            "currentColumn": 0,
            "currentRow": 0,
        }

    def gridCalculate(self, component):
        self.gridInfo[component]["currentColumn"] += 1
        if (
            self.gridInfo[component]["currentColumn"]
            >= self.gridInfo[component]["columns"]
        ):
            self.gridInfo[component]["currentRow"] += 1
            self.gridInfo[component]["currentColumn"] = 0
