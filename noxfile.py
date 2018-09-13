import nox

@nox.session(python=['2.7', '3.6', '3.7', 'pypy-6.0'])
def tests(session):
    session.install('pytest')
    session.run('pytest', 'rfc7464')

@nox.session
def lint(session):
    session.install('flake8')
    session.run('flake8', 'rfc7464')
