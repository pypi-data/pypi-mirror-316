#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-11-06 17:43:36
LastEditors  : Kofi
LastEditTime : 2023-11-06 17:43:38
Description  : 
"""
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QGraphicsView, QRubberBand, QFrame, QGraphicsScene
from PyQt5.QtGui import QPixmap, QTransform


class ImageView(QGraphicsView):
    def __init__(self, parent=None):
        super(ImageView, self).__init__(parent)
        self.setFrameShape(QFrame.NoFrame)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    def setup_crop(self, width, height):
        self.rband = QRubberBand(QRubberBand.Rectangle, self)
        coords = self.mapFromScene(0, 0, width, height)
        self.rband.setGeometry(QRect(coords.boundingRect()))
        self.rband.show()

    def crop_draw(self, x, y, width, height):
        coords = self.mapFromScene(x, y, width, height)
        self.rband.setGeometry(QRect(coords.boundingRect()))

    def get_coords(self):
        rect = self.rband.geometry()
        size = self.mapToScene(rect).boundingRect()
        x = int(size.x())
        y = int(size.y())
        width = int(size.width())
        height = int(size.height())
        return (x, y, width, height)

    def setPic(self, pixmap: QPixmap):
        self.scene.clear()
        self.scene.addPixmap(pixmap)
        self.scene.setSceneRect(0, 0, pixmap.width(), pixmap.height())
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def rotate(self, angle):
        # 获取当前的pixmap
        pixmap = self.scene().items()[0].pixmap()

        # 对pixmap进行旋转
        transform = QTransform().rotate(angle)
        rotated_pixmap = pixmap.transformed(transform)

        # 更新场景中的pixmap
        self.scene().clear()
        self.scene().addPixmap(rotated_pixmap)
        self.scene().setSceneRect(0, 0, rotated_pixmap.width(), rotated_pixmap.height())

        # 调整视图的显示范围
        self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)
