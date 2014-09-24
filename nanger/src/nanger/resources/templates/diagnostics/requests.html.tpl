{% extends "general_w.html.tpl" %}
{% block content %}
   <ul class="filter" data-original_value="Search requests" data-number_records="18">
        <div class="data-source" data-url="{{base_path }}diagnostics/requests/list?until={{ until }}" data-type="json" data-timeout="0"></div>
        <li class="template table-row">
            <div class="owner text-left" data-width="70">%[method]</div>
            <div class="message text-left" data-width="630">
                <a href="{{ base_path }}diagnostics/requests/%[id]">%[path]</a>
            </div>
            <div class="type text-right %[time_color]" data-width="80">%[time] ms</div>
            <div class="table-clear"></div>
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
