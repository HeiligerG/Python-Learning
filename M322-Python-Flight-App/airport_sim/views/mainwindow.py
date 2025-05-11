
from pathlib import Path
from PySide6.QtWidgets import (QMainWindow,QWidget,QVBoxLayout,QGridLayout,QTableView,
                               QHeaderView,QLabel,QHBoxLayout,QSlider,QPushButton)
from PySide6.QtCore import Qt
from controllers.airport_sim import AirportSim,AIRPORTS
from views.tablemodels import FlightModel,TicketModel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Airport Dashboard v9")
        self.sim=AirportSim(Path("resources/state.json"))
        central=QWidget(); self.setCentralWidget(central)
        main=QVBoxLayout(central)

        # top bar with counters and cleanup button
        topbar=QHBoxLayout()
        self.counter=QLabel(); self.counter.setAlignment(Qt.AlignCenter)
        btn=QPushButton("Remove Crashes")
        btn.clicked.connect(self.sim.remove_crashes)
        topbar.addWidget(self.counter); topbar.addWidget(btn)
        main.addLayout(topbar)

        grid=QGridLayout(); main.addLayout(grid,5)
        self.fModel=FlightModel(self.sim.flights)
        self.tModel=TicketModel(self.sim.tickets)
        self.proxies=[]

        for i,ap in enumerate(AIRPORTS):
            view=self._view(self.fModel,lambda o,ap=ap: o.dest==ap)
            grid.addWidget(self._wrap(ap,view),i//2,i%2)

        tview = QTableView()
        tview.setModel(self.tModel)
        tview.verticalHeader().hide()
        tview.setAlternatingRowColors(True)
        tview.setStyleSheet(
            "QTableView { background:#222; color:white; alternate-background-color:#333; }"
        )
        tview.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        main.addWidget(self._wrap("Tickets", tview), 2)

        # immer refreshen, wenn sich Tickets ändern
        self.sim.tickets_changed.connect(self.tModel.refresh)


        # speed
        box=QHBoxLayout(); box.addWidget(QLabel("Tempo"))
        slider=QSlider(Qt.Horizontal); slider.setRange(-4,6); slider.setValue(0)
        box.addWidget(slider); main.addLayout(box)
        slider.valueChanged.connect(lambda v:self.sim.set_speed(2**v))

        # signals
        self.sim.flights_changed.connect(self.refresh_ui)
        self.sim.tickets_changed.connect(self.tModel.refresh)
        self.sim.tickets_changed.connect(lambda: self.proxies[-1].invalidateFilter())
        for p in self.proxies:
            self.sim.flights_changed.connect(p.invalidateFilter)
        self.refresh_ui()

    def refresh_ui(self):
        self.fModel.refresh()
        counts=self.sim.count_by_status()
        self.counter.setText(" | ".join(f"{k}: {v}" for k,v in counts.items()))

    def _view(self,model,filter_fn,stretch=True):
        from PySide6.QtCore import QSortFilterProxyModel,QModelIndex
        class Proxy(QSortFilterProxyModel):
            def __init__(self,fn): super().__init__(); self.fn=fn
            def filterAcceptsRow(self,row,parent=QModelIndex()):
                return self.fn(model.objs[row])
        proxy=Proxy(filter_fn); proxy.setSourceModel(model); self.proxies.append(proxy)
        view=QTableView(); view.setModel(proxy)
        view.verticalHeader().hide(); view.setAlternatingRowColors(True)
        view.setStyleSheet("QTableView { color: white; }")
        if stretch:
            view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        else:
            view.resizeColumnsToContents()
        return view

    def _wrap(self,title,view):
        w=QWidget(); l=QVBoxLayout(w); lbl=QLabel(f"<b>{title}</b>"); lbl.setAlignment(Qt.AlignCenter)
        l.addWidget(lbl); l.addWidget(view); return w
