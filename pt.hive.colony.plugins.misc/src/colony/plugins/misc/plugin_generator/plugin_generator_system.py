import os
import sys

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
HELP_TEXT = "### PLUGIN GENERATOR HELP ###\n\
generate_web_mvc_plugin <author_name> <self.author_email> <self.plugin_namespace> <plugin_id> - generates all the stubs for an MVC plugin for the web framework"

class PluginGenerator:

	commands = ["generate_web_mvc_plugin"]
	
	def __init__(self):
		self.base_path = "D:\\projects\\pt.hive.prototype.gui.web.framework\\src\\main\\webapp\\plugins"
		self.templates_path = os.path.join(os.path.dirname(__file__), "templates\\web\\")
		
	def id2class(self, id):
		class_name = ""
		id_list = id.split("_")
		for id_part in id_list:
			class_name += id_part[0].upper() + id_part[1:]
		return class_name
	
	def namespace2dir(self, namespace):
		dir = ""
		namespace_list = namespace.split(".")
		for namespace_part in namespace_list:
			dir += namespace_part + "/"
		return dir[:-1]

	def replace_content(self, content):
		content = content.replace("{author}", self.author_name)
		content = content.replace("{email}", self.author_email)
		content = content.replace("{id}", self.plugin_id)
		content = content.replace("{namespace}", self.plugin_namespace)
		content = content.replace("{name}", self.plugin_name)
		content = content.replace("{short_name}", self.plugin_short_name)
		content = content.replace("{description}", self.plugin_description)
		content = content.replace("{version}", self.plugin_version)
		return content

	def generate_mvc_component(self):			
		file = open(os.path.join(self.templates_path, "mvc_module_template.js"), "r")
		content = file.read()
		file.close()
		content = self.replace_content(content)
		content = content.replace("{module_name}", self.module_name)
		content = content.replace("{path}", self.plugin_path)
		namespace_list = self.plugin_namespace.split(".")
		path = self.base_path
		for namespace_part in namespace_list:
			path = os.path.join(path, namespace_part)
			if not os.path.isdir(path):
				os.mkdir(path)
		path = os.path.join(path, self.plugin_id)
		if not os.path.isdir(path):
			os.mkdir(path)
		path = os.path.join(path, self.plugin_id + "_module.js")
		file = open(path, "w")
		file.write(content)
		file.close()
		self.generate_mvc_component_part("model")
		self.generate_mvc_component_part("view")
		self.generate_mvc_component_part("controller")
		self.generate_mvc_component_part("presentation_model")
			
	def generate_mvc_component_part(self, mvc_component_type):
		mvc_component_type_upper = self.id2class(mvc_component_type)[0].upper() + self.id2class(mvc_component_type)[1:]
		module_name = self.id2class(self.plugin_id) + mvc_component_type_upper
		inherited_module_name = "Abstract" + mvc_component_type_upper
		print os.path.join(self.templates_path, "mvc_component_template.js")
		file = open(os.path.join(self.templates_path, "mvc_component_template.js"), "r")
		content = file.read()
		file.close()
		content = self.replace_content(content)
		content = content.replace("{module_name}", module_name)
		content = content.replace("{inherited_module_name}", inherited_module_name)
		content = content.replace("{path}", self.plugin_path)
		content = content.replace("{mvc_component_type}", mvc_component_type)
		namespace_list = self.plugin_namespace.split(".")
		path = self.base_path
		for namespace_part in namespace_list:
			path = os.path.join(path, namespace_part)
			if not os.path.isdir(path):
				os.mkdir(path)
		path = os.path.join(path, self.plugin_id)
		if not os.path.isdir(path):
			os.mkdir(path)
		path = os.path.join(path, self.plugin_id + "_" + mvc_component_type + ".js")
		file = open(path, "w")
		file.write(content)
		file.close()
	
	def generate_plugin(self):
		file = open(os.path.join(self.templates_path, "plugin_template.js"), "r")
		content = file.read()
		file.close()
		content = self.replace_content(content)
		content = content.replace("{module_name}", self.module_name)
		content = content.replace("{path}", self.plugin_path)
		file = open(os.path.join(self.base_path, self.plugin_id + "_plugin.js"), "w")
		file.write(content)
		file.close()
		
	def generate_plugin_xml(self):
		file = open(os.path.join(self.templates_path, "plugin_template.xml"), "r")
		content = file.read()
		file.close()
		content = self.replace_content(content)
		content = content.replace("{module_name}", self.module_name)
		content = content.replace("{path}", self.plugin_path)
		file = open(os.path.join(self.base_path, self.plugin_id + "_plugin.xml"), "w")
		file.write(content)
		file.close()
	
	def get_all_commands(self):
		return self.commands

	def get_handler_command(self, command):
		if command in self.commands:
			method_name = "process_" + command
			attribute = getattr(self, method_name)
			return attribute

	def get_help(self):
		return HELP_TEXT

	def process_generate_web_mvc_plugin(self, args, output_method):
		if len(args) >= 4:
			self.author_name = args[0]
			self.author_email = args[1]
			self.plugin_namespace = args[2]
			self.plugin_id = args[3]
			self.plugin_name = "Insert '" + self.plugin_id + "' name here"
			self.plugin_short_name = "Insert '" + self.plugin_id + "' short name here"
			self.plugin_description = "Insert '" + self.plugin_id + "' description here"
			self.plugin_version = "1.0.0"
			self.module_name = self.id2class(self.plugin_id)
			self.plugin_path = self.namespace2dir(self.plugin_namespace) + "/" + self.plugin_id
			self.generate_mvc_component()
			self.generate_plugin()
			self.generate_plugin_xml()
		else:
			output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
        