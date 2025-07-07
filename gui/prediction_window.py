"""
Single Student Prediction Window
Beautiful form interface for individual student prediction
"""

import tkinter as tk
from tkinter import ttk, messagebox
from gui.styles import ModernStyles, WidgetFactory
import pandas as pd

class PredictionWindow:
    def __init__(self, parent, model_handler, data_processor):
        self.parent = parent
        self.model_handler = model_handler
        self.data_processor = data_processor
        
        self.create_window()
        self.create_widgets()
        
    def create_window(self):
        """Create and configure the prediction window"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("🎯 Student Performance Prediction")
        self.window.geometry("900x700")
        self.window.configure(bg=ModernStyles.COLORS['background'])
        
        # Center the window
        self.center_window()
        
        # Make window modal
        self.window.transient(self.parent)
        self.window.grab_set()
        
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """Create and arrange all widgets"""
        # Main container
        main_container = ttk.Frame(self.window, style='Main.TFrame')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_container)
        
        # Form container with scrollbar
        self.create_form_container(main_container)
        
        # Buttons
        self.create_buttons(main_container)
        
    def create_header(self, parent):
        """Create window header"""
        header_frame = WidgetFactory.create_card_frame(parent, padding=20)
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Title
        title_label = ttk.Label(header_frame, text="🎯 Student Performance Prediction", 
                               style='Heading.TLabel')
        title_label.pack(anchor='w')
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame, 
                                  text="Enter student information to predict academic performance", 
                                  style='Secondary.TLabel')
        subtitle_label.pack(anchor='w', pady=(5, 0))
        
    def create_form_container(self, parent):
        """Create scrollable form container"""
        # Create canvas and scrollbar for scrollable form
        canvas_frame = ttk.Frame(parent, style='Main.TFrame')
        canvas_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        self.canvas = tk.Canvas(canvas_frame, bg=ModernStyles.COLORS['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style='Main.TFrame')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Create form sections
        self.create_form_sections()
        
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def create_form_sections(self):
        """Create form sections with input fields"""
        self.form_data = {}
        
        # Section 1: Basic Information
        self.create_basic_info_section()
        
        # Section 2: Family Background
        self.create_family_section()
        
        # Section 3: Academic Information
        self.create_academic_section()
        
        # Section 4: Social & Lifestyle
        self.create_social_section()
        
        # Section 5: Previous Grades
        self.create_grades_section()
        
    def create_section_header(self, parent, title, icon):
        """Create a section header"""
        section_frame = WidgetFactory.create_card_frame(parent, padding=15)
        section_frame.pack(fill='x', pady=(0, 15))
        
        header_frame = ttk.Frame(section_frame, style='Card.TFrame')
        header_frame.pack(fill='x', pady=(0, 15))
        
        icon_label = ttk.Label(header_frame, text=icon, font=('Segoe UI', 16), style='Body.TLabel')
        icon_label.pack(side='left', padx=(0, 10))
        
        title_label = ttk.Label(header_frame, text=title, style='Subheading.TLabel')
        title_label.pack(side='left')
        
        return section_frame
        
    def create_form_field(self, parent, label_text, field_name, field_type='entry', options=None, default_value=''):
        """Create a form field with label and input"""
        field_frame = ttk.Frame(parent, style='Card.TFrame')
        field_frame.pack(fill='x', pady=5)
        field_frame.grid_columnconfigure(1, weight=1)
        
        # Label
        label = ttk.Label(field_frame, text=label_text, style='Body.TLabel', width=20)
        label.grid(row=0, column=0, sticky='w', padx=(0, 10))
        
        # Input widget
        if field_type == 'combobox':
            widget = ttk.Combobox(field_frame, values=options, state='readonly', style='Modern.TCombobox')
            if default_value:
                widget.set(default_value)
        elif field_type == 'spinbox':
            widget = tk.Spinbox(field_frame, from_=options[0], to=options[1], 
                               font=ModernStyles.FONTS['body'], relief='solid', bd=2)
            widget.delete(0, 'end')
            widget.insert(0, str(default_value) if default_value else str(options[0]))
        else:  # entry
            widget = ttk.Entry(field_frame, style='Modern.TEntry')
            if default_value:
                widget.insert(0, str(default_value))
                
        widget.grid(row=0, column=1, sticky='ew', padx=(0, 10))
        
        # Store reference
        self.form_data[field_name] = widget
        
        return widget
        
    def create_basic_info_section(self):
        """Create basic information section"""
        section = self.create_section_header(self.scrollable_frame, "Basic Information", "👤")
        
        self.create_form_field(section, "School:", "school", "combobox", ["GP", "MS"], "GP")
        self.create_form_field(section, "Gender:", "sex", "combobox", ["F", "M"], "F")
        self.create_form_field(section, "Age:", "age", "spinbox", [15, 22], 16)
        self.create_form_field(section, "Address Type:", "address", "combobox", ["U", "R"], "U")
        self.create_form_field(section, "Family Size:", "famsize", "combobox", ["LE3", "GT3"], "GT3")
        self.create_form_field(section, "Parent Status:", "Pstatus", "combobox", ["T", "A"], "T")
        
    def create_family_section(self):
        """Create family background section"""
        section = self.create_section_header(self.scrollable_frame, "Family Background", "👨‍👩‍👧‍👦")
        
        self.create_form_field(section, "Mother's Education:", "Medu", "spinbox", [0, 4], 2)
        self.create_form_field(section, "Father's Education:", "Fedu", "spinbox", [0, 4], 2)
        
        job_options = ["teacher", "health", "services", "at_home", "other"]
        self.create_form_field(section, "Mother's Job:", "Mjob", "combobox", job_options, "other")
        self.create_form_field(section, "Father's Job:", "Fjob", "combobox", job_options, "other")
        
        reason_options = ["home", "reputation", "course", "other"]
        self.create_form_field(section, "School Choice Reason:", "reason", "combobox", reason_options, "course")
        
        guardian_options = ["mother", "father", "other"]
        self.create_form_field(section, "Guardian:", "guardian", "combobox", guardian_options, "mother")
        
        self.create_form_field(section, "Travel Time:", "traveltime", "spinbox", [1, 4], 2)
        
    def create_academic_section(self):
        """Create academic information section"""
        section = self.create_section_header(self.scrollable_frame, "Academic Information", "📚")
        
        self.create_form_field(section, "Study Time (hrs/week):", "studytime", "spinbox", [1, 4], 2)
        self.create_form_field(section, "Past Failures:", "failures", "spinbox", [0, 3], 0)
        
        yes_no_options = ["yes", "no"]
        self.create_form_field(section, "School Support:", "schoolsup", "combobox", yes_no_options, "no")
        self.create_form_field(section, "Family Support:", "famsup", "combobox", yes_no_options, "yes")
        self.create_form_field(section, "Paid Classes:", "paid", "combobox", yes_no_options, "no")
        self.create_form_field(section, "Extra Activities:", "activities", "combobox", yes_no_options, "no")
        self.create_form_field(section, "Nursery School:", "nursery", "combobox", yes_no_options, "yes")
        self.create_form_field(section, "Higher Education:", "higher", "combobox", yes_no_options, "yes")
        
    def create_social_section(self):
        """Create social and lifestyle section"""
        section = self.create_section_header(self.scrollable_frame, "Social & Lifestyle", "🎭")
        
        yes_no_options = ["yes", "no"]
        self.create_form_field(section, "Internet Access:", "internet", "combobox", yes_no_options, "yes")
        self.create_form_field(section, "Romantic Relationship:", "romantic", "combobox", yes_no_options, "no")
        
        self.create_form_field(section, "Family Relations (1-5):", "famrel", "spinbox", [1, 5], 4)
        self.create_form_field(section, "Free Time (1-5):", "freetime", "spinbox", [1, 5], 3)
        self.create_form_field(section, "Going Out (1-5):", "goout", "spinbox", [1, 5], 3)
        self.create_form_field(section, "Workday Alcohol (1-5):", "Dalc", "spinbox", [1, 5], 1)
        self.create_form_field(section, "Weekend Alcohol (1-5):", "Walc", "spinbox", [1, 5], 1)
        self.create_form_field(section, "Health Status (1-5):", "health", "spinbox", [1, 5], 5)
        self.create_form_field(section, "Absences:", "absences", "spinbox", [0, 93], 0)
        
    def create_grades_section(self):
        """Create previous grades section"""
        section = self.create_section_header(self.scrollable_frame, "Previous Grades", "📊")
        
        self.create_form_field(section, "First Period Grade (0-20):", "G1", "spinbox", [0, 20], 10)
        self.create_form_field(section, "Second Period Grade (0-20):", "G2", "spinbox", [0, 20], 10)
        
    def create_buttons(self, parent):
        """Create action buttons"""
        button_frame = ttk.Frame(parent, style='Main.TFrame')
        button_frame.pack(fill='x', pady=(10, 0))
        
        # Left side - utility buttons
        left_frame = ttk.Frame(button_frame, style='Main.TFrame')
        left_frame.pack(side='left')
        
        clear_btn = WidgetFactory.create_modern_button(
            left_frame, "🗑️ Clear Form", 
            command=self.clear_form,
            style='Success.TButton'
        )
        clear_btn.pack(side='left', padx=(0, 10))
        
        sample_btn = WidgetFactory.create_modern_button(
            left_frame, "📋 Load Sample", 
            command=self.load_sample_data,
            style='Accent.TButton'
        )
        sample_btn.pack(side='left')
        
        # Right side - main actions
        right_frame = ttk.Frame(button_frame, style='Main.TFrame')
        right_frame.pack(side='right')
        
        cancel_btn = WidgetFactory.create_modern_button(
            right_frame, "❌ Cancel", 
            command=self.window.destroy,
            style='Success.TButton'
        )
        cancel_btn.pack(side='right', padx=(10, 0))
        
        predict_btn = WidgetFactory.create_modern_button(
            right_frame, "🎯 Predict Performance", 
            command=self.predict_performance,
            style='Modern.TButton'
        )
        predict_btn.pack(side='right')
        
    def clear_form(self):
        """Clear all form fields"""
        for field_name, widget in self.form_data.items():
            if isinstance(widget, ttk.Combobox):
                widget.set('')
            elif isinstance(widget, tk.Spinbox):
                widget.delete(0, 'end')
            else:  # Entry
                widget.delete(0, 'end')
                
    def load_sample_data(self):
        """Load sample student data"""
        sample_data = {
            'school': 'GP', 'sex': 'F', 'age': 18, 'address': 'U', 'famsize': 'GT3',
            'Pstatus': 'A', 'Medu': 4, 'Fedu': 4, 'Mjob': 'at_home', 'Fjob': 'teacher',
            'reason': 'course', 'guardian': 'mother', 'traveltime': 2, 'studytime': 2,
            'failures': 0, 'schoolsup': 'yes', 'famsup': 'no', 'paid': 'no',
            'activities': 'no', 'nursery': 'yes', 'higher': 'yes', 'internet': 'no',
            'romantic': 'no', 'famrel': 4, 'freetime': 3, 'goout': 4, 'Dalc': 1,
            'Walc': 1, 'health': 3, 'absences': 6, 'G1': 5, 'G2': 6
        }
        
        for field_name, value in sample_data.items():
            if field_name in self.form_data:
                widget = self.form_data[field_name]
                if isinstance(widget, ttk.Combobox):
                    widget.set(str(value))
                elif isinstance(widget, tk.Spinbox):
                    widget.delete(0, 'end')
                    widget.insert(0, str(value))
                else:  # Entry
                    widget.delete(0, 'end')
                    widget.insert(0, str(value))
                    
    def get_form_data(self):
        """Get all form data as dictionary"""
        data = {}
        for field_name, widget in self.form_data.items():
            if isinstance(widget, ttk.Combobox):
                value = widget.get()
            elif isinstance(widget, tk.Spinbox):
                value = widget.get()
            else:  # Entry
                value = widget.get()
                
            # Convert to appropriate type
            if field_name in ['age', 'Medu', 'Fedu', 'traveltime', 'studytime', 'failures',
                             'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences', 'G1', 'G2']:
                try:
                    data[field_name] = int(value) if value else 0
                except ValueError:
                    data[field_name] = 0
            else:
                data[field_name] = value
                
        return data
        
    def validate_form(self, data):
        """Validate form data"""
        required_fields = list(self.form_data.keys())
        missing_fields = []
        
        for field in required_fields:
            if not data.get(field, ''):
                missing_fields.append(field)
                
        if missing_fields:
            messagebox.showerror("Validation Error", 
                               f"Please fill in all required fields:\n{', '.join(missing_fields)}")
            return False
            
        return True
        
    def predict_performance(self):
       
        """Predict student performance"""
        try:
            # Get form data
            data = self.get_form_data()
            
            # Validate data
            if not self.validate_form(data):
                return
                
            # Create DataFrame
            df = pd.DataFrame([data])
            
            # Make prediction
            prediction, confidence = self.model_handler.predict_single(df)
            
            # Show results
            self.show_prediction_results(prediction, confidence, data)
            
        except Exception as e:
            messagebox.showerror("Prediction Error", f"Failed to make prediction: {str(e)}")
            
    def show_prediction_results(self, prediction, confidence, student_data):
        """Show prediction results in a new window"""
        result_window = tk.Toplevel(self.window)
        result_window.title("🎯 Prediction Results")
        result_window.geometry("600x500")
        result_window.configure(bg=ModernStyles.COLORS['background'])
        
        # Center the window
        result_window.update_idletasks()
        width = result_window.winfo_width()
        height = result_window.winfo_height()
        x = (result_window.winfo_screenwidth() // 2) - (width // 2)
        y = (result_window.winfo_screenheight() // 2) - (height // 2)
        result_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Make modal
        result_window.transient(self.window)
        result_window.grab_set()
        
        # Main container
        main_container = ttk.Frame(result_window, style='Main.TFrame')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Results card
        results_card = WidgetFactory.create_card_frame(main_container, padding=30)
        results_card.pack(fill='both', expand=True)
        
        # Header
        header_frame = ttk.Frame(results_card, style='Card.TFrame')
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Prediction result
        if prediction == 1:
            result_text = "✅ Good Performance Expected"
            result_color = ModernStyles.COLORS['primary']
            icon = "🎉"
            message = "This student is predicted to perform well academically."
        else:
            result_text = "⚠️ Needs Additional Support"
            result_color = ModernStyles.COLORS['success']
            icon = "📚"
            message = "This student may benefit from additional academic support."
            
        # Large icon
        icon_label = ttk.Label(header_frame, text=icon, font=('Segoe UI', 48), style='Body.TLabel')
        icon_label.pack(pady=(0, 10))
        
        # Result text
        result_label = ttk.Label(header_frame, text=result_text, style='Heading.TLabel')
        result_label.pack()
        
        # Message
        message_label = ttk.Label(header_frame, text=message, style='Body.TLabel', wraplength=400)
        message_label.pack(pady=(10, 0))
        
        # Confidence section
        confidence_frame = WidgetFactory.create_card_frame(results_card, padding=20)
        confidence_frame.pack(fill='x', pady=(20, 0))
        
        conf_title = ttk.Label(confidence_frame, text="Prediction Confidence", style='Subheading.TLabel')
        conf_title.pack(anchor='w')
        
        # Confidence bar
        conf_bar_frame = ttk.Frame(confidence_frame, style='Card.TFrame')
        conf_bar_frame.pack(fill='x', pady=(10, 0))
        
        confidence_percent = confidence * 100
        conf_progress = ttk.Progressbar(conf_bar_frame, length=400, mode='determinate', 
                                       style='Modern.Horizontal.TProgressbar')
        conf_progress.pack(fill='x')
        conf_progress['value'] = confidence_percent
        
        conf_text = ttk.Label(conf_bar_frame, text=f"{confidence_percent:.1f}% Confident", 
                             style='Body.TLabel')
        conf_text.pack(pady=(5, 0))
        
        # Recommendations section
        rec_frame = WidgetFactory.create_card_frame(results_card, padding=20)
        rec_frame.pack(fill='x', pady=(20, 0))
        
        rec_title = ttk.Label(rec_frame, text="💡 Recommendations", style='Subheading.TLabel')
        rec_title.pack(anchor='w', pady=(0, 10))
        
        recommendations = self.get_recommendations(prediction, student_data)
        for rec in recommendations:
            rec_label = ttk.Label(rec_frame, text=f"• {rec}", style='Body.TLabel', wraplength=500)
            rec_label.pack(anchor='w', pady=2)
            
        # Buttons
        button_frame = ttk.Frame(results_card, style='Card.TFrame')
        button_frame.pack(fill='x', pady=(20, 0))
        
        save_btn = WidgetFactory.create_modern_button(
            button_frame, "💾 Save Results", 
            command=lambda: self.save_results(prediction, confidence, student_data),
            style='Accent.TButton'
        )
        save_btn.pack(side='left')
        
        close_btn = WidgetFactory.create_modern_button(
            button_frame, "✅ Close", 
            command=result_window.destroy,
            style='Modern.TButton'
        )
        close_btn.pack(side='right')
        
    def get_recommendations(self, prediction, student_data):
        """Generate recommendations based on prediction and student data"""
        recommendations = []
        
        if prediction == 0:  # Poor performance predicted
            if student_data.get('studytime', 0) < 3:
                recommendations.append("Increase weekly study time to improve academic performance")
            if student_data.get('failures', 0) > 0:
                recommendations.append("Consider additional tutoring to address past academic challenges")
            if student_data.get('absences', 0) > 10:
                recommendations.append("Improve attendance to better engage with course material")
            if student_data.get('schoolsup', '') == 'no':
                recommendations.append("Consider enrolling in school support programs")
            if student_data.get('famsup', '') == 'no':
                recommendations.append("Encourage family involvement in academic activities")
        else:  # Good performance predicted
            recommendations.append("Continue current study habits and maintain good attendance")
            recommendations.append("Consider taking on leadership roles or advanced courses")
            if student_data.get('higher', '') == 'yes':
                recommendations.append("Start preparing for higher education applications")
            recommendations.append("Maintain a healthy balance between academics and social activities")
            
        if not recommendations:
            recommendations.append("Continue monitoring academic progress regularly")
            
        return recommendations
        
    def save_results(self, prediction, confidence, student_data):
        """Save prediction results to file"""
        try:
            from tkinter import filedialog
            import json
            from datetime import datetime
            
            file_path = filedialog.asksaveasfilename(
                title="Save Prediction Results",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("Text files", "*.txt")]
            )
            
            if file_path:
                results = {
                    'timestamp': datetime.now().isoformat(),
                    'student_data': student_data,
                    'prediction': int(prediction),
                    'prediction_text': "Good Performance" if prediction == 1 else "Needs Support",
                    'confidence': float(confidence),
                    'recommendations': self.get_recommendations(prediction, student_data)
                }
                
                with open(file_path, 'w') as f:
                    json.dump(results, f, indent=2)
                    
                messagebox.showinfo("Success", f"Results saved to: {file_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save results: {str(e)}")
