import windows_toasts


class ToastManager:
    """
    Manages the creation and display of toasts in Windows.
    """

    def __init__(self, app_name: str):
        self.app_name = app_name
        self.toaster = windows_toasts.InteractableWindowsToaster(self.app_name)
        self.toasts = {}
        self.next_id = 1

    def create_new_toast(self) -> int:
        toast_id = self.next_id
        self.next_id += 1

        toast = windows_toasts.Toast(group=self.app_name, duration=windows_toasts.ToastDuration.Long,
                                     attribution_text="")
        self.toasts[toast_id] = toast
        return toast_id

    def add_text_to_toast(self, toast_id: int, text_fields: list):
        if toast_id in self.toasts:
            toast = self.toasts[toast_id]
            toast.text_fields = text_fields

    def add_image_to_toast(self, toast_id: int, image_path: str):
        if toast_id in self.toasts:
            toast = self.toasts[toast_id]
            toast.AddImage(windows_toasts.ToastDisplayImage.fromPath(image_path))

    def add_button_to_toast(self, toast_id: int, button_label: str, button_args: str):
        if toast_id in self.toasts:
            toast = self.toasts[toast_id]
            toast.AddAction(windows_toasts.ToastButton(button_label, button_args))

    def add_input_to_toast(self, toast_id: int, input_id: str, placeholder: str, default_value: str):
        if toast_id in self.toasts:
            toast = self.toasts[toast_id]
            input_field = windows_toasts.ToastInputTextBox(input_id, placeholder, default_value)
            toast.AddInput(input_field)

    def set_toast_activated_callback(self, toast_id: int, callback):
        if toast_id in self.toasts:
            toast = self.toasts[toast_id]
            toast.on_activated = callback

    def display_toast(self, toast_id: int):
        if toast_id in self.toasts:
            toast = self.toasts[toast_id]
            self.toaster.show_toast(toast)

    def destroy_toast(self, toast_id: int):
        if toast_id in self.toasts:
            toast = self.toasts.pop(toast_id)
            self.toaster.remove_toast(toast)
