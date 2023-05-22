## DEV MYSQL CONFIG
export DEV_MYSQL_USER="root"
export DEV_MYSQL_PASSWORD="2YihtgU2SQ==*R90278A3K+/MzYvqm59nFQ==*ONQEn/gbPOmLZDDhiy2YkA==*h2cjWFqwvmgOliOPW+8AmA==" # Password encrypted
export DEV_MYSQL_HOST="127.0.0.1"
export DEV_MYSQL_PORT=3306
export DEV_MYSQL_DB="staging2"
export DEV_MYSQL_AUTH_PLUGIN="mysql_native_password"
export DEV_MYSQL_RAISE_WARNING=true
export DEV_ENCRYPTION_KEY="get_dev_enryption_key()"

## CLOUD TESTING ENVIRONMENT MYSQL CONFIG
export CLOUDTESTING_MYSQL_USER="root"
export CLOUDTESTING_MYSQL_PASSWORD="IJp74Q==*8HWo8l3VVwJBd52QEjNKjA==*Ud74uxG9J0gvIJQj4036jg==*8nvSfAKnBQF869MYk36dcg==" # Password encrypted
export CLOUDTESTING_MYSQL_HOST="127.0.0.1" 
export CLOUDTESTING_MYSQL_PORT=3308
export CLOUDTESTING_MYSQL_DB="sbm_recon"
export CLOUDTESTING_MYSQL_AUTH_PLUGIN="mysql_native_password"
export CLOUDTESTING_MYSQL_RAISE_WARNING=true
export CLOUDTESTING_ENCRYPTION_KEY="get_cloudtesting_enryption_key()"


## UAT/LIVE ENVIRONMENT MYSQL CONFIG
export LIVE_MYSQL_USER="root"
export LIVE_MYSQL_PASSWORD="8W4tGZq0sA==*tuQl1rbh/XnM15vCLpVquA==*n/Uv5zoQX0OU0GNPbwFgCg==*kAmZBOhA/59f589Tsfx0nw==" # Password encrypted
export LIVE_MYSQL_HOST="127.0.0.1" 
export LIVE_MYSQL_PORT=3306
export LIVE_MYSQL_DB="staging2"
export LIVE_MYSQL_AUTH_PLUGIN="mysql_native_password"
export LIVE_MYSQL_RAISE_WARNING=true
export LIVE_ENCRYPTION_KEY="get_live_enryption_key()"

export DEV_ML_USERNAME="ML_USER"

## FLASK API CONFIG
export FLASK_API_NAME="flask_api"
export FLASK_API_VERSION="V0.01"
export FLASK_API_DOCKERFILE_NAME="Dockerfile-Flask"
export FLASK_API_CONTAINER_NAME="FLASK_API_DEV"
