import tkinter as tk
from tkinter import ttk
from enum import Enum


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Page Conversion")
        self.geometry("640x490")
        self.columnconfigure(0, weight=1)

        self.__create_widgets()

    def __create_widgets(self):
        self.main_frame = HeaderFrame(self)
        self.main_frame.grid(row=0, column=0, sticky='ew')

        self.body_frame = SettingsFrame(self, controller=self)
        self.body_frame.grid(row=1, column=0, sticky='ew')

        self.conversion_frame = ConversionFrame(
            self, controller=self, text='Base Size'
            )
        self.conversion_frame.grid(row=2, column=0, sticky='ew')

        self.convert_to_frame = ConversionFrame(
            self, controller=self, text='Target Size'
            )
        self.convert_to_frame.grid(row=3, column=0, sticky='ew')

        self.output_frame = ViewConversion(self, text='Convert')
        self.output_frame.grid(row=4, column=0, sticky='ew')

    def update_entries(self, event):
        print("update entries triggered from: ", event.widget)

        # The combobox hierarchy: Master Frame, ComboBox
        the_widget = event.widget
        master_frame = the_widget.master
        select_size = the_widget.get()

        if select_size not in PageSizes.__members__:
            print('its custom size')
            master_frame.x_dimensions.state(['!disabled'])
            master_frame.y_dimensions.state(['!disabled'])
        else:
            master_frame.x_dimensions.state(['disabled'])
            master_frame.y_dimensions.state(['disabled'])
            self.update_units(event=event)

    def update_units(self, event):
        unit = self.body_frame.dimensions_box.get()
        widget = event.widget
        frame = widget.master
        if isinstance(frame, ConversionFrame):
            print('its a conversionframe!')
            xyvar = convert_sizes(widget.get(), unit)
            xvar = xyvar[0]
            yvar = xyvar[1]
            frame.x_var.set(str(xvar))
            frame.y_var.set(str(yvar))
            return
        else:
            select_size1 = self.conversion_frame.select_size.get()
            select_size2 = self.convert_to_frame.select_size.get()

            if select_size1 in PageSizes.__members__:
                xyvar1 = convert_sizes(select_size1, unit)
                xvar1 = xyvar1[0]
                yvar1 = xyvar1[1]
                self.conversion_frame.x_var.set(str(xvar1))
                self.conversion_frame.y_var.set(str(yvar1))

            if select_size2 in PageSizes.__members__:
                xyvar2 = convert_sizes(select_size2, unit)
                xvar2 = xyvar2[0]
                yvar2 = xyvar2[1]
                self.convert_to_frame.x_var.set(str(xvar2))
                self.convert_to_frame.y_var.set(str(yvar2))


class HeaderFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.__create_widgets()
        self.columnconfigure(0, weight=1)

    def __create_widgets(self):
        main_string = "Page Converter"

        self.label = ttk.Label(
            self, text=f"{main_string}", font=("Helvetica", 12, "bold"),
            justify='center', anchor='center'
            )

        self.label.grid(row=0, column=0, sticky='ew')


class SettingsFrame(ttk.Labelframe):
    def __init__(self, container, controller):
        super().__init__(container, text="Settings", padding=10)

        self.dimension_values = ['MM', 'CM', 'IN']
        self.controller = controller

        self.__create_widgets()

    def __create_widgets(self):
        self.label = ttk.Label(self, text="Measurement units:")
        self.label.grid(row=0, column=0)

        self.dimensions_box = ttk.Combobox(
            self, values=self.dimension_values, width=4
            )
        self.dimensions_box.bind(
            "<<ComboboxSelected>>", self.controller.update_units
            )
        self.dimensions_box.grid(row=0, column=1)
        self.dimensions_box.current(0)


class ConversionFrame(ttk.Labelframe):
    def __init__(self, container, controller, text):
        super().__init__(container, text=text)
        self.combo_sizes = list(PageSizes.__members__.keys())
        self.combo_sizes.append('Custom')
        self.controller = controller
        self.x_var = tk.StringVar()
        self.y_var = tk.StringVar()
        self.__create_widgets()

    def __create_widgets(self):

        self.size_label = ttk.Label(self, text='Size:')
        self.size_label.grid(row=0, column=0, padx=3)

        self.select_size = ttk.Combobox(
            self, values=self.combo_sizes, width=10
            )
        self.select_size.grid(row=0, column=1, padx=3)
        self.select_size.bind(
            "<<ComboboxSelected>>", self.controller.update_entries
            )
        self.select_size.set('Select a size')

        self.x_label = ttk.Label(self, text="Height:")
        self.x_label.grid(row=0, column=2, padx=3)

        self.x_dimensions = ttk.Entry(self, width=6, textvariable=self.x_var)
        self.x_dimensions.grid(row=0, column=3, padx=6)
        self.x_dimensions.state(['disabled'])

        self.y_label = ttk.Label(self, text="Width:")
        self.y_label.grid(row=0, column=4, padx=3)

        self.y_dimensions = ttk.Entry(self, width=6, textvariable=self.y_var)
        self.y_dimensions.grid(row=0, column=5, padx=6, pady=6)
        self.y_dimensions.state(['disabled'])


class ViewConversion(ttk.Labelframe):
    def __init__(self, container, text):
        super().__init__(container, text=text)
        self.__create_widgets()

    def __create_widgets(self):
        self.submit = ttk.Button(self, text='Submit')
        self.submit.grid(row=0, column=0, padx=6)


def convert_sizes(select_size, unit):
    size_val = PageSizes[select_size].value
    print('unit:', unit)

    conversion = MeasurementUnits[unit]
    operator = conversion.value['Operator']
    cvalue = conversion.value['Value']

    if operator == 'mult':
        xvar = round((size_val[0] * cvalue), 1)
        yvar = round((size_val[1] * cvalue), 1)

    elif operator == 'div':
        xvar = round((size_val[0] / cvalue), 1)
        yvar = round((size_val[1] / cvalue), 1)
    else:
        return (0, 0)
    return (xvar, yvar)


class PageSizes(Enum):
    # Sizes are in mm
    A0 = (841, 1189)
    A1 = (594, 841)
    A2 = (420, 594)
    A3 = (297, 420)
    A4 = (210, 297)
    A5 = (148, 210)
    A6 = (105, 148)
    A7 = (74, 105)
    A8 = (52, 74)
    A9 = (37, 52)
    A10 = (26, 37)


class MeasurementUnits(Enum):
    # Converting from MM (stored in Page Sizes)
    CM = {'Operator': 'div', 'Value': 10}
    MM = {'Operator': 'mult', 'Value': 1}
    IN = {'Operator': 'div', 'Value': 25.4}


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
