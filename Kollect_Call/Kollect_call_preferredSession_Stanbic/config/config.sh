## DEV MYSQL CONFIG
export DEV_MYSQL_USER="root"
export DEV_MYSQL_PASSWORD="+dHXMfreiw==*CN3PxWBhKBZ7z+dP/yd7pg==*PsZZmsSiB7t9czy01Hfi7w==*pYrIL6X207A9Qh7JSMhVag==" # Password encrypted
export DEV_MYSQL_HOST="127.0.0.1"
export DEV_MYSQL_PORT=3306
export DEV_MYSQL_DB="kollect_stanbic"
export DEV_MYSQL_AUTH_PLUGIN="mysql_native_password"
export DEV_MYSQL_RAISE_WARNING=true
export DEV_ENCRYPTION_KEY="get_dev_enryption_key()"

## CLOUD TESTING ENVIRONMENT MYSQL CONFIG
export CLOUDTESTING_MYSQL_USER="root"
export CLOUDTESTING_MYSQL_PASSWORD="G3yNKw==*gfTkxvdbZb0hrxzqXMizCg==*uuQkVae/oOgv1HtfxFqfGg==*iEm5g5gaAUUvcWziLhCTlA==" # Password encrypted
export CLOUDTESTING_MYSQL_HOST="127.0.0.1" 
export CLOUDTESTING_MYSQL_PORT=3307
export CLOUDTESTING_MYSQL_DB="kollect_stanbic"
export CLOUDTESTING_MYSQL_AUTH_PLUGIN="mysql_native_password"
export CLOUDTESTING_MYSQL_RAISE_WARNING=true
export CLOUDTESTING_ENCRYPTION_KEY="get_cloudtesting_enryption_key()"


## UAT/LIVE ENVIRONMENT MYSQL CONFIG
export LIVE_MYSQL_USER="root"
export LIVE_MYSQL_PASSWORD="+JRs6wwUIA==*uuYEPmy6/9eshVbHbQ/U4A==*D7XI1h41MMduhM635WWLgw==*1aha5rPdMuUFcWTl2sRKbQ==" # Password encrypted
export LIVE_MYSQL_HOST="127.0.0.1" 
export LIVE_MYSQL_PORT=3306
export LIVE_MYSQL_DB="kollect_stanbic"
export LIVE_MYSQL_AUTH_PLUGIN="mysql_native_password"
export LIVE_MYSQL_RAISE_WARNING=true
export LIVE_ENCRYPTION_KEY="get_live_enryption_key()"

export DEV_ML_USERNAME="ML_USER"

## FLASK API CONFIG
export FLASK_API_NAME="flask_api"
export FLASK_API_VERSION="V0.01"
export FLASK_API_DOCKERFILE_NAME="Dockerfile-Flask"
export FLASK_API_CONTAINER_NAME="FLASK_API_DEV"
