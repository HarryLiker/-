from PyQt5.QtWidgets import QMainWindow, QWidget, QShortcut, QHeaderView
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt, QModelIndex

from matplotlib.figure import Figure
import networkx as nx

from ui_mainwindow import Ui_MainWindow
from matrix_graph import GraphMatrixModel

from matplotlib_pkgs import FigureCanvas

gr = []
MaxCliques = []
Max = []

def N(vertex):
    return [i for i, n_v in enumerate(gr[vertex]) if n_v]

def Bron_Kerbosch(r,p,x):
    global Max
    global MaxCliques
    if len(p) == 0 and len(x) == 0:
        MaxCliques.append(list(r))
        if len(r) > len(Max):
            Max = list(r)
    for vertex in p[:]:
        r_new = r[:]
        r_new.append(vertex)
        p_new = [val for val in p if val in N(vertex)]
        x_new = [val for val in x if val in N(vertex)]
        Bron_Kerbosch(r_new, p_new, x_new)
        p.remove(vertex)
        x.append(vertex)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent: QWidget = None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # configure canvas graph view
        self.mtplt_figure = Figure()
        self.qt_figure = FigureCanvas(self.mtplt_figure)
        self.graph_ax = self.mtplt_figure.subplots()
        self.configureAx()

        self.qt_figure.setMinimumSize(100, 100)

        self.horizontalLayout_2.insertWidget(1, self.qt_figure)

        # configure connections
        self.startButton.clicked.connect(self.algo)
        #self.MaxCliqueButton.clicked.connect
        self.clearButton.clicked.connect(self.clearGraph)
        self.addButton.clicked.connect(self.addNode)
        self.deleteButton.clicked.connect(self.deleteNode)

        # configure table graph view
        self.matrix_graph = GraphMatrixModel(self)
        self.tableView.setModel(self.matrix_graph)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # title
        self.setWindowTitle('Курсовая работа №8')

        # shortcuts
        start_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_R), self)
        start_shortcut.activated.connect(self.algo)
        start_shortcut.setEnabled(True)

        clear_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_C), self)
        clear_shortcut.activated.connect(self.clearGraph)
        clear_shortcut.setEnabled(True)

    def addNode(self):
        graph = self.matrix_graph.graph
        self.matrix_graph.beginResetModel()
        graph.add_node(graph.number_of_nodes())
        self.matrix_graph.endResetModel()

    def deleteNode(self):
        graph = self.matrix_graph.graph
        if graph.number_of_nodes() == 0:
            return
        self.matrix_graph.beginResetModel()
        graph.remove_node(graph.number_of_nodes() - 1)
        self.matrix_graph.endResetModel()

    def configureAx(self):
        self.graph_ax.axis('off')
        self.graph_ax.margins(.5)

    def updateGraph(self):
        self.graph_ax.clear()

        G = self.matrix_graph.graph

        pos = nx.circular_layout(G)  # positions for all nodes

        # nodes
        nx.draw_networkx_nodes(G, pos, node_size=700, ax=self.graph_ax)

        # edges
        nx.draw_networkx_edges(G, pos, width=6, ax=self.graph_ax)

        # labels
        nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif', ax=self.graph_ax)

        self.configureAx()
        self.qt_figure.draw()

    def clearGraph(self):
        self.output('Граф сброшен')
        self.graph_ax.clear()
        self.configureAx()
        self.qt_figure.draw()

    def output(self, text: str):
        self.outputTextBrowser.append(text)


    def algo(self):
        global Max
        global MaxCliques
        self.output('Запуск алгоритма')
        graph = self.matrix_graph.graph

        for i in range(len(graph.nodes)):
            gr.append([0] * len(graph.nodes))
        a = list(graph.edges)

        for i in a:
            i = list(i)
            m = i[0]
            l = i[1]
            gr[m][l] = 1
            gr[l][m] = 1

        print(gr)


        Bron_Kerbosch([], [i for i in range(len(graph.nodes))], [])

        print("Max = ", Max)
        self.outputTextBrowser.append("Максимальные клики: ")
        for i in range(len(MaxCliques)):
            self.outputTextBrowser.append(str(MaxCliques[i]))
        self.outputTextBrowser.append("Наибольшая клика: ")
        self.outputTextBrowser.append(str(Max))
        print(gr)
        gr.clear()
        Max.clear()
        MaxCliques.clear()


        # HERE ALGORITHM <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< <3 ^-^

        self.updateGraph()  # must have
