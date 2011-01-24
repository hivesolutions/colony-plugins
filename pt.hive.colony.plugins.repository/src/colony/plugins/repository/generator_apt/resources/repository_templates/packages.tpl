${foreach item=package from=packages}Package: ${out value=package.name /}
Version: ${out value=package.version /}
Architecture: ${out value=package.architecture /}
Essential: ${out value=package.essential /}
Maintainer: ${out value=package.maintainer /}
Installed-Size: ${out value=package.installed_size /}
${if item=package.pre_dependencies value=None operator=neq}Pre-Depends: ${out value=package.pre_dependencies /}${/if}
${if item=package.dependencies value=None operator=neq}Depends: ${out value=package.dependencies /}${/if}
${if item=package.replaces value=None operator=neq}Replaces: ${out value=package.replaces /}${/if}
${if item=package.provides value=None operator=neq}Provides: ${out value=package.provides /}${/if}
Filename: ${out value=package.filename /}
Size: ${out value=package.size /}
MD5sum: ${out value=package.md5 /}
SHA1: ${out value=package.sha1 /}
SHA256: ${out value=package.sha256 /}
${if item=package.section value=None operator=neq}Section: ${out value=package.section /}${/if}
${if item=package.priority value=None operator=neq}Priority: ${out value=package.priority /}${/if}
${if item=package.description value=None operator=neq}Description: ${out value=package.description /}${/if}
${/foreach}
