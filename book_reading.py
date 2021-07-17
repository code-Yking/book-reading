import wx
import json
import datetime
import matplotlib
from pubsub import pub
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

from search import *
from menu_GUI import *

matplotlib.use('WXAgg')

'''CONSTANTS'''
JSON_LOC = 'books.json'
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']
NOW = datetime.datetime.now()

'''GLOBAL'''
s = 0

'''STYLE'''
# HEAD = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)


def open_json():
    with open(JSON_LOC) as f:
        data = json.load(f)
        f.close()
    return data


def insert_json(data):
    with open(JSON_LOC, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)
        f.close()
        pub.sendMessage('graphing.do')


class GraphInfo(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        info_sizer = wx.BoxSizer(wx.VERTICAL)
        header = wx.StaticText(self, -1, label='Reading Stats')
        font = wx.Font(14, wx.FONTFAMILY_DEFAULT,
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        header.SetFont(font)

        label_this_month = wx.StaticText(
            self, -1, label='Books read this month: ')
        label_latest = wx.StaticText(self, -1, label='Latest Book read: ')
        label_a_rate = wx.StaticText(self, -1, label='Average Reading Rate: ')
        label_r_rate = wx.StaticText(self, -1, label='Required Rate: ')

        more_states_btn = wx.Button(self, label='More Book Stats')

        search_btn = wx.Button(self, label='Search a Book')
        search_btn.Bind(wx.EVT_BUTTON, self.open_search)

        info_sizer.Add(header, 0, wx.ALL | wx.CENTER, 5)
        info_sizer.Add(label_this_month, 0, wx.ALL, 5)
        info_sizer.Add(label_latest, 0, wx.ALL, 5)
        info_sizer.Add(label_a_rate, 0, wx.ALL, 5)
        info_sizer.Add(label_r_rate, 0, wx.ALL, 5)
        info_sizer.Add(more_states_btn, 0, wx.ALL | wx.CENTER, 10)
        info_sizer.Add(search_btn, 0, wx.ALL | wx.CENTER, 5)
        self.SetSizer(info_sizer)

    def open_search(self, event):
        global s
        print(s)
        if s == 0:
            SearchFrame().Show()
            s += 1
            print(s)


class GraphsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        graph_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.figure = Figure(figsize=(5, 3))
        self.axes = self.figure.add_subplot()

        self.canvas = FigureCanvas(self, -1, self.figure)
        graph_sizer.Add(self.canvas, 0, wx.ALL | wx.CENTER, 5)
        self.set_graph()
        graph_info = GraphInfo(self)
        graph_sizer.Add(graph_info, 0, wx.ALL | wx.CENTER, 5)
        self.SetSizer(graph_sizer)

        pub.subscribe(self.set_graph, 'graphing.do')

    def set_graph(self, text=''):
        data = open_json()

        self.figure.clf()
        self.axes = self.figure.add_subplot()
        self.axes.set_title('Books read in the last 12 months')

        y_ax = []
        for n in range(1, 13):
            y_ax.append(len(data['2020']['{}'.format(n)]))
        # print(y_ax)
        # print(sorted(data['2020'].keys()))
        # test = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        mon = []
        for n in MONTHS:
            mon.append(n[:3])

        self.axes.plot(mon, y_ax, '')
        self.canvas.draw()

    def clear(self):
        self.figure.clf()


class ButtonsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.remove_btn = wx.Button(self, label='Remove Book')
        buttons_sizer.Add(self.remove_btn, 0, wx.ALL | wx.CENTER, 5)

        self.update_btn = wx.Button(self, label='Update Book')
        buttons_sizer.Add(self.update_btn, 0, wx.ALL | wx.CENTER, 5)

        self.reset_btn = wx.Button(self, label='Reset')
        buttons_sizer.Add(self.reset_btn, 0, wx.ALL | wx.CENTER, 5)

        self.remove_btn.Disable()
        self.update_btn.Disable()
        self.reset_btn.Disable()
        self.SetSizer(buttons_sizer)

        pub.subscribe(self.change_btn, 'btn_changing.do')

    def reset_btn(self, event):
        pass

    def change_btn(self, btn, change):
        if btn == 'rem':
            if change == 'en':
                self.remove_btn.Enable()
            elif change == 'dis':
                self.remove_btn.Disable()
        elif btn == 'up':
            if change == 'en':
                self.update_btn.Enable()
            elif change == 'dis':
                self.update_btn.Disable()
        elif btn == 'res':
            if change == 'en':
                self.reset_btn.Enable()
            elif change == 'dis':
                self.reset_btn.Disable()


class InputPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        now = datetime.datetime.now()
        self.month = str(now.month)
        self.year = str(now.year)

        input_sizer = wx.BoxSizer(wx.HORIZONTAL)

        years = list(map(str, [*range(2000, int(self.year) + 1, 1)]))
        self.year_combo = wx.ComboBox(self, choices=years)
        input_sizer.Add(self.year_combo, 0, wx.ALL | wx.CENTER, 5)
        self.year_combo.SetSelection(int(self.year) - 2000)
        self.year_combo.Bind(wx.EVT_COMBOBOX, self.month_year_change)

        self.month_combo = wx.ComboBox(self, choices=MONTHS)
        input_sizer.Add(self.month_combo, 0, wx.ALL | wx.CENTER, 5)
        self.month_combo.SetSelection(int(self.month) - 1)
        self.month_combo.Bind(wx.EVT_COMBOBOX, self.month_year_change)

        self.items = [""] + list(map(str, open_json()[self.year][self.month]))
        # items_2 = [""] + items
        # print(items_2)
        self.input_ctr = wx.ComboBox(self)
        input_sizer.Add(self.input_ctr, 0, wx.ALL | wx.CENTER, 5)
        self.input_ctr.Bind(wx.EVT_COMBOBOX, self.input_change)
        self.input_ctr.Bind(wx.EVT_TEXT, self.changed_text)

        for n in open_json()[self.year][self.month]:
            self.input_ctr.Append(str(n))

        self.add_btn = wx.Button(self, label='Add Book')
        self.add_btn.Bind(wx.EVT_BUTTON, self.add_input)
        input_sizer.Add(self.add_btn, 0, wx.ALL | wx.CENTER, 5)

        self.SetSizer(input_sizer)

    def changed_text(self, event):
        if not self.add_btn.IsEnabled():
            pub.sendMessage('btn_changing.do', btn='rem', change='en')
            pub.sendMessage('btn_changing.do', btn='up', change='en')
        print(current_edit)

    def input_change(self, event):
        data = open_json()
        self.add_btn.Disable()
        global current_edit
        current_edit = self.input_ctr.GetValue()
        pub.sendMessage('btn_changing.do', btn='rem', change='en')
        # print(list(self.input_ctr))
        self.input_ctr.Append("Insert new...")

    def month_year_change(self, event):
        month = int(MONTHS.index(self.month_combo.GetValue())) + 1
        year = str(self.year_combo.GetValue())
        print("Month: {} Year: {}".format(month, year))

        data = open_json()

        self.input_ctr.Clear()
        for n in data[year][str(month)]:
            self.input_ctr.Append(str(n))

    def add_input(self, event):
        month = int(MONTHS.index(self.month_combo.GetValue())) + 1
        year = str(self.year_combo.GetValue())
        book_no = int(self.input_ctr.GetValue())
        data = open_json()

        if year not in data:
            data[year] = {}

        if str(month) in data[year]:
            data[year][str(month)].append(book_no)
        else:
            data[year][str(month)] = []
            data[year][str(month)].append(book_no)
        insert_json(data)

        self.input_ctr.Clear()
        for n in data[year][str(month)]:
            self.input_ctr.Append(str(n))


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Book Reading", size=(700, 450))
        main_panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        nm = wx.StaticBox(main_panel, -1, '')
        nmSizer = wx.StaticBoxSizer(nm, wx.VERTICAL)

        buttons_panel = ButtonsPanel(main_panel)
        input_panel = InputPanel(main_panel)
        graphs_panel = GraphsPanel(main_panel)

        header = wx.StaticText(main_panel, -1, label='Reading Log')
        font = wx.Font(14, wx.FONTFAMILY_DEFAULT,
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        header.SetFont(font)

        main_sizer.Add(graphs_panel, 0, wx.ALIGN_CENTER_HORIZONTAL, border=10)
        main_sizer.Add(header, 0, wx.ALIGN_CENTER_HORIZONTAL, border=10)
        nmSizer.Add(input_panel, 0, wx.ALIGN_CENTER_HORIZONTAL, border=10)
        nmSizer.Add(buttons_panel, 0, wx.ALIGN_CENTER_HORIZONTAL, border=10)
        main_sizer.Add(nmSizer, 0, wx.ALIGN_CENTER_HORIZONTAL, border=5)
        main_panel.SetSizer(main_sizer)
        self.Show()
        self.Fit()

        self.SetMenuBar(MenuBar())


if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame()
    SearchFrame().Show()
    app.MainLoop()
