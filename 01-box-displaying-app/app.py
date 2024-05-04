import numpy as np
import pandas as pd
import panel as pn

from panel.layout.gridstack import GridStack

pn.extension("gridstack", notifications=True)


# Explicitly set template and add some text to the header area
template = pn.template.BootstrapTemplate(
    title="Box Displaying App",
)


GRID_SIZE = 4

# Main area component: GridStack
gstack = GridStack(
    sizing_mode="stretch_both",
    allow_resize=True,
    allow_drag=True,
    ncols=GRID_SIZE,
    nrows=GRID_SIZE,
    mode="override",
)
template.main.extend([gstack])

# Sidebar components: buttons!
add_btn = pn.widgets.Button(name="Add box", button_type="success")
remove_btn = pn.widgets.Button(name="Remove box", button_type="danger")
modal_btn = pn.widgets.Button(name="Grid info", button_type="primary")


# Callbacks
def add_box_callback(event):
    """
    Adds a box to the gridstack component. Tries to put at
    the end of the last row, if it's full, it goes to the next row.
    """

    def create_and_add_box(event):
        def resolve_box_insertion_coords(grid: np.ndarray):
            empty_spaces = np.where(grid == 0)
            if len(empty_spaces[0]) == 0:
                return None
            return empty_spaces[0][0], empty_spaces[1][0]

        coords = resolve_box_insertion_coords(gstack.grid)
        if coords:
            gstack[*coords] = pn.Spacer(
                styles=dict(background=colorpicker.value), margin=10
            )
        else:
            pn.state.notifications.error(
                "The grid is already full!", duration=4000
            )

        template.close_modal()

    modal_col.clear()
    modal_title = pn.pane.Markdown("# Choose the color of your block")
    colorpicker = pn.widgets.ColorPicker(value="#ff0000")
    confirm_add_btn = pn.widgets.Button(name="Confirm", button_type="success")
    confirm_add_btn.on_click(create_and_add_box)
    modal_col.extend([modal_title, colorpicker, confirm_add_btn])
    template.open_modal()


def remove_box_callback(event):
    object_keys = list(gstack.objects.keys())
    if len(object_keys) == 0:
        return
    key_to_remove = object_keys[-1]
    del gstack[key_to_remove[0], key_to_remove[1]]


def about_callback(event):
    # Insert elements into the modal column
    modal_col.clear()
    text = f"""
    # Current grid objects and grid structure
    
    ## Objects:
    {str(gstack.objects)}

    ## Structure:
    {str(gstack.grid)}

    """
    modal_col.append(pn.pane.Markdown(text))
    template.open_modal()


add_btn.on_click(add_box_callback)
remove_btn.on_click(remove_box_callback)
modal_btn.on_click(about_callback)
template.sidebar.extend([modal_btn, add_btn, remove_btn])


# Modal components: column for storing grid objects descriptions!
modal_col = pn.Column()
template.modal.extend([modal_col])

template.servable()
