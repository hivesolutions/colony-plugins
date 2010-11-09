{
    "type" : "plugin",
    "platform" : "${out value=plugin_descriptor.platform /}",
    "sub_platforms" : ${out value=plugin_descriptor.sub_platforms /},
    "id" : "${out value=plugin_descriptor.id /}",
    "name" : "${out value=plugin_descriptor.name /}",
    "short_name" : "${out value=plugin_descriptor.short_name /}",
    "description" : "${out value=plugin_descriptor.description /}",
    "version" : "${out value=plugin_descriptor.version /}",
    "author" : "${out value=plugin_descriptor.author /}",
    "capabilities" : ${out value=plugin_descriptor.capabilities /},
    "capabilities_allowed" : ${out value=plugin_descriptor.capabilities_allowed /},
    "dependencies" : ${out value=plugin_descriptor.dependencies /},
    "main_file" : "${out value=plugin_descriptor.main_file /}",
    "resources" : ${out value=plugin_descriptor.resources /}
}
