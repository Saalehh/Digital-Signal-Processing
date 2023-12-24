import cmath
import os
from utils import *
from plotting import *
from task3_test_cases.QuanTest1 import QuantizationTest1
from task3_test_cases.QuanTest2 import QuantizationTest2
from task4_test_cases.signalcompare import *
from task1_test_cases.comparesignals import *
from task6_test_cases.comparesignals import signal_samples_are_equal
from task6_test_cases.Shifting_and_Folding.Shift_Fold_Signal import Shift_Fold_Signal
from task6_test_cases.Derivative_Updated.DerivativeSignal import DerivativeSignal
from task7_test_cases.ConvTest import ConvTest
from task8_test_cases.CompareSignal import Compare_Signals


#######################################################################################################################
#                                                   Task 1                                                            #
#######################################################################################################################

def get_discrete_signal_dimensions(amplitude, analog_freq, sampling_freq, phase_shift, signal_type):
    amplitude = int(amplitude.get())
    analog_freq = int(analog_freq.get())
    sampling_freq = int(sampling_freq.get())
    phase_shift = float(phase_shift.get())
    signal_type = signal_type.get()

    digital_freq = (analog_freq / sampling_freq)

    indexes = []
    values = []

    if signal_type == 'sin':
        for i in range(0, sampling_freq):
            indexes.append(i)
            values.append(amplitude * math.sin((2 * math.pi * digital_freq * i) + phase_shift))
    elif signal_type == 'cos':
        for i in range(0, sampling_freq):
            indexes.append(i)
            values.append(amplitude * math.cos((2 * math.pi * digital_freq * i) + phase_shift))

    return indexes, values


def generate_signals_plot(amplitude, analog_freq, sampling_freq, phase_shift, signal_type):
    discrete_x, discrete_y = get_discrete_signal_dimensions(amplitude, analog_freq, sampling_freq, phase_shift,
                                                            signal_type)
    # DRAWING SIGNALS #
    # Create a 1x2 grid of subplots and plot in the first one
    plt.subplot(1, 2, 1)
    plot_continuous(discrete_x, discrete_y)

    # Plot in the second subplot
    plt.subplot(1, 2, 2)
    plot_discrete(discrete_x, discrete_y)

    plt.tight_layout()  # Ensures that the plots don't overlap
    plt.show()


#######################################################################################################################
#                                                   Task 2                                                            #
#######################################################################################################################


def plot_resulted_signal(arith_op, x_sig1, y_sig1, x_sig2, y_sig2, x_res, y_res):
    if arith_op in ('Add', 'Sub'):
        plt.figure(figsize=(12, 6))

        # Create a 2x3 grid of subplots and plot in the first one
        plt.subplot(2, 3, 1)
        plot_continuous(x_sig1, y_sig1, title="Cont Signal 1")

        # Plot in the second subplot
        plt.subplot(2, 3, 2)
        plot_continuous(x_sig2, y_sig2, title="Cont Signal 2")

        # Plot in the third subplot
        plt.subplot(2, 3, 3)
        plot_continuous(x_res, y_res, title="Cont Resulted Signal")

        # Plot in the fourth subplot
        plt.subplot(2, 3, 4)
        plot_discrete(x_sig1, y_sig1, title="Discrete Signal 1")

        # Plot in the fifth subplot
        plt.subplot(2, 3, 5)
        plot_discrete(x_sig2, y_sig2, title="Discrete Signal 2")

        # Plot in the sixths subplot
        plt.subplot(2, 3, 6)
        plot_discrete(x_res, y_res, title="Discrete Resulted Signal")

        plt.tight_layout()  # Ensures that the plots don't overlap
        plt.show()
    elif arith_op in ('Norm', 'ShiftByConst', 'MulByConst', 'Square'):
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


