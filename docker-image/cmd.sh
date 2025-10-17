#!/bin/bash

# env variable required:
# DB_NAME
# DB_SRC_DIR
# PGUSER
# PGPASSWORD
# PGHOST
# PGPORT
# ROLES_FILE
# AFTER_BUILD_SCRIPT
# TIMEOUT

if [ -z $TIMEOUT ]; then
  TIMEOUT=1
fi

sleep $TIMEOUT
echo start building database $DB_NAME from $DB_SRC_DIR
if [ -z $ROLES_FILE ]; then
  pg_import --rebuild -d $DB_NAME $DB_SRC_DIR
else
  pg_import --rebuild -r $ROLES_FILE -d $DB_NAME $DB_SRC_DIR
fi

if [[ ! -z $AFTER_BUILD_SCRIPT ]]; then
  psql -c "$AFTER_BUILD_SCRIPT" -d $DB_NAME
fi
echo done

if [ "$SIDECAR_MOD" == "true" ]; then
  sleep infinity
fi
