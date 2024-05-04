import numpy as np
import param
import panel as pn
from panel.viewable import Viewer

from panel.layout.gridstack import GridStack
from panel.template import BootstrapTemplate

pn.extension("gridstack", notifications=True, throttled=True)


# TODO - add the "edit box" button with required callbacks
# TODO - how to make an element of GridStack "selectable"?
# Needs to store the currently selected box
# Needs to open a modal with the color picker with the
# color of the selected box


class BoxAddingModal(Viewer):

    def __init__(self, template: BootstrapTemplate, **params):
        super().__init__(**params)
        self._template = template
        self.modal_title = pn.pane.Markdown("# Choose the color of your box")
        self.colorpicker = pn.widgets.ColorPicker(value="#ff0000")
        self.confirm_add_btn = pn.widgets.Button(
            name="Confirm", button_type="success"
        )
        self.confirm_add_btn.on_click(self.create_and_add_box)

    def create_and_add_box(self, event):
        def resolve_box_insertion_coords(grid: np.ndarray):
            empty_spaces = np.where(grid == 0)
            if len(empty_spaces[0]) == 0:
                return None
            return empty_spaces[0][0], empty_spaces[1][0]

        coords = resolve_box_insertion_coords(self.gstack.grid)
        if coords:
            self.gstack[*coords] = pn.Spacer(
                styles=dict(background=self.colorpicker.value), margin=10
            )
        else:
            pn.state.notifications.error(
                "The grid is already full!", duration=4000
            )

        self._template.close_modal()

    @property
    def gstack(self) -> GridStack:
        return self._template.main[0]

    @property
    def modal(self) -> pn.Column:
        return self._template.modal[0]

    def open_modal(self, event):
        self.modal.clear()
        self.modal.extend(
            [self.modal_title, self.colorpicker, self.confirm_add_btn]
        )
        self._template.open_modal()


class GridInfoModal(Viewer):

    def __init__(self, template: BootstrapTemplate, **params):
        super().__init__(**params)
        self._template = template

    @property
    def gstack(self) -> GridStack:
        return self._template.main[0]

    @property
    def modal(self) -> pn.Column:
        return self._template.modal[0]

    def open_modal(self, event):
        self.modal.clear()
        text = f"""
        # Current grid objects
        
        ## Objects:
        {str(self.gstack.objects)}

        """
        self.modal.append(pn.pane.Markdown(text))
        self._template.open_modal()


class Sidebar(Viewer):

    def __init__(self, template: BootstrapTemplate, **params):
        super().__init__(**params)
        self._template = template
        self._box_adding_modal = BoxAddingModal(template=template)
        self._grid_info_modal = GridInfoModal(template=template)
        self._add_btn = pn.widgets.Button(
            name="Add box", button_type="success"
        )
        self._remove_btn = pn.widgets.Button(
            name="Remove box", button_type="danger"
        )
        self._modal_btn = pn.widgets.Button(
            name="Grid info", button_type="primary"
        )
        # Adds callbacks to the buttons
        self._add_btn.on_click(self._box_adding_modal.open_modal)
        self._remove_btn.on_click(self.remove_box_callback)
        self._modal_btn.on_click(self._grid_info_modal.open_modal)

    def remove_box_callback(self, event):
        object_keys = list(self.gstack.objects.keys())
        if len(object_keys) == 0:
            pn.state.notifications.error(
                "The grid is already empty!", duration=4000
            )
            return
        key_to_remove = object_keys[-1]
        del self.gstack[key_to_remove[0], key_to_remove[1]]

    @property
    def gstack(self) -> GridStack:
        return self._template.main[0]

    @property
    def modal(self) -> pn.Column:
        return self._template.modal[0]

    @property
    def buttons(self):
        return [self._add_btn, self._remove_btn, self._modal_btn]


class App(Viewer):

    GRID_SIZE = 4

    def __init__(self, **params):
        super().__init__(**params)
        self._main = GridStack(
            sizing_mode="stretch_both",
            allow_resize=True,
            allow_drag=True,
            ncols=App.GRID_SIZE,
            nrows=App.GRID_SIZE,
            mode="override",
        )
        self._template = pn.template.BootstrapTemplate(
            title="Box Displaying App",
            sidebar_width=150,
        )
        self._modal = pn.Column()

        self._sidebar = Sidebar(template=self._template)
        self._template.main.extend([self._main])
        self._template.modal.extend([self._modal])
        self._template.sidebar.extend(self._sidebar.buttons)

    def servable(self):
        if pn.state.served:
            return self._template.servable()
        return self


App().servable()
