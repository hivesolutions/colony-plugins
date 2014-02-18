{% extends "general.html.tpl" %}
{% block content %}
    <ul class="filter" data-infinite="true" data-original_value="Search plugins">
        <div class="data-source" data-url="{{base_path }}plugins/list" data-type="json" data-timeout="0"></div>
        <li class="template clear">
            <div class="name"><a href="{{ base_path }}plugins/%[short_name]">%[name]</a></div>
            <div class="description">%[id]</div>
        </li>
        <div class="filter-no-results quote">
            No results found
        </div>
        <div class="filter-more">
            <span class="button more">Load more</span>
            <span class="button load">Loading</span>
        </div>
    </ul>
{% endblock %}
