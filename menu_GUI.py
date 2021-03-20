# from book_reading import *
import wx.adv


def menu_maker(menu, label, kind, func):
    item = wx.MenuItem(menu, -1, text=label, kind=kind)
    menu.Bind(wx.EVT_MENU, func, item, id=item.GetId())
    menu.Append(item)
    return item


class MenuBar(wx.MenuBar):
    def __init__(self):
        super().__init__()
        file_menu = wx.Menu()
        menu_maker(file_menu, "Preferences...\tCtrl-,", wx.ITEM_NORMAL, self.preferences)
        self.Append(file_menu, "&File")

    def preferences(self, event):
        pass

