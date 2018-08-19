import os
from flask_script import Manager, Shell
from flask_migrate import Migrate
from entity import *
from flasky import create_app


config_name = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config_name)
# manager = Manager(app)
#
# manager.add_command('shell', Shell(make_context=make_shell_context))
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post, Follow=Follow)



if __name__ == '__main__':
    # manager.run()
    app.run(debug=True)
