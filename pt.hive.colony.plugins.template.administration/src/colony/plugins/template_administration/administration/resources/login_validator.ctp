<?colony
values_map = self.parse_request_attributes(request)

if "username" in values_map:
    username = values_map["username"]

if "password" in values_map:
    password = values_map["password"]

# retrieves the main login plugin
main_login_plugin = plugin_manager.get_plugin_by_id("pt.hive.colony.plugins.main.login")

print main_login_plugin.validate_login(username, password)
?>
