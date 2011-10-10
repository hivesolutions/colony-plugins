${include file="doctype.html.tpl" /}
<head>
    <title>Colony Nanger</title>
    ${include file="includes.html.tpl" /}
</head>
<body>
    ${include file="header.html.tpl" /}
    <div id="main-container">
        <div id="content-body">
            ${include file_value=page_include /}
        </div>
    </div>
    ${include file="footer.html.tpl" /}
</body>
${include file="end_doctype.html.tpl" /}
