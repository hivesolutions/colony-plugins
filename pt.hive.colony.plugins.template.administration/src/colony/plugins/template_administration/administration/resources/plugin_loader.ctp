<?colony
# retrieves the initial loaded plugins
initial_loaded_plugins = plugin_manager.get_all_loaded_plugins()

values_map = self.parse_request_attributes(request)

if "type" in values_map:
    type = values_map["type"]

if "pluginId" in values_map:
    plugin_id = values_map["pluginId"]
    if type == "load":
        plugin_manager.load_plugin(plugin_id)
    elif type == "unload":
        plugin_manager.unload_plugin(plugin_id)

final_loaded_plugins = plugin_manager.get_all_loaded_plugins()

diference_loaded_plugins = []

if type == "load":
    for final_loaded_plugin in final_loaded_plugins:
        if not final_loaded_plugin in initial_loaded_plugins:
            diference_loaded_plugins.append(final_loaded_plugin)
elif type == "unload":
    for initial_loaded_plugin in initial_loaded_plugins:
        if not initial_loaded_plugin in final_loaded_plugins:
            diference_loaded_plugins.append(initial_loaded_plugin)

for diference_loaded_plugin in diference_loaded_plugins:
    print diference_loaded_plugin.id
?>
