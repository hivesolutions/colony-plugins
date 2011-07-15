<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Colony Framework</title>

        <!--  metadata inclusion -->
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

        <!-- css inclusion -->
        <link rel="stylesheet" type="text/css" href="/template_directory_list_handler/css/main.css" />

        <!-- favicon inclusion -->
        <link rel="icon" href="/template_directory_list_handler/images/favicon.ico" type="image/x-icon" />

        <!-- javascript inclusion -->
        <script type="text/javascript" src="/template_directory_list_handler/js/main.js"></script>
    </head>
    <body>
        <div id="wiki-header">
            <div class="wiki-header-contents">
                <div class="logo-image">
                    <img src="/template_directory_list_handler/images/colony_logo.png"/>
                </div>
            </div>
        </div>
        <div id="wiki-contents">
            <p></p>
            <div class="highlight">
                <img class="directory-list-image" src="/template_directory_list_handler/images/logo_folder.png"/>
                <div class="directory-list-text">
                    <b>Directory listing</b>
                    <p>
                        ${foreach item=directory_item from=directory_list}
                            <a href="${out_none value=directory_item.link quote=True xml_escape=True /}">${out_none value=directory_item.name xml_escape=True /}</a> /
                        ${/foreach}
                        ${out_none value=directory_final_item xml_escape=True /}
                    </p>
                </div>
            </div>
            <p></p>
            <div class="directory-list">
                ${include file_value=format_file /}
                <div class="view-modes">
                    <a href="?format=table" class="${out_none value=formats_map.table xml_escape=True /}">Table</a>
                    <a href="?format=mosaic" class="${out_none value=formats_map.mosaic xml_escape=True /}">Mosaic</a>
                    <a href="?format=thumbnail" class="${out_none value=formats_map.thumbnail xml_escape=True /}">Thumbnail</a>
                </div>
            </div>
        </div>
        <div id="wiki-footer">
            <div class="wiki-footer-contents">
                <div class="logo-image">
                    <a href="http://getcolony.com">
                        <img src="/template_directory_list_handler/images/powered_by_colony.png"/>
                    </a>
                </div>
                <div class="separator">
                    <img src="/template_directory_list_handler/images/separator.png"/>
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
