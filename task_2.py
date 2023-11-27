import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from functools import partial
from helper_functions import *
from plotting import *


def plot_resulted_signal(x_sig1, y_sig1, x_sig2, y_sig2, x_res, y_res):
    if arith_op == 'Add' or arith_op == 'Sub':
        plt.figure(figsize=(12, 6))

        # Create a 1x2 grid of subplots and plot in the first one
        plt.subplot(2, 3, 1)
        plot_continuous(x_sig1, y_sig1, title="Cont Signal 1")

        # Plot in the second subplot
        plt.subplot(2, 3, 2)
        plot_continuous(x_sig2, y_sig2, title="Cont Signal 2")

        # Plot in the third subplot
        plt.subplot(2, 3, 3)
        plot_continuous(x_res, y_res, title="Cont Resulted Signal")

        # Create a 1x2 grid of subplots and plot in the first one
        plt.subplot(2, 3, 4)
        plot_discrete(x_sig1, y_sig1, title="Discrete Signal 1")

        # Plot in the second subplot
        plt.subplot(2, 3, 5)
        plot_discrete(x_sig2, y_sig2, title="Discrete Signal 2")

        # Plot in the third subplot
        plt.subplot(2, 3, 6)
        plot_discrete(x_res, y_res, title="Discrete Resulted Signal")

        plt.tight_layout()  # Ensures that the plots don't overlap
        plt.show()
    elif arith_op == 'MulByConst' or arith_op == 'ShiftByConst' or arith_op == 'Norm':
        plt.figure(figsize=(12, 6))

        # Create a 1x2 grid of subplots and plot in the first one
        plt.subplot(2, 2, 1)
        plot_continuous(x_sig1, y_sig1, title="Input Signal")

        # Plot in the second subplot
        plt.subplot(2, 2, 2)
        plot_continuous(x_res, y_res, title="Resulted Signal")

        # Create a 1x2 grid of subplots and plot in the first one
        plt.subplot(2, 2, 3)
        plot_discrete(x_sig1, y_sig1, title="Input Signal")

        # Plot in the second subplot
        plt.subplot(2, 2, 4)
        plot_discrete(x_res, y_res, title="Resulted Signal")

        plt.tight_layout()  # Ensures that the plots don't overlap
        plt.show()


def perform_operation(arith_op, sig1, sig2, const, a, b):
    arith_op = arith_op.get()
    sig1 = sig1.get()
    x_sig1, y_sig1 = read_samples(sig1)
    if arith_op in ('Add', 'Sub'):
        sig2 = sig2.get()
        x_sig2, y_sig2 = read_samples(sig2)
        if len(x_sig2) > len(x_sig1):
            x_res = x_sig2
        else:
            x_res = x_sig1

        len1 = len(y_sig1)
        len2 = len(y_sig2)
        if len1 < len2:
            y_sig1.extend([0] * (len2 - len1))
        else:
            y_sig2.extend([0] * (len1 - len2))

        if arith_op == 'Add':
            y_res = [x + y for x, y in zip(y_sig1, y_sig2)]
        else:
            y_res = [x - y if x > y else y - x for x, y in zip(y_sig1, y_sig2)]

    elif arith_op in ('MulByConst', 'ShiftByConst'):
        const = int(const.get())
        if arith_op == 'MulByConst':
            x_res = x_sig1
            y_res = [y * const for y in y_sig1]
        elif arith_op == 'ShiftByConst':
            y_res = y_sig1
            x_res = [x - const for x in x_sig1]

    elif arith_op == 'Square':
        x_res = x_sig1
        y_res = [y * y for y in y_sig1]

    elif arith_op == 'Norm':
        a = int(a.get())
        b = int(b.get())
        x_res = x_sig1
        minimum = min(y_sig1)
        maximum = max(y_sig1)
        y_res = [((y - minimum) / (maximum - minimum)) * (b - a) + a for y in y_sig1]

    elif arith_op == 'Acc':
        x_res = x_sig1
        y_res = [y_sig1[0]]
        for i in range(1, len(x_res)):
            y_res.append(y_sig1[i] + y_res[-1])
    plot_resulted_signal(x_sig1, y_sig1, x_sig2, y_sig2, x_res, y_res)


