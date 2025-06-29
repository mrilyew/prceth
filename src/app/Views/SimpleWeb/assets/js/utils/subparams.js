import {proc_strtr, escapeHtml} from "./utils.js"

export const subparams = {
    'StringArgument': new class {
        renderValue(data) {
            let _u = u(`
                <input class="_val" type="text">
            `)

            if (data.is_long == true) {
                _u = u(`
                    <textarea class="_val"></textarea>
                `)
            }

            if (data.default != null) {
                if (data.is_long == true) {
                    _u.attr("default", data.default)
                } else {
                    _u.html(escapeHtml(data.default))
                }
            }

            if (data.assertion != null && data.assertion.not_null == true) {
                _u.attr("required", "true")
            }

            return _u
        }

        recieveValue(node) {
            return node.querySelector('._val').value
        }
    },
    'IntArgument': new class {
        renderValue(data) {
            const _u = u(`
                <input class="_val" type="number">
            `)

            if (data.default != null) {
                _u.attr("value", data.default)
            }

            return _u
        }

        recieveValue(node) {
            return node.querySelector('._val').value
        }
    },
    'LimitedArgument': new class {
        renderValue(data) {
            let _u = u(`
                <select class="_val"></select>
            `)

            data.values.forEach(itm => {
                _u.append(`<option value="${escapeHtml(itm)}">${escapeHtml(itm)}</option>`)
            })

            if (data.default != null) {
                _u.attr("default", data.default)
            }

            if (data.assertion != null && data.assertion.not_null == true) {
                _u.attr("required", "true")
            }

            return _u
        }

        recieveValue(node) {
            return node.querySelector('._val').value
        }
    },
    'BooleanArgument': new class {
        renderValue(data) {
            let _u = u(`
                <input type="checkbox" class="_val">
            `)

            if (data.default == true) {
                _u.attr("checked", "")
            }

            if (data.assertion != null && data.assertion.not_null == true) {
                _u.attr("required", "true")
            }

            return _u
        }

        recieveValue(node) {
            return Number(node.querySelector('._val').checked == true)
        }
    },
    'JsonArgument': new class {
        renderValue(data) {
            let _u = u(`
                <textarea class="_val"></textarea>
            `)

            if (data.default != null) {
                _u.html(escapeHtml(data.default))
            }

            if (data.assertion != null && data.assertion.not_null == true) {
                _u.attr("required", "true")
            }

            return _u
        }

        recieveValue(node) {
            return node.querySelector('._val').value
        }
    },
}
subparams['ObjectArgument'] = subparams['JsonArgument']
subparams['CsvArgument'] = subparams['JsonArgument']

export default subparams