def perform_operation(arith_op, sig1_path, sig2_path, const, a, b):
    arith_op = arith_op.get()
    sig1_path = sig1_path.get()
    sig2_path = sig2_path.get()
    signal1 = read_samples(sig1_path)
    x_sig1, y_sig1 = signal1.x, signal1.y
    x_sig2, y_sig2 = [], []

    if arith_op in ('Add', 'Sub'):
        signal2 = read_samples(sig2_path)
        x_sig2, y_sig2 = signal2.x, signal2.y

        # Check if the signals samples count are different
        len_signal_1 = len(x_sig1)
        len_signal_2 = len(x_sig2)
        if len_signal_1 > len_signal_2:
            #  make the indexes of the resulted signal to have the greater value
            x_res = x_sig1
            # pad the short signal wit zeroes
            y_sig2.extend([0] * (len_signal_1 - len_signal_2))
        else:
            x_res = x_sig2
            y_sig1.extend([0] * (len_signal_2 - len_signal_1))

        if arith_op == 'Add':
            y_res = [x + y for x, y in zip(y_sig1, y_sig2)]
        elif arith_op == 'Sub':
            y_res = [x - y if x > y else y - x for x, y in zip(y_sig1, y_sig2)]

    elif arith_op in ('MulByConst', 'ShiftByConst'):
        x_res = x_sig1
        const = int(const.get())
        if arith_op == 'MulByConst':
            y_res = [y * const for y in y_sig1]
        else:
            x_res = [x - const for x in x_sig1]

    elif arith_op == 'Square':
        x_res = x_sig1
        y_res = [y ** 2 for y in y_sig1]

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

    plot_resulted_signal(arith_op, x_sig1, y_sig1, x_sig2, y_sig2, x_res, y_res)


#######################################################################################################################
#                                                   Task 3                                                            #
#######################################################################################################################
def generate_quantized_signal_plot(input_type, levels, bits, test, input_signal):
    input_signal = input_signal.get()
    input_type = input_type.get()
    test = test.get()

    if input_type == '2':
        bits = int(bits.get())
        levels = int(math.pow(2, bits))
    else:
        levels = int(levels.get())
        bits = int(math.log(levels, 2))

    signal = read_samples(input_signal)
    x, y = signal.x, signal.y

    # Find min & max
    mini = min(y)
    maxi = max(y)

    # Find delta
    delta = (maxi - mini) / levels

    # Ranges & Midpoints
    ranges = []
    midpoints = []
    last = mini
    for i in range(levels):
        if i > 0:
            last = ranges[i - 1][1]
        ranges.append([last, round(last + delta, 4)])
        midpoints.append(round((last + last + delta) / 2, 4))

    # Intervals
    interval_index = []
    for i in range(len(x)):
        for j in range(len(ranges)):
            if ranges[j][0] <= y[i] <= ranges[j][1]:
                interval_index.append(j + 1)
                break

    # Quantization
    quantized_values = []
    error = []
    avg_error = 0
    for i in range(len(interval_index)):
        quantized_values.append(midpoints[interval_index[i] - 1])
        error.append(round(midpoints[interval_index[i] - 1] - y[i], 4))
        avg_error += (error[-1] * error[-1])
    avg_error = avg_error / len(x)
    print('Quantized values:', quantized_values)
    print('Quantization Error:', error)
    print('Average Power Error:', avg_error)
    plot_continuous_and_discrete(x, quantized_values)

    # Encoding
    encoded_values = []
    for i in interval_index:
        encoded_values.append(bin(i - 1)[2:].zfill(bits))  # Remove 0b prefix and put leading zeros
    print('Encoded Signal', encoded_values)
    plot_continuous_and_discrete(x, interval_index)

    if test == '1':
        QuantizationTest1('task3_test_cases/task3_test1/Quan1_Out.txt', encoded_values, quantized_values)
    else:
        QuantizationTest2('task3_test_cases/task3_test2/Quan2_Out.txt', interval_index, encoded_values,
                          quantized_values, error)


#######################################################################################################################
#                                                   Task 4                                                            #
#######################################################################################################################

def dft(signal):
    """
    This function takes a sampled signal x(n) and coverts it to the frequency domain by returning x(k) that is
     a complex number of real and imaginary parts e.g. a + bj
        - The magnitude/amplitude of the signal can be constructed by : A = sqrt(a^2 + b^2)
        - The phase of the signal can be constructed by: ⌀ = tan^-1(b / a).
    """
    index, x = signal.x, signal.y
    N = len(x)
    x_k = []

    for k in range(N):
        summation = 0
        for n in range(N):
            exp_term = cmath.exp(-1j * (2 * cmath.pi * k * n / N))
            term = x[n] * exp_term
            summation += term
        real_part = summation.real
        imaginary_part = summation.imag
        x_k.append(complex(real_part, imaginary_part))
    return x_k


