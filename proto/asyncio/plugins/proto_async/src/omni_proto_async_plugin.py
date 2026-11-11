import colony


class OmniProtoAsyncPlugin(colony.Plugin):
    """
    Throwaway plugin of the asyncio prototype, exposes sync and async
    twins of a few actions and the WebSocket handlers.
    """

    id = "pt.hive.omni.plugins.proto_async"
    name = "Omni Proto Async"
    description = "Throwaway asyncio prototype plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [colony.CPYTHON_ENVIRONMENT]
    capabilities = ["mvc_service", "controller_access"]
    dependencies = [
        colony.PluginDependency("pt.hive.colony.plugins.mvc.utils"),
        colony.PluginDependency("pt.hive.colony.plugins.misc.json"),
        colony.PluginDependency("pt.hive.omni.plugins.runtime"),
        colony.PluginDependency("pt.hive.omni.plugins.web_common"),
        colony.PluginDependency("pt.hive.omni.plugins.foundation"),
        colony.PluginDependency("pt.hive.omni.plugins.inventory"),
    ]
    main_modules = ["omni_proto_async"]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import omni_proto_async

        self.system = omni_proto_async.OmniProtoAsync(self)

    def end_load_plugin(self):
        colony.Plugin.end_load_plugin(self)
        self.system.load_components()

    def unload_plugin(self):
        colony.Plugin.unload_plugin(self)
        self.system.unload_components()

    def get_patterns(self):
        return self.system.get_patterns()

    def get_resource_patterns(self):
        return ()

    def get_websocket_patterns(self):
        return self.system.get_websocket_patterns()
