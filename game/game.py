from .utils import j2_env

def index(url):
    template = j2_env.get_template('index.jinja2')
    rendered_template = template.render(title="Home", url=url)
    return rendered_template
