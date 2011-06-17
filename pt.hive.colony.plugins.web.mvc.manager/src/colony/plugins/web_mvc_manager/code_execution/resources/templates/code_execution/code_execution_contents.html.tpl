<div id="meta-data">
    <div class="area">services</div>
</div>
<div id="contents">
    <h2>Code Execution</h2>
    <form data-action_target="code_execution" method="post">
        <div class="form-field-area">
            <h4>Command Prompt</h4>
            <hr/>
            <div class="form-field">
                <label>Command:</label>
                <div>
                    <textarea class="text" name="command" type="text"></textarea>
                </div>
            </div>
            ${if item=output_message value=None operator=neq}
                <div class="form-field">
                    <label>Output:</label>
                    <div>
                        <p>${out value=output_message /}</p>
                    </div>
                </div>
            ${/if}
        </div>
        <div class="form-button-area">
            <div class="cancel button button-blue">Cancel</div>
            <div class="submit button button-green">Execute</div>
        </div>
    </form>
</div>
