# sets the temporary variables
BIN_PATH=/usr/bin
COLONY_DEPLOY_NAME=colony_deploy

# sets the colony deploy flags
COLONY_DEPLOY_FLAGS=--flush

# prints a debug message
echo "Started installing containers"

# deploys the various plugins
$BIN_PATH/$COLONY_DEPLOY_NAME $COLONY_DEPLOY_FLAGS

# prints a debug message
echo "Finished installing containers"
