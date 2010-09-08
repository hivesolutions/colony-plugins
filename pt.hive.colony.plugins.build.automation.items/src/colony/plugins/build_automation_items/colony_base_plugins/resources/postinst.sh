for plugin in $(ls /usr/lib/colony/deploy); do
    echo "Installing $plugin"
    colony_deploy /usr/lib/colony/deploy/$plugin
done

echo "Finished installing plugins"
