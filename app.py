from flask import Flask, jsonify, render_template, request
import sqlite3

app = Flask(__name__)

# Define the path to your SQLite database file
DATABASE = 'db/books.db'

@app.route('/api/books', methods=['GET'])
def get_all_books():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        #  retrieving book titles and publication years,  and also fetch the author's name for each book
        cursor.execute("SELECT Books.book_id, Books.title, Books.publication_year, Authors.name FROM Books INNER JOIN book_author ON Books.book_id = book_author.book_id INNER JOIN Authors ON book_author.author_id = Authors.author_id") 
        books = cursor.fetchall()
        conn.close()

        # Convert the list of tuples into a list of dictionaries
        book_list = []
        for book in books:
            book_dict = {
                'book_id': book[0],
                'title': book[1],
                'publication_year': book[2],
                'author': book[3] #Include authors name in the book dictionary
                
            }
            book_list.append(book_dict)

        return jsonify({'books': book_list})
    except Exception as e:
        return jsonify({'error': str(e)})


# API to get all authors
@app.route('/api/authors', methods=['GET'])
def get_all_authors():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Authors")
        authors = cursor.fetchall()
        conn.close()
        return jsonify(authors)
    except Exception as e:
        return jsonify({'error': str(e)})

# API to get all reviews
@app.route('/api/reviews', methods=['GET'])
def get_all_reviews():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Reviews")
        reviews = cursor.fetchall()
        conn.close()
        return jsonify(reviews)
    except Exception as e:
        return jsonify({'error': str(e)})

# API to add a book to the database
@app.route('/api/add_book', methods=['POST'])
def add_book():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Get book details from the request
        data = request.get_json()
        title = data.get('title')
        publication_year = data.get('publication_year')
        authors = data.get('authors') #Retrieve authors's names as a list changed

        # Insert the book into the database along with the author's name 
        cursor.execute("INSERT INTO Books (title, publication_year) VALUES (?, ?)", (title, publication_year))
        book_id = cursor.lastrowid #Getting the ID of the newly inserted book

        # Insert authors into Authors table if they don't exist and then link them to the book changed
        for author in authors:
            cursor.execute("INSERT OR IGNORE INTO Authors (name) VALUES (?)", (author,))
            cursor.execute("SELECT author_id FROM Authors WHERE name=?", (author,))
            author_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO book_author (book_id, author_id) VALUES (?, ?)", (book_id, author_id))

        conn.commit()
        conn.close()

         # Print a message to the server logs
        print("Book added successfully")

        return jsonify({'message': 'Book added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

# Route to render the index.html page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