def idft(x):
    """
    This function takes a sampled signal in the frequency domain and compute the idft for this signal to return it back
    to the spatial/time domain.
    """
    indexes = []
    x_n = []
    N = len(x)

    for n in range(N):
        summation = 0
        indexes.append(n)
        for k in range(N):
            exp_term = cmath.exp(1j * (2 * cmath.pi * n * k / N))
            term = x[k] * exp_term
            summation += term
        result = round(summation.real, 4) / N
        x_n.append(result)
    return indexes, x_n


def get_amp_phase(dft_set):
    """
    This function takes the frequency domain components and calculates the amplitude and phase for each component
    """

    print("dft_set: ", dft_set)
    amps = []
    phases = []
    for k in range(len(dft_set)):
        amps.append(round(math.sqrt((dft_set[k].real ** 2) + (dft_set[k].imag ** 2)), 13))
        phases.append(math.degrees(math.atan(dft_set[k].imag / dft_set[k].real)))
    # phases = np.angle(dft_set)

    return amps, phases


def create_signal_file(amps, phases):
    """
    This function takes two lists of amplitudes and phases and write down then into a file as a signal
    """

    # Specify the directory and file name
    directory = "task4_test_cases/task_4_saved_signals"
    file_name = "created_signal.txt"

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create the file within the directory and open it in write mode
    file_path = os.path.join(directory, file_name)
    radians = [math.radians(phase) for phase in phases]
    N = len(amps)
    try:
        with open(file_path, "w") as file:
            file.write("0\n")
            file.write("1\n")
            file.write(f"{N}\n")
            for i in range(N):
                file.write(f"{amps[i]} {radians[i]}\n")
    except FileNotFoundError:
        print("File not found!")


def sketch_dft(amps, phases, Fs):
    """
    This function takes two lists of amplitudes and phases and the sampling frequency then plots the relations between
        - Frequency vs Amplitude
        - Frequency vs Phase
    """

    # Sketching the frequency versus amplitude
    N = len(amps)
    omega = (2 * cmath.pi * Fs) / N
    x = [i * omega for i in range(1, N + 1)]

    plt.subplot(1, 2, 1)
    plot_discrete(x, amps, title='Frequency vs Amplitude')
    # Sketching the frequency versus phase
    plt.subplot(1, 2, 2)
    plot_discrete(x, phases, title='Frequency vs Phase')
    plt.tight_layout()
    plt.show()


def calculate_x_k(amps, phases):
    """
    This function takes two lists of amplitudes and phases that are representing a sampled signal
     and calculates and returns the complex version of them
    """

    x_k = []
    for amp, phase in zip(amps, phases):
        real_part = amp * math.cos(phase)
        imaginary_part = amp * math.sin(phase)
        x_k.append(complex(real_part, imaginary_part))
    return x_k


def calc_idft(amps_phases_file):
    """
    This function takes a sampled signal in the form of amplitudes and phases and compute the idft for this signal.
    """
    samples = read_samples(amps_phases_file)
    amps, phases = samples.x, samples.y
    x = calculate_x_k(amps, phases)

    indexes, x_n = idft(x)
    return indexes, x_n


#######################################################################################################################
#                                                   Task 5                                                            #
#######################################################################################################################
def dct(signal_path, save_n_lines):
    signal_path = signal_path.get()
    save_n_lines = int(save_n_lines.get())
    samples = read_samples(signal_path)
    x, y = samples.x, samples.y
    complex_list = []
    N = len(y)
    for k in range(N):
        Yk = 0
        for n in range(N):
            Yk += y[n] * math.cos((math.pi / (4 * N)) * ((2 * n) - 1) * (2 * k - 1))
        Yk *= np.sqrt(2 / N)
        complex_list.append(Yk)
    x = [0] * N
    SignalSamplesAreEqual('task5_test_cases/DCT/DCT_output.txt', x, complex_list)
    save_task5_to_txt('saved_dct.txt', x, complex_list, save_n_lines)


