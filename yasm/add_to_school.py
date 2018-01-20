

@app.route("/")
def hello():
    return "Hello World!"


@app.route('/post/<post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'bad post id "%s"' % post_id


@app.route('/post/<int:post_id>')
def show_post_2(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/projects/')
def projects():
    return 'The project page'


@app.route('/about')
def about():
    return 'The about page'
