{% extends "general_w.html.tpl" %}
{% block content %}
    <div class="console">
        <textarea class="text" autocomplete="off"></textarea>
        <div>Hive Colony {{ information.version }} (Hive Solutions Lda. r{{ information.release }}:{{ information.build }} {{ information.release_date }})</div>
        <div>Python {{ version }}</div>
        <div>Type "help" for more information.</div>
        <div class="previous"></div>
        <div class="current"><span class="prompt"># </span><span class="line"><span class="cursor">&nbsp;</span></span></div>
        <div class="autocomplete">
            <div class="tooltip">
                <div class="doc"></div>
                <div class="params"></div>
                <div class="return"></div>
            </div>
            <ul></ul>
        </div>
    </div>
{% endblock %}
