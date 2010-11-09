${include file="doctype.html.tpl" /}
<head>
    <title>Hive Wiki - ${out_none value=page_name /}</title>
    ${include file="includes.html.tpl" /}
</head>
<body>
    ${include file="header.html.tpl" /}
    <div id="wiki-contents">
        ${include file_value=page_include /}
    </div>
    ${include file="footer.html.tpl" /}
</body>
${include file="end_doctype.html.tpl" /}
