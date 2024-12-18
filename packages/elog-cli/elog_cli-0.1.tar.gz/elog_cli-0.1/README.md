# elog-cli


wget http://elog:8080/v1/mock/users-auth -O user.json
~/.local/bin/openapi-python-client generate --url http://elog:8080/api-docs --output-path elog_management_backend_client --overwrite