import colony.base.plugin_system

class ${out value=scaffold_attributes.class_name /}Plugin(colony.base.plugin_system.Plugin):
    id = "${out value=scaffold_attributes.plugin_id /}"
    name = "${out value=scaffold_attributes.short_name /} Plugin"
    short_name = "${out value=scaffold_attributes.short_name /}"
    description = "${out value=scaffold_attributes.description /} plugin"
    version = "${out value=scaffold_attributes.plugin_version /}"
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "_console_command_extension",
        "plugin_test_case_bundle"
    ]
    main_modules = [
        "${out value=scaffold_attributes.backend_namespace /}.console_${out value=scaffold_attributes.variable_name /}",
        "${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_exceptions",
        "${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_system",
        "${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_test"
    ]

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import ${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_system
        import ${out value=scaffold_attributes.backend_namespace /}.console_${out value=scaffold_attributes.variable_name /}
        import ${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_test
        self.${out value=scaffold_attributes.variable_name /} = ${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_system.${out value=scaffold_attributes.class_name /}(self)
        self.console_${out value=scaffold_attributes.variable_name /} = ${out value=scaffold_attributes.backend_namespace /}.console_${out value=scaffold_attributes.variable_name /}.Console${out value=scaffold_attributes.class_name /}(self)
        self.${out value=scaffold_attributes.variable_name /}_test = ${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_test.${out value=scaffold_attributes.class_name /}Test(self)

    def dummy_method(self):
        return self.${out value=scaffold_attributes.variable_name /}.dummy_method()

    def get_console_extension_name(self):
        return self.console_${out value=scaffold_attributes.variable_name /}.get_console_extension_name()

    def get_commands_map(self):
        return self.console_${out value=scaffold_attributes.variable_name /}.get_commands_map()

    def get_plugin_test_case_bundle(self):
        return self.${out value=scaffold_attributes.variable_name /}_test.get_plugin_test_case_bundle()
