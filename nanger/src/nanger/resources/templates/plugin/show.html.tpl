{% extends "plugin/base.html.tpl" %}
{% block content %}
    <div class="quote">{{ plugin.name }}</div>
    <div class="separator-horizontal"></div>
    <table>
        <tbody>
            <tr>
                <td class="right label" width="50%">status</td>
                {% if plugin.loaded %}
                    <td class="left value valid" width="50%">active</td>
                {% else %}
                    <td class="left value invalid" width="50%">inactive</td>
                {% endif %}
            </tr>
            <tr>
                <td class="right label" width="50%">id</td>
                <td class="left value" width="50%">{{ plugin.id }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">version</td>
                <td class="left value" width="50%">{{ plugin.version }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">author</td>
                <td class="left value" width="50%">{{ plugin.get_author_name() }}</td>
            </tr>
            {% if plugin.loaded %}
                <tr>
                    <td class="right label" width="50%">uptime</td>
                    <td class="left value" width="50%">{{ plugin.get_uptime() }}</td>
                </tr>
            {% endif %}
        </tbody>
    </table>
{% endblock %}
