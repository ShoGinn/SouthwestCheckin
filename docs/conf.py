# -*- coding: utf-8 -*-
"""Documentation build configuration file for the `swcheckin` package."""

from email import message_from_string
from itertools import chain

import pkg_resources

# RTD hack start


def patch_setuptools_in_rtd():
    """Install newer setuptools and swcheckin in RTD."""
    import os  # pylint: disable=import-outside-toplevel
    import sys  # pylint: disable=import-outside-toplevel
    import subprocess  # pylint: disable=import-outside-toplevel

    if not os.getenv('READTHEDOCS') or os.getenv('READTHEDOCS_EXEC'):
        return

    # pylint: disable=unexpected-keyword-arg
    pyenv_python_executable = subprocess.check_output(
        ('pyenv', 'which', 'python3.7'), text=True,
    ).strip()
    setuptools_update_cmd = (
        pyenv_python_executable, '-m',
        'pip', 'install', '--force-reinstall',
        '--cache-dir', '/home/docs/checkouts/readthedocs.org/user_builds'
        '/swcheckin/.cache/pip', 'setuptools >= 40.9.0',
    )
    pip_update_cmd = (
        sys.executable, '-m',
        'pip', 'install', '--force-reinstall',
        '--cache-dir', '/home/docs/checkouts/readthedocs.org/user_builds'
        '/swcheckin/.cache/pip', 'pip >= 19.0.3',
    )
    swcheckin_install_cmd = (
        sys.executable, '-m',
        'pip', 'install', '--force-reinstall',
        '--cache-dir', '/home/docs/checkouts/readthedocs.org/user_builds'
        '/swcheckin/.cache/pip', '..[docs]',
    )
    print('>>>>> Bumping setuptools...', file=sys.stderr)
    subprocess.check_call(setuptools_update_cmd)
    print('>>>>> Bumping pip...', file=sys.stderr)
    subprocess.check_call(pip_update_cmd)
    print('>>>>> Installing swcheckin...', file=sys.stderr)
    subprocess.check_call(swcheckin_install_cmd)

    new_env = dict(os.environ)
    new_env['READTHEDOCS_EXEC'] = 'True'

    print('>>>>> Restarting Sphinx build...', file=sys.stderr)
    print(
        f'Sphinx build command is `{sys.executable} {" ".join(sys.argv)}`',
        file=sys.stderr,
    )
    os.execve(sys.executable, (sys.executable, *sys.argv), new_env)


patch_setuptools_in_rtd()
del patch_setuptools_in_rtd
# RTD hack end


def get_supported_pythons(classifiers):
    """Return min and max supported Python version from meta as tuples."""
    py_ver_classifier = 'Programming Language :: Python :: '
    vers = filter(lambda c: c.startswith(py_ver_classifier), classifiers)
    vers = map(lambda c: c[len(py_ver_classifier):], vers)
    vers = filter(lambda c: c[0].isdigit() and '.' in c, vers)
    vers = map(lambda c: tuple(c.split('.')), vers)
    vers = sorted(vers)
    del vers[1:-1]
    if len(vers) < 2:
        vers *= 2
    return vers


def get_github_data(project_urls):
    """Retrieve GitHub user/org and repo name from a bunch of links."""
    partitioned_urls = (p.partition(', ') for p in project_urls)
    for _url_type, _sep, url in partitioned_urls:
        proto, _gh, uri = url.partition('://github.com/')
        if proto not in ('http', 'https'):
            continue
        return uri.split('/')[:2]

    raise LookupError('There are no project URLs pointing to GitHub')


PYTHON_DISTRIBUTION_NAME = 'swcheckin'

