#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-07-11 16:09:53
LastEditors  : Kofi
LastEditTime : 2023-07-11 16:09:53
Description  : 
"""
from KofiPyQtHelper.enums.ComboboxValueType import ComboboxValueType
from PyQt5.QtWidgets import (
    QComboBox,
    QLineEdit,
    QTableWidget,
    QPlainTextEdit,
    QCheckBox,
)
from functools import partial


class ValueHelper:
    def     setComboValue(self, objInput: QComboBox, type: ComboboxValueType, items, val):
        if type == ComboboxValueType.Index.value:
            val = val if val != "" else 0
            current_index = val
        elif type == ComboboxValueType.Val.value:
            try:
                current_index = items.index(val)
            except:
                current_index = 0
        else:
            current_index = val

        objInput.setCurrentIndex(current_index)

    def setTextValue(self, objInput, val):
        objInput.setText(val)

    def setPlainTextValue(self, objInput, val):
        objInput.setPlainText(val)

    def getCurrentInput(self, name):
        for component in self.components:
            for key, objInput in component.items():
                if key == name:
                    return objInput
        return None

    def initComponentValues(self):
        component_setters = {
            QLineEdit: self.setTextValue,
            QPlainTextEdit: self.setPlainTextValue,
            QComboBox: self.setComboValue,
            QTableWidget: self.setTableData,
        }
        for component in self.components:
            for key, objInput in component.items():
                # 确保key存在于variates中
                if key not in self.variates:
                    continue
                # 获取组件的类型
                comp_type = type(objInput)
                # 如果组件类型在映射字典中，则调用相应的处理函数
                if comp_type in component_setters:
                    value = str(self.variates[key])
                    if comp_type == QComboBox:
                        # 对于QComboBox，需要提供额外的参数
                        component_setters[comp_type](
                            objInput,
                            self.items[key]["type"],
                            self.items[key]["data"],
                            value,
                        )
                    elif comp_type == QTableWidget:
                        # 对于QTableWidget，也需要特别处理
                        component_setters[comp_type](key, self.variates[key])
                    else:
                        # 对于其他类型，直接调用函数，并设置值
                        component_setters[comp_type](objInput, value)

    def clearComponentValues(self):
        """清除组件的值,恢复为默认值"""
        for component in self.components:
            for key, objInput in component.items():
                if type(objInput) == QLineEdit:
                    self.variates[key] = ""
                    self.setTextValue(objInput, str(self.variates[key]))
                elif type(objInput) == QComboBox:
                    self.setComboValue(
                        objInput,
                        self.items[key]["type"],
                        self.items[key]["data"],
                        self.variates[key],
                    )
                elif type(objInput) == QTableWidget:
                    self.variates[key] = []
                    self.setTableData(key, self.variates[key])

    def getCuttentInputValue(self, name: str):
        """通过组件名称获取组件值
        Args:
            name (str): 组件名称

        Returns:
            str, bool or list: 组件当前值
        """
        # 检查给定的名字是否对应于一个复选框组
        obj = self.getCurrentInput(name)

        if isinstance(obj, dict):
            # 返回被选中的复选框ID列表
            return [id for id, info in obj.items() if info["widget"].isChecked()]

        # 对于单个控件

        if obj is not None:
            if isinstance(obj, QLineEdit):
                return obj.text()
            elif isinstance(obj, QComboBox):
                return obj.currentText()
            elif isinstance(obj, QCheckBox):
                return obj.isChecked()

        return None

    def resetCheckboxgroup(self, name, datas):
        container = self.getCurrentInput(name + "_layout")
        current = self.getCurrentInput(name)
        for checkbox in current.values():
            checkbox_widget = checkbox["widget"]
            checkbox_widget.deleteLater()
        current.clear()
        group_checkboxes = {}

        for item_info in datas:
            checkbox = QCheckBox(item_info["label"])
            checkbox_value = item_info.get("value", False)
            checkbox.setChecked(checkbox_value)
            checkbox.stateChanged.connect(
                partial(self.checkboxKillFocus, {"name": name}, group_checkboxes)
            )
            # 将checkbox加入布局中
            container.addWidget(checkbox)
            # 保存checkbox的引用和值到字典中
            group_checkboxes[item_info["id"]] = {
                "widget": checkbox,
                "value": checkbox_value,
            }
        current.update(group_checkboxes)
