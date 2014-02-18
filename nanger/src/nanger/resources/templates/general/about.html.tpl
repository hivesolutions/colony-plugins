{% extends "general.html.tpl" %}
{% block content %}
    <div class="quote">
        The complete project was developed by the <a href="http://hive.pt">Hive Solutions</a><br />
        development team using only spare time.
    </div>
    <div class="separator-horizontal"></div>
    <div class="quote">
        Colony is currently licensed under the much permissive<br />
        <strong>GNU General Public License (GPL), Version 3</strong>
        and the<br/>
        current repository is hosted at <a href="https://github.com/hivesolutions/colony">github</a>.
    </div>
    <div class="separator-horizontal"></div>
    <table>
        <tbody>
            <tr>
                <td class="right label" width="50%">run mode</td>
                <td class="left value" width="50%">{{ information.run_mode }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">environment</td>
                <td class="left value" width="50%">{{ information.environment }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">version</td>
                <td class="left value" width="50%">{{ information.version }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">release</td>
                <td class="left value" width="50%">{{ information.release }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">release date</td>
                <td class="left value" width="50%">{{ information.release_date }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">uptime</td>
                <td class="left value" width="50%">{{ manager.get_uptime() }}</td>
            </tr>
        </tbody>
    </table>
{% endblock %}
