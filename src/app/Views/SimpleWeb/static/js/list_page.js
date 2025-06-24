class ListPageController {
    list() {
        u('.frame_content').html(`
            <div class='container'>
                <div class='container_head'>
                    <b>Content list</b>
                </div>
                <div class='container_body'>
                    <div class='container_body_sections'>
                        <div class='container_body_section'>
                            <b>Count</b>
                            <input data-name='count' data-type='param_value' type='text' value="10">
                        </div>
                        <div class='container_body_section'>
                            <b>Timestamp offset</b>
                            <input data-name='timestamp_after' data-type='param_value' type='text'>
                        </div>
                        <div class='container_body_section'>
                            <b>Representation name</b>
                            <input data-name='representation' data-type='param_value' type='text'>
                        </div>
                        <div class='container_body_section'>
                            <b>Order</b>
                            <input data-name='order' data-type='param_value' type='text'>
                        </div>
                    </div>
                    <div class='container_body_buttons'>
                        <input type='button' id='search' value='Search'>
                    </div>
                </div>
            </div>
            <div class='execution_side'></div>
        `)

        navigation_controller.setTab('list')
    }
}
