{% extends "general_w.html.tpl" %}
{% block content %}
    <div class="log">
        {% for line in latest %}
            <div class="line">{{ line }}</div>
        {% endfor %}
    </div>
{% endblock %}
