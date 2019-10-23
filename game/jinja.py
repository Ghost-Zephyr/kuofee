from jinja2 import Environment, FileSystemLoader
from .jwt import get

j2_env = Environment(loader=FileSystemLoader('jinja2templates'), trim_blocks=True)

def render_template(tf):
    template = j2_env.get_template(tf)
    rendered_template = template.render(player=get())
    return rendered_template

def render_game_template(tf, db):
    template = j2_env.get_template(tf)
    rendered_template = template.render(player=get())
    return rendered_template

