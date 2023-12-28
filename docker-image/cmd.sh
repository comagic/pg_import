#!/bin/bash

# env variable required:
# DB_NAME
# DB_SRC_DIR
# PG_USER
# PG_PASSWORD
# PG_HOST
# PG_PORT


echo start building database $DB_NAME from $DB_SRC_DIR
pg_import --rebuild -r $ROLES -d $DB_NAME $DB_SRC_DIR
echo done

if [ "$SIDECAR_MOD" == "true" ]; then
sleep infinity
fi
