${include file="doctype.html.tpl" /}
<head>
    <title>${out_none value=wiki_name /} - ${out_none value=page_name /}</title>
    ${include file="includes_print.html.tpl" /}
</head>
<body>
    ${include file="header_print.html.tpl" /}
    <div id="wiki-contents">
        ${out value=page_contents /}
    </div>
    ${include file="footer_print.html.tpl" /}
</body>
${include file="end_doctype.html.tpl" /}
