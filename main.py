import tkinter as tk
from tkinter import ttk, filedialog
from functools import partial
from dsp import *
from task4_test_cases.signalcompare import *


def task1_create_signal_window():
    close_windows()

    task_1_win = tk.Toplevel(win)
    task_1_win.geometry("500x500")
    task_1_win.configure(bg="black")
    task_1_win.title("Draw Signal")

    amplitude = tk.StringVar()
    analog_freq = tk.StringVar()
    sampling_freq = tk.StringVar()
    phase_shift = tk.StringVar()
    signal_type = tk.StringVar()

    # Create a style object for ttk widgets
    style = ttk.Style()

    inputs_frame = tk.Frame(task_1_win)
    inputs_frame.columnconfigure(0, weight=1)
    inputs_frame.columnconfigure(1, weight=1)
    inputs_frame.columnconfigure(2, weight=1)
    inputs_frame.configure(bg="black")

    # Labels
    style.configure("TLabel", foreground="white", background="black", font=("Arial", 14, "bold"))
    amp_label = ttk.Label(inputs_frame, text='Amplitude:')
    amp_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

    phi_label = ttk.Label(inputs_frame, text='Phase Shift:')
    phi_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')

    Fa_label = ttk.Label(inputs_frame, text='Analog Frequency:')
    Fa_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')

    Fs_label = ttk.Label(inputs_frame, text='Sampling Frequency:')
    Fs_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')

    sigType_label = ttk.Label(inputs_frame, text='Signal Type:')
    sigType_label.grid(row=4, column=0, padx=10, pady=10, sticky='w')

    # Entry Widgets
    style.configure("TEntry", font=("Arial", 12, "bold"))
    amp_entry = ttk.Entry(inputs_frame, textvariable=amplitude)
    amp_entry.grid(row=0, column=1, padx=10, pady=10)

    phi_entry = ttk.Entry(inputs_frame, textvariable=phase_shift)
    phi_entry.grid(row=1, column=1, padx=10, pady=10)

    Fa_entry = ttk.Entry(inputs_frame, textvariable=analog_freq)
    Fa_entry.grid(row=2, column=1, padx=10, pady=10)

    Fs_entry = ttk.Entry(inputs_frame, textvariable=sampling_freq)
    Fs_entry.grid(row=3, column=1, padx=10, pady=10)

    # OptionMenu (Combobox)
    style.configure("TCombobox", font=("Arial", 12, "bold"))
    options = ['sin', 'cos']
    signal_type.set('sin')

    drop_menu = ttk.Combobox(inputs_frame, textvariable=signal_type, values=options)
    drop_menu.grid(row=4, column=1, padx=10, pady=10)
    inputs_frame.pack(pady=50)

    # Generate Button
    style.configure("TButton", foreground="black", background="black", font=("Arial", 14, "bold"))
    button = ttk.Button(task_1_win,
                        text='Generate',
                        command=partial(generate_signals_plot, amplitude, analog_freq, sampling_freq, phase_shift,
                                        signal_type))

    button.pack(side="bottom", pady=50)


def task2_arithmatic_ops_window():
    close_windows()

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

    task_2_win = tk.Toplevel(win)
    task_2_win.geometry("500x500")
    task_2_win.configure(bg="black")
    task_2_win.title("Signal Calculator")

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

    default_frame = tk.Frame(task_2_win)
    default_frame.configure(bg="black")

    op_label = ttk.Label(default_frame, text='Arithmetic Operation :')
    op_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
    op_options = ['Add', 'Sub', 'MulByConst', 'Square', 'ShiftByConst', 'Norm', 'Acc']
    op_drop_menu = tk.OptionMenu(default_frame, arith_op, *op_options, command=update_selected_option)
    op_drop_menu.grid(row=0, column=1, padx=10, pady=10, sticky='w')
    default_frame.pack(pady=50)

    variable_frame = tk.Frame(task_2_win)
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
    calculate_button = ttk.Button(task_2_win, text='Calculate',
                                  command=partial(perform_operation, arith_op, sig1, sig2, const, a, b))
    calculate_button.pack(side="bottom", pady=30)


