from .app import create_app

APP = create_app()
APP.static_folder = 'static'