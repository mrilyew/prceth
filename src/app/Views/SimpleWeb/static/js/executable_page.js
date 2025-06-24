class ExecutablePageController {
    act_page() {
        u('.frame_content').html(`
            <div class='container'>
                <div class='container_head'>
                    <b>Act execution</b>
                </div>
                <div class='container_body'>
                    <div class='container_body_sections'></div>
                    <div class='container_body_buttons'>
                        <input type='button' id='addParams' value='+'>
                        <input type='button' id='executeBtn' value='Execute'>
                    </div>
                </div>
            </div>
            <div class='execution_side'></div>
        `)

        u('.container').on('click', '#addParams', (e) => {
            ExecutablePageController.addOption()
        })

        u('.container').on('keyup', "input[data-type='param_name']", (e) => {
            if(e.key == 'Backspace') {
                console.log(e.target)
                const cl = e.target.closest('.container_body_section')

                if(e.target.value.length > 0) {
                    return
                }

                try {
                    u(cl.previousSibling).find("input[data-type='param_name']").nodes[0].focus()
                    u(cl).remove()
                } catch(e) {}
            }
        })

        u('.container').on('click', "#executeBtn", async (e) => {
            let pars = collectParams(u('.container_body_sections .container_body_section').nodes)
            let data = await api.act(pars)

            u('.execution_side').html(`<pre>${escapeHtml(JSON.stringify(data, null, 3))}</pre>`)
        })

        ExecutablePageController.__our_tabs('act')
    }

    list_page() {
        u('.frame_content').html(`
            <div class='container'>
                <div class='container_head'>
                    <b>Executables list</b>
                </div>
                <div class='container_body'>
                    <div id="container_head">
                        <select id="_type">
                            <option value="act">Act</option>
                            <option value="extractor">Extractor</option>
                            <option value="representation">Representation</option>
                        </select>
                    </div>

                    <div class='container_body_buttons'>
                        <input type='button' id='findBtn' value='Find'>
                    </div>
                </div>
            </div>
            <div class='execution_side'>
                <div id="flex_results"></div>
            </div>
        `)

        u('.container').on('click', "#findBtn", async (e) => {
            let data = await api.act({
                'i': 'Executables.List',
                'class_type': u('#container_head #_type').nodes[0].value
            })

            u('.execution_side #flex_results').html('')
            data.payload.forEach(item => {
                let __sub = escapeHtml(item.sub)
                let __category = escapeHtml(item.category)
                let __name = escapeHtml(item.name)
                u('.execution_side #flex_results').append(`
                    <a href="#executable?id=${__sub}.${__category}.${__name}" class="flex_res">
                        <div><span>${__category}</span>.<b>${__name}</b></div>
                    </a>
                `)
            })
        })

        ExecutablePageController.__our_tabs('list')
    }

    async exec_page() {
        const ex_name = router.url.getParam('id')
        const its = ex_name.split('.')
        const class_type = its[0].slice(0, -1)
        const class_id = its[1] + '.' + its[2]
        const exec = await api.act({
            'i': 'Executables.Describe',
            'class_type': class_type,
            'class': class_id
        })

        u('.frame_content').html(`
            <div class='container'>
                <div class='container_head'>
                    <b>${escapeHtml(class_id)}</b>
                </div>
                <div class='container_body'>
                    <div class='container_body_sections'></div>
                    <div class='container_body_buttons'>
                        <input type='button' id='execBtn' value='Execute'>
                    </div>
                </div>
            </div>
            <div class='execution_side'>
                <div id="flex_results"></div>
            </div>
        `)
        upper_tabs_controller.setHtml(`
            <a href="#executables" data-name='act' class="tab">Act (by params)</a>
            <a href="#executables_list" data-name='list' class="tab">From list</a>  
            <a href="#executable?id=${class_type}.${escapeHtml(class_id)}" data-name='cur' class="tab">Execute</a>    
        `)
        upper_tabs_controller.setTab('cur')
        navigation_controller.setTab('exec')

        exec.payload.args.forEach(_val => {
            const _key = _val.name
            let arg_type = _val.type
            let ins = u(`
                <div class='container_body_section'></div>
            `)

            if(_val.hidden == true) {
                return
            }

            if(arg_type == 'StringArgument' || arg_type == 'CsvArgument' || arg_type == 'JsonArgument') {
                if(_val.is_long == true || arg_type == 'JsonArgument') {
                    ins.append(`
                        <b>${_key}</b>
                        <textarea data-pname="${_key}">${_val.default ?? ''}</textarea>
                    `)
                } else {
                    ins.append(`
                        <b>${_key}</b>
                        <input data-pname="${_key}" type='text' value="${_val.default ?? ''}">
                    `)
                }
            }

            if(arg_type == 'BooleanArgument') {
                ins.append(`
                    <label>
                        <b>${_key}</b>
                        <input type="checkbox" data-pname="${_key}" ${_val.default == true ? 'checked' : ''}>
                    </label>
                `)
            }

            if(arg_type == 'IntArgument') {
                ins.append(`
                    <label>
                        <b>${_key}</b>
                        <input type="number" data-pname="${_key}" value="${_val.default}">
                    </label>
                `)
            }

            u('.container_body_sections').append(ins)
        })

        u('.container').on('click', '#execBtn', async (e) => {
            let pars = collectParamsByEach(u('.container_body_sections').nodes[0])
            let data = await runner.run(class_type, class_id, pars)

            u('.execution_side').html(`<pre>${escapeHtml(JSON.stringify(data, null, 3))}</pre>`)
        })
    }

    static __our_tabs(select) {
        navigation_controller.setTab('exec')
        upper_tabs_controller.setHtml(`
            <a href="#executables" data-name='act' class="tab">Act (by params)</a>
            <a href="#executables_list" data-name='list' class="tab">From list</a>    
        `)
        upper_tabs_controller.setTab(select)
    }

    static addOption(name = '', val = '') {
        u('.container_body_sections').append(`
            <div class='container_body_section'>
                <input data-type='param_name' type='text' value="${name}">
                <input data-type='param_value' type='text' value="${val}">
            </div>
        `)
    }
}
