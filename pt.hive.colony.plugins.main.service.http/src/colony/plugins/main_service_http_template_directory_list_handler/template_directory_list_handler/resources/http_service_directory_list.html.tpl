<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <link rel="stylesheet" type="text/css" href="/template_directory_list_handler/css/main.css" />
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
					<a href="${out_none value=directory_item.link xml_escape=True /}">${out_none value=directory_item.name xml_escape=True /}</a> / 
					${/foreach}
					${out_none value=directory_final_item xml_escape=True /}
					</p>
				</div>
            </div>
            <p></p>
			<div class="directory-list">		
				<div class="table-view">
					<table cellspacing="0">
						<thead>
							<tr>
								<th class="column name">Name</th>
								<th class="column date">Last Modified</th>
								<th class="column size">Size</th>
							</tr>
						</thead>
						<tbody>
							${foreach item=directory_entry from=directory_entries}
							<tr>
								<td class="name ${out_none value=directory_entry.type xml_escape=True /}-small"><a href="${out_none value=directory_entry.name xml_escape=True /}">${out_none value=directory_entry.name xml_escape=True /}</a></td>
								<td class="date">${format_datetime value=directory_entry.modified_date format="%d/%m/%y %H:%M:%S" xml_escape=True /}</td>
								<td class="size">${out_none value=directory_entry.size_string xml_escape=True /}</td>
							</tr>
                			${/foreach}
						</tbody>
						<tfoot></tfoot>
					</table>
				</div>
				<div class="view-modes">
					<a href="#" class="active">Table</a>
					<a href="#">Mosaic</a>
					<a href="#">Thumbnail</a>
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
                    <br/>Copyright
                    <a href="http://www.hive.pt">Hive Solutions Lda.</a> distributed under
                    <a href="http://creativecommons.org/licenses/by-sa/3.0"> Creative Commons License</a>
                </div>
            </div>
        </div>
    </body>
</html>
