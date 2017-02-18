from setuptools import setup

setup(
    name='Pynitus',
    packages=['Pynitus'],
    include_package_data=True,
    install_requires=[
        'flask',
        'sqlalchemy',
        'python-vlc',
    ],
)
