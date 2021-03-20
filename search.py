from book_reading import *


def search_book(event):
    # book = self.input_book.GetValue()
    book = _b
    book_read = {}
    no_read = 0
    data = open_json()

    for y in data:
        for m in data[y]:
            for p in data[y][m]:
                if int(p) == int(book):
                    # print(y, m, p)
                    if any(x == int(y) for x in book_read):
                        book_read[int(y)].append(int(m))
                        book_read[int(y)].sort()
                        no_read += 1
                    else:
                        book_read[int(y)] = []
                        book_read[int(y)].append(int(m))
                        no_read += 1
                    # book_read.sort()
    print(book_read)
    # print(no_read)
    last_month = int(list(book_read[list(book_read)[-1]])[-1])
    last_read = "{} {}".format(MONTHS[last_month - 1], list(book_read)[-1])
    last_read_this = len(book_read[NOW.year])
    pub.sendMessage('details_changing.do', nm=no_read, lr=last_read, nrt=last_read_this)


class InputPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)

        label_book = wx.StaticText(self, -1, label='Book Number: ')
        self.input_book = wx.TextCtrl(self, -1)
        self.input_book.Bind(wx.EVT_TEXT, self.text_change)

        input_sizer.Add(label_book, 0, wx.ALL, 10)
        input_sizer.Add(self.input_book, 0, wx.ALL, 10)

        self.SetSizer(input_sizer)

    def text_change(self, event):
        global _b
        _b = self.input_book.GetValue()
        # print(_b)


class LeftInfoPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        info_sizer = wx.BoxSizer(wx.VERTICAL)

        self.last_read = wx.StaticText(self, 0, label='Last read: ')
        self.no_read = wx.StaticText(self, 0, label='Times read: ')
        self.no_read_this = wx.StaticText(self, 0, label='This year: ')

        info_sizer.Add(self.last_read, 0, wx.ALL, 5)
        info_sizer.Add(self.no_read, 0, wx.ALL, 5)
        info_sizer.Add(self.no_read_this, 0, wx.ALL, 5)

        self.SetSizer(info_sizer)

        pub.subscribe(self.change_details, 'details_changing.do')

    def change_details(self, lr, nm, nrt):
        self.last_read.SetLabel("Last read: {}".format(lr))
        self.no_read.SetLabel("Times read: {}".format(nm))
        self.no_read_this.SetLabel("This year: {}".format(nrt))

        self.parent.add_pref()
        self.parent.Fit()


class RightInfoPanel(wx.Panel):
    def __init__(self, parent):
        """Constructor"""
        super().__init__(parent)
        r_info_sizer = wx.BoxSizer(wx.VERTICAL)

        self.preferred = wx.StaticText(self, 0, label='Preferred Reading')
        self.preferred.SetForegroundColour((50,205,50))
        r_info_sizer.Add(self.preferred, 0, wx.ALL, 5)

        self.SetSizer(r_info_sizer)


class InfoPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.info_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.l_info_panel = LeftInfoPanel(self)

        self.info_sizer.Add(self.l_info_panel, 0, wx.EXPAND | wx.LEFT, 5)

        self.SetSizer(self.info_sizer)

    def add_pref(self):
        self.r_info_panel = RightInfoPanel(self)
        self.info_sizer.Add(self.r_info_panel, 0, wx.EXPAND | wx.RIGHT, 5)


class SearchFrame(wx.Frame):
    def __init__(self):
        """Constructor"""
        super().__init__(parent=None, title="Search Book")
        search_panel = wx.Panel(self)
        search_sizer = wx.BoxSizer(wx.VERTICAL)

        # header = wx.StaticText(search_panel, -1, label='Search Book')
        # font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        # header.SetFont(font)
        ''''''''

        input_panel = InputPanel(search_panel)
        ''''''

        btn_panel = wx.Panel(search_panel)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        add_btn = wx.Button(btn_panel, label='Search Book')
        add_btn.Bind(wx.EVT_BUTTON, search_book)

        btn_sizer.Add(add_btn, 0, wx.ALL | wx.CENTER, 5)

        btn_panel.SetSizer(btn_sizer)
        ''''''

        info_panel = InfoPanel(search_panel)

        ''''''''

        # search_sizer.Add(header, 0, wx.ALIGN_CENTER_HORIZONTAL, border=10)
        search_sizer.Add(input_panel, 0, wx.ALIGN_CENTER_HORIZONTAL, border=10)
        search_sizer.Add(btn_panel, 0, wx.ALIGN_CENTER_HORIZONTAL, border=10)
        search_sizer.Add(info_panel, 0, wx.EXPAND, border=10)

        search_panel.SetSizer(search_sizer)

        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        global s
        s = 0
        print(s)
        self.Destroy()
