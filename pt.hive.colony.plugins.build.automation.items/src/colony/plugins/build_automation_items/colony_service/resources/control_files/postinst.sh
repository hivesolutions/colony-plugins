# sets the temporary variables
ETC_PATH=/etc
INIT_D_PATH=$ETC_PATH/init.d
COLONY_NAME=colony

# prints a debug message
echo "Starting the colony service"

# starts the colony service
$INIT_D_PATH/$COLONY_NAME start

# prints a debug message
echo "Colony service started"

# prints a debug message
echo "You can now access administration at: https://127.0.0.1/manager"
