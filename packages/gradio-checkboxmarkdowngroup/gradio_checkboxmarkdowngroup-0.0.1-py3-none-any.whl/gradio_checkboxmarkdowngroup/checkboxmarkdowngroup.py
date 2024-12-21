"""gr.CheckboxMarkdownGroup() component"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any, Literal, Union

from gradio_client.documentation import document

from gradio.components.base import Component, FormComponent
from gradio.events import Events
from gradio.exceptions import Error
from dataclasses import dataclass

if TYPE_CHECKING:
    from gradio.components import Timer
    
@dataclass
class Choice:
    def __init__(self, id: str, title: str, content: str):
        self.id = id
        self.title = title
        self.content = content
        
# Define allowable types
ChoiceType = Literal["value", "index", "title", "content", "all"]


class CheckboxMarkdownGroup(FormComponent):
    """
    Creates a set of checkboxes. Can be used as an input to pass a set of values to a function or as an output to display values, a subset of which are selected.
    Demos: sentence_builder
    """

    EVENTS = [Events.change, Events.input, Events.select]

    def __init__(
        self,
        choices: list[Choice]
        | None = None,
        *,
        value: Sequence[str | float | int] | str | float | int | Callable | None = None,
        type: ChoiceType = "value",
        label: str | None = None,
        info: str | None = None,
        every: Timer | float | None = None,
        inputs: Component | Sequence[Component] | set[Component] | None = None,
        show_label: bool | None = None,
        container: bool = True,
        scale: int | None = None,
        min_width: int = 160,
        interactive: bool | None = None,
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        key: int | str | None = None,
    ):
        """
        Parameters:
            choices: A list of string or numeric options to select from. An option can also be a tuple of the form (name, value), where name is the displayed name of the checkbox button and value is the value to be passed to the function, or returned by the function.
            value: Default selected list of options. If a single choice is selected, it can be passed in as a string or numeric type. If callable, the function will be called whenever the app loads to set the initial value of the component.
            type: Type of value to be returned by component. "value" returns the list of strings of the choices selected, "index" returns the list of indices of the choices selected.
            label: the label for this component, displayed above the component if `show_label` is `True` and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component corresponds to.
            info: additional component description, appears below the label in smaller font. Supports markdown / HTML syntax.
            every: Continously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.
            inputs: Components that are used as inputs to calculate `value` if `value` is a function (has no effect otherwise). `value` is recalculated any time the inputs change.
            show_label: If True, will display label.
            container: If True, will place the component in a container - providing some extra padding around the border.
            scale: Relative width compared to adjacent Components in a Row. For example, if Component A has scale=2, and Component B has scale=1, A will be twice as wide as B. Should be an integer.
            min_width: Minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.
            interactive: If True, choices in this checkbox group will be checkable; if False, checking will be disabled. If not provided, this is inferred based on whether the component is used as an input or output.
            visible: If False, component will be hidden.
            elem_id: An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.
            elem_classes: An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.
            render: If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.
            key: if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.
        """
        self.choices = choices if choices else []
        valid_types = ["value", "index", "title", "content", "all"]
        if type not in valid_types:
            raise ValueError(
                f"Invalid value for parameter `type`: {type}. Please choose from one of: {valid_types}"
            )
        self.type = type
        super().__init__(
            label=label,
            info=info,
            every=every,
            inputs=inputs,
            show_label=show_label,
            container=container,
            scale=scale,
            min_width=min_width,
            interactive=interactive,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=render,
            key=key,
            value=value,
        )

    def example_payload(self) -> Any:
        return [self.choices[0].id] if self.choices else None

    def example_value(self) -> Any:
        return [self.choices[0].id] if self.choices else None

    def api_info(self) -> dict[str, Any]:
        return {
            "items": {"enum": [c.id for c in self.choices], "type": "string"},
            "title": "Checkbox Group",
            "type": "array",
        }

    def preprocess(
        self, payload: list[str | int | float]
    ) -> Union[list[str], list[int], list[dict]]:
        """
        Parameters:
            payload: the list of checked checkboxes' values
        Returns:
            Passes the list of checked checkboxes as a `list[str | int | float]` or their indices as a `list[int]` into the function, depending on `type`.
        """
        id_to_choice = {choice.id: choice for choice in self.choices}
        for value in payload:
            if value not in id_to_choice.keys():
                raise Error(
                    f"Value: {value!r} (type: {type(value)}) is not in the list of choices: {id_to_choice.keys()}"
                )
        if self.type == "value":
            # Return selected IDs directly
            return payload
        elif self.type == "index":
            # Return the indices of the selected choices
            return [i for i, c in enumerate(self.choices) if c.id in payload]
        elif self.type == "title":
            # Return the titles of the selected choices
            return [id_to_choice[i].title for i in payload if i in id_to_choice]
        elif self.type == "content":
            # Return the content of the selected choices
            return [id_to_choice[i].content for i in payload if i in id_to_choice]
        elif self.type == "all":
            # Return full choice objects as dictionaries
            return [id_to_choice[i].__dict__ for i in payload if i in id_to_choice]
        else:
            raise ValueError(
                f"Unknown type: {self.type}. Please choose from: 'value', 'index'."
            )


    def postprocess(
        self, value: list[str | int | float] | str | int | float | None
    ) -> list[str | int | float]:
        """
        Parameters:
            value: Expects a `list[str | int | float]` of values or a single `str | int | float` value, the checkboxes with these values are checked.
        Returns:
            the list of checked checkboxes' values
        """
        if value is None:
            return []
        if not isinstance(value, list):
            value = [value]
        return value
