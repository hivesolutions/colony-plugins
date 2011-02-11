${foreach item=package from=packages}${out_map value=package.package key_map=package.package_keys key_order_list=package.package_keys_order key_separator=": " allow_empty=False /}
${/foreach}
