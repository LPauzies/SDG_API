from app import app
from app import config
from flask_swagger_ui import get_swaggerui_blueprint

def parse_arguments():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server", type=str, help="The host to declare to run the server, default is 127.0.0.1")
    parser.add_argument("-p", "--port", type=str, help="The port to declare to run the server, default is 5000")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    server = "127.0.0.1"
    port = "5000"
    if args.server:
        server = args.server
    if args.port:
        port = args.port
    #Configure the app
    app.config['DEBUG'] = True
    app.config['SWAGGER_URL'] = '/api/docs'
    app.config['DATA_SWAGGER'] = 'http://' + server + ':' + port + '/swagger'
    app.config['BUNDLE_ERRORS'] = True
    # Define the blueprint of the API
    swaggerui_blueprint = get_swaggerui_blueprint(
        app.config['SWAGGER_URL'], # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        app.config['DATA_SWAGGER'],
        config = {  # Swagger UI config overrides
            'app_name': config.API_NAME
        },
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=app.config['SWAGGER_URL'])
    #Run it
    app.run(host=server, port=port)
