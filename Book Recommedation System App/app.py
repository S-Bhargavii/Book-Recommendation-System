import numpy as np
from flask import Flask, render_template, request
# import pickle
import pandas as pd
popular_df = pd.read_pickle('popular.pkl')
# now the dataframe is saved to the popular_df variable
app = Flask(__name__)
books = pd.read_pickle('books.pkl')
similarity_score = pd.read_pickle('similarity_score.pkl')
pivot_table = pd.read_pickle('pivot_table.pkl')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/popular')
def popular():
    return render_template('popular.html',
                           name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           img=list(popular_df['Image-URL-L'].values),
                           avg=list(popular_df['Avg-Rating'].values),
                           num=list(popular_df['num_ratings'].values))


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend-books', methods=['post'])
def recommend():
    book_name = request.form.get('user_input')
    distances = similarity_score[np.where(
        pivot_table.index == book_name)[0][0]]
    similar_items = sorted(list(enumerate(distances)),
                           key=lambda x: x[1], reverse=True)[1:6]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pivot_table.index[i[0]]]
        item.extend(temp_df.drop_duplicates('Book-Title')['Book-Title'])
        item.extend(temp_df.drop_duplicates('Book-Title')['Book-Author'])
        item.extend(temp_df.drop_duplicates('Book-Title')['Image-URL-L'])
        data.append(item)
    print("bhargavi")
    return render_template('recommended-books.html', book_name=book_name, data=data)


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
