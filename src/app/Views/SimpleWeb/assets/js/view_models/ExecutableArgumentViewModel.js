import {proc_strtr, escapeHtml} from "../utils/utils.js"

class ExecutableArgumentViewModel {
    template(data) {
        return u(`
            <div>
                <b>${proc_strtr(escapeHtml(data.name), 500)}</b>
            </div>
        `)
    }
}

export default ExecutableArgumentViewModel
