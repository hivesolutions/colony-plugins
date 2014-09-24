{% extends "general.html.tpl" %}
{% block content %}
    <ul>
        <li>
            <div class="name">
                <a href="{{ base_path }}diagnostics/requests">Requests List</a>
            </div>
            <div class="description">Display diagnostics grouped inside requests</div>
        </li>
    </ul>
{% endblock %}
