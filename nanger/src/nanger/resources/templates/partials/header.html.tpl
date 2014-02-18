<div id="header">
    <h1>{{ title }}</h1>
    {% block links %}
        <div class="links">
            {% if area == "home" %}
                <a href="{{ base_path }}index" class="active">home</a>
            {% else %}
                <a href="{{ base_path }}index">home</a>
            {% endif %}
            //
            {% if area == "plugins" %}
                <a href="{{ base_path }}plugins" class="active">plugins</a>
            {% else %}
                <a href="{{ base_path }}plugins">plugins</a>
            {% endif %}
            //
            {% if area == "console" %}
                <a href="{{ base_path }}console" class="active">console</a>
            {% else %}
                <a href="{{ base_path }}console">console</a>
            {% endif %}
            //
            {% if area == "log" %}
                <a href="{{ base_path }}log" class="active">log</a>
            {% else %}
                <a href="{{ base_path }}log">log</a>
            {% endif %}
            //
            {% if area == "about" %}
                <a href="{{ base_path }}about" class="active">about</a>
            {% else %}
                <a href="{{ base_path }}about">about</a>
            {% endif %}
        </div>
    {% endblock %}
</div>
