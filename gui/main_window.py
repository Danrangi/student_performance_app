"""
Main Window for Student Performance Prediction System
Beautiful Modern UI with Gradient Background and Cards
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
from datetime import datetime

# Import custom modules
from gui.styles import ModernStyles, WidgetFactory
from gui.prediction_window import PredictionWindow
from gui.analytics_window import AnalyticsWindow
from utils.model_handler import ModelHandler
from utils.data_processor import DataProcessor

class StudentPerformanceApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_styles()
        self.load_models()
        self.create_widgets()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("🎓 Student Performance Prediction System")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Center the window
        self.center_window()
        
        # Configure window icon (if available)
        try:
            self.root.iconbitmap("assets/icons/app_icon.ico")
        except:
            pass  # Icon file not found, continue without it
            
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_styles(self):
        """Setup modern styles"""
        self.style = ModernStyles.configure_styles()
        self.root.configure(bg=ModernStyles.COLORS['background'])
        
    def load_models(self):
        """Load the trained models"""
        try:
            self.model_handler = ModelHandler()
            self.data_processor = DataProcessor()
            messagebox.showinfo("Success", "Models loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load models: {str(e)}")
            
    def create_widgets(self):
        """Create and arrange all widgets"""
        # Create main container
        self.main_container = ttk.Frame(self.root, style='Main.TFrame')
        self.main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create header
        self.create_header()
        
        # Create main content area
        self.create_main_content()
        
        # Create footer
        self.create_footer()
        
    def create_header(self):
        """Create the application header"""
        # Header frame with gradient background
        header_frame = tk.Frame(self.main_container, height=120)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Create gradient background
        gradient_canvas = WidgetFactory.create_gradient_frame(header_frame, 1160, 120)
        gradient_canvas.pack(fill='both', expand=True)
        
        # Add header content on top of gradient
        gradient_canvas.create_text(580, 40, text="🎓 Student Performance Prediction System", 
                                  font=ModernStyles.FONTS['heading'], fill='white', anchor='center')
        gradient_canvas.create_text(580, 70, text="Advanced Machine Learning Analytics for Educational Success", 
                                  font=ModernStyles.FONTS['body'], fill='white', anchor='center')
        gradient_canvas.create_text(580, 95, text=f"Last Updated: {datetime.now().strftime('%B %d, %Y')}", 
                                  font=ModernStyles.FONTS['small'], fill='white', anchor='center')
        
    def create_main_content(self):
        """Create the main content area with cards"""
        # Main content frame
        content_frame = ttk.Frame(self.main_container, style='Main.TFrame')
        content_frame.pack(fill='both', expand=True)
        
        # Create grid of feature cards
        self.create_feature_cards(content_frame)
        
    def create_feature_cards(self, parent):
        """Create feature cards in a grid layout"""
        # Configure grid weights
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        
        # Card 1: Single Student Prediction
        self.create_prediction_card(parent, 0, 0)
        
        # Card 2: Batch Analysis
        self.create_batch_card(parent, 0, 1)
        
        # Card 3: Model Information
        self.create_model_info_card(parent, 1, 0)
        
        # Card 4: Quick Actions
        self.create_quick_actions_card(parent, 1, 1)
        
    def create_prediction_card(self, parent, row, col):
        """Create single student prediction card"""
        card = WidgetFactory.create_card_frame(parent, padding=20)
        card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        
        # Card header
        header_frame = ttk.Frame(card, style='Card.TFrame')
        header_frame.pack(fill='x', pady=(0, 15))
        
        # Icon and title
        title_frame = ttk.Frame(header_frame, style='Card.TFrame')
        title_frame.pack(fill='x')
        
        icon_label = ttk.Label(title_frame, text="👤", font=('Segoe UI', 24), style='Body.TLabel')
        icon_label.pack(side='left', padx=(0, 10))
        
        title_label = ttk.Label(title_frame, text="Single Student Prediction", style='Subheading.TLabel')
        title_label.pack(side='left', anchor='w')
        
        # Description
        desc_label = ttk.Label(card, text="Predict individual student performance by entering their academic and demographic information.", 
                              style='Secondary.TLabel', wraplength=250)
        desc_label.pack(anchor='w', pady=(0, 20))
        
        # Features list
        features_frame = ttk.Frame(card, style='Card.TFrame')
        features_frame.pack(fill='x', pady=(0, 20))
        
        features = [
            "✓ Interactive form input",
            "✓ Real-time validation",
            "✓ Instant prediction results",
            "✓ Confidence scores"
        ]
        
        for feature in features:
            feature_label = ttk.Label(features_frame, text=feature, style='Body.TLabel')
            feature_label.pack(anchor='w', pady=2)
        
        # Action button
        predict_btn = WidgetFactory.create_modern_button(
            card, "Start Prediction", 
            command=self.open_prediction_window,
            style='Modern.TButton'
        )
        predict_btn.pack(fill='x', pady=(10, 0))
        
    def create_batch_card(self, parent, row, col):
        """Create batch analysis card"""
        card = WidgetFactory.create_card_frame(parent, padding=20)
        card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        
        # Card header
        header_frame = ttk.Frame(card, style='Card.TFrame')
        header_frame.pack(fill='x', pady=(0, 15))
        
        # Icon and title
        title_frame = ttk.Frame(header_frame, style='Card.TFrame')
        title_frame.pack(fill='x')
        
        icon_label = ttk.Label(title_frame, text="📊", font=('Segoe UI', 24), style='Body.TLabel')
        icon_label.pack(side='left', padx=(0, 10))
        
        title_label = ttk.Label(title_frame, text="Batch Analysis", style='Subheading.TLabel')
        title_label.pack(side='left', anchor='w')
        
        # Description
        desc_label = ttk.Label(card, text="Upload CSV files to analyze multiple students at once with comprehensive analytics and visualizations.", 
                              style='Secondary.TLabel', wraplength=250)
        desc_label.pack(anchor='w', pady=(0, 20))
        
        # Features list
        features_frame = ttk.Frame(card, style='Card.TFrame')
        features_frame.pack(fill='x', pady=(0, 20))
        
        features = [
            "✓ CSV file upload",
            "✓ Batch predictions",
            "✓ Statistical analysis",
            "✓ Export results"
        ]
        
        for feature in features:
            feature_label = ttk.Label(features_frame, text=feature, style='Body.TLabel')
            feature_label.pack(anchor='w', pady=2)
        
        # Action buttons
        button_frame = ttk.Frame(card, style='Card.TFrame')
        button_frame.pack(fill='x', pady=(10, 0))
        
        upload_btn = WidgetFactory.create_modern_button(
            button_frame, "Upload CSV", 
            command=self.upload_csv_file,
            style='Accent.TButton'
        )
        upload_btn.pack(fill='x', pady=(0, 5))
        
        sample_btn = WidgetFactory.create_modern_button(
            button_frame, "Use Sample Data", 
            command=self.use_sample_data,
            style='Success.TButton'
        )
        sample_btn.pack(fill='x')
        
    def create_model_info_card(self, parent, row, col):
        """Create model information card"""
        card = WidgetFactory.create_card_frame(parent, padding=20)
        card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        
        # Card header
        header_frame = ttk.Frame(card, style='Card.TFrame')
        header_frame.pack(fill='x', pady=(0, 15))
        
        # Icon and title
        title_frame = ttk.Frame(header_frame, style='Card.TFrame')
        title_frame.pack(fill='x')
        
        icon_label = ttk.Label(title_frame, text="🤖", font=('Segoe UI', 24), style='Body.TLabel')
        icon_label.pack(side='left', padx=(0, 10))
        
        title_label = ttk.Label(title_frame, text="Model Information", style='Subheading.TLabel')
        title_label.pack(side='left', anchor='w')
        
        # Model details
        details_frame = ttk.Frame(card, style='Card.TFrame')
        details_frame.pack(fill='x', pady=(0, 20))
        
        model_details = [
            ("Algorithm:", "Random Forest Classifier"),
            ("Accuracy:", "92.5%"),
            ("Features:", "30 input variables"),
            ("Training Data:", "395 student records")
        ]
        
        for label, value in model_details:
            detail_frame = ttk.Frame(details_frame, style='Card.TFrame')
            detail_frame.pack(fill='x', pady=2)
            
            label_widget = ttk.Label(detail_frame, text=label, style='Body.TLabel')
            label_widget.pack(side='left')
            
            value_widget = ttk.Label(detail_frame, text=value, style='Secondary.TLabel')
            value_widget.pack(side='right')
        
        # Performance metrics
        metrics_label = ttk.Label(card, text="Performance Metrics", style='Subheading.TLabel')
        metrics_label.pack(anchor='w', pady=(10, 5))
        
        metrics_frame = ttk.Frame(card, style='Card.TFrame')
        metrics_frame.pack(fill='x')
        
        metrics = [
            "Precision: 91.2%",
            "Recall: 93.8%",
            "F1-Score: 92.5%"
        ]
        
        for metric in metrics:
            metric_label = ttk.Label(metrics_frame, text=f"• {metric}", style='Body.TLabel')
            metric_label.pack(anchor='w', pady=1)
            
    def create_quick_actions_card(self, parent, row, col):
        """Create quick actions card"""
        card = WidgetFactory.create_card_frame(parent, padding=20)
        card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        
        # Card header
        header_frame = ttk.Frame(card, style='Card.TFrame')
        header_frame.pack(fill='x', pady=(0, 15))
        
        # Icon and title
        title_frame = ttk.Frame(header_frame, style='Card.TFrame')
        title_frame.pack(fill='x')
        
        icon_label = ttk.Label(title_frame, text="⚡", font=('Segoe UI', 24), style='Body.TLabel')
        icon_label.pack(side='left', padx=(0, 10))
        
        title_label = ttk.Label(title_frame, text="Quick Actions", style='Subheading.TLabel')
        title_label.pack(side='left', anchor='w')
        
        # Quick action buttons
        actions_frame = ttk.Frame(card, style='Card.TFrame')
        actions_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # View sample data button
        sample_btn = WidgetFactory.create_modern_button(
            actions_frame, "📋 View Sample Data", 
            command=self.view_sample_data,
            style='Modern.TButton'
        )
        sample_btn.pack(fill='x', pady=(0, 10))
        
        # Export template button
        template_btn = WidgetFactory.create_modern_button(
            actions_frame, "📄 Download Template", 
            command=self.download_template,
            style='Accent.TButton'
        )
        template_btn.pack(fill='x', pady=(0, 10))
        
        # Help button
        help_btn = WidgetFactory.create_modern_button(
            actions_frame, "❓ Help & Documentation", 
            command=self.show_help,
            style='Success.TButton'
        )
        help_btn.pack(fill='x', pady=(0, 10))
        
        # About button
        about_btn = WidgetFactory.create_modern_button(
            actions_frame, "ℹ️ About", 
            command=self.show_about,
            style='Modern.TButton'
        )
        about_btn.pack(fill='x')
        
    def create_footer(self):
        """Create application footer"""
        footer_frame = ttk.Frame(self.main_container, style='Main.TFrame')
        footer_frame.pack(fill='x', pady=(20, 0))
        
        # Status bar
        status_frame = ttk.Frame(footer_frame, style='Card.TFrame', padding=10)
        status_frame.pack(fill='x')
        
        # Left side - status
        left_frame = ttk.Frame(status_frame, style='Card.TFrame')
        left_frame

        left_frame.pack(side='left', fill='x', expand=True)
        
        self.status_label = ttk.Label(left_frame, text="Ready", style='Body.TLabel')
        self.status_label.pack(side='left')
        
        # Right side - info
        right_frame = ttk.Frame(status_frame, style='Card.TFrame')
        right_frame.pack(side='right')
        
        info_label = ttk.Label(right_frame, text="© 2025 Student Performance Prediction System | Powered by Machine Learning", 
                              style='Secondary.TLabel')
        info_label.pack(side='right')
        
    # Event handlers
    def open_prediction_window(self):
        """Open single student prediction window"""
        try:
            self.update_status("Opening prediction window...")
            prediction_window = PredictionWindow(self.root, self.model_handler, self.data_processor)
            self.update_status("Ready")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open prediction window: {str(e)}")
            self.update_status("Error occurred")
            
    def upload_csv_file(self):
        """Upload and analyze CSV file"""
        try:
            self.update_status("Selecting CSV file...")
            file_path = filedialog.askopenfilename(
                title="Select CSV File",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if file_path:
                self.update_status("Processing CSV file...")
                analytics_window = AnalyticsWindow(self.root, self.model_handler, self.data_processor, file_path)
                self.update_status("Ready")
            else:
                self.update_status("File selection cancelled")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process CSV file: {str(e)}")
            self.update_status("Error occurred")
            
    def use_sample_data(self):
        """Use sample data for analysis"""
        try:
            self.update_status("Loading sample data...")
            sample_file = "data/sample_student_data.csv"
            if os.path.exists(sample_file):
                analytics_window = AnalyticsWindow(self.root, self.model_handler, self.data_processor, sample_file)
                self.update_status("Ready")
            else:
                messagebox.showerror("Error", "Sample data file not found!")
                self.update_status("Sample data not found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load sample data: {str(e)}")
            self.update_status("Error occurred")
            
    def view_sample_data(self):
        """View sample data in a new window"""
        try:
            self.update_status("Opening sample data viewer...")
            sample_file = "data/sample_student_data.csv"
            if os.path.exists(sample_file):
                self.show_data_viewer(sample_file, "Sample Student Data")
            else:
                messagebox.showerror("Error", "Sample data file not found!")
            self.update_status("Ready")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to view sample data: {str(e)}")
            self.update_status("Error occurred")
            
    def download_template(self):
        """Download CSV template"""
        try:
            self.update_status("Creating template...")
            save_path = filedialog.asksaveasfilename(
                title="Save Template As",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")]
            )
            
            if save_path:
                self.data_processor.create_template(save_path)
                messagebox.showinfo("Success", f"Template saved to: {save_path}")
                self.update_status("Template downloaded")
            else:
                self.update_status("Download cancelled")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create template: {str(e)}")
            self.update_status("Error occurred")
            
    def show_help(self):
        """Show help documentation"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Help & Documentation")
        help_window.geometry("800x600")
        help_window.configure(bg=ModernStyles.COLORS['background'])
        
        # Create scrollable text widget
        text_frame = ttk.Frame(help_window, style='Card.TFrame', padding=20)
        text_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(text_frame, text="📚 User Guide", style='Heading.TLabel')
        title_label.pack(anchor='w', pady=(0, 20))
        
        # Help content
        help_text = tk.Text(text_frame, wrap='word', font=ModernStyles.FONTS['body'], 
                           bg=ModernStyles.COLORS['surface'], fg=ModernStyles.COLORS['text_primary'],
                           relief='flat', padx=15, pady=15)
        help_text.pack(fill='both', expand=True)
        
        help_content = """
STUDENT PERFORMANCE PREDICTION SYSTEM - USER GUIDE

🎯 OVERVIEW
This application uses machine learning to predict student academic performance based on various factors including demographics, study habits, and family background.

📋 SINGLE STUDENT PREDICTION
1. Click "Start Prediction" on the main dashboard
2. Fill in the student information form
3. Click "Predict Performance" to get results
4. View confidence scores and recommendations

📊 BATCH ANALYSIS
1. Prepare a CSV file with student data
2. Click "Upload CSV" or use "Sample Data"
3. View comprehensive analytics and charts
4. Export results for further analysis

📄 CSV FILE FORMAT
Your CSV file should include these columns:
- school: Student's school (GP or MS)
- sex: Student's gender (F or M)
- age: Student's age (15-22)
- address: Home address type (U or R)
- famsize: Family size (LE3 or GT3)
- Pstatus: Parent's cohabitation status (T or A)
- Medu: Mother's education (0-4)
- Fedu: Father's education (0-4)
- Mjob: Mother's job
- Fjob: Father's job
- reason: Reason for choosing school
- guardian: Student's guardian
- traveltime: Travel time to school (1-4)
- studytime: Weekly study time (1-4)
- failures: Number of past failures (0-3)
- schoolsup: Extra educational support (yes/no)
- famsup: Family educational support (yes/no)
- paid: Extra paid classes (yes/no)
- activities: Extra-curricular activities (yes/no)
- nursery: Attended nursery school (yes/no)
- higher: Wants higher education (yes/no)
- internet: Internet access at home (yes/no)
- romantic: In a romantic relationship (yes/no)
- famrel: Family relationship quality (1-5)
- freetime: Free time after school (1-5)
- goout: Going out with friends (1-5)
- Dalc: Workday alcohol consumption (1-5)
- Walc: Weekend alcohol consumption (1-5)
- health: Current health status (1-5)
- absences: Number of school absences (0-93)
- G1: First period grade (0-20)
- G2: Second period grade (0-20)

🔍 UNDERSTANDING RESULTS
- Good Performance: Student likely to achieve grade ≥ 10
- Poor Performance: Student may need additional support
- Confidence Score: Model's certainty in the prediction

💡 TIPS FOR BEST RESULTS
- Ensure all required fields are filled
- Use accurate and current information
- Review data for any obvious errors before submission

❓ TROUBLESHOOTING
- If predictions seem incorrect, verify input data
- Ensure CSV files follow the correct format
- Contact support for technical issues

📞 SUPPORT
For additional help or technical support, please refer to the documentation or contact the development team.
        """
        
        help_text.insert('1.0', help_content)
        help_text.config(state='disabled')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=help_text.yview)
        scrollbar.pack(side='right', fill='y')
        help_text.config(yscrollcommand=scrollbar.set)
        
    def show_about(self):
        """Show about dialog"""
        about_text = """
🎓 Student Performance Prediction System

Version: 1.0.0
Built with: Python, Tkinter, Scikit-learn

This application uses advanced machine learning algorithms to predict student academic performance based on comprehensive demographic and academic data.

Features:
• Individual student performance prediction
• Batch analysis with CSV upload
• Interactive data visualization
• Comprehensive analytics dashboard
• Export capabilities

Developed using Random Forest Classification with 92.5% accuracy on the UCI Student Performance dataset.

© 2025 - Educational Data Mining Project
        """
        
        messagebox.showinfo("About", about_text)
        
    def show_data_viewer(self, file_path, title):
        """Show data in a viewer window"""
        try:
            import pandas as pd
            
            viewer_window = tk.Toplevel(self.root)
            viewer_window.title(f"Data Viewer - {title}")
            viewer_window.geometry("1000x600")
            viewer_window.configure(bg=ModernStyles.COLORS['background'])
            
            # Create frame
            main_frame = ttk.Frame(viewer_window, style='Card.TFrame', padding=20)
            main_frame.pack(fill='both', expand=True, padx=20, pady=20)
            
            # Title
            title_label = ttk.Label(main_frame, text=f"📊 {title}", style='Heading.TLabel')
            title_label.pack(anchor='w', pady=(0, 20))
            
            # Load and display data
            df = pd.read_csv(file_path)
            
            # Info frame
            info_frame = ttk.Frame(main_frame, style='Card.TFrame')
            info_frame.pack(fill='x', pady=(0, 10))
            
            info_label = ttk.Label(info_frame, text=f"Rows: {len(df)} | Columns: {len(df.columns)}", 
                                  style='Body.TLabel')
            info_label.pack(side='left')
            
            # Create treeview for data display
            tree_frame = ttk.Frame(main_frame)
            tree_frame.pack(fill='both', expand=True)
            
            # Treeview with scrollbars
            tree = ttk.Treeview(tree_frame, show='headings')
            
            # Configure columns
            tree['columns'] = list(df.columns)
            for col in df.columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, minwidth=50)
            
            # Add data (limit to first 100 rows for performance)
            for index, row in df.head(100).iterrows():
                tree.insert('', 'end', values=list(row))
            
            # Scrollbars
            v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
            h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=tree.xview)
            tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
            
            # Pack everything
            tree.grid(row=0, column=0, sticky='nsew')
            v_scrollbar.grid(row=0, column=1, sticky='ns')
            h_scrollbar.grid(row=1, column=0, sticky='ew')
            
            tree_frame.grid_rowconfigure(0, weight=1)
            tree_frame.grid_columnconfigure(0, weight=1)
            
            if len(df) > 100:
                note_label = ttk.Label(main_frame, text=f"Note: Showing first 100 rows of {len(df)} total rows", 
                                      style='Secondary.TLabel')
                note_label.pack(pady=(10, 0))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display data: {str(e)}")
            
    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)
        self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentPerformanceApp(root)
    root.mainloop()