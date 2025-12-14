from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'secret_key'

books = []

@app.route('/')
def index():
    return render_template('books.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book = {
            'id': len(books) + 1,
            'title': request.form['title'],
            'author': request.form['author'],
            'year': request.form['year']
        }
        books.append(book)
        flash('Libro agregado correctamente', 'success')
        return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = next((b for b in books if b['id'] == book_id), None)
    if not book:
        flash('Libro no encontrado', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        book['title'] = request.form['title']
        book['author'] = request.form['author']
        book['year'] = request.form['year']
        flash('Libro actualizado correctamente', 'success')
        return redirect(url_for('index'))

    return render_template('edit_book.html', book=book)

@app.route('/delete/<int:book_id>', methods=['GET', 'POST'])
def delete_book(book_id):
    book = next((b for b in books if b['id'] == book_id), None)
    if not book:
        flash('Libro no encontrado', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        books.remove(book)
        flash('Libro eliminado correctamente', 'success')
        return redirect(url_for('index'))

    return render_template('delete_book.html', book=book)

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        query = request.form['query'].lower()
        results = [b for b in books if query in b['title'].lower()]
    return render_template('search.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
