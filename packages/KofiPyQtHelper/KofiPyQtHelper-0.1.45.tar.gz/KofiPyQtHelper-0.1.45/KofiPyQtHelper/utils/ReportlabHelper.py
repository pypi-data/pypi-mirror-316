#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2024-12-11 15:58:21
LastEditors  : Kofi
LastEditTime : 2024-12-11 15:58:21
Description  : 
"""
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4, landscape, LETTER, LEGAL
from reportlab.lib.units import mm
from reportlab.platypus import Image, Paragraph, Table, TableStyle, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
import re
import os
import copy

font_path = os.path.abspath("SimSun.ttf")


def has_balanced_braces(s):
    # 使用正则表达式查找所有的花括号
    return bool(re.search(r"\{[^{}]*\}", s))


class ReportlabHelper:
    def __init__(self):
        pdfmetrics.registerFont(TTFont("SimSun", font_path))
        self.styles = getSampleStyleSheet()
        self.style_normal = self.styles["Normal"]
        self.style_normal.fontName = "SimSun"

    def createDocument(self, template, filename, datas):
        pagesize = self.__getPageSize(template)
        bottom_margin, top_margin, right_margin, left_margin = self.__getPageMargin(
            template
        )
        # 创建 SimpleDocTemplate
        document = SimpleDocTemplate(
            filename,
            pagesize=pagesize,
            leftMargin=left_margin,
            topMargin=top_margin,
            rightMargin=right_margin,
            bottomMargin=bottom_margin,
        )
        elements = []

        if "pageSettings" in template:
            current = self.__groupDataByAttribute(
                datas[template["pageSettings"]["datasource"]],
                template["pageSettings"]["group"],
            )
            datas["dataSources"] = copy.deepcopy(
                datas[template["pageSettings"]["datasource"]]
            )
            for group_name, group_data in current.items():
                datas["currentGroupingNumber"] = group_name
                datas["currentGroupingCount"] = len(group_data)
                if "additional" in template["pageSettings"]:
                    for key, value in template["pageSettings"]["additional"].items():
                        datas[key] = group_data[0][value]

                pages = len(group_data) // template["pageSettings"]["recordsPageSize"]
                if len(group_data) % template["pageSettings"]["recordsPageSize"] > 0:
                    pages += 1
                for page in range(pages):
                    start_index = page * template["pageSettings"]["recordsPageSize"]
                    end_index = (page + 1) * template["pageSettings"]["recordsPageSize"]
                    datas[template["pageSettings"]["datasource"]] = group_data[
                        start_index:end_index
                    ]
                    self.__createElement(template, datas, elements)
                    elements.append(PageBreak())
        else:
            self.__createElement(template, datas, elements)

        document.build(elements)

    def __createElement(self, template, datas, elements):
        items = sorted(template["content"], key=lambda x: x["order"])
        for item in items:
            if item["type"] == "table":
                element = self.__createTables(item, datas)
            elif item["type"] == "label":
                element = self.__createLabel(item, datas)
            elif item["type"] == "spacer":
                element = self.__createSpacer(item)
            if isinstance(element, list):
                elements.extend(element)  # 合并列表
            else:
                elements.append(element)

    def __groupDataByAttribute(self, datas, attribute):
        groups = {}
        for data in datas:
            attr_value = data.get(attribute, None)
            if attr_value not in groups:
                groups[attr_value] = []
            groups[attr_value].append(data)
        return groups

    def __getPageMargin(self, template):
        if isinstance(template["margin"], list):
            margin_list = template["margin"]
            # 根据列表长度动态设置边距
            if len(margin_list) == 2:
                top_bottom_margin, side_margin = margin_list
                top_margin = bottom_margin = top_bottom_margin * mm
                left_margin = right_margin = side_margin * mm
            elif len(margin_list) == 3:
                top_margin, side_margin, bottom_margin = margin_list
                left_margin = right_margin = side_margin * mm
                top_margin *= mm
                bottom_margin *= mm
            else:
                left_margin, top_margin, right_margin, bottom_margin = [
                    m * mm for m in margin_list
                ]
        elif isinstance(template["margin"], int):
            # 使用整数设置统一边距
            left_margin = top_margin = right_margin = bottom_margin = (
                template["margin"] * mm
            )
        else:
            # 默认边距设置
            left_margin = top_margin = right_margin = bottom_margin = 10 * mm
        return bottom_margin, top_margin, right_margin, left_margin

    def __getPageSize(self, template):
        page = template["page"]
        pagesize = A4
        if page["type"] == "letter":
            if "orientation" in page and page["orientation"] == "landscape":
                pagesize = landscape(LETTER)
            else:
                pagesize = LETTER
        elif page["type"] == "legal":
            if "orientation" in page and page["orientation"] == "landscape":
                pagesize = landscape(LEGAL)
            else:
                pagesize = LEGAL
        elif page["type"] == "A4":
            if "orientation" in page and page["orientation"] == "landscape":
                pagesize = landscape(A4)
            else:
                pagesize = A4
        elif page["type"] == "custom":
            if "width" in page and "height" in page:
                pagesize = (page["width"] * mm, page["height"] * mm)

        return pagesize

    def __createTables(self, items, datas):
        elements = []
        item = items["content"]
        if "datasource" in item:
            for data in datas[item["datasource"]]:
                self.__createTableItem(elements, item, data)
        else:
            self.__createTableItem(elements, item, datas)
        if "arrange" in item:
            count = item["arrange"]["count"]
            arranged_elements = []
            row = []

            for index, table in enumerate(elements):
                row.append(table)
                if (index + 1) % count == 0:
                    # 将两个 Table 作为一行放入一个父 Table 中
                    parent_table = Table([row])
                    arranged_elements.append(parent_table)
                    row = []

            if row:
                parent_table = Table([row])
                arranged_elements.append(parent_table)

            return arranged_elements
        else:
            return elements

    def __createTableItem(self, elements, item, data):
        table_data = []
        for row in item["datatemplate"]:
            cell_data = []
            for cell in row:
                if cell["type"] == "image":
                    cell_data.append(self.__createImage(cell, data))
                elif cell["type"] == "text":
                    content = self.__getContent(cell, data)
                    cell_data.append(content)
                elif cell["type"] == "empty":
                    cell_data.append("")
            table_data.append(cell_data)
        ops = {}
        if "colWidths" in item:
            ops["colWidths"] = item["colWidths"]
        if "rowHeights" in item:
            if isinstance(item["rowHeights"], int):
                ops["rowHeights"] = item["rowHeights"]
            elif isinstance(item["rowHeights"], list):
                ops["rowHeights"] = [item["rowHeights"] * len(item["datatemplate"])]
        table = Table(table_data, **ops)
        self.__setTableStyle(item, table)
        # 应用合并设置
        self.__setMergeStyle(item, table)

        elements.append(table)

    def __setTableStyle(self, item, table):
        tableStyle = [["FONTNAME", (0, 0), (-1, -1), "SimSun"]]
        for entry in item["style"]:
            # 将 entry 的第一个元素作为样式名称
            style_name = entry[0]

            # 解包 entry 的其余部分，将列表转换为元组
            style_params = tuple(
                tuple(param) if isinstance(param, list) else param
                for param in entry[1:]
            )

            # 添加到 tableStyle 列表中
            tableStyle.append((style_name, *style_params))

        table.setStyle(TableStyle(tableStyle))

    def __setMergeStyle(self, item, table):
        if "mergeConfigurations" in item:
            span_commands = []  # 用于存储所有 SPAN 样式命令

            for merge in item["mergeConfigurations"]:
                start = (merge["col"], merge["row"])
                end = start
                # 计算合并的结束坐标
                if "rowspan" in merge:
                    end = (end[0], end[1] + merge["rowspan"] - 1)

                if "colspan" in merge:
                    end = (end[0] + merge["colspan"] - 1, end[1])

                    # 添加 SPAN 命令
                span_commands.append(("SPAN", start, end))

                # 一次性应用所有的 SPAN 样式
            if span_commands:
                table.setStyle(TableStyle(span_commands))

    def __createImage(self, cell, data):
        img_path = self.__getContent(cell, data)
        target_width, target_height = self.__getImage(
            img_path,
            width=cell["width"] if "width" in cell else None,
            height=cell["height"] if "height" in cell else None,
        )
        return Image(img_path, width=target_width, height=target_height)

    def __getContent(self, item, datas):
        if has_balanced_braces(item["content"]):
            if type(item["name"]) == str:
                if "format" in item and item["name"] in item["format"]:
                    content = item["content"].replace(
                        "{" + f'{item["name"]}' + "}",
                        item["format"][item["name"]].format(str(datas[item["name"]])),
                    )
                else:
                    content = item["content"].replace(
                        "{" + f'{item["name"]}' + "}", str(datas[item["name"]])
                    )
            elif type(item["name"]) == list:
                content = item["content"]
                for i, row in enumerate(item["name"]):
                    content = content.replace("{" + f"{row}" + "}", datas[row])
        else:
            content = item["content"]
        return content

    def __getImage(self, img_path, width=None, height=None):
        image = ImageReader(img_path)
        original_width, original_height = image.getSize()

        if width is not None:
            target_width = width
            ratio = original_width / target_width
            if height is None:
                target_height = original_height / ratio
            else:
                target_height = height
        elif height is not None:
            target_height = height
            ratio = original_height / target_height
            if width is None:
                target_width = original_width / ratio
            else:
                target_width = width
        else:
            target_width = original_width
            target_height = original_height

        return target_width, target_height

    def __createLabel(self, item, datas):
        content = self.__getContent(item, datas)
        custom_style = copy.deepcopy(self.style_normal)
        if "style" in item and len(item["style"]) > 0:
            for key, value in item["style"].items():
                setattr(custom_style, key, value)
        return Paragraph(content, custom_style)

    def __createSpacer(self, item):
        return Spacer(0, item["value"] * mm)

    def __createFooter(self, item):
        pass

    def __createHeader(self, item):
        pass
