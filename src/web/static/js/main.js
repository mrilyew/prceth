u(document).on('DOMContentLoaded', (e) => {
    u("body").append(`
        <div id="container">
            <div id="left_container">
                <header>
                    <div id="left_btn"></div>
                    <div id="cntr_logo">
                        <b>${window.pre_consts.title}</b>
                    </div>
                    <div id="right_btn"></div>
                </header>
            </div>
            <div id="right_container"></div>
        </div>
    `)
})
