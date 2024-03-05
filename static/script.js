// Array to store book data
const books = [];

// Function to add a book to the list and send it to the server
function addBook() {
  const bookTitle = document.getElementById("bookTitle").value;
  const publicationYear = document.getElementById("publicationYear").value;
  const authorName = document.getElementById("authorNames").value; // This will retrieve Author's name
  const authors = authorName.split(",").map((name) => name.trim()); // Split author names by comma and trim whitespace changed

  // Create a JSON object with book data
  const bookData = {
    title: bookTitle,
    publication_year: publicationYear,
    authors: authors, // Include multiple authors in the data sent to the server Changed
  };

  // Send the book data to the server via POST request
  fetch("/api/add_book", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(bookData),
  })
    .then((response) => response.json())
    .then((data) => {
      // Display a success message or handle errors if needed
      console.log(data.message);

      // Add the new book data to the books array
      books.push(bookData);
      console.log(books);

      // Refresh the book list
      displayBooks();
    })
    .catch((error) => {
      console.error("Error adding book:", error);
    });
}

// Function to display books in the list
function displayBooks() {
  const bookList = document.getElementById("bookList");
  bookList.innerHTML = ""; // Clear existing book list

  books.forEach((book) => {
    const bookElement = document.createElement("div");
    bookElement.innerHTML = `
            <h2>Added Successfully :${book.title}</h2>
            <p>Authors: ${book.authors}</p>
            <p>Publication Year: ${book.publication_year}</p>
        `;
    bookList.appendChild(bookElement);
  });
}

// Function to fetch and display all books from the server
function showAllBooks() {
  fetch("/api/books")
    .then((response) => response.json())
    .then((data) => {
      const bookList = document.getElementById("allbooks");
      bookList.innerHTML = ""; // Clear existing book list

      data.books.forEach((book) => {
        // Access the 'books' key in the JSON response
        const bookElement = document.createElement("div");
        bookElement.innerHTML = `
                    <h2>${book.title}</h2> 
                    <!-- Display authors separated by comma -->
                    <p>Author: ${book.author.join(", ")}</p>  
                    <p>Publication Year: ${book.publication_year}</p>
                `;
        bookList.appendChild(bookElement);
      });
    })
    .catch((error) => {
      console.error("Error fetching all books:", error);
    });
}
