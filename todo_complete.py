import json
import sys
import datetime

from PySide6 import QtCore, QtGui, QtWidgets, QtSvg, QtSvgWidgets
from PySide6.QtGui import QPalette, QColor, QIcon

from PySide6.QtCore import Qt, QSize
from PySide6.QtSvgWidgets import QSvgWidget

from MainWindow import Ui_MainWindow

def statusIcon(i):
  switcher = {
    #0: 'new.gif',
    1: 'inprogress.png',
    2: 'checked.png'
  }
  return switcher.get(i)

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

      if index.column() == 0:

        # Load the svg
        #renderer = QtSvg.QSvgRenderer(statusIcon(value))
        #renderer.framesPerSecond()
        #renderer.animated()
        # Prepare a QImage with desired characteritisc
        #self.orig_svg = QtGui.QImage(500, 500, QtGui.QImage.Format_ARGB32)
        # Get QPainter that paints to the image
        #painter = QtGui.QPainter(self.orig_svg)
        #renderer.render(painter)

        #return QIcon("tick.png").pixmap(QSize())

        #return QIcon("tick.png").toImage()
        #return QIcon("error-404.svg").toImage()
        #return QtGui.setIcon(self.orig_svg)
        #return QtGui.QIcon(QtGui.QPixmap.fromImage(self.orig_svg))
        return QIcon(statusIcon(value))

    if role == Qt.DisplayRole:
      value = self.todos[index.row()][index.column()]
      return value

    if role == Qt.BackgroundRole:
      value = self.todos[index.row()][index.column()]
      if isinstance(value, int) or isinstance(value, float):
        value = int(value)  # Convert to integer for indexing.
        return QtGui.QColor('#2166ac')


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
    self.todoView.setStyleSheet("background-color: transparent, alternate-background-color")
    self.addButton.pressed.connect(self.add)
    self.deleteButton.pressed.connect(self.delete)
    self.completeButton.pressed.connect(self.complete)

  def add(self):
    """
    Add an item to our todo list, getting the text from the QLineEdit .todoEdit
    and then clearing it.
    """
    task_category = "(Other)"
    task = self.todoEdit.text()
    task_iteration = 0
    task_iteration_total = 1
    completion_type_id = 0 #0 = new, 1 = in progress, 2 =  complete
    created_dttm = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if task:  # Don't add empty strings.
      # Access the list via the model.
      self.model.todos.append((completion_type_id, task_category, task, task_iteration, task_iteration_total, created_dttm))
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
      completion_type_id, task_category, task, task_iteration, task_iteration_total, created_dttm = self.model.todos[row]

      #Increments iteration counts (allows for over-incrementing iterations for tracking purposes)
      if completion_type_id == 0:
        #task_iteration = task_iteration + 1
        completion_type_id = 1
      elif completion_type_id == 1 and task_iteration < task_iteration_total:
        task_iteration = task_iteration + 1
        if task_iteration >= task_iteration_total:
          completion_type_id = 2
      elif task_iteration >= task_iteration_total:
        completion_type_id = 2
        task_iteration = task_iteration + 1
      #if task_iteration < task_iteration_total:

      #On completion, check iteration counts vs total
      #update icons (new, in progress, complete)

      self.model.todos[row] = (completion_type_id,task_category, task, task_iteration, task_iteration_total, created_dttm)
      # .dataChanged takes top-left and bottom right, which are equal
      # for a single selection.
      self.model.dataChanged.emit(index, index)
      # Clear the selection (as it is no longer valid).
      self.todoView.clearSelection()
      self.save()
      self.model.layoutChanged.emit()

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
