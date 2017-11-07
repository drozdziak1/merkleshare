import os
import jinja2

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

TEMPLATE_PATH = os.path.join(DIR_PATH, 'output', 'index.html')


def render(data, verbose=False):
    """
    Fill the HTML template with data.

    :param str data: The encrypted base64 data to put in the template

    :returns: the template string
    :rtype: str
    """
    ctxt = {'ciphertext': data}
    path, filename = os.path.split(TEMPLATE_PATH)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(ctxt)
