import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext
from PIL import Image, ImageTk
import os
import threading
import webbrowser
from google import genai
from google.genai import types
from io import BytesIO

class GeminiImageGeneratorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gemini Image Generator")
        self.root.geometry("1000x850")  # Increased height for better visibility
        self.root.configure(bg="#f0f0f0")
        
        # Variables
        self.input_image_path = ""
        self.output_image_path = ""
        self.api_key = tk.StringVar(value="")
        self.language = tk.StringVar(value="en")  # Default language: English
        self.status = tk.StringVar(value="Ready")
        
        # Multilingual dictionary
        self.translations = {
            "en": {
                "title": "Gemini Image Generator",
                "api_config": "API Configuration",
                "api_key": "API Key:",
                "get_api_key": "Get API Key",
                "images": "Images",
                "input_image": "Input Image:",
                "no_input": "No image selected",
                "select_image": "Select Image",
                "generated_image": "Generated Image:",
                "no_output": "No image generated",
                "save_image": "Save Image",
                "prompt": "Prompt",
                "colorization": "Colorize",
                "add_objects": "Add Objects",
                "change_background": "Change Background",
                "artistic_effect": "Artistic Effect",
                "ready": "Ready",
                "generating": "Generating...",
                "completed": "Completed",
                "error": "Error",
                "select_first": "Select an input image first",
                "no_image_save": "No generated image to save",
                "image_saved": "Image saved: ",
                "generation_complete": "Image generation completed successfully",
                "generation_failed": "Image generation failed",
                "colorize_prompt": "Colorize this image while maintaining exactly the original structure, details, and proportions. Do not alter faces, objects, or other elements of the image. Apply realistic and natural colors that match the original scene.",
                "objects_prompt": "Maintain exactly the structure and original colors of the image, but add a vase of flowers on the table. Make sure the added object integrates naturally with the existing image, respecting perspective and lighting.",
                "background_prompt": "Change the background of the image to a mountain landscape while keeping the main subject exactly as it appears in the original image. Make sure the lighting and shadows on the subject are consistent with the new background.",
                "artistic_prompt": "Transform this image by applying an impressionist artistic style. Keep the main subjects recognizable but apply visible brushstrokes and vibrant colors typical of impressionist style.",
                "log": "Log",
                "model_response": "Model response: ",
                "about": "About",
                "language": "Language:",
                "generate_image": "Generate Image",
                "refresh": "Refresh"
            },
            "it": {
                "title": "Generatore di Immagini Gemini",
                "api_config": "Configurazione API",
                "api_key": "API Key:",
                "get_api_key": "Ottieni API Key",
                "images": "Immagini",
                "input_image": "Immagine di Input:",
                "no_input": "Nessuna immagine selezionata",
                "select_image": "Seleziona Immagine",
                "generated_image": "Immagine Generata:",
                "no_output": "Nessuna immagine generata",
                "save_image": "Salva Immagine",
                "prompt": "Prompt",
                "colorization": "Colorazione",
                "add_objects": "Aggiungi Oggetti",
                "change_background": "Cambia Sfondo",
                "artistic_effect": "Effetto Artistico",
                "ready": "Pronto",
                "generating": "Generazione in corso...",
                "completed": "Completato",
                "error": "Errore",
                "select_first": "Seleziona prima un'immagine di input",
                "no_image_save": "Nessuna immagine generata da salvare",
                "image_saved": "Immagine salvata: ",
                "generation_complete": "Generazione dell'immagine completata con successo",
                "generation_failed": "Generazione dell'immagine fallita",
                "colorize_prompt": "Colora questa immagine mantenendo esattamente la struttura, i dettagli e le proporzioni originali. Non alterare i volti, gli oggetti o altri elementi dell'immagine. Applica colori realistici e naturali che corrispondano alla scena originale.",
                "objects_prompt": "Mantieni esattamente la struttura e i colori originali dell'immagine, ma aggiungi un vaso di fiori sul tavolo. Assicurati che l'oggetto aggiunto si integri naturalmente con l'immagine esistente, rispettando la prospettiva e l'illuminazione.",
                "background_prompt": "Cambia lo sfondo dell'immagine con un paesaggio montano mantenendo il soggetto principale esattamente come appare nell'immagine originale. Assicurati che l'illuminazione e le ombre sul soggetto siano coerenti con il nuovo sfondo.",
                "artistic_prompt": "Trasforma questa immagine applicando uno stile artistico impressionista. Mantieni riconoscibili i soggetti principali ma applica pennellate visibili e colori vivaci tipici dello stile impressionista.",
                "log": "Log",
                "model_response": "Risposta del modello: ",
                "about": "Informazioni",
                "language": "Lingua:",
                "generate_image": "Genera Immagine",
                "refresh": "Aggiorna"
            }
        }
        
        # Setup widgets
        self.create_widgets()
        self.update_language()
        
    def create_widgets(self):
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 10))
        style.configure('TLabel', font=('Helvetica', 10))
        style.configure('TLabelframe.Label', font=('Helvetica', 10, 'bold'))
        
        # Main menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Language menu
        language_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Language", menu=language_menu)
        language_menu.add_radiobutton(label="English", variable=self.language, value="en", command=self.update_language)
        language_menu.add_radiobutton(label="Italiano", variable=self.language, value="it", command=self.update_language)
        
        # About menu
        about_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="About", menu=about_menu)
        about_menu.add_command(label="About", command=self.show_about)
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # API Key frame
        self.api_frame = ttk.LabelFrame(main_frame, text="API Configuration", padding=10)
        self.api_frame.pack(fill=tk.X, pady=5)
        
        api_key_frame = ttk.Frame(self.api_frame)
        api_key_frame.pack(fill=tk.X)
        
        self.api_label = ttk.Label(api_key_frame, text="API Key:")
        self.api_label.pack(side=tk.LEFT, padx=5)
        ttk.Entry(api_key_frame, textvariable=self.api_key, width=50).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # Add Get API Key button
        self.get_api_btn = ttk.Button(api_key_frame, text="Get API Key", command=self.open_api_key_page)
        self.get_api_btn.pack(side=tk.RIGHT, padx=5)
        
        # Image selection and display frame
        self.image_frame = ttk.LabelFrame(main_frame, text="Images", padding=10)
        self.image_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create a frame for both image displays
        image_displays_frame = ttk.Frame(self.image_frame)
        image_displays_frame.pack(fill=tk.BOTH, expand=True)
        image_displays_frame.columnconfigure(0, weight=1)
        image_displays_frame.columnconfigure(1, weight=1)
        
        # Left side: input image
        input_frame = ttk.Frame(image_displays_frame)
        input_frame.grid(row=0, column=0, padx=10, sticky=tk.NSEW)
        
        self.input_label = ttk.Label(input_frame, text="Input Image:")
        self.input_label.pack(anchor=tk.W)
        
        # Use tk.Frame with white background for image display
        self.input_image_frame = tk.Frame(input_frame, width=400, height=350, bd=1, relief=tk.SOLID, bg="white")
        self.input_image_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.input_image_frame.pack_propagate(False)  # Prevent the frame from shrinking
        
        self.input_image_label = tk.Label(self.input_image_frame, text="No image selected", bg="white")
        self.input_image_label.pack(fill=tk.BOTH, expand=True)
        
        self.select_btn = ttk.Button(input_frame, text="Select Image", command=self.select_input_image)
        self.select_btn.pack(fill=tk.X, pady=5)
        
        # Right side: output image
        output_frame = ttk.Frame(image_displays_frame)
        output_frame.grid(row=0, column=1, padx=10, sticky=tk.NSEW)
        
        self.output_label = ttk.Label(output_frame, text="Generated Image:")
        self.output_label.pack(anchor=tk.W)
        
        # Use tk.Frame with white background for image display
        self.output_image_frame = tk.Frame(output_frame, width=400, height=350, bd=1, relief=tk.SOLID, bg="white")
        self.output_image_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.output_image_frame.pack_propagate(False)  # Prevent the frame from shrinking
        
        self.output_image_label = tk.Label(self.output_image_frame, text="No image generated", bg="white")
        self.output_image_label.pack(fill=tk.BOTH, expand=True)
        
        self.save_btn = ttk.Button(output_frame, text="Save Image", command=self.save_output_image)
        self.save_btn.pack(fill=tk.X, pady=5)
        
        # Prompt frame
        self.prompt_frame = ttk.LabelFrame(main_frame, text="Prompt", padding=10)
        self.prompt_frame.pack(fill=tk.X, pady=5)
        
        self.prompt_text = scrolledtext.ScrolledText(self.prompt_frame, wrap=tk.WORD, height=5, font=('Helvetica', 10))
        self.prompt_text.pack(fill=tk.X, expand=True)
        
        # Preset prompt buttons
        preset_frame = ttk.Frame(self.prompt_frame)
        preset_frame.pack(fill=tk.X, pady=5)
        
        self.colorize_btn = ttk.Button(preset_frame, text="Colorize", command=lambda: self.set_preset_prompt("colorize"))
        self.colorize_btn.pack(side=tk.LEFT, padx=5)
        
        self.objects_btn = ttk.Button(preset_frame, text="Add Objects", command=lambda: self.set_preset_prompt("objects"))
        self.objects_btn.pack(side=tk.LEFT, padx=5)
        
        self.background_btn = ttk.Button(preset_frame, text="Change Background", command=lambda: self.set_preset_prompt("background"))
        self.background_btn.pack(side=tk.LEFT, padx=5)
        
        self.artistic_btn = ttk.Button(preset_frame, text="Artistic Effect", command=lambda: self.set_preset_prompt("artistic"))
        self.artistic_btn.pack(side=tk.LEFT, padx=5)
        
        # Control frame
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        self.status_label = ttk.Label(control_frame, textvariable=self.status)
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        self.progress_bar = ttk.Progressbar(control_frame, mode="indeterminate", length=200)
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Add refresh button
        self.refresh_btn = ttk.Button(control_frame, text="Refresh", command=self.refresh_app)
        self.refresh_btn.pack(side=tk.RIGHT, padx=5)
        
        self.generate_btn = ttk.Button(control_frame, text="Generate Image", command=self.generate_image)
        self.generate_btn.pack(side=tk.RIGHT, padx=5)
        
        # Log output - with larger font
        self.log_frame = ttk.LabelFrame(main_frame, text="Log", padding=10)
        self.log_frame.pack(fill=tk.X, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(self.log_frame, wrap=tk.WORD, height=6, font=('Courier', 11))
        self.log_text.pack(fill=tk.X, expand=True)
        self.log_text.config(state=tk.DISABLED)
        
        # Footer with credits
        footer_frame = ttk.Frame(self.root)
        footer_frame.pack(fill=tk.X, pady=5)
        
        footer_text = "© 2025 Open Source by Francesco Gruner"
        footer_label = ttk.Label(footer_frame, text=footer_text, cursor="hand2")
        footer_label.pack(side=tk.RIGHT, padx=10)
        footer_label.bind("<Button-1>", lambda e: self.open_profile("linkedin"))
        
        youtube_btn = ttk.Button(footer_frame, text="YouTube", width=10, command=lambda: self.open_profile("youtube"))
        youtube_btn.pack(side=tk.RIGHT, padx=5)
        
        linkedin_btn = ttk.Button(footer_frame, text="LinkedIn", width=10, command=lambda: self.open_profile("linkedin"))
        linkedin_btn.pack(side=tk.RIGHT, padx=5)
    
    def update_language(self):
        lang = self.language.get()
        t = self.translations[lang]
        
        # Update window title
        self.root.title(t["title"])
        
        # Update labels and widgets
        self.api_frame.configure(text=t["api_config"])
        self.api_label.configure(text=t["api_key"])
        self.get_api_btn.configure(text=t["get_api_key"])
        
        self.image_frame.configure(text=t["images"])
        self.input_label.configure(text=t["input_image"])
        self.output_label.configure(text=t["generated_image"])
        self.select_btn.configure(text=t["select_image"])
        self.save_btn.configure(text=t["save_image"])
        
        self.prompt_frame.configure(text=t["prompt"])
        self.colorize_btn.configure(text=t["colorization"])
        self.objects_btn.configure(text=t["add_objects"])
        self.background_btn.configure(text=t["change_background"])
        self.artistic_btn.configure(text=t["artistic_effect"])
        
        self.generate_btn.configure(text=t["generate_image"])
        self.refresh_btn.configure(text=t["refresh"])
        self.log_frame.configure(text=t["log"])
        
        # Reset image labels if no images are selected
        if not self.input_image_path:
            self.input_image_label.config(text=t["no_input"])
        if not hasattr(self, 'generated_image'):
            self.output_image_label.config(text=t["no_output"])
        
        # Set default prompt based on language
        self.set_preset_prompt("colorize")
        
        # Update status
        self.status.set(t["ready"])
    
    def select_input_image(self):
        lang = self.language.get()
        file_path = filedialog.askopenfilename(
            title=self.translations[lang]["select_image"],
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        
        if file_path:
            self.input_image_path = file_path
            self.log_message(f"{file_path}")
            self.display_image(file_path, self.input_image_label)
    
    def save_output_image(self):
        lang = self.language.get()
        t = self.translations[lang]
        
        if not hasattr(self, 'generated_image'):
            self.log_message(t["no_image_save"])
            return
        
        file_path = filedialog.asksaveasfilename(
            title=t["save_image"],
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("All files", "*.*")]
        )
        
        if file_path:
            self.generated_image.save(file_path)
            self.log_message(f"{t['image_saved']}{file_path}")
    
    def set_preset_prompt(self, preset_type):
        lang = self.language.get()
        t = self.translations[lang]
        
        prompts = {
            "colorize": t["colorize_prompt"],
            "objects": t["objects_prompt"],
            "background": t["background_prompt"],
            "artistic": t["artistic_prompt"]
        }
        
        self.prompt_text.delete(1.0, tk.END)
        self.prompt_text.insert(tk.END, prompts.get(preset_type, t["colorize_prompt"]))
    
    def display_image(self, image_path, label_widget):
        try:
            img = Image.open(image_path)
            
            # Maintain proportions while adapting to available area
            max_width = 400
            max_height = 350
            
            width, height = img.size
            ratio = min(max_width/width, max_height/height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            label_widget.config(image=photo, text="", bg="white")
            label_widget.image = photo  # Keep a reference
        except Exception as e:
            self.log_message(f"Error: {e}")
    
    def generate_image(self):
        lang = self.language.get()
        t = self.translations[lang]
        
        if not self.input_image_path:
            self.log_message(t["select_first"])
            return
        
        api_key = self.api_key.get()
        if not api_key:
            self.log_message("API Key is required. Please enter your API key or get one by clicking the 'Get API Key' button.")
            return
        
        # Get custom prompt
        text_prompt = self.prompt_text.get(1.0, tk.END).strip()
        if not text_prompt:
            text_prompt = t["colorize_prompt"]
        
        # Start generation in a separate thread
        thread = threading.Thread(target=self.process_image, args=(text_prompt,))
        thread.daemon = True
        thread.start()
        
        # Update interface
        self.status.set(t["generating"])
        self.progress_bar.start()
        self.generate_btn.config(state=tk.DISABLED)
    
    def process_image(self, text_prompt):
        lang = self.language.get()
        t = self.translations[lang]
        
        try:
            # Set API key
            api_key = self.api_key.get()
            client = genai.Client(api_key=api_key)
            
            # Load image with PIL
            image = Image.open(self.input_image_path)
            
            # Prepare contents: text prompt and image
            contents = [text_prompt, image]
            
            # Log the prompt
            self.root.after(0, lambda: self.log_message(f"Prompt: {text_prompt}"))
            
            # Request to model specifying text and image output
            self.root.after(0, lambda: self.log_message("Sending request to Gemini model..."))
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp-image-generation",
                contents=contents,
                config=types.GenerateContentConfig(
                    response_modalities=["Text", "Image"]
                )
            )
            
            # Iterate through response parts to handle text and image
            model_response_text = ""
            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    model_response_text += part.text + "\n"
                elif part.inline_data is not None:
                    self.root.after(0, lambda: self.log_message("Received image from model"))
                    image_data = BytesIO(part.inline_data.data)
                    img = Image.open(image_data)
                    
                    # Salva l'immagine come ricevuta, senza conversioni
                    self.generated_image = img
                    
                    # Update interface safely
                    self.root.after(0, lambda: self.display_generated_image(self.generated_image))
            
            # Log text response
            if model_response_text:
                self.root.after(0, lambda: self.log_message(f"{t['model_response']}{model_response_text}"))
            
            self.root.after(0, lambda: self.complete_generation())
            
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"Error: {str(e)}"))
            self.root.after(0, lambda: self.complete_generation(False))
    
    def display_generated_image(self, image):
        # Maintain proportions while adapting to available area
        max_width = 400
        max_height = 350
        
        width, height = image.size
        ratio = min(max_width/width, max_height/height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        
        img = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        
        self.output_image_label.config(image=photo, text="", bg="white")
        self.output_image_label.image = photo  # Keep a reference
    
    def complete_generation(self, success=True):
        lang = self.language.get()
        t = self.translations[lang]
        
        self.progress_bar.stop()
        self.status.set(t["completed"] if success else t["error"])
        self.log_message(t["generation_complete"] if success else t["generation_failed"])
        self.generate_btn.config(state=tk.NORMAL)
    
    def log_message(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def refresh_app(self):
        # Reset the application state
        lang = self.language.get()
        t = self.translations[lang]
        
        # Stop any ongoing processes
        self.progress_bar.stop()
        self.status.set(t["ready"])
        
        # Re-enable buttons
        self.generate_btn.config(state=tk.NORMAL)
        
        # Clear logs
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        self.log_message("Application refreshed")
    
    def open_api_key_page(self):
        webbrowser.open("https://aistudio.google.com/")
    
    def show_about(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("About")
        about_window.geometry("400x300")
        about_window.resizable(False, False)
        
        about_frame = ttk.Frame(about_window, padding=20)
        about_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(about_frame, text="Gemini Image Generator", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)
        
        description = """
An open-source application that allows you to transform and 
generate images using the new Google's Gemini generative AI model
gemini-2.0-flash-exp-image-generation.

Created by Francesco Gruner
        """
        
        desc_label = ttk.Label(about_frame, text=description, justify="center")
        desc_label.pack(pady=10)
        
        version_label = ttk.Label(about_frame, text="Version 1.0.0", font=("Helvetica", 10, "italic"))
        version_label.pack(pady=5)
        
        links_frame = ttk.Frame(about_frame)
        links_frame.pack(pady=10)
        
        linkedin_btn = ttk.Button(links_frame, text="LinkedIn", width=15, command=lambda: self.open_profile("linkedin"))
        linkedin_btn.pack(side=tk.LEFT, padx=5)
        
        youtube_btn = ttk.Button(links_frame, text="YouTube Channel", width=15, command=lambda: self.open_profile("youtube"))
        youtube_btn.pack(side=tk.LEFT, padx=5)
        
        close_btn = ttk.Button(about_frame, text="Close", command=about_window.destroy)
        close_btn.pack(pady=10)
    
    def open_profile(self, profile_type):
        if profile_type == "linkedin":
            webbrowser.open("https://www.linkedin.com/in/francescogruner/")
        elif profile_type == "youtube":
            webbrowser.open("https://www.youtube.com/@FrancescoGruner")

if __name__ == "__main__":
    root = tk.Tk()
    app = GeminiImageGeneratorUI(root)
    root.mainloop()