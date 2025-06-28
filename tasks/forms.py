from django import forms
from tasks.models import Task

class TaskForm(forms.Form):
    title = forms.CharField(max_length=250, label="Task Title")
    description = forms.CharField(widget=forms.Textarea, label= "Task description")
    due_date = forms.DateField(widget=forms.SelectDateWidget, label="Due Date")
    assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices = [], label = "Assigned To")


    def __init__(self, *args, **kwargs):
        employees = kwargs.pop("employees", [])
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].choices = [(emp.id, emp.name) for emp in employees]

class StyledFormMixin:
    # mixing to apply style to form field
    default_classes = ("w-full px-8 py-4 border border-gray-300 rounded-lg "
                    "focus:outline-none focus:border-rose-500 "
                    "focus:ring focus:ring-rose-200 transition")
    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class' : self.default_classes,
                    'placeholder' : f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class' : f"{self.default_classes}",
                    'placeholder' : f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    "class": "px-8 py-4 border border-gray-300 rounded-lg "
                    "focus:outline-none focus:border-rose-500 "
                    "focus:ring focus:ring-rose-200 transition"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    "class": "space-y-2"
                })
            else:
                print("Inside")
                field.widget.attrs.update({
                    'class' : self.default_classes
                })

#Django Model Form
class TaskModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assigned_to']
        widgets = {
            'due_date' : forms.SelectDateWidget,
            'assigned_to' : forms.CheckboxSelectMultiple
        }
        # or
        # exclude = ['project', 'is_completed', 'created_at', 'updated_at']
        '''Manual Widget'''
        # widgets = {
        #     'title': forms.TextInput(attrs={
        #         'class': (
        #             "w-full px-8 py-4 border border-gray-300 rounded-lg "
        #             "focus:outline-none focus:border-rose-500 "
        #             "focus:ring focus:ring-rose-200 transition"
        #         ),
        #         'placeholder': 'Enter Task Title'
        #     }),
        #     'description': forms.Textarea(attrs={
        #         'class': (
        #             "w-full px-8 py-4 border border-gray-300 rounded-lg resize-none "
        #             "focus:outline-none focus:border-rose-500 "
        #             "focus:ring focus:ring-rose-200 transition"
        #         ),
        #         'placeholder': 'Provide detailed task information'
        #     }),
        #     'due_date': forms.SelectDateWidget(attrs={
        #         'class': (
        #             "border border-gray-300 rounded-lg px-3 py-2 "
        #             "focus:outline-none focus:border-rose-500 "
        #             "focus:ring focus:ring-rose-200 transition"
        #         )
        #     }),
        #     'assigned_to': forms.CheckboxSelectMultiple(attrs={
        #         'class': (
        #             "space-y-2"
        #         )
        #     }),
        # }

    '''Using Mixin Widget'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()



