#!/bin/bash
# Create a setup script and immediately start the apache instance.  Our URL prefix
# is specified by the --mount-point setting.  We need to specify a PYTHONPATH before
# starting the apache instance. Run this script from THIS directory.
mod_wsgi-express setup-server --working-directory nameserver --url-alias /sne/nameserver_atlas/static static --application-type module nameserver.wsgi --server-root /tmp --port 8085 --mount-point /sne/nameserver_atlas

export PYTHONPATH=$(pwd)
/tmp/apachectl start
