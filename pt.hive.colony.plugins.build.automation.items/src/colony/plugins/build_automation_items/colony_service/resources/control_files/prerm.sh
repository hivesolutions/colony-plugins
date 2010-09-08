# sets the temporary variables
ETC_PATH=/etc
INIT_D_PATH=$ETC_PATH/init.d
COLONY_NAME=colony

# prints a debug message
echo "Stopping the colony service"

# starts the colony service
$INIT_D_PATH/$COLONY_NAME stop

# prints a debug message
echo "Colony service stopped"
