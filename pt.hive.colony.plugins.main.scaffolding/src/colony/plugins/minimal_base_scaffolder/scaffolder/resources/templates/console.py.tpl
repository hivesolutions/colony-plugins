class Console${out value=scaffold_attributes.class_name /}:
    def __init__(self, ${out value=scaffold_attributes.variable_name /}_plugin):
        self.${out value=scaffold_attributes.variable_name /}_plugin = ${out value=scaffold_attributes.variable_name /}_plugin
        self.commands_map = self.__generate_commands_map()

    def get_console_extension_name(self):
        return ${out value=scaffold_attributes.variable_name /}

    def get_commands_map(self):
        return self.commands_map

    def process_dummy_command(self, arguments, arguments_map, output_method, console_context):
        ${out value=scaffold_attributes.variable_name /}_plugin = self.${out value=scaffold_attributes.variable_name /}_plugin
        ${out value=scaffold_attributes.variable_name /} = ${out value=scaffold_attributes.variable_name /}_plugin.${out value=scaffold_attributes.variable_name /}
        dummy_result = ${out value=scaffold_attributes.variable_name /}.dummy_method()
        output_method(dummy_result)

    def __generate_commands_map(self):
        return {
            "dummy_command" : {
                "handler" : self.process_dummy_command,
                "description" : "runs the dummy command",
                "arguments" : [
                    {
                        "name" : "dummy_command",
                        "description" : "performs the dummy command",
                        "values" : str,
                        "mandatory" : True
                    }
                ]
            }
        }
