from bottle import route, run, get, post, request, error, template, static_file
from poetry import Poem

# Static files CSS
@route('/static/css/<filename:re:.*\.css>')
def send_css(filename):
    return static_file(filename, root='static/css')

# Routes

@get('/') 
def poem():
    """Home page, form to give the poem creator some inspiration."""
    return template('templates/home.html')


@post('/') # https://buxty.com/b/2013/12/jinja2-templates-and-bottle/
def generate_poem():
    """Post and generate poem."""
    source_word = request.forms.get('source_word')
    p = Poem(source_word)
    p.generate_poem()
    info = {'poem_text':p.full_poem_list, 'poem_title':p.title}
    return template('templates/poem.html', info)


# Error handling

@error(500)
def error500(error):
    return template('templates/500.html')


# Main

if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True)

