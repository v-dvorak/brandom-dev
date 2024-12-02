import random
import time
import tkinter as tk
from tkinter import messagebox, ttk

ROW_UPDATE_DELAY = 1000  # in ms
BOXES_PER_ROW = 10

generating_finished = True
grid_generated = False
generated_numbers: list[int] = []
row_index = 0
num_rows = 0
num_cols = 0


def generate_and_shuffle_numbers(upper_bound: int, save: bool = True):
    """
    Generates a list of numbers [1, given upper_bound] and returns it shuffled.
    The generated list is, by default, saved to a file named as the time at which it was generated.

    :param upper_bound: The upper bound of the generated list
    :param save: Whether to save the generated list to a file, default is True
    :return: Shuffled list of number [1, upper bound]
    """
    assert upper_bound > 0

    # generate a list [1, upper_bound]
    numbers = list(range(1, upper_bound + 1))
    # shuffle it
    random.shuffle(numbers)

    if save:
        current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"{current_time}.txt"
        with open(file_name, "w") as file:
            for number in numbers:
                file.write(f"{number}\n")

    return numbers


def create_single_box(row: int, col: int, grid_frame: tk.Frame) -> None:
    """
    Creates single frame, puts it into Tkinter grid frame grid.
    :param row: The row of the grid frame
    :param col: The column of the grid frame
    :param grid_frame: The tk grid frame
    """
    # create frame
    frame = tk.Frame(
        grid_frame,
        width=90,
        height=90,
        borderwidth=1,
        relief="solid",
    )
    frame.grid(row=row, column=col, padx=5, pady=5)

    # put text label inside the frame
    label = tk.Label(
        frame,
        text="",
        bg="white",
        fg="white",
        font=("Arial", 16),
        width=5,
        height=2,
    )
    label.pack(expand=True)


def validate_number_input(*args):
    """
    UTIL. Validates an input to ensure it's a non-negative integer.
    """
    value = part_entry_var.get()
    if not value.isdigit():
        participants_entry.configure(bg="red")
        return

    value = int(value)
    if value > 0:
        generate_button.config(state="normal")
        participants_entry.configure(bg="white")
    else:
        generate_button.config(state="disabled")
        participants_entry.configure(bg="red")


def generate_grid():
    global row_index, generating_finished, generate_button, grid_generated, num_rows, num_cols, generated_numbers

    # validate inputs
    try:
        num_participants = int(participants_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")
        return

    if not (num_participants > 0):
        messagebox.showerror("Input Error", "The first number must be between 41 and 120.")
        return

    # ask the user for confirmation on grid regeneration
    if grid_generated:
        response = messagebox.askyesno(
            "Regenerate Result",
            "Are you sure you want to regenerate the result? This will overwrite the current result."
        )
        if not response:
            return

    # lock inputs
    generate_button.config(state="disabled")
    participants_entry.configure(state="disabled")
    going_entry.configure(state="disabled")

    grid_generated = True

    # clear existing grid
    for widget in grid_frame.winfo_children():
        widget.destroy()
    # calculate grid dimensions
    num_rows = num_participants // BOXES_PER_ROW  # Calculate the number of rows (5 columns per row)
    last_row_num = num_participants % BOXES_PER_ROW

    # create a white empty grid
    for row in range(num_rows):
        for col in range(BOXES_PER_ROW):
            create_single_box(row, col, grid_frame)

    if last_row_num > 0:
        for col in range(last_row_num):
            create_single_box(num_rows, col, grid_frame)
        num_rows += 1

    # randomly generate numbers
    generated_numbers = generate_and_shuffle_numbers(num_participants)

    # start updating
    row_index = 0
    generating_finished = False
    root.after(ROW_UPDATE_DELAY, update_grid_row)


def update_grid_row() -> None:
    """
    Updates every box in a row based on generated numbers.
    """
    global row_index, generating_finished

    # if all rows are updated reset locks on inputs and return
    if row_index >= num_rows:
        generating_finished = True
        generate_button.config(state="normal")
        participants_entry.configure(state="normal")
        going_entry.configure(state="normal")
        return  # Stop once all rows are updated

    # retrieve values from input
    max_going = int(going_entry.get())
    num_participants = int(participants_entry.get())

    # for all boxes in row
    for col in range(BOXES_PER_ROW):
        # calculate box index in generated numbers
        box_index = col + BOXES_PER_ROW * row_index

        # last row can be truncated, check for it
        if box_index >= num_participants:
            break

        # get reference to box
        frame = grid_frame.grid_slaves(row=row_index, column=col)[0]
        label = frame.winfo_children()[0]

        # get random number at box index and set color accordingly
        box_num = generated_numbers[box_index]
        label.config(
            text=box_num,
            bg="red" if box_index >= max_going else "green",
            fg="white"
        )

    # advance
    row_index += 1
    root.after(ROW_UPDATE_DELAY, update_grid_row)


if __name__ == "__main__":
    # SETUP WINDOW
    root = tk.Tk()
    root.title("BRandom")

    # input frame
    input_frame = tk.Frame(root, padx=10, pady=10)
    input_frame.pack(side="left", fill="y")

    # number of participants
    tk.Label(input_frame, text="Number of participants:").pack(anchor="w")
    part_entry_var = tk.StringVar()
    part_entry_var.trace_add("write", validate_number_input)  # Trigger validation on changes
    participants_entry = tk.Entry(input_frame, textvariable=part_entry_var)
    participants_entry.pack(fill="x", pady=5)

    # number of participants going
    tk.Label(input_frame, text="Number of participants going:").pack(anchor="w")
    going_entry = ttk.Combobox(input_frame, values=[40, 80], state="readonly")
    going_entry.pack(fill="x", pady=5)
    going_entry.set(40)

    # button to generate numbers and visualize
    generate_button = tk.Button(input_frame, text="Generate", command=generate_grid)
    generate_button.pack(pady=10)

    # right frame for box grid
    grid_frame = tk.Frame(root, padx=10, pady=10)
    grid_frame.pack(side="right", expand=True, fill="both")

    # RUN WINDOW
    root.mainloop()
