${foreach item=package from=packages}Package: ${out value=package.name /}
Version: ${out value=package.version /}
Architecture: ${out value=package.architecture /}
Essential: ${out value=package.essential /}
Maintainer: ${out value=package.maintainer /}
Installed-Size: ${out value=package.installed_size /}
Pre-Depends: ${out value=package.pre_dependencies /}
Depends: ${out value=package.dependencies /}
Replaces: ${out value=package.replaces /}
Provides: ${out value=package.provides /}
Filename: ${out value=package.filename /}
Size: ${out value=package.size /}
MD5sum: ${out value=package.md5 /}
SHA1: ${out value=package.sha1 /}
SHA256: ${out value=package.sha256 /}
Section: ${out value=package.section /}
Priority: ${out value=package.priority /}
Description: ${out value=package.description /}

${/foreach}
