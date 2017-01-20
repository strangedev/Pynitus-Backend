import os


def htmlRelPath(config, path):
    return os.path.join(config.get("html_dir"), path)


def getConfig(config):
    return {

            "/css/bootstrap.min.css": {
                "tools.staticfile.on": True,
                "tools.staticfile.filename": htmlRelPath(config, "css/bootstrap.min.css")
            },

            "/fonts/glyphicons-halflings-regular.eot": {
                "tools.staticfile.on": True,
                "tools.staticfile.filename": htmlRelPath(config, "fonts/glyphicons-halflings-regular.eot")
            },

            "/fonts/glyphicons-halflings-regular.svg": {
                "tools.staticfile.on": True,
                "tools.staticfile.filename": htmlRelPath(config, "fonts/glyphicons-halflings-regular.svg")
            },

            "/fonts/glyphicons-halflings-regular.ttf": {
                "tools.staticfile.on": True,
                "tools.staticfile.filename": htmlRelPath(config, "fonts/glyphicons-halflings-regular.ttf")
            },

            "/fonts/glyphicons-halflings-regular.woff": {
                "tools.staticfile.on": True,
                "tools.staticfile.filename": htmlRelPath(config, "fonts/glyphicons-halflings-regular.woff")
            },

            "/fonts/glyphicons-halflings-regular.woff2": {
                "tools.staticfile.on": True,
                "tools.staticfile.filename": htmlRelPath(config, "fonts/glyphicons-halflings-regular.woff2")
            },

            '/favicon.ico':
                {
                'tools.staticfile.on': True,
                'tools.staticfile.filename': htmlRelPath(config, "img/pynitus_32x32.ico")
            },

            '/favicon.png':
                {
                'tools.staticfile.on': True,
                'tools.staticfile.filename': htmlRelPath(config, "img/pynitus_32x32.png")
            }

        }