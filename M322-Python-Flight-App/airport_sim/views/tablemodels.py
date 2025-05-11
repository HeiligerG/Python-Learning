
from PySide6 import QtCore, QtGui
from dataclasses import fields
COLOR={"En Route":"#F39C12","Delay":"#E74C3C","At Gate":"#27AE60","Boarding":"#2980B9","Crash":"#8B0000"}
class Base(QtCore.QAbstractTableModel):
    def __init__(self,objs): super().__init__(); self.objs=objs; self.cols=[f.name for f in fields(objs[0])] if objs else []
    def rowCount(self,p=QtCore.QModelIndex()): return len(self.objs)
    def columnCount(self,p=QtCore.QModelIndex()): return len(self.cols)
    def data(self,idx,role=QtCore.Qt.DisplayRole):
        if not idx.isValid(): return None
        obj=self.objs[idx.row()]
        val=getattr(obj,self.cols[idx.column()])
        if role==QtCore.Qt.DisplayRole: return "" if val is None else str(val)
        if role==QtCore.Qt.BackgroundRole and hasattr(obj,"status"):
            c=COLOR.get(getattr(obj,"status"))
            if c: return QtGui.QBrush(QtGui.QColor(c))
        return None
    def headerData(self,s,ori,role):
        if role!=QtCore.Qt.DisplayRole: return None
        return self.cols[s].capitalize() if ori==QtCore.Qt.Horizontal else s+1
    def refresh(self): self.beginResetModel(); self.endResetModel()
class FlightModel(Base): pass
class TicketModel(Base): pass
class TicketModel(Base):
    def refresh(self):
        # falls beim Start keine Tickets da waren → Spalten jetzt nachziehen
        if self.objs and not self.cols:
            self.cols = [f.name for f in fields(self.objs[0])]
        super().refresh()
