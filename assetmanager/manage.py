import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_script import Manager, Server
from assetmanager import create_app, loaddata


app = create_app()
manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = "0.0.0.0",
    port = 8888)
)
manager.add_command("import", loaddata.RSS())

if __name__ == "__main__":
    manager.run()