def task3_quantization_window():
    close_windows()
    def toggle_levels_visibility_on():
        levels_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        bits_entry.grid_forget()

    def toggle_bits_visibility_on():
        bits_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        levels_entry.grid_forget()

    task_3_win = tk.Toplevel(win)
    task_3_win.geometry("500x500")
    task_3_win.title("Signal Quantization")
    task_3_win.configure(bg="black")

    input_type = tk.StringVar()
    levels = tk.StringVar()
    bits = tk.StringVar()
    test = tk.StringVar()
    signal = tk.StringVar()

    style = ttk.Style()
    style.configure("TLabel", foreground="white", background="black", font=("Arial", 14, "bold"))
    style.configure("TEntry", font=("Arial", 12, "bold"))
    style.configure("TRadiobutton", foreground="white", background="black", font=("Arial", 14, "bold"))
    style.configure("TButton", foreground="black", background="black", font=("Arial", 14, "bold"))

    radio_frame = tk.Frame(task_3_win)
    radio_frame.configure(bg="black")

    levels_radio = ttk.Radiobutton(radio_frame, text='Levels Number:', variable=input_type, value="Levels",
                                   style="TRadiobutton", command=toggle_levels_visibility_on)
    levels_radio.grid(row=0, column=0, padx=10, pady=10, sticky='w')
    levels_entry = ttk.Entry(radio_frame, textvariable=levels, style="TEntry")
    levels_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

    bits_radio = ttk.Radiobutton(radio_frame, text='Bits Number:', variable=input_type, value="Bits",
                                 style="TRadiobutton",
                                 command=toggle_bits_visibility_on)
    bits_radio.grid(row=1, column=0, padx=10, pady=10, sticky='w')
    bits_entry = ttk.Entry(radio_frame, textvariable=bits, style="TEntry")
    bits_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

    test_label = ttk.Label(radio_frame, text='Test Number:', style="TLabel")
    test_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')
    test_entry = ttk.Entry(radio_frame, textvariable=test, style="TEntry")
    test_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')

    # input signals
    signal_label = ttk.Label(radio_frame, text='Input Signal :')
    signal_entry = ttk.Entry(radio_frame, textvariable=signal)
    browse_button_signal = ttk.Button(radio_frame, text="Browse", command=lambda: browse_signal_file(signal_entry))

    signal_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')
    signal_entry.grid(row=3, column=1, padx=10, pady=10, sticky='w')
    browse_button_signal.grid(row=3, column=2, padx=10, pady=10, sticky='w')

    radio_frame.pack(pady=50)

    button = ttk.Button(task_3_win, text='Generate',
                        command=partial(generate_quantized_signal_plot, input_type, levels, bits, test, signal),
                        style="TButton")
    button.pack(side="bottom", pady=30)
    task_3_win.mainloop()


