# My_Library 
#### Video Demo: <url here>
#### Description: TODO

This is intended to be a personal use library for bookworms.  Maybe you have dozens or even hundreds of books.  How do you keep track of them?
What if you could have a searchable library for your books?  Enter the book details including your rating and a summary.
Easy access for when you want to purchase more books or are looking for something to read. 
What if you and your friends want to peruse each other's library?  Now you can. You will also be able to see the ratings and reviews of all users for a particular book.

I chose flask-sqalchemy for the orm models and because I have read/assisted with code in a webapp with sqlalchemy.  Although not overly familiar, I thought a good starting point.   Likewise for heroku postgresql. I wanted a cloudbased server that I myself did not have to maintain. And given that I do not have a pc but a laptop and I want users to be able to use the app whenever they choose and the app is heavy on users updating their information, a flask-sqlalchemy-postgresql structure seemed most logical.

I have used enivronmental variables for security and included them in gitignore.

I also have chosen to use a class structure for the database tables. This will enable me to use methods versus straight sql syntax.  This should create a code that is easier to read and avoids clutter in the routes.

Users will be able to maintain a database of their personal libraries.  They will be able to insert, query, and delete books as they come and go.
Users will be able to maintain a wishlist of books to acquire.
Users will be able to view others reviews of said books.
