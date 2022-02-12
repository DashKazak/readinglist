""" Program to create and manage a list of books that the user wishes to read, and books that the user has read. """


from bookstore import Book, BookStore
from menu import Menu
from readinglist.bookstore import BookError

import ui

store = BookStore()

def main():

    menu = create_menu()
    while True:
        choice = ui.display_menu_get_choice(menu)
        action = menu.get_action(choice)
        action() 
        if choice == 'Q':
            break


def create_menu():
    menu = Menu()
    menu.add_option('1', 'Add Book', add_book)
    menu.add_option('2', 'Search For Book', search_book)
    menu.add_option('3', 'Show Unread Books', show_unread_books)
    menu.add_option('4', 'Show Read Books', show_read_books)
    menu.add_option('5', 'Show All Books', show_all_books)
    menu.add_option('6', 'Show Number of Books in Database', book_count) # new menu option to show number of books
    menu.add_option('7', 'Change Book Read Status', change_read)
    menu.add_option('8', 'Delete Book', delete_book)
    menu.add_option('Q', 'Quit', quit_program)
    return menu


def add_book():
    try: 
        new_book = ui.get_book_info()
        new_book.save() #the program will try to save the file
        # but, in bookstore.py line 107 we indicated that the book list can't have duplicates. If this error is encountered, the program will jump to the except statement below instead of printing long developer log error message. 
        
    except BookError as e: 
        ui.message(e)
        

def show_read_books():
    read_books = store.get_books_by_read_value(True)
    ui.show_books(read_books)


def show_unread_books():
    unread_books = store.get_books_by_read_value(False)
    ui.show_books(unread_books)


def show_all_books():
    books = store.get_all_books()
    ui.show_books(books)

def book_count(): # new method to count number of books in database
    count = store.book_count() # stores number of books into a count variable
    ui.message(count) # prints the count variable to the user


def search_book():
    search_term = ui.ask_question('Enter search term, will match partial authors or titles.')
    matches = store.book_search(search_term)
    ui.show_books(matches)


def change_read():
    book_id = ui.get_book_id()
    book = store.get_book_by_id(book_id)  
    new_read = ui.get_read_value()     
    book.read = new_read 
    book.save()
    if book.read: 
        ui.message(f'You changed {book.title} by {book.author} to status \'read\'')
    else: 
        ui.message(f'You changed {book.title} by {book.author}  to status \'not read\'')

    if book is not None: # If book value is not None, then the changes are saved
        new_read = ui.get_read_value()     
        book.read = new_read 
        book.save()
    else: # If book value is None, then this message is displayed, and the program jumps back to the main menu
        ui.message('That book is not in the database. Please select an option:')
    
def delete_book():
    try:
        search_id = ui.get_book_id()
        match_id = store.get_book_by_id(search_id)
        match_id.delete()  
    except:
        ui.message('Error: Book Not Found')

def quit_program():
    ui.message('Thanks and bye!')


if __name__ == '__main__':
    main()