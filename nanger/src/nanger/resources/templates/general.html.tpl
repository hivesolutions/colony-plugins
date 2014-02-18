{% include "partials/doctype.html.tpl" %}
<head>
    <title>{{ title }}</title>
    {% include "partials/content_type.html.tpl" %}
    {% include "partials/includes.html.tpl" %}
</head>
<body class="{% block classes %}ux{% endblock %}">
    {% include "partials/header.html.tpl" %}
    <div id="content">
        {% block content %}{% endblock %}
    </div>
    {% include "partials/footer.html.tpl" %}
</body>
{% include "partials/end_doctype.html.tpl" %}
