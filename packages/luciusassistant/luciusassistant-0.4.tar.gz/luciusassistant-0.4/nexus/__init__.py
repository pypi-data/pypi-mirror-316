import tkinter as tk

def on_button_click(button_name):
    print(f"{button_name} button clicked")

def main():
    root = tk.Tk()
    root.title("Nexus Application")
    root.geometry("800x800")

    # Configure root window grid
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Text area at the top - switched to grid and made expandable
    text_area = tk.Text(root)
    text_area.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # Toolbar at the bottom - switched to grid
    toolbar = tk.Frame(root)
    toolbar.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

    # Adding 4 buttons to the toolbar
    button_names = ["Button 1", "Button 2", "Button 3", "Button 4"]
    for name in button_names:
        button = tk.Button(toolbar, text=name, command=lambda n=name: on_button_click(n))
        button.pack(side=tk.LEFT, padx=5)

    root.mainloop()

if __name__ == "__main__":
    main()