import tkinter as tk
from tkinter import ttk
from enum import Enum
from tkinter import messagebox
import math
"""
I got my X and Y backwards and i cba fixing it. Just remember that if you read this code.

"""


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Page Conversion")
        self.geometry("640x240")
        self.columnconfigure(0, weight=1)

        self.__create_widgets()

    def __create_widgets(self):
        self.main_frame = HeaderFrame(self)
        self.main_frame.grid(row=0, column=0, sticky='ew')

        self.body_frame = SettingsFrame(self, controller=self)
        self.body_frame.grid(row=1, column=0, sticky='ew')

        self.conversion_frame = ConversionFrame(
            self, controller=self, text='Base Size', add=False
            )
        
        self.conversion_frame.grid(row=2, column=0, sticky='ew')

        self.convert_to_frame = ConversionFrame(
            self, controller=self, text='Target Size', add=True
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
    def __init__(self, container, controller, text, add):
        super().__init__(container, text=text,)
        self.combo_sizes = list(PageSizes.__members__.keys())
        self.controller = controller
        self.x_var = tk.StringVar()
        self.y_var = tk.StringVar()
        if add: self.add_custom()
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

        self.x_label = ttk.Label(self, text="Width:")
        self.x_label.grid(row=0, column=2, padx=3)

        self.x_dimensions = ttk.Entry(self, width=6, textvariable=self.x_var)
        self.x_dimensions.grid(row=0, column=3, padx=6)
        self.x_dimensions.state(['disabled'])

        self.y_label = ttk.Label(self, text="Height:")
        self.y_label.grid(row=0, column=4, padx=3)

        self.y_dimensions = ttk.Entry(self, width=6, textvariable=self.y_var)
        self.y_dimensions.grid(row=0, column=5, padx=6, pady=6)
        self.y_dimensions.state(['disabled'])
    
    def add_custom(self):
        self.combo_sizes.append('Custom')

class ViewConversion(ttk.Labelframe):
    def __init__(self, container, text):
        super().__init__(container, text=text)
        self.container = container
        self.__create_widgets()

    def __create_widgets(self):
        self.submit = ttk.Button(self, text='Submit', command=self.__display_page)
        self.submit.grid(row=0, column=0, padx=6)
        self.caution = ttk.Label(self, text='Custom sizes that are less than 20mm of difference from the base page may look buggy.')
        self.caution.grid(row=0, column=1)
    
    def __display_page(self):
        pc = calculate_size(self.container)
        match pc:
            case ErrorCodes.BlankValue:
                messagebox.showwarning(title='Warning', message="Please ensure entries aren't blank.")
            case ErrorCodes.BaseSmall:
                messagebox.showwarning(title="Warning", message="Ensure the base page is not smaller than the conversion page.")
            case ErrorCodes.BothEqual:
                messagebox.showwarning(title="Warning", message="Both pages cannot be equally sized.")
            case ErrorCodes.WidthEqual:
                messagebox.showwarning(title="Warning", message="Widths cannot be equal.")
            case ErrorCodes.HeightEqual:
                messagebox.showwarning(title="Warning", message="Heights cannot be equal.")
            case _:
                page = PageWindow(self, pc)
                print(pc)

class PageWindow(tk.Toplevel):
    def __init__(self, master, pc):
        super().__init__(master)
        self.master = master
        self.pc = pc
        self.geometry("520x695")
        self.resizable(False, False)
        self.__create_widgets()
    
    def __create_widgets(self):
        self.canvas = tk.Canvas(self, width=420, height=595, background='white')
        self.canvas.pack(pady=50)
        self.__calculate_canvas(self.pc)
    
    def __calculate_canvas(self, pc):
        units = self.master.container.body_frame.dimensions_box.get()
        main_window = self.master.container
        bsize = pc['p_base']
        csize = pc['p_conv']
        conv_type = pc['conv_type']
        
        match conv_type:
            case 'Standard':
                a = int(bsize[1:])
                b = int(csize[1:])
                
                c = b - a
                
                canvas_size = PagePixels.A5.value 
                
                pheight = canvas_size[1]
                pwidth = canvas_size[0]
                
                nheight = round(pheight / (2 ** (c / 2)))
                nwidth = round(pwidth / (2 ** (c / 2)))
                
                print(f'Original: {pheight}, {pwidth}')
                print({'Height': nheight, 'Width': nwidth})
                
                pad_w = (pwidth - nwidth) // 2
                pad_h = (pheight - nheight) // 2
                
                x1 = pad_w + nwidth
                y1 = pad_h + nheight
            
            case 'Custom':
                bheight = pc['conv_x']
                bwidth = pc['conv_y'] 
                canvas_size = PageSizes.A5.value
                base_size = PageSizes[pc['p_base']].value
                canvas_pix = PagePixels.A5.value
                
                # scale from base size to canvas size
                # mes x (a5/a10)
                
                bheight = pc['conv_y'] * (canvas_size[1] / base_size[1])
                bwidth = pc['conv_x'] * (canvas_size[0] / base_size[0])
                
                #mm to pix, add options for cm and in.
                
                match units:
                    
                    case 'MM':
                        nheight = (bheight / 25.4) * 72
                        nwidth = (bwidth / 25.4) * 72
                    case 'IN':
                        nheight = bheight * 72
                        nwidth = bwidth * 72
                    case 'CM':
                        nheight = (bheight / 2.54) * 72
                        nwidth = (bwidth / 2.54) * 72
                
                diffy = canvas_pix[1] - nheight
                diffx = canvas_pix[0] - nwidth
                # 120mm x (210/1189) = 21.19 mm
                
                pad_h = diffy / 2
                pad_w = diffx / 2
                
                x1 = pad_w + nwidth
                y1 = pad_h + nheight
                
                self.canvas.create_rectangle(pad_w, pad_h, x1, y1, outline='black')
                print('Custom')
            case _:
                return
        
        if pad_h < 20 or pad_w < 20:
            #We need to move the fuckin text inside da square.
            xtext_x = pad_w + (nwidth / 2)
            xtext_y = pad_h + 20
            
            ytext_x = pad_w + nwidth - 20
            ytext_y = pad_h + (nheight / 2)
        else:
            xtext_x = (pad_w * 1.5) + nwidth
            xtext_y = pad_h + (nheight / 2) + 20
            
            ytext_x = pad_w + (nwidth / 2) + 20
            ytext_y = (pad_h / 2)
        
        yline_x1 = pad_w + (nwidth / 2)
        yline_y1 = 0
        
        yline_x2 = yline_x1
        yline_y2 = pad_h
        
        xline_x1 = (pad_w * 2) + nwidth
        xline_y1 = pad_h + (nheight / 2)
        
        xline_x2 = pad_w + nwidth
        xline_y2 = xline_y1
        
        self.canvas.create_rectangle(pad_w, pad_h, x1, y1, outline='black')
        self.canvas.create_line(yline_x1, yline_y1, yline_x2, yline_y2, dash=(4, 4), fill='black', width=2)
        self.canvas.create_line(xline_x1, xline_y1, xline_x2, xline_y2, dash=(4, 4), fill='black', width=2)
        self.canvas.create_text(xtext_x, xtext_y, text=f'{pc['x_margin']}')
        self.canvas.create_text(ytext_x, ytext_y, text=f'{pc['y_margin']}')
        
        
        
        


def calculate_size(master):
    try:
        pbx = float(master.conversion_frame.x_var.get())
        pby = float(master.conversion_frame.y_var.get())
        pbsize = master.conversion_frame.select_size.get()
        
        pcx = float(master.convert_to_frame.x_var.get())
        pcy = float(master.convert_to_frame.y_var.get())
        pcsize = master.convert_to_frame.select_size.get()
    except ValueError:
        return ErrorCodes.BlankValue
    
    if pcsize == 'Custom' or pbsize == 'Custom':
        conv_type = 'Custom'
    else:
        conv_type = 'Standard'
        
    if pbx < pcx or pby < pcy:
        return ErrorCodes.BaseSmall
    
    if pbx == pcx and pby == pcy:
        return ErrorCodes.BothEqual
    elif pbx == pcx:
        return ErrorCodes.HeightEqual
    elif pby == pcy:
        return ErrorCodes.WidthEqual
        
    diffx = pbx - pcx
    diffy = pby - pcy
    
    x_margin = diffx / 2
    y_margin = diffy / 2
    
    toreturn = {'x_margin': round(x_margin, 1), 'y_margin': round(y_margin, 1), 'p_base': pbsize, 'p_conv': pcsize, 'conv_type': conv_type, 'conv_x': pcx, 'conv_y': pcy}
    
    return toreturn
    

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

class PagePixels(Enum):
    #Size in PX
    A0 = (2384, 3370)
    A1 = (1684, 2384)
    A2 = (1191, 1684)
    A3 = (842, 1191)
    A4 = (595,  842)
    A5 = (420, 595)
    A6 = (298, 420)
    A7 = (210, 298)
    A8 = (147, 210)
    A9 = (105, 147)
    A10 = (74, 105)

class MeasurementUnits(Enum):
    # Converting from MM (stored in Page Sizes)
    CM = {'Operator': 'div', 'Value': 10}
    MM = {'Operator': 'mult', 'Value': 1}
    IN = {'Operator': 'div', 'Value': 25.4}


class ErrorCodes(Enum):
    # Error codes
    BlankValue = 'Blank'
    BaseSmall = 'BaseSmall'
    BothEqual = 'BothEqual'
    HeightEqual = 'HeightEqual'
    WidthEqual = 'WidthEqual'


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
