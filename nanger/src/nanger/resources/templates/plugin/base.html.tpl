{% extends "general.html.tpl" %}
{% block links %}
    {{ super() }}
    <div class="links sub-links">
        {% if sub_area == "info" %}
            <a href="{{ base_path }}plugins/{{ plugin.short_name }}" class="active">info</a>
        {% else %}
            <a href="{{ base_path }}plugins/{{ plugin.short_name }}">info</a>
        {% endif %}
        //
        {% if plugin.loaded %}
            {% if sub_area == "reload" %}
                <a href="{{ base_path }}plugins/{{ plugin.short_name }}/reload" class="active link-confirm"
                   data-message="Do you really want to reload {{ plugin.name }} ?">reload</a>
            {% else %}
                <a href="{{ base_path }}plugins/{{ plugin.short_name }}/reload" class="link-confirm"
                   data-message="Do you really want to reload {{ plugin.name }} ?">reload</a>
            {% endif %}
            //
            {% if sub_area == "unload" %}
                <a href="{{ base_path }}plugins/{{ plugin.short_name }}/unload" class="active link-confirm"
                   data-message="Do you really want to unload {{ plugin.name }} ?">unload</a>
            {% else %}
                <a href="{{ base_path }}plugins/{{ plugin.short_name }}/unload" class="link-confirm"
                   data-message="Do you really want to unload {{ plugin.name }} ?">unload</a>
            {% endif %}
        {% else %}
            {% if sub_area == "load" %}
                <a href="{{ base_path }}plugins/{{ plugin.short_name }}/load" class="active">load</a>
            {% else %}
                <a href="{{ base_path }}plugins/{{ plugin.short_name }}/load">load</a>
            {% endif %}
        {% endif %}
    </div>
{% endblock %}
