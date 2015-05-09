import os

from invoke import ctask as task
from invoke import Collection
from invoke.tasks import call

from . import build, db, django, docs, test


@task(name='clean-python')
def clean_python(ctx):
    """Remove Python file artifacts"""
    ctx.run('find . -name \'*.pyc\' -exec rm -f {} +')
    ctx.run('find . -name \'*.pyo\' -exec rm -f {} +')
    ctx.run('find . -name \'*~\' -exec rm -f {} +')
    ctx.run('find . -name \'__pycache__\' -exec rm -fr {} +')


@task(pre=[build.clean, call(docs.clean, builddir='_build'), clean_python, test.clean])
def clean(ctx):
    """Remove all build, test, coverage and Python artifacts"""
    pass


@task
def develop(ctx):
    """Install (or update) all packages required for development"""
    ctx.run('pip install -U pip setuptools wheel')
    ctx.run('pip install -U -r requirements.txt')
    ctx.run('pip install -U -e .[docs]')
    ctx.run('pip install -U -e .[tests]')


ns = Collection(clean_python, clean, develop, build, db, django, docs, test)
ns.configure({
    'base_dir': os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'env': 'dev',
    'pkg_name': '{{ cookiecutter.pkg_name }}',
    'run': {
        'echo': True,
        'pty': True,
    },
})
