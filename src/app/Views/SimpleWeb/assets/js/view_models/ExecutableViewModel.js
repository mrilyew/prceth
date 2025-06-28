import {proc_strtr, escapeHtml} from "../utils/utils.js"

class ExecutableViewModel {
    template(data) {
        return u(`
            <a href="#execute?name=${escapeHtml(data.class_name)}" class="scroll_element no_overflow">
                <b>${proc_strtr(escapeHtml(data.class_name), 500)}</b>
            </a>
        `)
    }
}

export default ExecutableViewModel
