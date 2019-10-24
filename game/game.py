from .jinja import get, j2_env, render_template, render_game_template

# --- Home Paige route functions ---
def index():
    return render_template('index.jinja2')

def login():
    return render_template('login.jinja2')

def register():
    return render_template('register.jinja2')

def about():
    return render_template('game/about.jinja2')

# --- Game route functions ---
def player():
    return render_template('game/player.jinja2')

def mainMenu(db):
    return render_game_template('game/index.jinja2', db)

def qpAi(db, mode):
    template = j2_env.get_template('game/play/quickPlay.jinja2')
    rendered_template = template.render(mode=mode, player=get())
    return rendered_template


def walterPenny():
    template = j2_env.get_template('game/screens/WalterPenny.jinja2')
    rendered_template = template.render()
    return rendered_template

