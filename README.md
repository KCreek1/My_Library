# My_Library 
(under development)
This is intended to be a personal use library for bookworms.  Maybe you have dozens or even hundreds of books.  How do you keep track of them?
What if you could have a searchable library for your books?  Enter the book details including your rating and a summary.
Easy access for when you want to purchase more or are looking for something to read. 
What if you and your friends want to peruse each others library?  Now you can. Maybe even request to borrow a book.

Chose flask-sqalchemy for the orm models and because I have read/assisted with code in an app with sqlalchemy. Likewise for heroku postgresql. I wanted a cloudbased server that I myself did not have to maintain. And given that I do not have a pc but a laptop and I want users to be able to use the app whenever they chose and theat the app is heavy on users updating their information a flask-sqlalchemy-postgresql route seemed most logical.

I have used enivronmental variables for security and included them in gitignore.

users will be able to maintain a database of their personal libraries.  They will be able to insert, query, and delete books as they come and go.
Users will be able to maintain a wishlist of books to acquire.
users will be able to view others reviews of said books.