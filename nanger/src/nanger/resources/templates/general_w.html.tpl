${include file="partials/doctype.html.tpl" /}
<head>
    <title>${out_none value=title xml_escape=True /}</title>
    ${include file="partials/content_type.html.tpl" /}
    ${include file="partials/includes.html.tpl" /}
</head>
<body class="ux wide">
    ${include file="partials/header.html.tpl" /}
    <div id="content">
        ${include file_value=page_include /}
    </div>
    ${include file="partials/footer.html.tpl" /}
</body>
${include file="partials/end_doctype.html.tpl" /}
