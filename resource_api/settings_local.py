import django


def version_server():
    server_version = django.get_version()
    return server_version
