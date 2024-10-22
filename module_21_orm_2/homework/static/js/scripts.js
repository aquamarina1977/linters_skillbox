document.getElementById('search-bar').addEventListener('keyup', function() {
    let query = this.value;
    if (query.length > 2) {
        fetch(`/search_books?q=${query}`)
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('No books found');
                }
            })
            .then(data => {
                const resultsContainer = document.getElementById('search-results');
                resultsContainer.innerHTML = ''; // Clear previous results

                if (data.length > 0) {
                    data.forEach(book => {
                        const bookItem = document.createElement('div');
                        bookItem.innerHTML = `<strong>${book.name}</strong> (Released: ${book.release_date})`;
                        resultsContainer.appendChild(bookItem);
                    });
                } else {
                    resultsContainer.innerHTML = '<p>No books found matching the query.</p>';
                }
            })
            .catch(error => {
                console.error(error);
            });
    }
});
