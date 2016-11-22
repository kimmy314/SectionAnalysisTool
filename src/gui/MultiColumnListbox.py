import tkinter.font as tkFont
import tkinter.ttk as ttk
import tkinter as tk

__author__ = 'Kim Nguyen'
class MultiColumnListbox(object):
    '''use a ttk.TreeView as a multicolumn ListBox'''

    def __init__(self, frame, headers, data, entry, infoList):
        self._headers = headers
        self._data = data
        self._frame = frame
        self.tree = None
        self._setup_widgets()
        self._build_tree()
        self._entry = entry
        self._infoList = infoList

    def _setup_widgets(self):
        container = ttk.Frame(self._frame)
        container.pack(fill='both', expand=True)
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=self._headers, show="headings", height=10)
        vsb = ttk.Scrollbar(orient="vertical",
            command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        self.tree.bind("<Double-1>", self.OnDoubleClick)

    def _build_tree(self):
        for col in self._headers:
            self.tree.heading(col, text=col.title())
            # adjust the column's width to the header string
            self.tree.column(col,
                width=tkFont.Font().measure(col.title()))

        for item in self._data:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(self._headers[ix], width=None) < col_w:
                    self.tree.column(self._headers[ix], width=col_w)
                    
    def OnDoubleClick(self, event):
        if self._entry != None:
            index = self.index()
            info = self._infoList[index]
            entryVar = tk.StringVar()
            entryVar.set(', '.join(str(x) for x in info))
            self._entry.configure(textvariable=entryVar)

    def addRow(self, item):
        self.tree.insert('', 'end', values=item)
        for i in range(len(item)):
            col_w = tkFont.Font().measure(item[i])
            if self.tree.column(self._headers[i], width=None) < col_w:
                self.tree.column(self._headers[i], width=col_w)

    def removeRow(self):
        item = None
        try:
            return self.index()
        except IndexError:
            pass
        finally:
            try:
                item = self.tree.selection()[0]
                self.tree.delete(item)
            except IndexError:
                pass

    def editRow(self, edits):
        index = self.removeRow()
        self.tree.insert('', index, values=edits)
        return index

    def index(self):
        item = self.tree.selection()[0]
        return self.tree.index(item)

    def getValues(self):
        # get a list of children of the root node
        children = self.tree.get_children()
        values = []
        for child in children:
            values.append(self.tree.set(child))
        return values

    def clear(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self._data = []
        self._infoList = []
