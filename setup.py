from setuptools import setup

setup(
    name='Pynitus',
    version="0.1",
    packages=['Pynitus'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-cors',
        'sqlalchemy',
        'python-memcached',
        'tinnitus',
        'argon2',
        'pytaglib',
        'PyYAML',
    ],
    author='strangedev, Pynitus Universe',
    author_email='strange.dev@gmail.com',
    license='AGPL-3.0',
    keywords='playlist server music collaborative',
    url='https://pynitus-universe.github.io/Pynitus/'

)
