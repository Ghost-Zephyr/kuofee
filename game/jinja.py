from jinja2 import Environment, FileSystemLoader

j2_env = Environment(loader=FileSystemLoader('jinja2templates'), trim_blocks=True)
