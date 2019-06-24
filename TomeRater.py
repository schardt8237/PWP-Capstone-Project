class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        
        print("User email address has been updated.")

    def __repr__(self):
        return "Name: {0}, email: {1}, total books read: {2}".format(self.name,self.email,str(len(self.books)))

    def __eq__(self, other_user):
        return (self.name == other_user.name) and (self.email == other_user.email)
        
    def read_book(self, book, rating=None):
        self.books[book] = rating
        
    def get_average_rating(self):
        if len(self.books) > 0:
            sum_of_ratings = 0
            total_ratings = 0
            
            for rating in self.books.values():
                # handle books with no rating
                if rating != None:
                    sum_of_ratings += rating
                    total_ratings += 1
            
            return sum_of_ratings / total_ratings
        else:
            return 0

class Book(object):
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []
        
    def get_title(self):
        return self.title
        
    def get_isbn(self):
        return self.isbn
        
    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        
        print("Book's ISBN has been updated.")
        
    def add_rating(self, rating):
        if rating != None and rating >= 0 < 5:
            self.ratings.append(rating)
        else:
            print("Invalid Rating")
            
    def __eq__(self, other_book):
        return self.title == other_book.title and self.isbn == other_book.isbn
    
    def get_average_rating(self):
        sum_of_ratings = 0
        total_ratings = len(self.ratings)
        
        for rating in self.ratings:
            sum_of_ratings += rating
            
        return sum_of_ratings / total_ratings
        
    def __hash__(self):
        return hash((self.title, self.isbn))
        
    def __repr__(self):
        return "{title} (ISBN: {isbn})".format(title=self.title,isbn=str(self.isbn))
        
class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author
        
    def get_author(self):
        return self.author
        
    def __repr__(self):
        return "{title} by {author}".format(title=self.title, author=self.author)
        
class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level
        
    def get_subject(self):
        return self.subject
        
    def get_level(self):
        return self.level
        
    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title=self.title, level=self.level, subject=self.subject)

class TomeRater(object):
    def __init__(self):
        self.users = {}
        self.books = {}
        
    def create_book(self, title, isbn):
        return Book(title, isbn)
        
    def create_novel(self, title, author, isbn):
        return Fiction(title, author, isbn)
        
    def create_non_fiction(self, title, subject, level, isbn):
        return Non_Fiction(title, subject, level, isbn)
        
    def add_book_to_user(self, book, email, rating=None):        
        if email in self.users:            
            if book in self.books:
                self.books[book] += 1
                self.users[email].read_book(book, rating)
                book.add_rating(rating)
            elif self.is_isbn_unique(book.get_isbn()):
                self.books[book] = 0
                self.users[email].read_book(book, rating)
                book.add_rating(rating)
            else:
                print("ISBN in use.")
        else:
            print("No user with email {email}!".format(email=email))
            
    def add_user(self, name, email, user_books=None):
        if email in self.users.keys():
            print("This email address is already in use.")
        elif "@" not in email:
            print("Address must contain an '@' character")
        elif ".com" not in email and ".edu" not in email and ".org" not in email:
            print("Address must contain either '.com', '.edu', or '.org'")
        else:
            self.users[email] = User(name, email)
        
            if user_books != None:
                for book in user_books:
                    self.add_book_to_user(book, email)
                
    def print_catalog(self):
        for key in self.books.keys():
            print(key)
        
    def print_users(self):
        for value in self.users.values():
            print(value)
    
    def most_read_book(self):
        most_read_value = -1;
        most_read_key = None
        
        for book, times_read in self.books.items():
            if times_read > most_read_value:
                most_read_value = times_read
                most_read_key = book
                
        return most_read_key
    
    def highest_rated_book(self):
        highest_rated = list(self.books.keys())[0];
                
        for book in self.books.keys():
            if book.get_average_rating() > highest_rated.get_average_rating():
                highest_rated = book
                
        return highest_rated
        
    def most_positive_user(self):
        most_positive = list(self.users.values())[0];
                
        for user in self.users.values():
            if user.get_average_rating() > most_positive.get_average_rating():
                most_positive = user
                
        return most_positive
        
    # Checks for existence of an ISBN in books dictionary
    def is_isbn_unique(self, isbn):
        for book in self.books.keys():
            if isbn == book.get_isbn():
                return False
                
        return True
        
    def __repr__(self):
        user_message = "List of users:"
        books_message = "List of books:"
        
        users = ""
        
        for value in self.users.values():
            users += str(value) + "\n"
            
        catalog = ""
        
        for key in self.books.keys():
            catalog += str(key) + "\n"
            
        return "{0}\n{1}\n{2}\n{3}".format(user_message,users,books_message,catalog)
        
    def __eq__(self, other_tome):
        return self.users == other_tome.users and self.books == other_tome.books