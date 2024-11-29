# My_Library 
#### Video Demo: <url here>
#### Description: 

This is intended to be a personal use library for bookworms.  Maybe you have dozens or even hundreds of books.  How do you keep track of them?

With this web app you will have easy access to a database of books you own, books you want to own, and reviews to see if you want to own a book.

#### Design Choices:

I chose a flask app because we not only used it in class but because python is very intuitive for me.
I chose sqalchemy for the orm models and because I have beta tested and assisted with codecommits in a webapp with sqlalchemy.
Although not overly familiar, I thought a good starting point so as to not be overwhelmed.
Likewise for Heroku postgresql. I wanted a cloudbased server that I myself did not have to maintain. And I want users to be able to use the app whenever they choose. 
The app is heavy on the user's ability to add to and update their information, so it seemed a wise choice.
In addition, I would like to be able to make the app publicly available and Heroku offers app hosting.
For me, a flask-sqlalchemy-postgresql structure seemed most logical.

#### Project Structure:

**Static:** this is the standard folder which contains my styles.css as well as images to be used in the webpages.


**Gitignore:**  This folder is to place files that are not to be passed to other potential developers.  It includes the following standard files and folders:

- .env:  I have placed the Heroku database credentials in this folder so that I can then put it in gitignore.  This way it will be obscured for security.  As well as allowing for ease in changing credentials if needed.

- .venv:**  To place the local virtual environment.

- pycache 
    
- flask_session


**Requirements.txt:**  This is the list of libraries and packages that need to be installed in local .venv to work on this project.


**database.py:** This file sets up the database configuration, initiates the creation of the app and tables.


**helpers.py:**  Standard type file that contains frequently used functions.  For this project - as follows:

- login_required: ensures users are logged in to use certain features.

- apology: launches an html with image and error code in case of errors.

- get_current_user: retrieves user_id to use in queries.

- get_questions_1() and get_questions_2():  provides security questions list to be used in the register and password_reset routes/templates. 

- select_values(): provides list of options for search menu in the reviews route/template.


**models.py:**  This file allows you to create the following classes:

- User: table model for personal information of the user.  These are the username, hashed password, security questions that are selected, hashed security answers as well as fields for email and about_me that will be used in future improvements.

- Book: table model for books that are owned by a user.  The data contained therein are the book title, author, year published, genre, series name (if applicable), ratings, review, and boolean value for whether a book is to be private.

- Wishlist:  table model for books that a user would like to own. The data contained therein are the book title, author, year published, and series name (if applicable).

- Review: table model designed to allow for a user to see all ratings and reviews from all users for a particular book (that are not set to private). 

- BookGenre: this is and enum designed to limit the selection of genres that can be chosed to facilitate ease in searching for ratings and reviews.


**app.py:**  This is the flask/python code that contains all the routes for this program.  There is standard setup that was used as a guide from the original finance project. This includes the app.config, init_db(app), app= Flask(__name__). 

The following is a description of the routes:

- after_request: Ensures the responses aren't cached (copied from finance as standard)

- register: This allows a user to select a username (unique identifier) as well as a hashed password and security questions and hashed answers.  It will reject duplicate usernames.  If successful, the user will be added to the database.

- login: From finance and refactored to used sqlalchemy. Verifies username and password.

- passwordreset: Enables a user to verify username and security answers before being redirected to enter a new password.  There are multiple post requests.  Step 1 is to verify username exists.  If it does, then the username is stored in session and passed to step 2.  This is to answer the security questions that are populated based on username.  These answers are checked with check_hash.  If successful, then new_password is launched.

- new_password: A user may select a new password. When they do, their new password is updated into the database and they are redirected to login.

- index: The page a user will first come upon.  It contains basic info as to what the app does and how it can be used.

- library: Once a user is logged in a homepage is displayed.  This queries the book table and passes the values to a table of books owned by the user.  It includes the ability to add new books, update current books, and delete books.

- wishlist:  This queries the wishlist table and passes the values to a table of books the user wishes to own.  It includes the ability to add new books, move books from the wishlist to the library, and delete books.

- reviews:  This enables a user to search for books based on select_values from helpers.py.  It will then query the review table joined with the book table to pass the results to a table that will show all reviews from all users for a particular book or author or genre so long as that book has not been set to private.

- add_book: This takes an argument of book_type.  Depending on whether a user is adding a book from library or wishlist - once the user inputs the book info it will be saved to the correct table.  Title, author, and genre are required.  Other fields are populated by default values if the user does not input them.  Books in library may also be set to private to prevent them from being queried by other users in reviews.

- delete_book:  This also takes an argument of book_type.  It is connected in the row of the table via the book_id so when it is clicked it will deleted the associated book from the correct table.  Withint the template is a launched confirmation popup to avoid unintended deletion.

- update_book: This is available in library so a user may update book details and add any you may be missing.  Updating the book table.

- move_to_library:  This is available in wishlist so when a user obtains a book they may easily add it to the library without the redundancy of re-entry.  It queries the wishlist, takes the pertinent info and updates the book table, and then deletes from wishlist table.

- app.errorhandler:  Throughout the routes I have implemented this route so errors can be logged to aid in debugging.  This in conjuction with try/except and db.session.rollback() will help handle errors while assisting in debugging and maintains the integrity of the database when errors do occur.


**Templates:**  Standard html/jinja2 templates designed to workd with the routes.

- layout: Sets the basics of the pages to be extended.  It does source bootstrap.  It contains a navbar for which only Register and Login appear when a user is not logged in.  Once a user is logged in, additional options of My Library, Wishlist, Reviews, and Logout appear.

- register:  Form with user information fields including username, password, confirmation, security questions dropdowns (x2), and security answers (x2).

- login:  Standard username and password as well as an option for Forget Password which launches passwordreset page.

- passwordreset: (Only launched via "Forgot Password" button on login page.)  This page contains a form with username and a submit button.  Once the username is entered and verified, the page reloads to show two security questions and fields for their associated answers.  Once those are successfully submitted, new_password is launched.

- new_password:  This contains a simple form that asks for a new password and confirmation with a "Update Password" button.

- index:  A simple text page that contains information on the web app.

- library:  Once a user logs in, this page displays a table of the books and user currently owns and the details of the books.  It also contains an "Add Book" button as well as "Update Book" and "Delete" buttons - all of which launch their associated templates, if they exist. "Delete" launches a confirmation popup so avoid unintended deletions.

- wishlist:  This page contains a table of books a user would like to own and the details of those books. Like the Library page, it also has an "Add Book" and a "Delete" button with the same functions.  It also has a "Move to Library" button that a user can click to move the selected book from Wishlist to Library.

- reviews:  This allows a user to query for ratings and review of books based on selected criteria: Title, Author, Genre, Series.  It will then populate a table of all reviews for all users meeting that criteria.  It will filter out any books marked "private".

- add_book:  This is launched either from library or wishlist.  It will display a form for users to submit that contain details on a particular book.  When submitted, it will add the book to whichever page launched the add_book action.

- update_book:  This is launched from library.  It pulls up the current details of a book and then enables the user to update them as necessary.

- apology:  This is the apology image and error code if an error is reached.


**Planned Future Improvements:**

- Profile Page: This will include an about me page as well as the ability to reset password.

- Borrow:  Added functionality to request to borrow books from users that you are familiar with in your local area.