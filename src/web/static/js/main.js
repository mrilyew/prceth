u(document).on('DOMContentLoaded', (e) => {
    u("body").append(`    
    <div class="page_grid">
        <div class="page relative">
            <div class="bg_block"></div>
            <div class="page_sticky">
                <header>
                    <div class="header_wrapper">
                        <div class="logo_wrap">
                            <span class="logo">${window.pre_consts.title}</span>
                        </div>
                        <nav>
                            <div data-id="collection" class="nav_element">
                                <span>Коллекции</span>
                            </div>
                            <div data-id="files" class="nav_element">
                                <span>Файлы</span>
                            </div>
                            <div data-id="search" class="nav_element">
                                <span>Поиск</span>
                            </div>
                        </nav>
                    </div>
                </header>
                <div class="horizontal_slider_tabs">
                    <div class="horizontal_slider_tab" data-id="collection">
                        <div class="or_tab_inversed">Новая</div>
                        <div class="or_tab_inversed">Искать</div>
                    </div>
                    <div class="horizontal_slider_tab" data-id="files">
                        <div class="or_tab_inversed">Загрузить</div>
                        <div class="or_tab_inversed">Искать</div>
                    </div>
                    <div class="horizontal_slider_tab" data-id="search">
                        <input type="search" placeholder="...">
                    </div>
                </div>
            </div>
            <div class="horizontal_slider"></div>
            <div class="content_block">
                <div class="content_block_left"></div>
                <div class="content_block_center colored" style="height: 1025px;">
                    <div class="content_block_title">
                        <h4>Коллекции</h4>
                    </div>
                </div>
                <div class="content_block_right colored"></div>
            </div>
        </div>
        <div class="right_block"></div>
    </div>
    `)
})

u(document).on('mouseover', '.header_wrapper .nav_element', (e) => {
    const target = u(e.target).closest('.nav_element')
    const id     = target.attr("data-id")
    target.addClass("hovered")

    setTimeout(() => {
        if(!target.hasClass("hovered")) {
            return
        }

        u(".horizontal_slider_tab.shown").removeClass("shown")
        u(`.horizontal_slider_tab[data-id="${id}"]`).addClass("shown")
    }, 400)
})

u(document).on('mouseover', '.horizontal_slider_tab', (e) => {
    u(e.target).closest(".horizontal_slider_tab").addClass("hovered")
})

u(document).on('mouseout', '.horizontal_slider_tab', (e) => {
    u(e.target).closest(".horizontal_slider_tab").removeClass("hovered")
})

u(document).on('mouseout', '.header_wrapper .nav_element, .horizontal_slider_tab', (e) => {
    const target = u(e.target).closest('.nav_element')
    target.removeClass("hovered")

    setTimeout(() => {
        if(u(".nav_element.hovered, .horizontal_slider_tab.hovered").length < 1) {
            u(".horizontal_slider_tab.shown").removeClass("shown")
            return
        }
    }, 1000)
})

u(document).on('click', '.header_wrapper .logo_wrap .logo', (e) => {
    window.scrollTo(0, 0)
})
