from bottle import route, run, get, post, request
from poetry import Poem

# TODO: Templates, links to github repo etc


@get('/') 
def poem():
    return '''
        <form action="/" method="post">
            Input a word to inspire the poem generator: <input name="source_word" type="text" />
            The default maximum length of lines in the poem is 48 characters. If you'd rather your poem have shorter or longer lines, input the max chars you want your line to have. (Must be > 33): <input name="max_len" type="text" />
            <input value="Create a poem" type="submit" />
        </form>


        <h2><i>Please be patient -- art takes time.</i></h2>
    '''

@post('/')
def generate_poem():
    source_word = request.forms.get('source_word')
    max_len = request.forms.get('max_len')
    # TODO: "Art takes time..."
    if max_len and int(max_len) > 33:
        p = Poem(source_word, max_line_len=int(max_len))
    else:
        p = Poem(source_word)
    return p.site_rep()

run(host='localhost', port=8080, debug=True)