def task4_5_fourier_window():
    close_windows()

    task_4_5_window = tk.Toplevel(win)
    task_4_5_window.geometry("500x500")
    task_4_5_window.title("Fourier")
    task_4_5_window.configure(bg="black")

    # region TASK 4 VARIABLES
    menu_op = tk.StringVar()
    signal_path = tk.StringVar()
    Fs = tk.StringVar()
    new_amp = tk.StringVar()
    new_phase = tk.StringVar()
    component_num = tk.StringVar()
    save_nlines = tk.StringVar()

    # endregion

    # region TASK 4 WIDGETS

    def fourier_transform(signal_path, Fs):
        signal_path = signal_path.get()
        Fs = float(Fs.get())
        signal = read_samples(signal_path)
        x_k = dft(signal)
        amps, phases = get_amp_phase(x_k)
        print(f"ret_amps:{amps}")
        print(f"ret_phases:{phases}")
        sketch_dft(amps, phases, Fs)
        samples = read_samples('task4_test_cases/DFT/Output_Signal_DFT_A-Phase.txt')
        a, p = samples.x, samples.y
        print(f"act_amps:{a}")
        print(f"act_phases:{p}")
        amp2 = []
        # for i in range(len(p)):
        #     p[i] = round(p[i], 8)=
        for i in a:
            amp2.append(round(i, 13))

        print(SignalComapreAmplitude(a, amps))
        print(SignalComapreAmplitude(p, phases))
        create_signal_file(amps, phases)
        return amps, phases

    def reconstruct_idft(signal_path, Fs, component_num, new_amp, new_phase):
        if type(Fs) == 'StringVar':
            Fs = float(Fs.get())

        if type(signal_path) == 'StringVar':
            signal_path = signal_path.get()
        amps, phases = fourier_transform(signal_path, Fs)
        component_num = int(component_num.get())

        if new_amp.get() != "" and new_phase.get() != "":
            new_amp = float(new_amp.get())
            new_phase = float(new_phase.get())
            amps[component_num - 1] = new_amp
            phases[component_num - 1] = new_phase

        elif new_amp.get() != "":
            new_amp = float(new_amp.get())
            amps[component_num - 1] = new_amp

        elif new_phase.get() != "":
            new_phase = float(new_phase.get())
            phases[component_num - 1] = new_phase

        create_signal_file(amps, phases)

        indexes, x_n = calc_idft('./task_4_saved_signals/created_signal.txt')
        plot_discrete(indexes, x_n, 'Reconstructed IDFT')
        plt.show()

    def read_ft(signal_path):
        signal_path = signal_path.get()
        indexes, x_n = calc_idft(signal_path)
        plot_discrete(indexes, x_n, 'IDFT')
        plt.show()

    def update_selected_option(*args):
        toggle_widgets_visibility(menu_op.get())

    def toggle_widgets_visibility(op):
        if op == 'Construct FT':
            transform_button.pack(x=230, y=200)
            # save_button.place(x=235, y=250)
        else:
            transform_button.place_forget()
            # save_button.place_forget()

        if op == 'Modify Amp & Phase':
            comp_label.place(x=120, y=200)
            comp_entry.place(x=260, y=200)
            amp_label.place(x=120, y=250)
            amp_entry.place(x=260, y=250)
            phase_label.place(x=120, y=300)
            phase_entry.place(x=260, y=300)
            # save_button.place(x=230, y=400)
            reconstruct_button.place(x=205, y=350)
        else:
            comp_label.place_forget()
            comp_entry.place_forget()
            amp_label.place_forget()
            amp_entry.place_forget()
            phase_label.place_forget()
            phase_entry.place_forget()
            reconstruct_button.place_forget()

        if op == 'Construct IDFT':
            read_button.place(x=230, y=200)
        else:
            read_button.place_forget()

        if op == 'Construct DCT':
            read_dct_button.place(x=230, y=200)
            save_nlines_label.place(x=120, y=150)
            save_nlines_entry.place(x=260, y=150)
            fs_label.place_forget()
            fs_entry.place_forget()
        else:
            read_dct_button.place_forget()
            save_nlines_label.place_forget()
            save_nlines_entry.place_forget()
            fs_label.place(x=120, y=150)
            fs_entry.place(x=260, y=150)

        if op == 'Remove DC':
            remove_dc_button.place(x=230, y=200)
            fs_label.place_forget()
            fs_entry.place_forget()
        else:
            remove_dc_button.place_forget()
            fs_label.place(x=120, y=150)
            fs_entry.place(x=260, y=150)

    op_label = tk.Label(task_4_5_window, text='Frequency Domain:')
    op_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
    op_options = ['Construct FT', 'Modify Amp & Phase', 'Construct IDFT', 'Construct DCT', 'Remove DC']
    op_dropMenu = tk.OptionMenu(task_4_5_window, menu_op, *op_options, command=update_selected_option)
    op_dropMenu.grid(row=0, column=1, padx=10, pady=10, sticky='w')

    path_label = tk.Label(task_4_5_window, text='Signal Path:')
    path_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')

    path_entry = tk.Entry(task_4_5_window, textvariable=signal_path)
    path_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

    browse_button_signal = ttk.Button(task_4_5_window, text="Browse", command=lambda: browse_signal_file(path_entry))
    browse_button_signal.grid(row=1, column=2, padx=10, pady=10, sticky='w')



    fs_label = tk.Label(task_4_5_window, text='Sampling Frequency:')
    fs_label.place(x=120, y=150)
    fs_entry = tk.Entry(task_4_5_window, textvariable=Fs)
    fs_entry.place(x=260, y=150)

    transform_button = tk.Button(task_4_5_window, text='Transform', command=partial(fourier_transform, signal_path, Fs),
                              activeforeground='red')

    # save_button = Button(win, text='Save FT', command=partial(save_ft, amps, phases), activeforeground='red')

    comp_label = tk.Label(task_4_5_window, text='Component Number:')
    comp_entry = tk.Entry(task_4_5_window, textvariable=component_num)

    amp_label = tk.Label(task_4_5_window, text='New Amplitude:')
    amp_entry = tk.Entry(task_4_5_window, textvariable=new_amp)

    phase_label = tk.Label(task_4_5_window, text='New Phase:')
    phase_entry = tk.Entry(task_4_5_window, textvariable=new_phase)

    save_nlines_label = tk.Label(task_4_5_window, text='Save nLines:')
    save_nlines_entry = tk.Entry(task_4_5_window, textvariable=save_nlines)

    reconstruct_button = tk.Button(task_4_5_window, text='Reconstruct IDFT',
                                command=partial(reconstruct_idft, signal_path, Fs, component_num, new_amp, new_phase),
                                activeforeground='red')

    read_button = tk.Button(task_4_5_window, text='Read FT', command=partial(read_ft, signal_path), activeforeground='red')

    read_dct_button = tk.Button(task_4_5_window, text='Read DCT', command=partial(dct, signal_path, save_nlines),
                             activeforeground='red')

    remove_dc_button = tk.Button(task_4_5_window, text='Remove DC', command=partial(remove_dc, signal_path), activeforeground='red')