def browse_signal_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)


def update_selected_option(op):
    toggle_signal_visibility(op)


def toggle_signal_visibility(op):
    # Hide all fields
    sig1_label.grid_forget()
    sig1_entry.grid_forget()
    browse_button_sig1.grid_forget()
    sig2_label.grid_forget()
    sig2_entry.grid_forget()
    browse_button_sig2.grid_forget()
    const_label.grid_forget()
    const_entry.grid_forget()
    from_label.grid_forget()
    from_entry.grid_forget()
    to_label.grid_forget()
    to_entry.grid_forget()

    if op in ('Add', 'Sub'):
        sig1_label.configure(text="Input Signal 1:")
        sig1_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        sig1_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        browse_button_sig1.grid(row=0, column=2, padx=10, pady=10, sticky='w')
        sig2_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        sig2_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        browse_button_sig2.grid(row=1, column=2, padx=10, pady=10, sticky='w')

    if op in ('MulByConst', 'ShiftByConst'):
        sig1_label.configure(text="Input Signal:")
        sig1_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        sig1_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        browse_button_sig1.grid(row=0, column=2, padx=10, pady=10, sticky='w')
        const_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        const_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

    if op == 'Norm':
        sig1_label.configure(text="Input Signal:")
        sig1_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        sig1_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        browse_button_sig1.grid(row=0, column=2, padx=10, pady=10, sticky='w')
        from_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        from_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        to_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        to_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')

    if op in ('Square', 'Acc'):
        sig1_label.configure(text="Input Signal:")
        sig1_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        sig1_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')


# region GUI

win = tk.Tk()
win.geometry("500x500")
win.configure(bg="black")
win.title("Signal Calculator")

arith_op = tk.StringVar()
sig1 = tk.StringVar()
sig2 = tk.StringVar()
const = tk.StringVar()
a = tk.StringVar()
b = tk.StringVar()

style = ttk.Style()
style.configure("TLabel", foreground="white", background="black", font=("Arial", 14, "bold"))
style.configure("TEntry", font=("Arial", 12, "bold"))
style.configure("TButton", foreground="black", background="black", font=("Arial", 14, "bold"))

default_frame = tk.Frame(win)
default_frame.configure(bg="black")

op_label = ttk.Label(default_frame, text='Arithmetic Operation :')
op_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
op_options = ['Add', 'Sub', 'MulByConst', 'Square', 'ShiftByConst', 'Norm', 'Acc']
op_drop_menu = tk.OptionMenu(default_frame, arith_op, *op_options, command=update_selected_option)
op_drop_menu.grid(row=0, column=1, padx=10, pady=10, sticky='w')
default_frame.pack(pady=50)

variable_frame = tk.Frame(win)
variable_frame.configure(bg="black")

# Variable Labels Widgets
sig1_label = ttk.Label(variable_frame, text='Input Signal 1 :')

sig2_label = ttk.Label(variable_frame, text='Input Signal 2 :')
const_label = ttk.Label(variable_frame, text='Constant :')
from_label = ttk.Label(variable_frame, text='From :')
to_label = ttk.Label(variable_frame, text='To :')

# Variable Entry Widgets
sig1_entry = ttk.Entry(variable_frame, textvariable=sig1)

sig2_entry = ttk.Entry(variable_frame, textvariable=sig2)
const_entry = ttk.Entry(variable_frame, textvariable=const)
from_entry = ttk.Entry(variable_frame, textvariable=a)
to_entry = ttk.Entry(variable_frame, textvariable=b)

# Create "Browse" buttons for selecting files
browse_button_sig1 = ttk.Button(variable_frame, text="Browse", command=lambda: browse_signal_file(sig1_entry))
browse_button_sig2 = ttk.Button(variable_frame, text="Browse", command=lambda: browse_signal_file(sig2_entry))

variable_frame.pack(pady=10)

# Calculate Button
calculate_button = ttk.Button(win, text='Calculate',
                              command=partial(perform_operation, arith_op, sig1, sig2, const, a, b))
calculate_button.pack(side="bottom", pady=30)

win.mainloop()

# endregion
