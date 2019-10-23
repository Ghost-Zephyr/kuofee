from .jinja import *
from .jwt import get

# --- Home Paige route functions ---
def index():
    return render_template('index.jinja2')

def login():
    return render_template('login.jinja2')

def register():
    return render_template('register.jinja2')

# --- Game route functions ---
def mainMenu(db):
    return render_game_template('game/index.jinja2', db)

def qpAi(db, mode):
    template = j2_env.get_template('game/screens/quickPlay.jinja2')
    rendered_template = template.render(mode=mode)
    return rendered_template


def walterPenny():
    template = j2_env.get_template('game/screens/WalterPenny.jinja2')
    rendered_template = template.render()
    return rendered_template

