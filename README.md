# My Library
**My Library** is a simple web app for managing personal book collections. Track the books you own, maintain a wishlist, and explore reviews from other readers. Built with Python and Flask, it’s lightweight, easy to deploy, and perfect for book enthusiasts who want a digital shelf.

## Features
- **Library Management**: Add, edit, and organize your owned books.
- **Wishlist**: Keep track of books you’d like to read or purchase.
- **User Reviews**: Read and contribute reviews to help others discover great books.
- **Cloud-Hosted Database**: Uses Heroku PostgreSQL for easy deployment and scaling.
- **Local Setup Option**: Easily adaptable to SQLite for local testing or lightweight personal use.
  
## Tech Stack
- **Flask**: Minimalist Python web framework for quick and intuitive development.
- **SQLAlchemy**: ORM for managing relational databases in a Pythonic way.
- **PostgreSQL (Heroku)**:  Cloud-hosted, scalable database service.
- **HTML/CSS**: Simple, responsive front-end styling.
- App can be refactored to run with SQLite for local or smaller-scale use.

## Project Structure
```
my-library/
├── static/              # CSS and static assets
├── templates/           # HTML templates
├── .env                 # Environment variables (not tracked in version control)
├── .gitignore           # Git exclusions (e.g., .env, .venv)
├── app.py               # Main Flask application
├── database.py          # DB config and model definitions
├── requirements.txt     # Project dependencies
└── README.md            # This file
```


## Setup Instructions

### Prerequisites:
-Python 3.x

-(Optional) Heroku account (https://www.heroku.com/) (for deployment)


## Local Development

### 1. Clone the repository:
```bash
git clone https://github.com/yourusername/my-library.git
cd my-library
```

### 2. Set up a virtual environment:
```bash
python3 -m venv .venv
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```


### 4. Set environment variables
Create a `.env` file in the project root with your configuration. Example (for Heroku):
```dotenv
DATABASE_URL=your-heroku-postgres-url
SECRET_KEY=your-secret-key
```
Note: Keep your `.env` file private and excluded via `.gitignore`.


### 5. Run the app locally:
```
python app.py
```
Notice comments in `database.py`

Open http://localhost:5000 in your browser to view the app.


## Deployment
This app is currently deployed using Heroku’s GitHub Integration. You can:

- Push changes to the main branch on GitHub
- Visit your Heroku dashboard → Deploy tab
- Click Deploy Branch to publish updates

If you prefer to use the Heroku CLI, you can also follow manual deployment instructions (not required in this setup).



## Testing
You can view or contribute to test tracking using the link to the test sheet:
https://docs.google.com/spreadsheets/d/1oI64fKkLgGjBmIqVZ3b9Xh9YvQ1HvZDY44hCYNW75Iw/edit