def task6_signal_operations_window():
    close_windows()

    task6_window = tk.Toplevel(win)
    task6_window.geometry("600x500")
    task6_window.title("Signal Operations")
    task6_window.configure(bg="black")

    def update_selected_option(*args):
        toggle_widgets_visibility(menu_op.get())

    def toggle_widgets_visibility(op):
        if op == 'Smoothing':
            window_size_label.place(x=120, y=150)
            window_size_entry.place(x=260, y=150)
        else:
            window_size_label.place_forget()
            window_size_entry.place_forget()

        if op == 'Shifting':
            kSteps_label.place(x=120, y=150)
            kSteps_entry.place(x=260, y=150)
        else:
            kSteps_label.place_forget()
            kSteps_entry.place_forget()

        if op == 'Folding':
            shift_fold_check.place(x=190, y=150)
        else:
            shift_fold_check.place_forget()

    def toggle_shift_fold_visibility(*args):
        if isShiftFold.get() == 1:
            kSteps_label.place(x=120, y=200)
            kSteps_entry.place(x=260, y=200)
        else:
            kSteps_label.place_forget()
            kSteps_entry.place_forget()

    menu_op = tk.StringVar()
    signal_path = tk.StringVar()
    window_size = tk.StringVar()
    kSteps = tk.StringVar()
    isShiftFold = tk.IntVar()

    op_label = tk.Label(task6_window, text='Time Domain:')
    op_label.place(x=90, y=50)
    op_options = ['Smoothing', 'Sharpening', 'Shifting', 'Folding', 'Remove DC']
    op_dropMenu = tk.OptionMenu(task6_window, menu_op, *op_options, command=update_selected_option)
    op_dropMenu.place(x=230, y=45)

    path_label = tk.Label(task6_window, text='Signal Path:')
    path_label.place(x=90, y=100)
    path_entry = tk.Entry(task6_window, textvariable=signal_path)
    path_entry.place(x=230, y=100)

    browse_button_signal = ttk.Button(task6_window, text="Browse", command=lambda: browse_signal_file(path_entry))
    browse_button_signal.place(x=370, y=85)

    window_size_label = tk.Label(task6_window, text='Window Size:')
    window_size_entry = tk.Entry(task6_window, textvariable=window_size)

    kSteps_label = tk.Label(task6_window, text='K Steps:')
    kSteps_entry = tk.Entry(task6_window, textvariable=kSteps)

    shift_fold_check = tk.Checkbutton(task6_window, text="Shift Folded Signal", command=toggle_shift_fold_visibility,
                                   variable=isShiftFold)

    calc_button = tk.Button(task6_window, text='Calculate',
                         command=partial(calc_operation, menu_op, signal_path, window_size, kSteps, isShiftFold),
                         activeforeground='red')
    calc_button.place(x=230, y=250)


def task7_convolution_window():
    close_windows()

    task7_window = tk.Toplevel(win)
    task7_window.geometry("500x500")
    task7_window.title("Signal Convolution")
    task7_window.configure(bg="black")

    signal1_path = tk.StringVar()
    signal2_path = tk.StringVar()

    path1_label = tk.Label(task7_window, text='First Signal Path:')
    path1_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
    path1_entry = tk.Entry(task7_window, textvariable=signal1_path)
    path1_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')
    browse_button_signal = ttk.Button(task7_window, text="Browse", command=lambda: browse_signal_file(path1_entry))
    browse_button_signal.grid(row=0, column=2, padx=10, pady=10, sticky='w')

    path2_label = tk.Label(task7_window, text='Second Signal Path:')
    path2_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
    path2_entry = tk.Entry(task7_window, textvariable=signal2_path)
    path2_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')
    browse_button_signal = ttk.Button(task7_window, text="Browse", command=lambda: browse_signal_file(path2_entry))
    browse_button_signal.grid(row=1, column=2, padx=10, pady=10, sticky='w')

    calc_button = tk.Button(task7_window, text='Convolve', command=partial(convolve, signal1_path, signal2_path),
                         activeforeground='red')
    calc_button.place(x=230, y=200)


