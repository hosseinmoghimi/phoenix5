from phoenix.server_settings import phoenix_apps

def app_is_installed(app_name):
    return app_name in (phoenix_app['name'] for phoenix_app in phoenix_apps)