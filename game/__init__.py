from .jinja import *
from . import admin
from . import game
from . import api
from . import jwt

def err404(error):
    template = j2_env.get_template('error.jinja2')
    rendered_template = template.render(title="Error 404", err=error, player=jwt.get())
    return rendered_template
