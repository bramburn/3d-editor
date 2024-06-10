import sys
from PySide6.QtGui import QVector3D, QColor, QQuaternion
from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.Qt3DRender import Qt3DRender

class CoordinateAxis:
    def __init__(self, root_entity):
        self.root_entity = root_entity

        # Create the X-axis (red)
        x_axis_mesh = Qt3DExtras.QConeMesh()
        x_axis_mesh.setBottomRadius(0.1)
        x_axis_mesh.setLength(10)
        x_axis_mesh.setRings(10)
        x_axis_mesh.setSlices(10)
        x_axis_mesh.setTopRadius(0.1)
        x_axis_entity = Qt3DCore.QEntity(self.root_entity)
        x_axis_entity.addComponent(x_axis_mesh)
        x_axis_material = Qt3DExtras.QPhongMaterial()
        x_axis_material.setDiffuse(QColor("red"))
        x_axis_entity.addComponent(x_axis_material)
        transform = Qt3DCore.QTransform()
        transform.setTranslation(QVector3D(0, 0, 0))
        x_axis_entity.addComponent(transform)

        # Create the Y-axis (green)
        y_axis_mesh = Qt3DExtras.QCylinderMesh()
        y_axis_mesh.setRadius(0.1)
        y_axis_mesh.setLength(10)
        y_axis_mesh.setRings(10)
        y_axis_mesh.setSlices(10)
        y_axis_entity = Qt3DCore.QEntity(self.root_entity)
        y_axis_entity.addComponent(y_axis_mesh)
        y_axis_material = Qt3DExtras.QPhongMaterial()
        y_axis_material.setDiffuse(QColor("green"))
        y_axis_entity.addComponent(y_axis_material)
        transform = Qt3DCore.QTransform()
        transform.setTranslation(QVector3D(0, 0, 0))
        transform.setRotation(QQuaternion.fromAxisAndAngle(QVector3D(0, 0, 1), 90))
        y_axis_entity.addComponent(transform)

        # Create the Z-axis (blue)
        z_axis_mesh = Qt3DExtras.QConeMesh()
        z_axis_mesh.setBottomRadius(0.1)
        z_axis_mesh.setLength(10)
        z_axis_mesh.setRings(10)
        z_axis_mesh.setSlices(10)
        z_axis_mesh.setTopRadius(0.1)
        z_axis_entity = Qt3DCore.QEntity(self.root_entity)
        z_axis_entity.addComponent(z_axis_mesh)
        z_axis_material = Qt3DExtras.QPhongMaterial()
        z_axis_material.setDiffuse(QColor("blue"))
        z_axis_entity.addComponent(z_axis_material)
        transform = Qt3DCore.QTransform()
        transform.setTranslation(QVector3D(0, 0, 0))
        transform.setRotation(QQuaternion.fromAxisAndAngle(QVector3D(0, 0, 1), 90))
        z_axis_entity.addComponent(transform)