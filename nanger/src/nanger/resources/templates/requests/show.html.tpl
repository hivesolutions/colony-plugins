{% extends "general.html.tpl" %}
{% block content %}
    <div class="quote">{{ data.path }}</div>
    <div class="separator-horizontal"></div>
    <table>
        <tbody>
            <tr>
                <td class="right label" width="50%">method</td>
                <td class="left value" width="50%">{{ data.method }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">time</td>
                <td class="left value" width="50%">{{ data.time }} ms</td>
            </tr>
            {% for key, value in data.totals %}
                <tr>
                    <td class="right label" width="50%">{{ key }}</td>
                    <td class="left value" width="50%">{{ value }} ms</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
{% endblock %}
