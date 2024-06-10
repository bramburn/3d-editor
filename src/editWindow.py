from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.QtWidgets import (QColorDialog, QDialog, QFormLayout, QLineEdit, QLabel,
                               QHBoxLayout, QDoubleSpinBox, QMenu)
from PySide6.QtGui import QColor, QMouseEvent, QVector3D, QQuaternion
from PySide6.QtCore import Qt
from src.command import Command
from src.constants import STL_SCALE


class EditWindow(QDialog):
    """
    A class used to represent an Edit Window which allows for editing the attributes of a selected object.
    ...
    """

    def __init__(self, mainWindow, parent=None):
        super().__init__(parent)

        self.mainWindow = mainWindow
        self.setWindowTitle("Edit Object")

        # Create a form for editing the selected object's attributes
        self.editForm = QFormLayout(self)

        # Create input fields for the attributes
        self.nameEdit = QLineEdit()

        # Create a label for the color
        self.colorLabel = QLabel()
        self.colorLabel.setAutoFillBackground(True)
        self.colorLabel.mousePressEvent = self.handleMouseClick
        self.colorLabel.setCursor(Qt.PointingHandCursor)

        # Create separate input fields for each component of the position
        self.positionXEdit = self.createSpinBox(-100.0, 100.0, 1)
        self.positionYEdit = self.createSpinBox(-100.0, 100.0, 1)
        self.positionZEdit = self.createSpinBox(-100.0, 100.0, 1)

        # Create a QHBoxLayout for the position fields
        self.positionLayout = QHBoxLayout()
        self.positionLayout.addWidget(self.positionXEdit)
        self.positionLayout.addWidget(self.positionYEdit)
        self.positionLayout.addWidget(self.positionZEdit)

        # Create separate input fields for each component of the orientation
        self.orientationWEdit = self.createSpinBox(-1.0, 1.0, 0.05)
        self.orientationXEdit = self.createSpinBox(-1.0, 1.0, 0.05)
        self.orientationYEdit = self.createSpinBox(-1.0, 1.0, 0.05)
        self.orientationZEdit = self.createSpinBox(-1.0, 1.0, 0.05)

        # Create a QHBoxLayout for the orientation fields
        self.orientationLayout = QHBoxLayout()
        self.orientationLayout.addWidget(self.orientationWEdit)
        self.orientationLayout.addWidget(self.orientationXEdit)
        self.orientationLayout.addWidget(self.orientationYEdit)
        self.orientationLayout.addWidget(self.orientationZEdit)

        # Create separate input fields for each dimension of the object
        self.dimensionXEdit = self.createSpinBox(0.0, 100.0, 1)
        self.dimensionYEdit = self.createSpinBox(0.0, 100.0, 1)
        self.dimensionZEdit = self.createSpinBox(0.0, 100.0, 1)

        # Create a QHBoxLayout for the dimension fields
        self.dimensionLayout = QHBoxLayout()
        self.dimensionLayout.addWidget(self.dimensionXEdit)
        self.dimensionLayout.addWidget(self.dimensionYEdit)
        self.dimensionLayout.addWidget(self.dimensionZEdit)

        # Add the input fields to the form
        self.editForm.addRow("Name:", self.nameEdit)
        self.editForm.addRow("Color:", self.colorLabel)
        self.editForm.addRow("Position:", self.positionLayout)
        self.editForm.addRow("Orientation:", self.orientationLayout)
        self.editForm.addRow("Dimensions:", self.dimensionLayout)

        # Create a list to keep track of the changes
        self.history = []
        self.history_index = -1

        # Connect the editingFinished signals to the applyChanges methods
        self.nameEdit.editingFinished.connect(self.applyNameChange)
        self.positionXEdit.valueChanged.connect(self.applyPositionChange)
        self.positionYEdit.valueChanged.connect(self.applyPositionChange)
        self.positionZEdit.valueChanged.connect(self.applyPositionChange)
        self.orientationWEdit.valueChanged.connect(self.applyOrientationChange)
        self.orientationXEdit.valueChanged.connect(self.applyOrientationChange)
        self.orientationYEdit.valueChanged.connect(self.applyOrientationChange)
        self.orientationZEdit.valueChanged.connect(self.applyOrientationChange)
        self.dimensionXEdit.valueChanged.connect(self.applyDimensionChange)
        self.dimensionYEdit.valueChanged.connect(self.applyDimensionChange)
        self.dimensionZEdit.valueChanged.connect(self.applyDimensionChange)

    def createSpinBox(self, min_val, max_val, step):
        spin_box = QDoubleSpinBox()
        spin_box.setMinimum(min_val)
        spin_box.setMaximum(max_val)
        spin_box.setSingleStep(step)
        return spin_box

    def executeCommand(self, data):
        command = Command(self.selectedEntity, data)
        command.execute()
        self.history.append(command)
        self.history_index += 1

    def applyNameChange(self):
        name = self.nameEdit.text()
        self.executeCommand({'name': name})

    def applyPositionChange(self):
        position = QVector3D(self.positionXEdit.value(), self.positionYEdit.value(), self.positionZEdit.value())
        self.executeCommand({'position': position})

    def applyOrientationChange(self):
        orientation = QQuaternion(self.orientationWEdit.value(), self.orientationXEdit.value(),
                                  self.orientationYEdit.value(), self.orientationZEdit.value())
        self.executeCommand({'orientation': orientation})

    def applyDimensionChange(self):
        dimensions = QVector3D(self.dimensionXEdit.value(), self.dimensionYEdit.value(), self.dimensionZEdit.value())
        self.executeCommand({'dimensions': dimensions})

    def handleMouseClick(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.openColorPicker(event)
        elif event.button() == Qt.RightButton:
            self.showContextMenu(event.pos())

    def openColorPicker(self, event: QMouseEvent):
        color = QColorDialog.getColor(self.selectedEntity.material.diffuse())
        if color.isValid():
            self.updateColorLabel(color)
            self.executeCommand({'color': color.getRgb()})

    def showContextMenu(self, position):
        menu = QMenu(self)
        resetAction = menu.addAction("Reset Color")
        resetAction.triggered.connect(self.resetColor)
        menu.exec(self.colorLabel.mapToGlobal(position))

    def resetColor(self):
        defaultColor = QColor(255, 255, 255)  # Example default color
        self.updateColorLabel(defaultColor)
        self.executeCommand({'color': defaultColor.getRgb()})

    def updateColorLabel(self, color):
        palette = self.colorLabel.palette()
        palette.setColor(self.colorLabel.backgroundRole(), color)
        self.colorLabel.setPalette(palette)

    def blockOrUnblockSignals(self, block):
        self.nameEdit.blockSignals(block)
        self.positionXEdit.blockSignals(block)
        self.positionYEdit.blockSignals(block)
        self.positionZEdit.blockSignals(block)
        self.orientationWEdit.blockSignals(block)
        self.orientationXEdit.blockSignals(block)
        self.orientationYEdit.blockSignals(block)
        self.orientationZEdit.blockSignals(block)
        self.dimensionXEdit.blockSignals(block)
        self.dimensionYEdit.blockSignals(block)
        self.dimensionZEdit.blockSignals(block)

    def loadEntity(self, entity):
        self.selectedEntity = entity
        self.blockOrUnblockSignals(True)
        self.nameEdit.setText(entity.name)
        self.updateColorLabel(entity.material.diffuse())
        self.positionXEdit.setValue(entity.transform.translation().x())
        self.positionYEdit.setValue(entity.transform.translation().y())
        self.positionZEdit.setValue(entity.transform.translation().z())
        self.orientationWEdit.setValue(entity.transform.rotation().scalar())
        self.orientationXEdit.setValue(entity.transform.rotation().x())
        self.orientationYEdit.setValue(entity.transform.rotation().y())
        self.orientationZEdit.setValue(entity.transform.rotation().z())
        self.dimensionXEdit.setValue(entity.mesh.xExtent() if isinstance(entity.mesh, Qt3DExtras.QCuboidMesh) else 0)
        self.dimensionYEdit.setValue(entity.mesh.yExtent() if isinstance(entity.mesh, Qt3DExtras.QCuboidMesh) else 0)
        self.dimensionZEdit.setValue(entity.mesh.zExtent() if isinstance(entity.mesh, Qt3DExtras.QCuboidMesh) else 0)
        self.blockOrUnblockSignals(False)

    def undo(self):
        if self.history_index >= 0:
            command = self.history[self.history_index]
            command.undo()
            self.history_index -= 1

    def redo(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            command = self.history[self.history_index]
            command.execute()