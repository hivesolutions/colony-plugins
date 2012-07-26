<ul class="filter entities-list">
    <input type="text" class="text-field section-input filter-input" data-original_value="Search plugins" />
    <div class="data-source" data-url="${out_none value=base_path /}plugins/list" data-type="json"></div>
    <li class="template clear">
        <div class="name"><a href="${out_none value=base_path /}plugins/%[short_name]">%[name]</a></div>
        <div class="description">%[id]</div>
    </li>
    <div class="filter-no-results quote">
        No results found
    </div>
    <div class="filter-more">
        <span class="button">Load more</span>
    </div>
</ul>
