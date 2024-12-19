#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-06-28 08:24:37
LastEditors  : Kofi
LastEditTime : 2023-07-11 23:36:21
Description  : 
"""
from loguru import logger
import os, json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QHBoxLayout, QComboBox
from KofiPyQtHelper.utils.UiHelper import UiHelper
from KofiPyQtHelper.utils.CommonHelper import CommonHelper


class BaseWidget(QWidget, UiHelper):
    currentCommand = {}

    def __init__(
        self,
        name,
        parent,
        category="",
        title=None,
        height=None,
        loadData=True,
        currentRow=None,
        baseUI=True,
        command=None,
        initDataCommand=None,
        initParams=None,
    ) -> None:
        self.category = category
        self.name = name
        self.setParent(parent)
        super(BaseWidget, self).__init__()
        if command:
            self.currentCommand.update(command)
            self.commands.update(command)

        self.currentRow = currentRow
        self.setTitle(title)
        self.setHeight(height)
        if baseUI:
            self.initUI()
        else:
            self.initTabUI()
        self.load_datas(loadData, initDataCommand, initParams)
        self.loadStyle()

    def loadStyle(self):
        style = CommonHelper.readQss("./styles/index.qss")
        if style != None:
            self.setStyleSheet(style)

    def setHeight(self, height):
        if height != None:
            self.currentHeight = int(height)

    def setTitle(self, title):
        if title != None:
            self.setWindowTitle(title)

    def setParent(self, parent):
        if parent != None:
            self.parent = parent
        else:
            self.parent = None

    def initTabUI(self) -> None:
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(5, 15, 15, 5)
        self.setLayout(main_layout)

    def initUI(self) -> None:
        shell = QVBoxLayout()
        shell.setContentsMargins(0, 0, 0, 0)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main = QWidget()
        main.setLayout(main_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        if "layout_datas" in locals().keys() or (
            self.layout_datas != [] or self.layout_datas != None
        ):
            self.init(main_layout, self.layout_datas)

        scroll.setWidget(main)
        shell.addWidget(scroll)

        self.initButtonLayout(shell, scroll)

        self.setLayout(shell)

    def initButtonLayout(self, shell, scroll):
        if self.button_datas != None:
            button_layout = QHBoxLayout()
            self.init(button_layout, self.button_datas)
            button_widget = QWidget()
            button_widget.setLayout(button_layout)
            shell.addWidget(button_widget, Qt.AlignJustify)
            if hasattr(self, "currentHeight"):
                scroll.setMinimumHeight(self.currentHeight - 70)
        else:
            if hasattr(self, "currentHeight"):
                scroll.setMinimumHeight(self.currentHeight - 10)

    def load_datas(self, loadData, initDataCommand, params):
        """加载数据"""
        if not loadData:
            return
        jsonData = None
        try:
            if initDataCommand:
                info = {}
                info["params"] = params if params else []
                info["params"].append({"name": "window", "value": self})
                jsonData = self.commands[initDataCommand](info)
            else:
                path = CommonHelper.getAbsFilePath(
                    "./config/datas/{0}/{1}_data.json".format(self.category, self.name)
                )
                if os.path.exists(path):
                    with open(path, "r", encoding="UTF-8") as f:
                        jsonData = json.load(f)
            if jsonData is not None:
                self.variates = CommonHelper.merageDict(self.variates, jsonData)
                self.initComponentValues()
        except OSError as e:  # 更精准地捕获特定异常
            logger.exception("Error opening or reading the file: %s", e)
        except json.JSONDecodeError as e:  # 捕获JSON解码错误
            logger.exception("JSON decode error: %s", e)
        except KeyError as e:  # 处理字典键错误
            logger.exception("Key error: %s", e)
        except Exception as e:  # 其他未预见异常
            logger.exception("An unexpected error occurred: %s", e)

    def initComponent(self, args):
        current = self.parameterSearchByName(args, "currentType")
        components = self.parameterSearchByName(args, "components")
        if current != None and components != None:
            if type(current) == dict:
                if current["type"] == "variates":
                    currentType = self.variates[current["value"]]
                elif current["type"] == "components":
                    currentType = self.getCuttentInputValue(current["value"])
            elif type(current) == str:
                currentType = current
            self.loadItems(currentType, components)

    def loadItems(self, currentType, components):
        try:
            items = [
                string.strip()
                for string in pd.read_csv(
                    "./files/" + self.category + "/" + currentType + ".DAT",
                    nrows=1,
                    encoding="utf8",
                ).columns.values
                if string.strip()
            ]

            for componentName in components:
                currentComponent = self.window.getCurrentInput(componentName)
                currentComponent.addItems(items)

        except Exception as e:
            logger.exception(e)

    def conditionalReturn(self, args):
        condition = self.parameterSearchByName(args, "fileName", "condition")
        if condition["type"] == "variates":
            for result in condition["result"]:
                if self.variates[condition["name"]] == result["item"]:
                    return result
        return None

    def initWindow(
        self,
        fileName,
        args,
        title,
        width,
        height,
        category="",
        variates=None,
        currentRow=None,
        loadData=True,
        initDataCommand=None,
        initParams=None,
    ):
        self.window = None

        communications = self.parameterSearchByName(args, "communications")
        paramNames = self.parameterSearchByName(args, "paramNames")
        parent = self if paramNames != None and communications != None else None

        self.window = BaseWidget(
            name=fileName,
            parent=parent,
            category=category if category else "",
            title=title,
            height=height,
            currentRow=currentRow,
            loadData=loadData,
            command=self.currentCommand,
            initDataCommand=initDataCommand,
            initParams=initParams,
        )
        self.window.setWindowModality(Qt.ApplicationModal)
        if width != None and height != None:
            self.window.setFixedSize(int(width), int(height))

        if variates != None:
            self.window.variates = variates
            self.window.initComponentValues()

        if paramNames != None and "in" in paramNames:
            for param in paramNames["in"]:
                if type(self.getCuttentInputValue(param["from"])) == QComboBox:
                    self.window.variates[param["to"]] = self.getCuttentInputValue(
                        param["from"]
                    ).value()
                else:
                    self.window.variates[param["to"]] = self.getCuttentInputValue(
                        param["from"]
                    )

            self.window.initComponentValues()

    def closeEvent(self, event) -> None:
        if hasattr(self, "closeCommand"):
            self.commands[self.closeCommand["name"]](self.closeCommand["params"])
        return super().closeEvent(event)
