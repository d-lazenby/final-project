#Note to reviewer: When I ran populate.py from the command line, though my code seemed to work, there were periodic "None" generated as output and I'm not sure why -- sorry! These disappeared when I ran individual methods from the command line, e.g. Tome_Rater.most_positive_user(), etc., didn't generate these.

#TomeRater. An application that stores books and their users and reviews.

#Creates User
class User:
    def __init__(self, name, email):
        self.name = name #string
        self.email = email #string
        self.books = {} 

    #gets user email
    def get_email(self):
        return self.email

    #changes user email from email to address
    def change_email(self, address):
        self.email = address
        return "Your new email address is " + address + "."

    #returns user information
    def __repr__(self):
        return "User: " + self.name + ", email: " + self.email + ", books read: " + str(len(self.books))

    #checks to see if two users are the same
    def __eq__(self, other_user):
        if (self.email == other_user.email) and (self.name == other_user.name):
            return True
        return False
    
    #adds book:rating to self.books
    def read_book(self, book, rating=None):
        if rating is None:
            self.books[book] = rating
        elif not ((0 <= rating) and (rating <= 4)):
            print("Invalid rating.")
        else:
            self.books[book] = rating
    
    #Calculates average rating given by user for books read in self.books
    def get_average_rating(self):
        sum = 0
        count = 0
        for rating in self.books.values():
            if (rating == None) or not ((0 <= rating) and (rating <= 4)):
                continue
            sum += rating
            count += 1
        # Ensures that there is no ZeroDivision error and that books that have not been rated are not counted in the average
        if count == 0:
            average = 0
        else:
            average = sum / count
        return average

#####################################################################################

#Creates Book
class Book:
    def __init__(self, title, isbn):
        self.title = title #string
        self.isbn = isbn #int
        self.ratings = []
        
    def __repr__(self):
        return self.title
    
    #get title of book    
    def get_title(self):
        return self.title
        
    #get isbn
    def get_isbn(self):
        return self.isbn
    
    #changes isbn
    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        
    #adds rating between 1 and 4
    def add_rating(self, rating):
        if not ((0 <= rating) and (rating <= 4)):
            print("Invalid Rating")
        else:
            self.ratings.append(rating) 
        
    #checks if two book entries are equal
    def __eq__(self, other_book):
        if (self.title == other_book.title) and (self.isbn == other_book.isbn):
            return True
        return False
    
    def __hash__(self):
        return hash((self.title, self.isbn))
    
    def get_average_rating(self):
        sum = 0 
        count = 0
        for rating in self.ratings:
            if (rating == None):
                continue
            sum += rating
            count += 1
        average = sum / count
        return average   
        
#Creates Fiction subclass
class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    #gets author    
    def get_author(self):
        return self.author

    def __repr__(self):
        return "{} by {}".format(self.title, self.author)
        
#Creates Non-Fiction subclass
class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def __repr__(self):
        vowels = ["a", "e", "i", "o", "u"]
        if self.level[0] in vowels:
            return "{}, an {} manual on {}".format(self.title, self.level, self.subject)
        else:
            return "{}, a {} manual on {}".format(self.title, self.level, self.subject)

    # gets subject
    def get_subject(self):
        return self.subject

    # gets level
    def get_level(self):
        return self.level
    

#####################################################################################

#Creates TomeRater

class TomeRater:
    def __init__(self):
        self.users = {}
        self.books = {}
        self.isbns = {}

    def create_book(self, title, isbn):
        return Book(title, isbn)

    def create_novel(self, title, author, isbn):
        return Fiction(title, author, isbn)

    def create_non_fiction(self, title, subject, level, isbn):
        return Non_Fiction(title, subject, level, isbn)
                
    def add_book_to_user(self, book, email, rating=None):
        book_isbn = book.get_isbn()
        book_title = book.get_title()
        #Ensures that all ISBNs are unique
        if (book_isbn in self.isbns.values()) and (book not in self.books):
            print("The ISBN given for {} already exists, please check.".format(book.get_title()))
        else:
            self.isbns[book] = book_isbn
        if not self.users.get(email):
            print("No user with this email!")
        else:
            self.users.get(email).read_book(book, rating)
            #If book has been rated, add this rating
            if rating is not None:
                book.add_rating(rating)
            #Add to number of times book has been read
            if book not in self.books:
                self.books[book] = 1
            else:
                self.books[book] += 1

    def add_user(self, name, email, user_books=None):
        user = User(name, email)
        #Ensures that all users have valid emails.
        if (email.count("@") == 0):
            print("Invalid email. Please provide an email containg '@'.")
        elif (email.count(".com") + email.count(".org") + email.count(".edu") + email.count(".co.uk")) == 0:
            print("Invalid email.")
        #Ensures that all users have unique emails.
        elif email in self.users.keys():
            print("Email already exists. Please supply another email.")
        else:
            self.users[email] = user
            if user_books:
                for book in user_books:
                    self.add_book_to_user(book, email)

    def print_catalog(self):
        for book in self.books.keys():
            print(book)

    def print_users(self):
        for user in self.users.values():
            print(user)

    def get_most_read_book(self):
        most_times_read = max(self.books.values())
        counter = 0
        for i in self.books.values():
            if i == most_times_read:
                counter += 1
        if counter == 1:
            for key, value in self.books.items():
                if value == most_times_read:
                    print("The most read book is " + str(key) + ", which has been read " + str(most_times_read) + " times.")
        elif counter > 1:
            print("The most read books are ")
            for key, value in self.books.items():
                if value == most_times_read:
                    print(str(key) + ", ")
            print("which have been read " + str(most_times_read) + " times.")
            
    def highest_rated_book(self):
        average_ratings = {book: book.get_average_rating() for book, value in self.books.items()}
        highest_average = max(average_ratings.values())
        counter = 0
        for i in average_ratings.values():
            if i == highest_average:
                counter += 1
        if counter == 1:
            for key, avg in average_ratings.items():
                if avg == highest_average:
                    print("The highest rated book is " + str(key) + ", which has an average rating of " + str(avg) + ".")
        elif counter > 1:
            print("The highest rated books are ")
            for key, avg in average_ratings.items():
                if avg == highest_average:
                    print(str(key) + ", ")
            print("which have an average rating of " + str(highest_average) + ".")
            
    def most_positive_user(self):
        average_ratings = {}
        for email, user in self.users.items():
            #for if a user has been added but they haven't read any books
            if len(user.books) == 0:
                continue
            else:
                average_ratings[email] = user.get_average_rating()
        highest_average = max(average_ratings.values())
        counter = 0
        for i in average_ratings.values():
            if i == highest_average:
                counter += 1
        if counter == 1:
            for key, avg in average_ratings.items():
                if avg == highest_average:
                    print("The most positive user is " + str(key) + ", who gives an average rating of " + str(avg) + ".")
        elif counter > 1:
            print("The most positive users are ")
            for key, avg in average_ratings.items():
                if avg == highest_average:
                    print(str(key) + ", ")
            print("who give an average rating of " + str(highest_average) + ".")

