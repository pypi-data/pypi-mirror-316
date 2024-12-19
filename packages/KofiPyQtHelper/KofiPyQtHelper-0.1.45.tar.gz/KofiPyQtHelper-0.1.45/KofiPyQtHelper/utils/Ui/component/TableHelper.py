#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-07-11 15:27:34
LastEditors  : Kofi
LastEditTime : 2023-07-11 15:27:34
Description  : 
"""
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtWidgets import (
    QWidget,
    QTableWidget,
    QAbstractItemView,
    QTableWidgetItem,
    QComboBox,
    QStyledItemDelegate,
    QHeaderView,
    QLineEdit,
)
from KofiPyQtHelper.enums.ColumnType import ColumnType
from KofiPyQtHelper.components.Pagination import Pagination
from functools import partial


class TableHelper:
    def initTable(self, parent: QWidget, info):
        table = QTableWidget()
        table.setObjectName(info["name"])
        table._double_func = partial(self.tableDoubleClicked, table, info["name"])
        if "height" in info:
            table.setFixedHeight(info["height"])
        if "" in info:
            table.cellDoubleClicked.connect(table._double_func)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.initTableHeader(table, info["columns"])
        self.tables[info["name"]] = info["columns"]
        self.components.append({info["name"]: table})
        self.setTableData(info["name"], [])
        parent.addWidget(table)

    def initTableHeader(self, controls, info):
        columns = info["names"]
        controls.setColumnCount(len(info["header"]))
        controls.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        controls.setHorizontalHeaderLabels(info["header"])
        controls.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        for index, column in enumerate(columns):
            if "width" in column:
                controls.setColumnWidth(index, int(column["width"]))
            if column["type"] == "hidden":
                controls.setColumnHidden(index, True)

    def setTableData(self, name, datas):
        table = self.tables[name]
        columns = table["names"]
        current = self.getCurrentInput(name)
        self.initTableHeader(current, table)

        current.clearContents()
        self.variates[name] = list(datas)
        current.setEditTriggers(QAbstractItemView.NoEditTriggers)
        current.setRowCount(len(datas))

        def setItem(row, column, value, is_widget=False):
            if is_widget:
                current.setCellWidget(row, column, value)
            else:
                current.setItem(row, column, QTableWidgetItem(str(value)))

        value_setters = {
            ColumnType.Hidden: lambda value: None,
            ColumnType.Text: lambda value: value[key],
            ColumnType.Enums: lambda value: (
                str(value[key].value) if row["item"] == "value" else str(value[key])
            ),
            ColumnType.Flag: lambda value: item.get("data", ["否", "是"])[value[key]],
            ColumnType.Enable: lambda value: item.get("data", ["禁用", "启用"])[
                value[key]
            ],
            ColumnType.ChildrenText: lambda value: str(
                value[key][item.get("index", 0)][item["value"]]
            ),
            ColumnType.Buttons: lambda value: self.createButtonLayout(
                item["content"], name
            ),
        }

        for row, data in enumerate(datas):
            for column, item in enumerate(columns):
                types = ColumnType(item.get("type", ColumnType.Text))
                key = item["name"]

                value_setter = value_setters.get(types, lambda value: value[key])
                value = value_setter(data)

                if types == ColumnType.Buttons:
                    setItem(row, column, value, is_widget=True)
                elif value is not None:
                    setItem(row, column, value)

        current.resizeColumnsToContents()

    def tableDoubleClicked(self, current, name, row, column):
        item = current.item(row, column)

        try:
            current.cellDoubleClicked.disconnect(current._double_func)
            if item:
                table = self.tables[name]
                columns = table["names"]
                types = ColumnType(columns[column].get("type", ColumnType.Text))
                key = columns[column]["name"]
                value = columns[column].get("value", None)
                info = columns[column]

                if types == ColumnType.Flag:
                    info["items"] = ["否", "是"]
                elif types == ColumnType.Enable:
                    info["items"] = ["禁用", "启用"]

                current.itemChange_func = partial(
                    self.tableItemChanged, current, name, types, key, value
                )

                # 保存委托，防止被垃圾回收器回收
                if not hasattr(current, "_delegates"):
                    current._delegates = {}

                delegate = EditDelegate(info)
                current._delegates[column] = delegate
                current.setItemDelegateForColumn(column, delegate)

                current.editItem(item)
                current.itemChanged.connect(current.itemChange_func)

        except Exception as e:
            print(e)

        finally:
            # 确保传递正确的参数绑定
            current.cellDoubleClicked.connect(current._double_func)

    def tableItemChanged(self, current, name, types, key, value, item):
        current.itemChanged.disconnect(current.itemChange_func)
        try:
            row = item.row()
            if types == ColumnType.ChildrenText:
                self.variates[name][row][key][0][value] = item.text()
            elif types == ColumnType.Text:
                self.variates[name][row][key] = item.text()
            elif types == ColumnType.Flag:
                idx = ["否", "是"].index(item.text())
                self.variates[name][row][key] = idx

        except Exception as e:
            logger.error(f"Error in tableItemChanged: {e}")

    def initPagination(self, parent: QWidget, info):
        pagination = Pagination(**info)
        params = info.get("params", [])
        params.append({"name": "window", "value": self})

        # 定义一个内部函数来处理信号，并传递额外所需的参数
        def signal_handler(currentPage, pageSize):
            params.append({"name": "currentPage", "value": currentPage})
            params.append({"name": "pageSize", "value": pageSize})
            # 在这里，我们直接将信号的参数与其他必要的参数一同传递给目标函数
            self.commands[info["command"]](params)

        # 使用 signal_handler 作为信号的槽
        pagination.Signal_PageNumChange.connect(signal_handler)
        self.components.append({info["name"]: pagination})
        parent.addWidget(pagination)


class EditDelegate(QStyledItemDelegate):
    def __init__(self, info, parent=None) -> None:
        try:
            self.info = info
            self.types = ColumnType(self.info.get("type", ColumnType.Text))
            super().__init__(parent)
        except Exception as e:
            print(e)

    def createEditor(self, parent, option, index):
        try:
            editor = None
            # 根据列的类型创建不同的编辑器
            if self.types in (ColumnType.ChildrenText, ColumnType.Text):
                editor = QLineEdit(parent)
                if "validator" in self.info:
                    if self.info["validator"] == "Int":
                        editor.setValidator(QIntValidator())
                    elif self.info["validator"] == "Float":
                        editor.setValidator(QDoubleValidator())
                    elif self.info["validator"] == "Reg":
                        regexp = QRegExp(self.info["reg"])
                        validator = QRegExpValidator(regexp)
                        editor.setValidator(validator)
                editor.editingFinished.connect(
                    lambda: self.commit_editor_data(editor, index)
                )
            elif self.types in (ColumnType.Flag, ColumnType.Enable):
                editor = QComboBox(parent)
                editor.addItems(
                    self.info.get("items", self.info["items"])
                )  # 假设info字典中有items键存储下拉选项
                editor.currentIndexChanged.connect(
                    lambda _: self.commit_editor_data(editor, index)
                )
            else:
                editor = super(EditDelegate, self).createEditor(parent, option, index)

            return editor
        except Exception as e:
            print(e)

    def setEditorData(self, editor, index):
        try:
            value = index.model().data(index, Qt.EditRole)
            if self.types in (ColumnType.ChildrenText, ColumnType.Text):
                editor.setText(str(value))
            elif self.types == ColumnType.Flag:
                editor.setCurrentIndex(editor.findText(value))
        except Exception as e:
            print(e)

    def setModelData(self, editor, model, index):
        try:
            if self.types in (ColumnType.ChildrenText, ColumnType.Text):
                model.setData(index, editor.text(), Qt.EditRole)
            elif self.types == ColumnType.Flag:
                model.setData(index, editor.currentText(), Qt.EditRole)

        except Exception as e:
            print(e)

    def commit_editor_data(self, editor, index):
        self.setModelData(editor, index.model(), index)
