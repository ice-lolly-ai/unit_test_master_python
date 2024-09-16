import tkinter as tk
from tkinter import ttk, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
import re
import ast
import subprocess
import io
import contextlib

def open_file(event=None):
    file_path = filedialog.askopenfilename(
        filetypes=[("Python Files", "*.py")])
    if file_path:
        display_file_content(file_path)
        # Remove the open file link after loading a file
        left_window.tag_delete("link")
        left_window.unbind("<Button-1>")

def display_file_content(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    
    # Clear the left window before displaying new content
    left_window.delete(1.0, tk.END)
    left_window.insert(tk.END, code)

    # Extract function calls and display them in the bottom window
    extract_function_calls(code)

    # Extract functions from the code
    functions = extract_functions_from_code(code)
    
    # Generate and display unit tests in the right window
    unit_tests = generate_unit_tests(functions)
    right_window.delete(1.0, tk.END)
    right_window.insert(tk.END, unit_tests)

    # Run the generated unit tests and display results in the bottom window
    run_and_display_tests(unit_tests)

def extract_function_calls(code):
    # Use regex to find function calls in the code
    function_calls = re.findall(r'\b\w+\(.*?\)', code)

    # Clear the bottom window before displaying new content
    bottom_window.delete(1.0, tk.END)
    if function_calls:
        bottom_window.insert(tk.END, "Function Calls:\n\n")
        for call in function_calls:
            bottom_window.insert(tk.END, f"{call}\n")
    else:
        bottom_window.insert(tk.END, "No function calls found.")

def extract_functions_from_code(code):
    """
    Extracts all function definitions from the provided Python code.
    """
    parsed_code = ast.parse(code)
    functions = [node for node in ast.walk(parsed_code) if isinstance(node, ast.FunctionDef)]
    return functions

def generate_unit_tests(functions):
    """
    Generates unit test code for the provided function definitions.
    """
    unit_tests = "import unittest\n\n"
    unit_tests += "class TestFunctions(unittest.TestCase):\n"
    
    for func in functions:
        func_name = func.name
        unit_tests += f"    def test_{func_name}(self):\n"
        unit_tests += f"        # TODO: Add tests for {func_name}\n"
        unit_tests += "        pass\n\n"
    
    unit_tests += "if __name__ == '__main__':\n"
    unit_tests += "    unittest.main()\n"
    
    return unit_tests

def run_and_display_tests(unit_tests):
    """
    Runs the given unit tests and displays the results in the bottom window.
    """
    # Save the generated unit tests to a temporary file
    test_file = "temp_tests.py"
    with open(test_file, 'w') as file:
        file.write(unit_tests)
    
    # Run the unit tests and capture the output
    with io.StringIO() as buf, contextlib.redirect_stdout(buf):
        try:
            result = subprocess.run(
                ['python', test_file],
                capture_output=True,
                text=True,
                check=True
            )
            output = buf.getvalue()
            test_result = result.stdout
            if result.returncode == 0:
                display_test_results("PASS\n" + test_result, "green")
            else:
                display_test_results("FAIL\n" + test_result, "red")
        except subprocess.CalledProcessError as e:
            output = buf.getvalue()
            display_test_results("FAIL\n" + e.output, "red")

def display_test_results(results, color):
    """
    Displays test results in the bottom window with coloring.
    """
    bottom_window.delete(1.0, tk.END)
    bottom_window.insert(tk.END, results)
    bottom_window.tag_configure("pass", foreground="green")
    bottom_window.tag_configure("fail", foreground="red")
    if color == "green":
        bottom_window.tag_add("pass", "1.0", "end")
    else:
        bottom_window.tag_add("fail", "1.0", "end")

def on_drop(event):
    file_path = event.data.strip().split('\n')[0]  # Get the first file path from the drop event
    if file_path.endswith(".py"):
        display_file_content(file_path)

def setup_drag_and_drop(widget):
    widget.drop_target_register(DND_FILES)
    widget.dnd_bind('<<Drop>>', on_drop)

# Initialize the main application window
root = TkinterDnD.Tk()
root.title("Python File Viewer")
root.geometry("800x600")  # Set a default window size
root.configure(bg='#121212')  # Set main window background to dark

# Create a frame for the buttons
button_frame = tk.Frame(root, bg='#121212')  # Dark background for the button frame
button_frame.pack(side=tk.TOP, pady=10)

# Create the three buttons and add them to the frame
buttons = []
for i in range(1, 4):
    button = ttk.Button(button_frame, text=f"Button {i}", command=lambda i=i: button_clicked(i))
    button.pack(side=tk.LEFT, padx=20)
    buttons.append(button)

# Create a frame for the left and right windows
main_frame = tk.Frame(root, bg='#121212')
main_frame.pack(fill=tk.BOTH, expand=True)

# Create left window (text widget) with drag-and-drop capability
left_window = tk.Text(main_frame, wrap=tk.WORD, bg='#000000', fg='#ffffff', font=('Courier', 12))
left_window.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Setup drag-and-drop functionality
setup_drag_and_drop(left_window)

# Create right window (text widget)
right_window = tk.Text(main_frame, wrap=tk.WORD, bg='#000000', fg='#ffffff', font=('Courier', 12))
right_window.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create a frame for the bottom window
bottom_frame = tk.Frame(root, bg='#121212')
bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# Create bottom window (text widget) for function calls and test results
bottom_window = tk.Text(bottom_frame, wrap=tk.WORD, bg='#000000', fg='#ffffff', font=('Courier', 12))
bottom_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Add a link to open file dialog in the left window
def add_open_link():
    left_window.insert(tk.END, "Click here to open a .py file\n")
    left_window.tag_add("link", "end-2c", "end-1c")
    left_window.tag_configure("link", foreground="blue", underline=True)
    left_window.bind("<Button-1>", open_file)  # Binding left mouse click to open_file

add_open_link()

# Function to handle button clicks
def button_clicked(button_num):
    print(f"Button {button_num} clicked")

# Run the application
root.mainloop()
