mod_wsgi-express setup-server --working-directory nameserver --url-alias /static static --application-type module nameserver.wsgi --server-root /tmp --port=8085 --allow-localhost
