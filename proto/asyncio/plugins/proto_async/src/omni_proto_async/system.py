import colony


class OmniProtoAsync(colony.System):

    def load_components(self):
        mvc_utils_plugin = self.plugin.mvc_utils_plugin
        omni_foundation_plugin = self.plugin.omni_foundation_plugin
        entity_manager_arguments = omni_foundation_plugin.get_entity_manager_arguments()
        mvc_utils_plugin.assign_controllers(self, self.plugin, entity_manager_arguments)

    def unload_components(self):
        self.plugin.mvc_utils_plugin.unassign_controllers(self)

    def get_patterns(self):
        main = self.main_controller
        return (
            (r"omni_proto/fast", main.fast, "get", "json"),
            (r"omni_proto/slow_sync", main.slow_sync, "get", "json"),
            (r"omni_proto/slow_async", main.slow_async, "get", "json"),
            (r"omni_proto/products_sync", main.products_sync, "get", "json"),
            (r"omni_proto/products_async", main.products_async, "get", "json"),
            (r"omni_proto/lazy_async", main.lazy_async, "get", "json"),
            (r"omni_proto/isolation_async", main.isolation_async, "get", "json"),
            (r"omni_proto/isolation_naive", main.isolation_naive, "get", "json"),
            (r"omni_proto/stock_bump", main.stock_bump, "get", "json"),
            (r"omni_proto/request_info", main.request_info, "get", "json"),
        )

    def get_websocket_patterns(self):
        main = self.main_controller
        return (
            (r"/ws/progress", main.ws_progress),
            (r"/ws/pos", main.ws_pos),
        )
