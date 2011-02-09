${foreach item=package from=packages}${out_none prefix="Package: " value=package.name allow_empty=False /}
${out_none prefix="Version: " value=package.version allow_empty=False /}
${out_none prefix="Architecture: " value=package.architecture allow_empty=False /}
${out_none prefix="Essential: " value=package.essential allow_empty=False /}
${out_none prefix="Maintainer: " value=package.maintainer allow_empty=False /}
${out_none prefix="Installed-Size: " value=package.installed_size allow_empty=False /}
${out_none prefix="Pre-Depends: " value=package.pre_dependencies allow_empty=False /}
${out_none prefix="Depends: " value=package.dependencies allow_empty=False /}
${out_none prefix="Replaces: " value=package.replaces allow_empty=False /}
${out_none prefix="Provides: " value=package.provides allow_empty=False /}
${out_none prefix="Filename: " value=package.filename allow_empty=False /}
${out_none prefix="Size: " value=package.size allow_empty=False /}
${out_none prefix="MD5sum: " value=package.md5 allow_empty=False /}
${out_none prefix="SHA1: " value=package.sha1 allow_empty=False /}
${out_none prefix="SHA256: " value=package.sha256 allow_empty=False /}
${out_none prefix="Section: " value=package.section allow_empty=False /}
${out_none prefix="Priority: " value=package.priority allow_empty=False /}
${out_none prefix="Description: " value=package.description allow_empty=False /}

${/foreach}
