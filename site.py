from bottle import route, run, get, post, request, error, SimpleTemplate
from poetry import Poem

# TODO: Templates, links to github repo etc


@get('/') 
def poem():
    """Home page, form to give the poem creator some inspiration."""
    return '''
        <form action="/" method="post">
            Input a word to inspire the poem generator: <input name="source_word" type="text" /><br>
            The default maximum length of lines in the poem is 48 characters. If you'd rather your poem have shorter or longer lines, input the max chars you want your line to have. (Must be > 33): <input name="max_len" type="text" />
            <input value="Create a poem" type="submit" />
        </form>


        <h2><i>Please be patient -- art takes time.</i></h2>

        <br><br>Code that runs this site can be found <a href='https://github.com/jzettac/poetry-generation-site'>here</a> on GitHub.
    '''


@post('/')
def generate_poem():
    """Post and generate poem."""
    source_word = request.forms.get('source_word')
    max_len = request.forms.get('max_len')
    # TODO: "Art takes time..."
    if max_len and int(max_len) > 33:
        p = Poem(source_word, max_line_len=int(max_len))
    else:
        p = Poem(source_word)
    return p.site_rep()


# Error handling

@error(500)
def error500(error):
    return 'There was a problem generating your poem. :(<br> Try again with a different word! <a href="/">Home.</a>'

# Main

if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True)

