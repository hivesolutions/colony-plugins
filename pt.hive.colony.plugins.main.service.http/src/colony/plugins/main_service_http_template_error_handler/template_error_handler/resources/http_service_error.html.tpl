<!DOCTYPE html>
<html lang="en">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>Colony Framework</title>

        <!-- css inclusion -->
        <link rel="stylesheet" type="text/css" href="/template_error_handler/css/main.css" />

        <!-- favicon inclusion -->
        <link rel="icon" href="/template_error_handler/images/favicon.ico" type="image/x-icon" />

        <!-- javascript inclusion -->
        <script type="text/javascript" src="/template_error_handler/js/main.js"></script>
    </head>
    <body>
        <div id="wiki-header">
            <div class="wiki-header-contents">
                <div class="logo-image">
                    <img src="/template_error_handler/images/colony_logo.png"/>
                </div>
            </div>
        </div>
        <div id="wiki-contents">
            <p></p>
            <div class="highlight">
                <img class="error-image" src="/template_error_handler/images/${out_none value=error_image xml_escape=True /}.png"/>
                <div class="error-text">
                    <b>There was a problem in colony web server...</b>
                    <p>Error ${out_none value=error_code xml_escape=True /} - ${out_none value=error_description xml_escape=True /}</p>
                </div>
            </div>
            <p></p>
            <div class="error">
                <p class="description-header">
                    <b>Description</b>
                </p>
                <p class="description">
                    ${out_none value=error xml_escape=True /}
                </p>
                <p class="traceback-header">
                    <b>Traceback</b>
                </p>
                ${foreach item=traceback_line from=traceback}
                    <p class="traceback">${out_none value=traceback_line xml_escape=True /}</p>
                ${/foreach}
            </div>
        </div>
        <div id="wiki-footer">
            <div class="wiki-footer-contents">
                <div class="logo-image">
                    <a href="http://getcolony.com">
                        <img src="/template_error_handler/images/powered_by_colony.png"/>
                    </a>
                </div>
                <div class="separator">
                    <img src="/template_error_handler/images/separator.png"/>
                </div>
                <div class="text-contents">Document provided by colony framework in ${out_none value=delta_time xml_escape=True /} seconds
                    <br />Copyright
                    <a href="http://hive.pt">Hive Solutions Lda.</a> distributed under
                    <a href="http://creativecommons.org/licenses/by-sa/3.0"> Creative Commons License</a>
                </div>
            </div>
        </div>
    </body>
</html>
