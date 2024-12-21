from pydantic import BaseModel, Field
import numerous.widgets as wi
from anywidget import AnyWidget
from pydantic import ValidationError
def number_field(label, tooltip, start, stop, default, multiple_of):
    """Create a number field.
    Args:
        label: The label of the field.
        tooltip: The tooltip of the field.
        start: The minimum value of the field.
        stop: The maximum value of the field.
        default: The default value of the field.
        multiple_of: The increment of the field.
    """
    widget =  wi.Number(label=label, tooltip=tooltip, default=default, start=start, stop=stop, step=multiple_of)
    def generate_widget():
        return widget
    return Field(ge = start, default=default, le =stop, multiple_of=multiple_of, widget_factory=generate_widget, tooltip=tooltip)

class StateModel(BaseModel):
    """A model that can be used to generate a ui from a pydantic model and sync the ui with the model.
    
    Args:
        *args: The arguments to pass to the pydantic model.
        **kwargs: The keyword arguments to pass to the pydantic model.
    """

    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)

        for k, v in self.model_fields.items():
            if "widget_factory" in v.json_schema_extra:
                v.json_schema_extra['widget'] = v.json_schema_extra['widget_factory']()

    @property
    def changed(self) -> bool:
        """Check if the model has changed.
        Returns:
            bool: True if the model has changed, False otherwise.
        """
        _changed = []
        for k, v in self.model_fields.items():
            _changed.append(getattr(self,k) != v.json_schema_extra["widget"].value)
        return any(_changed)

    def update_widgets(self) -> None:
        """Update the widgets with the values from the model."""
        for k, v in self.model_fields.items():
           v.json_schema_extra["widget"].value = getattr(self,k)

    def get_widget(self, field: str) -> AnyWidget:
        """Get the widget for a field.
        Args:
            field: The field to get the widget for.
        Returns:
            AnyWidget: The widget for the field.
        """
        return self.model_fields[field].json_schema_extra["widget"]

    def update_values(self) -> None:
        """Update the values of the model with the values from the widgets."""
        for k, v in self.model_fields.items():
            setattr(self, k, v.json_schema_extra["widget"].value)

    def validate(self, field, value, raise_error=False) -> bool:
        """Validate a value for a field.
        Args:
            field: The field to validate the value for.
            value: The value to validate.
        Returns:
            bool: True if the value is valid, False otherwise.
        """
        model = self.model_dump()
        model[field] = value
        try:
            self.__class__(**model)
        except ValidationError as e:
            if raise_error:
                raise e
            return False
        return True
    
    def widget_value_valid(self, field: str) -> bool:
        """Check if the value of a widget is valid.
        Args:
            field: The field to check the value for.
        Returns:
            bool: True if the value is valid, False otherwise.
        """
        val = self.get_widget(field).value
        #print("Field", field, " Value", val)
        valid = self.validate(field, val)
        #print("Valid", valid)
        return valid

    def all_valid(self) -> bool:
        """Check if all fields are valid.
        Returns:
            bool: True if all fields widgets values are valid, False otherwise.
        """
        return all(self.widget_value_valid(field) for field in self.model_fields.keys())

    def apply_values(self, values: dict|BaseModel, to_widgets=True, to_model=True) -> None:
        """Apply values to the model or widgets.
        Args:
            values: The values to apply.
            to_widgets: Whether to apply the values to the widgets.
            to_model: Whether to apply the values to the model.
        """
        if isinstance(values, BaseModel):
            values = values.model_dump()
            
        if to_widgets:
            for k, v in values.items():

                self.model_fields[k].json_schema_extra['widget'].value = v
        if to_model:
            for k, v in values.items():
                setattr(self, k, v)
            