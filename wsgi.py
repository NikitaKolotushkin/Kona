from app import create_app, db
from config import current_config


app = create_app(config_class = current_config)[0]

if __name__ == '__main__':
    app.run(host=current_config.HOST, port=current_config.PORT, debug=current_config.DEBUG, use_reloader=current_config.RELOADER)