def remove_dc(signal_path):
    signal_path = signal_path.get()
    samples = read_samples(signal_path)
    X, Y = samples.x, samples.y

    mean = np.mean(Y)
    new_y = [round(y - mean, 3) for y in Y]
    SignalSamplesAreEqual('task5_test_cases/Remove DC component/DC_component_output.txt', X, new_y)


def save_task5_to_txt(filename, amplitude, phase, m):
    with open(filename, 'w') as file:
        file.write(f"{0}\n")
        file.write(f"{1}\n")
        file.write(f"{len(amplitude)}\n")
        for i, (amp, pha) in enumerate(zip(amplitude, phase)):
            if i < m:
                file.write(f"{amp:.0f},{pha:.14f}\n")


#######################################################################################################################
#                                                   Task 6                                                            #
#######################################################################################################################

def calc_operation(menu_op, signal_path, window_size, kSteps, isShiftFold):
    op = menu_op.get()
    signal_path = signal_path.get()

    if op == 'Smoothing':
        window_size = int(window_size.get())
        smooth(signal_path, window_size)
    elif op == 'Sharpening':
        sharpen(signal_path)
    elif op == 'Shifting':
        kSteps = int(kSteps.get())
        x, y = read_samples(signal_path)
        shift(x, y, kSteps)
    elif op == 'Folding':
        isShiftFold = isShiftFold.get()
        fold(signal_path, isShiftFold, kSteps)
    elif op == 'Remove DC':
        remove_dc_using_idft(signal_path)


def smooth(signal_path, window_size):
    """
    Reduces Signal Noise
    """
    x, y = read_samples(signal_path)
    x = []
    mov_avg = []
    for i in range(len(y)):
        avg = 0
        if i <= len(y) - window_size:
            for j in range(0, window_size):
                avg += y[i + j]
            x.append(i)
            mov_avg.append(avg / window_size)
    print('********** Moving Average Test 1 **********')  # window_size = 3 task6_test_cases/Moving Average/Signal1.txt
    signal_samples_are_equal('task6_test_cases/Moving Average/OutMovAvgTest1.txt', x, mov_avg)
    print('********** Moving Average Test 2 **********')  # window_size = 5 task6_test_cases/Moving Average/Signal2.txt
    signal_samples_are_equal('task6_test_cases/Moving Average/OutMovAvgTest2.txt', x, mov_avg)
    print('')


def sharpen(signal_path):
    DerivativeSignal()
    x, y = read_samples(signal_path)
    plot_discrete(x, y, title='Before Sharpening')
    plt.show()

    x = []
    new_y = []
    for i in range(1, len(y)):
        x.append(len(new_y))
        new_y.append(y[i] - y[i - 1])
    plot_discrete(x, new_y, title='After 1st Derivative Sharpening')
    plt.show()

    x = []
    new_y = []
    for i in range(1, len(y) - 1):
        x.append(len(new_y))
        new_y.append(y[i - 1] + y[i + 1] - 2 * y[i])
    plot_discrete(x, new_y, title='After 2nd Derivative Sharpening')
    plt.show()


def shift(x, y, kSteps):
    for i in range(len(x)):
        x[i] += kSteps
    # task6_test_cases/Shifting_and_Folding/Output_fold.txt
    Shift_Fold_Signal('task6_test_cases/Shifting_and_Folding/Output_ShifFoldedby500.txt', x, y)
    print('')
    Shift_Fold_Signal('task6_test_cases/Shifting_and_Folding/Output_ShiftFoldedby-500.txt', x, y)


def fold(signal_path, is_shift_fold, k_steps):
    signal = read_samples(signal_path)
    X, Y, type, is_periodic = signal.x, signal.y, signal.type, signal.is_periodic
    new_x = [-x for x in X]
    folded_signal = Signal(type=type, is_periodic=is_periodic, x=new_x[::-1], y=Y[::-1])
    Shift_Fold_Signal('task6_test_cases/Shifting_and_Folding/Output_fold.txt', folded_signal.x, folded_signal.y)
    if is_shift_fold == 1:
        k_steps = int(k_steps.get())
        shift(folded_signal.x, folded_signal.y, k_steps)


def remove_dc_using_idft(signal_path):
    signal = read_samples(signal_path)
    x = dft(signal)
    x[0] = complex(0, 0)
    indexes, x_n = idft(x)
    signal_samples_are_equal(r'task5_test_cases\Remove DC component\DC_component_output.txt', indexes, x_n)
    return x_n


