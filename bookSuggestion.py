import json
import random
import tkinter as tk

JSON_LOC = 'books.json'


def open_json():
    with open(JSON_LOC) as f:
        data = json.load(f)
        f.close()
    return data


class bookSuggestion():
    def __init__(self, book_dict):
        self.book_dict = book_dict
        self.book_nos = []

        if self.book_dict['latest']:
            print('yes')
        else:
            print('no')

    def recall(self):

        for year, year_list in self.book_dict.items():
            try:
                for month, month_list in year_list.items():
                    for book in month_list:
                        self.book_nos.append(book)
            except:
                continue
        book_sugg = random.randint(1, self.book_dict['latest'])

        while book_sugg in self.book_nos:
            book_sugg = random.randint(1, self.book_dict['latest'])
        print(book_sugg)


class MainFrame():
    def __init__(self, master):
        # super().__init__()
        self.master = master
        self.label_new_book = tk.Label(self.master, text="Insert new book: ")
        self.label_new_book.grid(column=1, row=1)

        self.input_new_book = tk.Entry(self.master)
        self.input_new_book.grid(column=2, row=1)

        self.button_new_book = tk.Button(
            self.master, text="Add new book", command=self.print_test)
        self.button_new_book.grid(column=3, row=1)

        self.label_search_book = tk.Label(self.master, text="Search book: ")
        self.label_search_book.grid(column=1, row=4)

    def print_test(self):
        print('hi')


if __name__ == "__main__":
    root = tk.Tk()
    frame = MainFrame(root)
    root.mainloop()

# threshold = int(input("Enter the inputs : ") or "42")
# latest_books = bookSuggestion(open_json())
# latest_books.recall()
