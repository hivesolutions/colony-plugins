import colony.base.plugin_system
import colony.base.decorators

class ${out value=scaffold_attributes.class_name /}Plugin(colony.base.plugin_system.Plugin):
    id = "${out value=scaffold_attributes.plugin_id /}"
    short_name = "${out value=scaffold_attributes.short_name /} Plugin"
    version = "${out value=scaffold_attributes.plugin_version /}"
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "plugin_test_case_bundle",
        "web.mvc_service"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.web.mvc.utils", "${out value=scaffold_attributes.plugin_version /}"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.resources.resource_manager", "${out value=scaffold_attributes.plugin_version /}"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.misc.json", "${out value=scaffold_attributes.plugin_version /}")
    ]
    main_modules = [
        "${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_controllers",
        "${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_entity_models",
        "${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_exceptions",
        "${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_system",
        "${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_test"
    ]

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import ${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_system
        import ${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_test
        self.${out value=scaffold_attributes.variable_name /} = ${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_system.${out value=scaffold_attributes.class_name /}(self)
        self.${out value=scaffold_attributes.variable_name /}_test = ${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_test.${out value=scaffold_attributes.class_name /}Test(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)
        self.${out value=scaffold_attributes.variable_name /}.load_components()

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("${out value=scaffold_attributes.plugin_id /}", "${out value=scaffold_attributes.plugin_version /}")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("${out value=scaffold_attributes.plugin_id /}", "${out value=scaffold_attributes.plugin_version /}")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies("${out value=scaffold_attributes.plugin_id /}", "${out value=scaffold_attributes.plugin_version /}")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_plugin_test_case_bundle(self):
        return self.${out value=scaffold_attributes.variable_name /}_test.get_plugin_test_case_bundle()

    def get_patterns(self):
        return self.${out value=scaffold_attributes.variable_name /}.get_patterns()

    def get_communication_patterns(self):
        return ()

    def get_resource_patterns(self):
        return ()

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.web.mvc.utils")
    def set_web_mvc_utils_plugin(self, web_mvc_utils_plugin):
        self.web_mvc_utils_plugin = web_mvc_utils_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.resources.resource_manager")
    def set_resource_manager_plugin(self, resource_manager_plugin):
        self.resource_manager_plugin = resource_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.json")
    def set_json_plugin(self, json_plugin):
        self.json_plugin = json_plugin
