from .jinja import j2_env
from .jwt import get

def render_template(tf, title, url):
    template = j2_env.get_template(tf)
    player = get()
    rendered_template = template.render(title=title, url=url, player=player)
    return rendered_template

def index(url):
    return render_template('index.jinja2', "Home", url)

def login(url):
    return render_template('login.jinja2', "Login", url)
