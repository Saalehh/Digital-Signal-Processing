import tkinter as tk
from tkinter import messagebox


# creating the main window
root = tk.Tk()

# region setting the window size
root.geometry('500x700')
# setting the title
root.title("My GUI")
# endregion

# region creating a label
label = tk.Label(root, text="Hello World!", font=("Arial", 20))
label.pack(padx=10, pady=10)
# endregion

# region creating a textbox
textbox = tk.Text(root, height=3, font=("Arial", 16))
textbox.pack(padx=10, pady=10)
# getting the textbox value
textbox_value = textbox.get('1.0', tk.END)  # form the beginning of the text to its end
# endregion

# region creating a checkbox
# we should create a variable to store the state of the checkbox in it
check_state = tk.IntVar()  # integer value
check_box = tk.Checkbutton(root, text="Show Messagebox", font=("Arial", 15), variable=check_state)
check_box.pack(padx=10, pady=10)
# endregion

# region creating an entry, an entry is a textbox of one line
entry = tk.Entry(root, font=("Arial", 16))
entry.pack(padx=10, pady=10)
# endregion

# region creating a button
# creating the function that will be executed when we click the button
def click_me():
    print("clicked!")
button = tk.Button(root, text="Click Me!", command=click_me)
button.pack(padx=10, pady=10)
# endregion

# region creating buttons like calculator
button_frame = tk.Frame(root)
button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)
button_frame.columnconfigure(2, weight=1)

btn1 = tk.Button(button_frame, text="1", font=("Arial", 18))
btn1.grid(row=0, column=0, sticky=tk.W+tk.E)
# this time we used grid instead of pack, as we need to show these button in grid view,
# and we also specified its parent as the button_frame not the root, as these buttons will inside the frame we created

btn2 = tk.Button(button_frame, text="2", font=("Arial", 18))
btn2.grid(row=0, column=1, sticky=tk.W+tk.E)

btn3 = tk.Button(button_frame, text="3", font=("Arial", 18))
btn3.grid(row=0, column=2, sticky=tk.W+tk.E)

btn4 = tk.Button(button_frame, text="4", font=("Arial", 18))
btn4.grid(row=1, column=0, sticky=tk.W+tk.E)

btn5 = tk.Button(button_frame, text="5", font=("Arial", 18))
btn5.grid(row=1, column=1, sticky=tk.W+tk.E)

btn6 = tk.Button(button_frame, text="6", font=("Arial", 18))
btn6.grid(row=1, column=2, sticky=tk.W+tk.E)

button_frame.pack(fill=tk.X)  # fill= tk.X means to fill the X dimension
# endregion

# region placing our component in the exactly specified place
placed_btn = tk.Button(root, text="Placed using palce()", font=("Arial", 18))
placed_btn.place(x=120, y=400)
# endregion

# region events on closing the widow
def on_close():
    if messagebox.askyesno(title="Quit?", message="Are you sure you want to quit!"):
        root.destroy()
    else:
        pass
root.protocol("WM_DELETE_WINDOW", on_close)
# endregion


# showing the window
root.mainloop()

if __name__ == '__main__':
    x = [4]
    print(x)