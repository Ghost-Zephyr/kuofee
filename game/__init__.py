import jinja2
import game
import api
import jwt

def err404(url, error):
    template = j2_env.get_template('error.jinja2')
    rendered_template = template.render(title="Error 404" url=url, err=error)
    return rendered_template
