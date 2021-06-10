import json
import sys
import datetime

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QPalette, QColor

from PySide6.QtCore import Qt

from MainWindow import Ui_MainWindow

tick = QtGui.QImage("tick.png")


class TodoModel(QtCore.QAbstractTableModel):
  def __init__(self, todos=None):
    super().__init__()
    self.todos = todos or []

  def data(self, index, role):
    if role == Qt.DisplayRole:
      value = self.todos[index.row()][index.column()]

      return value

    if role == Qt.DecorationRole:
      value = self.todos[index.row()][index.column()]
      if isinstance(value, bool):
        if value:
          return QtGui.QIcon("tick.png")

    if role == Qt.DisplayRole:
      value = self._data[index.row()][index.column()]
      return value

    if role == Qt.BackgroundRole:
      value = self.data[index.row()][index.column()]
      if isinstance(value, int) or isinstance(value, float):
        value = int(value)  # Convert to integer for indexing.
        return QtGui.QColor('#ffbf00')

  def rowCount(self, index):
    return len(self.todos)

  def columnCount(self, index):
    return len(self.todos[0])



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
  def __init__(self):
    super().__init__()

    self.setupUi(self)
    self.model = TodoModel()
    self.load()
    self.todoView.setModel(self.model)
    self.addButton.pressed.connect(self.add)
    self.deleteButton.pressed.connect(self.delete)
    self.completeButton.pressed.connect(self.complete)

  def add(self):
    """
    Add an item to our todo list, getting the text from the QLineEdit .todoEdit
    and then clearing it.
    """
    text = self.todoEdit.text()
    number = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if text:  # Don't add empty strings.
      # Access the list via the model.
      self.model.todos.append((False, text, number))
      # Trigger refresh.
      self.model.layoutChanged.emit()
      # Empty the input
      self.todoEdit.setText("")
      self.save()

  def delete(self):
    indexes = self.todoView.selectedIndexes()
    if indexes:
      # Indexes is a list of a single item in single-select mode.
      index = indexes[0]
      # Remove the item and refresh.
      del self.model.todos[index.row()]
      self.model.layoutChanged.emit()
      # Clear the selection (as it is no longer valid).
      self.todoView.clearSelection()
      self.save()

  def complete(self):
    indexes = self.todoView.selectedIndexes()
    if indexes:
      index = indexes[0]
      row = index.row()
      status, text, number = self.model.todos[row]
      self.model.todos[row] = (True, text, number)
      # .dataChanged takes top-left and bottom right, which are equal
      # for a single selection.
      self.model.dataChanged.emit(index, index)
      # Clear the selection (as it is no longer valid).
      self.todoView.clearSelection()
      self.save()

  def load(self):
    try:
      with open("data.json", "r") as f:
        self.model.todos = json.load(f)
    except Exception:
      pass

  def save(self):
    with open("data.json", "w") as f:
      data = json.dump(self.model.todos, f)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()

darkPalette = QPalette()
darkPalette.setColor(QPalette.Window, QColor(53, 53, 53))
darkPalette.setColor(QPalette.WindowText, Qt.white)
darkPalette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127))
darkPalette.setColor(QPalette.Base, QColor(42, 42, 42))
darkPalette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
darkPalette.setColor(QPalette.ToolTipBase, Qt.white)
darkPalette.setColor(QPalette.ToolTipText, Qt.white)
darkPalette.setColor(QPalette.Text, Qt.darkGray)

#darkPalette.setColor(QPalette.QLineEdit.Text, Qt.white)
darkPalette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
darkPalette.setColor(QPalette.Dark, QColor(35, 35, 35))
darkPalette.setColor(QPalette.Shadow, QColor(20, 20, 20))
darkPalette.setColor(QPalette.Button, QColor(53, 53, 53))
darkPalette.setColor(QPalette.ButtonText, QColor(53, 53, 53))
darkPalette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
darkPalette.setColor(QPalette.BrightText, Qt.red)
darkPalette.setColor(QPalette.Link, QColor(42, 130, 218))
darkPalette.setColor(QPalette.Highlight, QColor(42, 130, 218))
darkPalette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(80, 80, 80))
darkPalette.setColor(QPalette.HighlightedText, Qt.white)
darkPalette.setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(127, 127, 127))
app.setPalette(darkPalette)

window.show()
app.exec()
