#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2022-09-22 10:53:08
LastEditors  : Kofi
LastEditTime : 2022-09-22 10:53:08
Description  : 命令集
"""

import json, codecs, os, shutil
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPlainTextEdit, QApplication, QMessageBox, QFileDialog
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from loguru import logger
from KofiPyQtHelper.utils.ExcelHelper import ExcelHelper
from KofiPyQtHelper.utils.CommonHelper import CommonHelper
from KofiPyQtHelper.utils.Commands.HistoryCommand import HistoryCommand
from KofiPyQtHelper.utils.Commands.GraphCommand import GraphCommand
from KofiPyQtHelper.utils.Commands.WidgetCommand import WidgetCommand
from KofiPyQtHelper.utils.Commands.PdfCommand import PdfCommand
from KofiPyQtHelper.utils.Commands.BaseCommand import BaseCommand


class Command(HistoryCommand, GraphCommand, WidgetCommand, PdfCommand, BaseCommand):
    show_infoes_signal = pyqtSignal(str, object)

    def __init__(self):
        self.commands.update(
            {
                "confirm": self.confirm,
                "confirmParent": self.confirmParent,
                "openFile": self.openFile,
                "loadExcelVariates": self.loadExcelVariates,
                "saveFile": self.saveFile,
                "selectFolder": self.selectFolder,
            }
        )
        HistoryCommand.__init__(self)
        GraphCommand.__init__(self)
        WidgetCommand.__init__(self)
        PdfCommand.__init__(self)

        self.show_infoes_signal.connect(self.show_infoes)

    def generateFile(self, savePath):
        path = CommonHelper.getAbsFilePath(savePath)
        if not os.path.exists(path):
            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))
            file = open(path, "w")
            file.close()

    def generateTemplate(self, folder, file, savePath) -> bool:
        """依据模版生成数据文件

        Args:
            folder (_type_): 模版所在文件夹
            file (_type_): 模版名称
            savePath (_type_): 生成文件位置及名称

        Returns:
            Boolean: 是否成功
        """
        try:
            env = Environment(loader=FileSystemLoader(folder))
            template = env.get_template(file)
            content = template.render(self.variates)
            self.generateFile(savePath)
            self.writeToFile(savePath, content)
            return True
        except Exception as e:
            logger.exception(e)
            return False

    def verifyVariates(self):
        result = True
        for key, value in self.variates.items():
            if value == "" and key != "flie":
                result = False
                break
        return result

    def generateDataToFile(self, dataPath) -> None:
        """保存数据到文件
        Args:
            dataPath (_type_): 文件名称
        """
        self.generateFile(dataPath)
        self.writeJsonToFile(dataPath, self.variates)

    def confirm(self, args):
        try:
            dataPath = self.parameterSearchByName(args, "dataPath")
            folder = self.parameterSearchByName(args, "folder")
            file = self.parameterSearchByName(args, "file")
            savePath = self.parameterSearchByName(args, "savePath")

            if self.verifyVariates():
                self.generateTemplate(folder, file, savePath)
                if dataPath != None:
                    self.generateDataToFile(dataPath)
                QMessageBox.about(self, "提示", "保存成功")
                self.close()
            else:
                QMessageBox.about(self, "提示", "保存失败,请将所有数据填写完整")
        except Exception as e:
            logger.exception(e)

    def confirmParent(self, args):
        variateNames = self.parameterSearchByName(args, "variateName")
        params = self.parameterSearchByName(args, "paramNames")
        currentParams = params["out"] if "out" in params else params

        for param in currentParams:
            if variateNames:
                for item in variateNames:
                    self.variates[item["name"]] = self.getCurrentInput(
                        item["value"]
                    ).currentText()

            if self.currentRow != None:
                self.parent.variates[param][self.currentRow] = self.variates
            else:
                self.parent.variates[param].append(self.variates)
            self.parent.setTableData(param, self.parent.variates[param])

            """ 控制按钮是否禁用
            """
            buttonName = self.parameterSearchByName(args, "buttonName")
            length = self.parameterSearchByName(args, "listLength")

            if length != None:
                if len(self.parent.variates[param]) >= int(length):
                    self.parent.getCurrentInput(buttonName).setEnabled(False)
                else:
                    self.parent.getCurrentInput(buttonName).setEnabled(True)

        self.close()

    def writeToFile(self, filename, content):
        file = codecs.open(CommonHelper.getAbsFilePath(filename), "w", "GBK")
        file.writelines(content)
        file.close()

    def writeJsonToFile(self, filename, jsonData):
        content = json.dumps(jsonData)
        file = codecs.open(CommonHelper.getAbsFilePath(filename), "w")
        file.write(content)
        file.close()

    def show_infoes(self, info: str, component: QPlainTextEdit):
        """同步显示自定义任务的返回信息"""
        cursor = component.textCursor()
        cursor.insertText(info)
        component.setTextCursor(cursor)
        component.ensureCursorVisible()
        QApplication.processEvents()

    def openFile(self, args):
        try:
            fileTitle = self.parameterSearchByName(args, "fileTitle")
            fileType = self.parameterSearchByName(args, "fileType")
            if fileType == None:
                fileType = "All Files (*)"
            fileName, fileTypes = QFileDialog.getOpenFileName(
                self, fileTitle, "./", fileType
            )
            componentName = self.parameterSearchByName(args, "componentName")
            objInput = self.getCurrentInput(componentName)
            self.setTextValue(objInput, fileName)
        except Exception as e:
            logger.exception(e)

    def selectFolder(self, args):
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            folderPath = QFileDialog.getExistingDirectory(
                self, "选择目录", "", options=options  # 对话框标题  # 初始目录
            )
            componentName = self.parameterSearchByName(args, "componentName")
            objInput = self.getCurrentInput(componentName)
            self.setTextValue(objInput, folderPath)
        except Exception as e:
            logger.exception(e)

    def processExcelFile(self, loadFile, variateTemplate, childrenCount):
        currentFile = self.getCurrentInput(loadFile).text()
        if not currentFile:
            QMessageBox.about(self, "提示", "请选择加载的数据文件")
            return
        category_path = (
            "./config/values/{0}/".format(self.category)
            if self.category
            else "./config/values/"
        )
        path = CommonHelper.getAbsFilePath(f"{category_path}{variateTemplate}")

        try:
            with open(path, "r", encoding="UTF-8") as f:
                jsonData = json.load(f)
            sheet, configList = ExcelHelper.readExcelToVariates(currentFile, jsonData)
        except Exception as e:
            logger.exception(e)
            QMessageBox.about(self, "提示", "文件格式不正确")
            return

        self.getCurrentInput(loadFile).setText("")
        # 准备索引映射以避免多次循环
        config_map = {
            config["title"]: (
                config["index"],
                config["name"],
                config.get("parent"),
                config.get("isChildren"),
            )
            for config in configList
            if "index" in config
        }
        datas = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            data = {}
            for title, (index, name, parent, isChildren) in config_map.items():
                value = row[index]
                if isChildren:
                    if parent not in data:
                        data[parent] = []
                        items = [{} for _ in range(childrenCount)]
                    else:
                        items = data[parent]
                    items[0][name] = value  # 假设childrenCount至少为1
                else:
                    data[name] = value
            datas.append(data)
        return datas

    def loadExcelVariates(self, args):
        variateTemplate = self.parameterSearchByName(args, "variateTemplate")
        loadFile = self.parameterSearchByName(args, "fileName")
        variateName = self.parameterSearchByName(args, "variateName")
        childrenCount = self.parameterSearchByName(args, "childrenCount")
        datas = self.processExcelFile(loadFile, variateTemplate, childrenCount)
        if datas is None:
            QMessageBox.about(self, "提示", "文件格式错误,请使用正确的数据文件")
        else:
            self.variates[variateName].extend(datas)
            self.initComponentValues()

    def getExcelVariates(self, args):
        variateTemplate = self.parameterSearchByName(args, "variateTemplate")
        loadFile = self.parameterSearchByName(args, "fileName")
        childrenCount = self.parameterSearchByName(args, "childrenCount")

        datas = self.processExcelFile(loadFile, variateTemplate, childrenCount)
        if datas is None:
            QMessageBox.about(self, "提示", "文件格式错误,请使用正确的数据文件")

        return datas

    def saveFile(self, args):
        variateName = self.parameterSearchByName(args, "variateName")
        fileName = self.parameterSearchByName(args, "fileName")
        oldFile = self.variates[fileName]
        if Path(oldFile).exists():
            try:
                flag = False
                if variateName == "FanOrCompIn":
                    _, _, _, flag = self.getPropertyDiagramDatas(oldFile, 4, True)
                elif variateName == "CombustionChamber":
                    _, _, flag = self.verifyCombustionChamberData(oldFile)
                elif variateName == "TurbineIn":
                    _, _, _, flag = self.getPropertyDiagramDatas(oldFile, 6, False)

                if flag:
                    newFileName = self.parameterSearchByName(args, "newFileName")
                    filePath = CommonHelper.getAbsFilePath(
                        "./files/{0}/{1}".format(self.category, newFileName)
                    )
                    shutil.copyfile(oldFile, filePath)
                    QMessageBox.about(self, "提示", "导入成功")

            except Exception as e:
                logger.exception(e)
                QMessageBox.about(self, "提示", "导入失败")
        else:
            QMessageBox.about(self, "提示", "文件不存在")
