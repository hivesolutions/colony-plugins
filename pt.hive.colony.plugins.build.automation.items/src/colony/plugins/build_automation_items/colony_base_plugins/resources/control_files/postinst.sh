# sets the temporary variables
BIN_PATH=/usr/bin
COLONY_HOME=/usr/lib/colony
DEPLOY_PATH=$COLONY_HOME/deploy
COLONY_DEPLOY_NAME=colony_deploy

# iterates over all the plugins to deploy them
for plugin in $(ls $DEPLOY_PATH); do
    # prints a debug message
    echo "Installing $plugin"

    # deploys the plugin
    $BIN_PATH/$COLONY_DEPLOY_NAME $DEPLOY_PATH/$plugin
done

# prints a debug message
echo "Finished installing plugins"