PRJ_DIST = pkg_resources.get_distribution(PYTHON_DISTRIBUTION_NAME)
PRJ_PKG_INFO = PRJ_DIST.get_metadata(PRJ_DIST.PKG_INFO)
PRJ_META = message_from_string(PRJ_PKG_INFO)
PRJ_AUTHOR = PRJ_META['Author']
PRJ_LICENSE = PRJ_META['License']
PRJ_SUMMARY = PRJ_META['Summary']
PRJ_DESCRIPTION = PRJ_META['Description']
PRJ_PY_VER_RANGE = get_supported_pythons(PRJ_META.get_all('Classifier'))
PRJ_PY_MIN_SUPPORTED, PRJ_PY_MAX_SUPPORTED = map('.'.join, PRJ_PY_VER_RANGE)
PRJ_GITHUB_USER, PRJ_GITHUB_REPO = get_github_data(
    chain(
        (PRJ_META['Home-page'],),
        PRJ_META.get_all('Project-URL'),
    ),
)

# pylint: disable=invalid-name
project = PRJ_DIST.project_name
author = PRJ_AUTHOR
copyright = f'2019, {author}'  # pylint: disable=invalid-name,redefined-builtin

# The full version, including alpha/beta/rc tags
release = PRJ_DIST.version
# The short X.Y version

version = pkg_resources.parse_version(release).base_version

rst_epilog = f"""
.. |project| replace:: {project}
.. |min_py_supported| replace:: {PRJ_PY_MIN_SUPPORTED}
.. |max_py_supported| replace:: {PRJ_PY_MAX_SUPPORTED}
"""

# -- General configuration -----------------------------------------------------
# If your documentation needs a minimal Sphinx version, state it here.
#
needs_sphinx = '1.7.5'

# Sphinx extension module names.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinxcontrib.apidoc',
]

# sphinxcontrib.apidoc configuration options
apidoc_extra_args = ['--implicit-namespaces', '../src/swcheckin']
apidoc_module_dir = '.'
apidoc_output_dir = 'reference'
apidoc_separate_modules = True

# Paths that contain templates, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# Configuration for the `autodoc' extension.
autodoc_member_order = 'bysource'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    'description': PRJ_SUMMARY,
    'github_user': PRJ_GITHUB_USER,
    'github_repo': PRJ_GITHUB_REPO,
    'github_type': 'star',
    'github_banner': True,
    'travis_button': True,
    'codecov_button': True,
    # 'travis_tld': 'com',
    'show_relbars': True,
    'show_related': True,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = f'{project}doc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc, f'{project}.tex', f'{project} Documentation',
        '[author]', 'manual',
    ),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (
        master_doc, project, f'{project} Documentation',
        [author], 1,
    ),
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc, project, f'{project} Documentation',
        author, project, 'One line description of project.',
        'Miscellaneous',
    ),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']


# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'gidgethub': ('https://gidgethub.readthedocs.io/en/latest/', None),
    'python': ('https://docs.python.org/', None),
}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


# Patch alabaster theme
# Ref: https://github.com/bitprophet/alabaster/pull/147
# FIXME: drop this hack once the PR is merged & released; pylint: disable=fixme
def set_up_travis_context(
        app, pagename, templatename,  # pylint: disable=unused-argument
        context,
        doctree,  # pylint: disable=unused-argument
):
    """Add complete Travis URLs to Jinja2 context."""
    github_slug = '/'.join(
        # (context['theme_github_user'], context['theme_github_repo']),
        (PRJ_GITHUB_USER, PRJ_GITHUB_REPO),
    )

    travis_button = 'true'  # str(context['theme_travis_button']).lower()
    travis_button_enabled = travis_button == 'true'

    travis_slug = github_slug if travis_button_enabled else travis_button

    travis_tld = 'com'  # context["theme_travis_tld"].strip(".").lower()
    travis_base_uri = 'travis-ci.{}/{}'.format(travis_tld, travis_slug)
    context['theme_travis_build_url'] = 'https://{}'.format(travis_base_uri)
    context['theme_travis_badge_url'] = 'https://api.{}.svg?branch={}'.format(
        travis_base_uri, 'master',  # context['theme_badge_branch'],
    )


def setup(app):
    """Patch the sphinx theme set up stage."""
    app.connect('html-page-context', set_up_travis_context)
