${foreach item=package from=packages}${out_map value=package.package key_map=package.package_keys key_separator=": " allow_empty=False /}${/foreach}