#######################################################################################################################
#                                                   Task 7                                                            #
#######################################################################################################################


def convolve(signal1_path, signal2_path):
    signal_1 = read_samples(signal1_path.get())
    signal_2 = read_samples(signal2_path.get())
    x1, y1 = signal_1.x, signal_1.y
    x2, y2 = signal_2.x, signal_2.y
    new_x = []
    new_y = []
    new_x0 = min(x1[0], x2[0])
    for I in range(0, len(x1) + len(x2) - 1):
        summation = 0
        i = I
        j = 0
        for J in range(0, I + 1):
            if len(y1) > i >= 0 and 0 <= j < len(y2):
                summation += (y1[i] * y2[j])
            i -= 1
            j += 1
        new_x.append(new_x0)
        new_y.append(summation)
        new_x0 += 1

    ConvTest(new_x, new_y)


#######################################################################################################################
#                                                   Task 8                                                            #
#######################################################################################################################
def correlate(signal1_path, signal2_path):
    signal1 = read_samples(signal1_path.get())
    signal2 = read_samples(signal2_path.get())

    X1, Y1 = signal1.x, signal1.y
    X2, Y2 = signal2.x, signal2.y
    N = len(Y2)
    r12 = []
    y_normalized = []

    for i in range(N):
        y1xy2 = [y1 * y2 for y1, y2 in zip(Y1, Y2)]
        summation = sum(y1xy2)
        r12.append(summation / N)

        # Shift Y2 for the next iteration
        shifted_Y2 = Y2[1:]
        shifted_Y2.append(Y2[0])
        Y2 = shifted_Y2
        y_normalized.append(r12[i] / ((1 / N) * math.sqrt(sum(x ** 2 for x in Y1) * sum(x ** 2 for x in Y2))))
    print(r12)
    print(y_normalized)

    Compare_Signals('task8_test_cases/Corr_Output.txt', X1, y_normalized)


#######################################################################################################################
#                                                   Task 9                                                            #
#######################################################################################################################
def fast_convolve(signal1_path, signal2_path):
    signal_1 = read_samples(signal1_path.get())
    signal_2 = read_samples(signal2_path.get())

    x1, y1 = signal_1.x, signal_1.y
    x2, y2 = signal_2.x, signal_2.y

    n = len(y1) + len(y2) - 1
    y1 = np.pad(y1, (0, n - len(y1)))
    y2 = np.pad(y2, (0, n - len(y2)))

    signal_1.y = y1
    signal_2.y = y2

    x_k1 = dft(signal_1)
    x_k2 = dft(signal_2)

    # Element-wise multiplication
    result = [a * b for a, b in zip(x_k1, x_k2)]

    indexes, x_n = idft(result)

    indexes[0] = min(signal_1.x[0], signal_2.x[0])
    indexes[1:] = [indexes[0] + i for i in range(1, n)]
    ConvTest(indexes, x_n)
    return indexes, x_n


def fast_correlate(signal1_path, signal2_path):
    signal_1 = read_samples(signal1_path.get())
    signal_2 = read_samples(signal2_path.get())

    x1, y1 = signal_1.x, signal_1.y
    x2, y2 = signal_2.x, signal_2.y

    n = len(y1) + len(y2) - 1
    maximum_length = max(len(y1), len(y2))
    y1 = np.pad(y1, (0, maximum_length - len(y1)))
    y2 = np.pad(y2, (0, maximum_length - len(y2)))

    signal_1.y = y1
    signal_2.y = y2

    # for i in range(maximum_length):
    x_k1 = dft(signal_1)
    x_k2 = dft(signal_2)

    # Element-wise multiplication
    result = [np.conj(a) * b for a, b in zip(x_k1, x_k2)]

    indexes, x_n = idft(result)
    x_n = [a / maximum_length for a in x_n]

    indexes[0] = min(signal_1.x[0], signal_2.x[0])
    indexes[1:] = [indexes[0] + i for i in range(1, maximum_length)]
    Compare_Signals('task8_test_cases/Corr_Output.txt', indexes, x_n)
    return indexes, x_n