def task8_correlation_window():
    close_windows()

    task8_window = tk.Toplevel(win)
    task8_window.geometry("500x500")
    task8_window.title("Signal Correlation")
    task8_window.configure(bg="black")

    signal1_path = tk.StringVar()
    signal2_path = tk.StringVar()

    path1_label = tk.Label(task8_window, text='First Signal Path:')
    path1_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
    path1_entry = tk.Entry(task8_window, textvariable=signal1_path)
    path1_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')
    browse_button_signal = ttk.Button(task8_window, text="Browse", command=lambda: browse_signal_file(path1_entry))
    browse_button_signal.grid(row=0, column=2, padx=10, pady=10, sticky='w')

    path2_label = tk.Label(task8_window, text='Second Signal Path:')
    path2_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
    path2_entry = tk.Entry(task8_window, textvariable=signal2_path)
    path2_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')
    browse_button_signal = ttk.Button(task8_window, text="Browse", command=lambda: browse_signal_file(path2_entry))
    browse_button_signal.grid(row=1, column=2, padx=10, pady=10, sticky='w')

    calc_button = tk.Button(task8_window, text='Correlate', command=partial(correlate, signal1_path, signal2_path),
                         activeforeground='red')
    calc_button.place(x=230, y=200)


def task9_fast_window():
    close_windows()

    task9_window = tk.Toplevel(win)
    task9_window.geometry("500x500")
    task9_window.title("Fast Convolution and Correlation")
    task9_window.configure(bg="black")

    signal1_path = tk.StringVar()
    signal2_path = tk.StringVar()

    path1_label = tk.Label(task9_window, text='First Signal Path:')
    path1_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
    path1_entry = tk.Entry(task9_window, textvariable=signal1_path)
    path1_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')
    browse_button_signal = ttk.Button(task9_window, text="Browse", command=lambda: browse_signal_file(path1_entry))
    browse_button_signal.grid(row=0, column=2, padx=10, pady=10, sticky='w')

    path2_label = tk.Label(task9_window, text='Second Signal Path:')
    path2_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
    path2_entry = tk.Entry(task9_window, textvariable=signal2_path)
    path2_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')
    browse_button_signal = ttk.Button(task9_window, text="Browse", command=lambda: browse_signal_file(path2_entry))
    browse_button_signal.grid(row=1, column=2, padx=10, pady=10, sticky='w')

    calc_button = tk.Button(task9_window, text='Fast Convolve', command=partial(fast_convolve, signal1_path, signal2_path),
                            activeforeground='red')
    calc_button.place(x=230, y=200)
    calc_button = tk.Button(task9_window, text='Fast Correlate', command=partial(fast_correlate, signal1_path, signal2_path),
                         activeforeground='red')
    calc_button.place(x=230, y=250)


def browse_signal_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)


# Function to close all windows except the main window
def close_windows():
    for window in win.winfo_children():
        if type(window) != ttk.Button:
            window.destroy()


# region GUI
win = tk.Tk()
win.geometry("500x400")
win.configure(bg="black")

# Create a style object for ttk widgets
style = ttk.Style()
style.configure("TButton", foreground="black", background="black", font=("Arial", 14, "bold"))
button1 = ttk.Button(win,
                     text='TASK 1',
                     command=task1_create_signal_window)
button1.grid(row=0, column=0, padx=70, pady=20)

# Create a button that opens Another Window
button2 = ttk.Button(win, text="TASK 2", command=task2_arithmatic_ops_window)
button2.grid(row=0, column=1, padx=10, pady=20)

# Create a button that opens Another Window
button3 = ttk.Button(win, text="TASK 3", command=task3_quantization_window)
button3.grid(row=1, column=0, padx=10, pady=20)

# Create a button that opens Another Window
button4 = ttk.Button(win, text="TASK 4&5", command=task4_5_fourier_window)
button4.grid(row=1, column=1, padx=10, pady=20)

# Create a button that opens Another Window
button6 = ttk.Button(win, text="TASK 6", command=task6_signal_operations_window)
button6.grid(row=2, column=0, padx=10, pady=20)


# Create a button that opens Another Window
button7 = ttk.Button(win, text="TASK 7", command=task7_convolution_window)
button7.grid(row=2, column=1, padx=10, pady=20)


# Create a button that opens Another Window
button8 = ttk.Button(win, text="TASK 8", command=task8_correlation_window)
button8.grid(row=3, column=0, padx=10, pady=20)


# Create a button that opens Another Window
button9 = ttk.Button(win, text="TASK 9", command=task9_fast_window)
button9.grid(row=3, column=1, padx=10, pady=20)

win.mainloop()
