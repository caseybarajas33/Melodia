import tkinter as tk
from tkinter import filedialog, messagebox
from ttkbootstrap import Style
from ttkbootstrap import ttk  # Import ttk from ttkbootstrap
from ttkbootstrap.constants import *

class MelodiaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Melodia")
        self.root.geometry("1024x768")
        
        # Configure modern styles
        self.style = Style(theme='superhero')  # Use a modern-looking theme
        
        # Main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        
        # Header
        header_frame = ttk.Frame(self.main_container)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        ttk.Label(header_frame, 
             text="Melodia",
             font=('Helvetica', 24, 'bold'),
             style='primary.TLabel').grid(row=0, column=0, sticky="w")
        ttk.Label(header_frame,
             text="Machine Learning Music Generation",
             font=('Helvetica', 16),
             style='secondary.TLabel').grid(row=1, column=0, sticky="w")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.grid(row=1, column=0, sticky="nsew")
        
        # Create and setup tabs
        self.setup_training_tab()
        self.setup_generation_tab()
        
        # Configure weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_container.columnconfigure(0, weight=1)
        self.main_container.rowconfigure(1, weight=1)
    
    def setup_training_tab(self):
        """Set up the training tab"""
        self.training_tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(self.training_tab, text="Training")
        
        # Data section
        data_frame = ttk.LabelFrame(self.training_tab,
                                  text="Training Data",
                                  style='info.TLabelframe',
                                  padding=(20, 10))
        data_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 20))
        
        ttk.Label(data_frame, text="Dataset Directory:").grid(row=0, column=0, sticky="w")
        self.data_dir_var = tk.StringVar()
        ttk.Entry(data_frame, textvariable=self.data_dir_var).grid(row=0, column=1, sticky="ew", padx=10)
        ttk.Button(data_frame, text="Browse", command=self.browse_data_dir).grid(row=0, column=2)
        
        # Parameters section
        param_frame = ttk.LabelFrame(self.training_tab,
                                   text="Training Parameters",
                                   style='info.TLabelframe',
                                   padding=(20, 10))
        param_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        
        # Grid for parameters
        params = [
            ("Batch Size:", "batch_size", "32"),
            ("Epochs:", "epochs", "100"),
            ("Learning Rate:", "learning_rate", "0.001"),
            ("Validation Split:", "val_split", "0.1")
        ]
        
        for i, (label, var_name, default) in enumerate(params):
            ttk.Label(param_frame, text=label).grid(row=i, column=0, sticky="w", pady=5)
            setattr(self, var_name, tk.StringVar(value=default))
            ttk.Entry(param_frame,
                     textvariable=getattr(self, var_name),
                     width=15).grid(row=i, column=1, sticky="w", padx=10, pady=5)
        
        # Training control section
        control_frame = ttk.Frame(self.training_tab)
        control_frame.grid(row=2, column=0, sticky="ew", pady=20)
        
        self.train_button = ttk.Button(control_frame,
                                     text="Start Training",
                                     style='success.TButton',
                                     command=self.start_training)
        self.train_button.pack(pady=10)
        
        # Configure weights
        self.training_tab.columnconfigure(0, weight=1)
        data_frame.columnconfigure(1, weight=1)
        param_frame.columnconfigure(1, weight=1)
    
    def setup_generation_tab(self):
        """Set up the generation tab"""
        self.generation_tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(self.generation_tab, text="Generation")
        
        # Model section
        model_frame = ttk.LabelFrame(self.generation_tab,
                                   text="Model Selection",
                                   style='info.TLabelframe',
                                   padding=(20, 10))
        model_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 20))
        
        ttk.Label(model_frame, text="Model Path:").grid(row=0, column=0, sticky="w")
        self.model_path_var = tk.StringVar()
        ttk.Entry(model_frame, textvariable=self.model_path_var).grid(row=0, column=1, sticky="ew", padx=10)
        ttk.Button(model_frame, text="Browse", command=self.browse_model).grid(row=0, column=2)
        
        # Generation parameters
        gen_frame = ttk.LabelFrame(self.generation_tab,
                                 text="Generation Settings",
                                 style='info.TLabelframe',
                                 padding=(20, 10))
        gen_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        
        # Parameters grid
        params = [
            ("Number of Samples:", "num_samples", "1"),
            ("Temperature:", "temperature", "1.0")
        ]
        
        for i, (label, var_name, default) in enumerate(params):
            ttk.Label(gen_frame, text=label).grid(row=i, column=0, sticky="w", pady=5)
            setattr(self, var_name, tk.StringVar(value=default))
            ttk.Entry(gen_frame,
                     textvariable=getattr(self, var_name),
                     width=15).grid(row=i, column=1, sticky="w", padx=10, pady=5)
        
        # Style selection
        ttk.Label(gen_frame, text="Style:").grid(row=2, column=0, sticky="w", pady=5)
        self.style_var = tk.StringVar()
        style_combo = ttk.Combobox(gen_frame,
                                 textvariable=self.style_var,
                                 values=['Classical', 'Jazz', 'Folk', 'Blues'],
                                 width=20)
        style_combo.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        
        # Generation control
        control_frame = ttk.Frame(self.generation_tab)
        control_frame.grid(row=2, column=0, sticky="ew", pady=20)
        
        self.generate_button = ttk.Button(control_frame,
                                        text="Generate Music",
                                        style='success.TButton',
                                        command=self.generate_music)
        self.generate_button.pack(pady=10)
        
        # Configure weights
        self.generation_tab.columnconfigure(0, weight=1)
        model_frame.columnconfigure(1, weight=1)
        gen_frame.columnconfigure(1, weight=1)
    
    def browse_data_dir(self):
        directory = filedialog.askdirectory(title="Select Training Data Directory")
        if directory:
            self.data_dir_var.set(directory)
    
    def browse_model(self):
        file_path = filedialog.askopenfilename(
            title="Select Model File",
            filetypes=[("Model files", "*.h5;*.keras")]
        )
        if file_path:
            self.model_path_var.set(file_path)
    
    def start_training(self):
        if not self.data_dir_var.get():
            messagebox.showerror("Error", "Please select a training data directory")
            return
        
        try:
            batch_size = int(self.batch_size.get())
            epochs = int(self.epochs.get())
            lr = float(self.learning_rate.get())
            val_split = float(self.val_split.get())
            
            if batch_size <= 0 or epochs <= 0 or lr <= 0 or val_split <= 0:
                raise ValueError
            
        except ValueError:
            messagebox.showerror("Error", "Invalid training parameters")
            return
        
        messagebox.showinfo("Training", "Training started! (Placeholder)")
    
    def generate_music(self):
        if not self.model_path_var.get():
            messagebox.showerror("Error", "Please select a model file")
            return
        
        try:
            num_samples = int(self.num_samples.get())
            temperature = float(self.temperature.get())
            
            if num_samples <= 0 or temperature <= 0:
                raise ValueError
                
        except ValueError:
            messagebox.showerror("Error", "Invalid generation parameters")
            return
        
        messagebox.showinfo("Generation", "Generation started! (Placeholder)")

def main():
    root = tk.Tk()
    app = MelodiaGUI(root)
    
    # Center window on screen
    window_width = 1024
    window_height = 768
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()