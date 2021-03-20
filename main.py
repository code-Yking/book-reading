import json
import random

JSON_LOC = 'books.json'


def open_json():
    with open(JSON_LOC) as f:
        data = json.load(f)
        f.close()
    return data


class main():
    def __init__(self):
        self.book_dict = {}
        self.book_nos = []
        self.latest = 0

        self.recall(open_json())
        self.stats(open_json())

    def recall(self, book_dict):
        for year, year_list in book_dict.items():
            try:
                for month, month_list in year_list.items():
                    for book in month_list:
                        self.book_nos.append(book)
            except:
                continue

        try:
            self.latest = book_dict['latest']
        except:
            self.latest = 0

    def stats(self, book_dict):
        import datetime
        now = datetime.datetime.now()

        read_this_month = len(book_dict[str(now.year)][str(now.month)])

        print('---------------------------------')
        print('|         BOOK READING          |')
        print('|    Books read this month: {}   |'.format(read_this_month))
        print('|    Books read this year: {}    |'.format(' '))
        print('|                               |')
        print('---------------------------------')

    def suggest(self):
        book_sugg = random.randint(1, self.latest)

        while book_sugg in self.book_nos:
            book_sugg = random.randint(1, self.latest)
        return (book_sugg)

    def post_select(self, book):
        print(f'{book} will be added to the memory.')


if __name__ == "__main__":
    main_books = main()

    threshold = int(input("Enter Latest Book No. (Return empty to use {}): ".format(
        main_books.latest)) or main_books.latest)
    suggestion = main_books.suggest()
    print(f'Suggested Reading: {suggestion}')

    choice_decision = input('Enter Y if chosen, lest click Enter')
    count_choice = 1
    while(choice_decision != 'Y'):
        count_choice = count_choice + 1
        suggestion = main_books.suggest()

        print(f'Option no. {count_choice}: {suggestion}')
        choice_decision = input()

    main_books.post_select(suggestion)
