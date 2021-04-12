from bottle import route, run, get, post, request, error
from bottle import jinja2_view as view, jinja2_template as template
from poetry import Poem

# TODO: Templates, links to github repo etc


@get('/') 
@jinja2_view('home.html', template_lookup=['templates']) # TODO: create templates/home.html
def poem():
    """Home page, form to give the poem creator some inspiration."""
    return '''
        <form action="/" method="post">
            Input a word to inspire the poem generator: <input name="source_word" type="text" /><br>
            <input value="Create a poem" type="submit" />
        </form>


        <h2><i>Please be patient -- art takes time.</i></h2>

        <br><br>Code that runs this site can be found <a href='https://github.com/jzettac/poetry-generation-site'>here</a> on GitHub.
    '''


@post('/')
@jinja2_view('poem.html', template_lookup=['templates']) # TODO: create templates/poem.html
# https://buxty.com/b/2013/12/jinja2-templates-and-bottle/
def generate_poem():
    """Post and generate poem."""
    source_word = request.forms.get('source_word')
    # TODO: "Art takes time..."
    p = Poem(source_word)
    return p.site_rep()


# Error handling

@error(500)
@jinja2_view('500.html', template_lookup=['templates']) # TODO: create templates/500.html
def error500(error):
    return 'There was a problem generating your poem. :(<br> Try again with a different word! <a href="/">Home.</a>'

# Main

if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True)

