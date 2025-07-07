"""
Analytics Window for Batch Student Performance Analysis
Beautiful dashboard with charts and statistics
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from gui.styles import ModernStyles, WidgetFactory
import numpy as np

class AnalyticsWindow:
    def __init__(self, parent, model_handler, data_processor, file_path):
        self.parent = parent
        self.model_handler = model_handler
        self.data_processor = data_processor
        self.file_path = file_path
        self.df = None
        self.predictions = None
        
        self.create_window()
        self.load_and_process_data()
        self.create_widgets()
        
    def create_window(self):
        """Create and configure the analytics window"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("📊 Batch Analytics Dashboard")
        self.window.geometry("1400x900")
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
        
    def load_and_process_data(self):
        """Load and process the CSV data"""
        try:
            # Load data
            self.df = pd.read_csv(self.file_path)
            
            # Make predictions
            predictions, confidences = self.model_handler.predict_batch(self.df)
            
            # Add predictions to dataframe
            self.df['Predicted_Performance'] = predictions
            self.df['Confidence'] = confidences
            self.df['Performance_Label'] = self.df['Predicted_Performance'].map({
                1: 'Good Performance', 
                0: 'Needs Support'
            })
            
            self.predictions = predictions
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process data: {str(e)}")
            self.window.destroy()
            
    def create_widgets(self):
        """Create and arrange all widgets"""
        # Main container
        main_container = ttk.Frame(self.window, style='Main.TFrame')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_container)
        
        # Create notebook for tabs
        self.create_notebook(main_container)
        
        # Footer with action buttons
        self.create_footer(main_container)
        
    def create_header(self, parent):
        """Create dashboard header"""
        header_frame = WidgetFactory.create_card_frame(parent, padding=20)
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Title and stats
        title_frame = ttk.Frame(header_frame, style='Card.TFrame')
        title_frame.pack(fill='x')
        
        # Left side - title
        left_frame = ttk.Frame(title_frame, style='Card.TFrame')
        left_frame.pack(side='left', fill='x', expand=True)
        
        title_label = ttk.Label(left_frame, text="📊 Batch Analytics Dashboard", 
                               style='Heading.TLabel')
        title_label.pack(anchor='w')
        
        subtitle_label = ttk.Label(left_frame, text=f"Analysis of {len(self.df)} students", 
                                  style='Secondary.TLabel')
        subtitle_label.pack(anchor='w', pady=(5, 0))
        
        # Right side - quick stats
        stats_frame = ttk.Frame(title_frame, style='Card.TFrame')
        stats_frame.pack(side='right')
        
        good_performance = sum(self.predictions)
        needs_support = len(self.predictions) - good_performance
        
        # Stats cards
        self.create_stat_card(stats_frame, "✅ Good Performance", good_performance, 
                             f"{(good_performance/len(self.predictions)*100):.1f}%", 0, 0)
        self.create_stat_card(stats_frame, "⚠️ Needs Support", needs_support, 
                             f"{(needs_support/len(self.predictions)*100):.1f}%", 0, 1)
        
    def create_stat_card(self, parent, title, value, percentage, row, col):
        """Create a statistics card"""
        card = WidgetFactory.create_card_frame(parent, padding=15)
        card.grid(row=row, column=col, padx=5, pady=5)
        
        title_label = ttk.Label(card, text=title, style='Body.TLabel')
        title_label.pack()
        
        value_label = ttk.Label(card, text=str(value), font=('Segoe UI', 20, 'bold'), 
                               style='Body.TLabel')
        value_label.pack()
        
        percent_label = ttk.Label(card, text=percentage, style='Secondary.TLabel')
        percent_label.pack()
        
    def create_notebook(self, parent):
        """Create tabbed interface"""
        self.notebook = ttk.Notebook(parent, style='Modern.TNotebook')
        self.notebook.pack(fill='both', expand=True, pady=(0, 20))
        
        # Tab 1: Overview
        self.create_overview_tab()
        
        # Tab 2: Visualizations
        self.create_visualizations_tab()
        
        # Tab 3: Detailed Analysis
        self.create_analysis_tab()
        
        # Tab 4: Data Table
        self.create_data_tab()
        
    def create_overview_tab(self):
        """Create overview tab"""
        overview_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(overview_frame, text="📋 Overview")
        
        # Create scrollable frame
        canvas = tk.Canvas(overview_frame, bg=ModernStyles.COLORS['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(overview_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Main.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        # Summary statistics
        self.create_summary_section(scrollable_frame)
        
        # Performance distribution
        self.create_performance_distribution(scrollable_frame)
        
        # Key insights
        self.create_insights_section(scrollable_frame)
        
    def create_summary_section(self, parent):
        """Create summary statistics section"""
        section_frame = WidgetFactory.create_card_frame(parent, padding=20)
        section_frame.pack(fill='x', pady=(0, 20), padx=20)
        
        title_label = ttk.Label(section_frame, text="📊 Summary Statistics", style='Subheading.TLabel')
        title_label.pack(anchor='w', pady=(0, 15))
        
        # Create grid for statistics
        stats_grid = ttk.Frame(section_frame, style='Card.TFrame')
        stats_grid.pack(fill='x')
        
        # Configure grid
        for i in range(4):
            stats_grid.grid_columnconfigure(i, weight=1)
            
        # Calculate statistics
        total_students = len(self.df)
        good_performance = sum(self.predictions)
        needs_support = total_students - good_performance
        avg_confidence = np.mean(self.df['Confidence'])
        
        # Age statistics
        avg_age = self.df['age'].mean()
        
        # Study time statistics
        avg_study_time = self.df['studytime'].mean()
        
        # Absence statistics
        avg_absences = self.df['absences'].mean()
        
        # Previous grades
        if 'G1' in self.df.columns and 'G2' in self.df.columns:
            avg_g1 = self.df['G1'].mean()
            avg_g2 = self.df['G2'].mean()
        else:
            avg_g1 = avg_g2 = 0
            
        stats_data = [
            ("Total Students", total_students, "👥"),
            ("Average Age", f"{avg_age:.1f} years", "🎂"),
            ("Avg Study Time", f"{avg_study_time:.1f}/4", "📚"),
            ("Avg Confidence", f"{avg_confidence:.1f}%", "🎯"),
            ("Good Performance", f"{good_performance} ({good_performance/total_students*100:.1f}%)", "✅"),
            ("Needs Support", f"{needs_support} ({needs_support/total_students*100:.1f}%)", "⚠️"),
            ("Avg Absences", f"{avg_absences:.1f}", "📅"),
            ("Avg G1 Score", f"{avg_g1:.1f}/20", "📊")
        ]
        
        for i, (label, value, icon) in enumerate(stats_data):
            row = i // 4
            col = i % 4
            
            stat_card = WidgetFactory.create_card_frame(stats_grid, padding=15)
            stat_card.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            
            icon_label = ttk.Label(stat_card, text=icon, font=('Segoe UI', 16), style='Body.TLabel')
            icon_label.pack()
            
            label_widget = ttk.Label(stat_card, text=label, style='Body.TLabel')
            label_widget.pack()
            
            value_widget = ttk.Label(stat_card, text=str(value), style='Secondary.TLabel')
            value_widget.pack()
            
    def create_performance_distribution(self, parent):
        """Create performance distribution chart"""
        section_frame = WidgetFactory.create_card_frame(parent, padding=20)
        section_frame.pack(fill='x', pady=(0, 20), padx=20)
        
        title_label = ttk.Label(section_frame, text="📈 Performance Distribution", style='Subheading.TLabel')
        title_label.pack(anchor='w', pady=(0, 15))
        
        # Create matplotlib figure
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        fig.patch.set_facecolor(ModernStyles.COLORS['surface'])
        
        # Pie chart
        performance_counts = self.df['Performance_Label'].value_counts()
        colors = [ModernStyles.COLORS['primary'], ModernStyles.COLORS['success']]
        ax1.pie(performance_counts.values, labels=performance_counts.index, autopct='%1.1f%%', 
                colors=colors, startangle=90)
        ax1.set_title('Performance Distribution', fontsize=12, fontweight='bold')
        
        # Confidence distribution
        ax2.hist(self.df['Confidence'], bins=20, color=ModernStyles.COLORS['accent'], alpha=0.7, edgecolor='black')
        ax2.set_xlabel('Prediction Confidence')
        ax2.set_ylabel('Number of Students')
        ax2.set_title('Confidence Score Distribution', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Embed in tkinter
        canvas_widget = FigureCanvasTkAgg(fig, section_frame)
        canvas_widget.draw()
        canvas_widget.get_tk_widget().pack(fill='both', expand=True)
        
    def create_insights_section(self, parent):
        """Create key insights section"""
        section_frame = WidgetFactory.create_card_frame(parent, padding=20)
        section_frame.pack(fill='x', pady=(0, 20), padx=20)
        
        title_label = ttk.Label(section_frame, text="💡 Key Insights", style='Subheading.TLabel')
        title_label.pack(anchor='w', pady=(0, 15))
        
        insights = self.generate_insights()
        
        for insight in insights:
            insight_frame = ttk.Frame(section_frame, style='Card.TFrame')
            insight_frame.pack(fill='x', pady=5)
            
            bullet_label = ttk.Label(insight_frame, text="•", style='Body.TLabel')
            bullet_label.pack(side='left', padx=(0, 10))
            
            insight_label = ttk.Label(insight_frame, text=insight, style='Body.TLabel', wraplength=800)
            insight_label.pack(side='left', fill='x', expand=True)
            
    def generate_insights(self):
        """Generate insights from the data"""
        insights = []
        
        # Performance insights
        good_performance_rate = sum(self.predictions) / len(self.predictions) * 100
        if good_performance_rate > 70:
            insights.append(f"Excellent overall performance: {good_performance_rate:.1f}% of students are predicted to perform well")
        elif good_performance_rate > 50:
            insights.append(f"Moderate performance: {good_performance_rate:.1f}% of students are predicted to perform well")
        else:
            insights.append(f"Concerning performance: Only {good_performance_rate:.1f}% of students are predicted to perform well")
            
        # Age insights
        avg_age = self.df['age'].mean()
        if avg_age > 18:
            insights.append(f"Students are relatively older (avg: {avg_age:.1f} years), which may indicate grade repetition")
        else:
            insights.append(f"Students are at typical age (avg: {avg_age:.1f} years) for their grade level")
            
        # Study time insights
        low_study_time = len(self.df[self.df['studytime'] <= 2])
        if low_study_time > len(self.df) * 0.5:
            insights.append(f"{low_study_time} students ({low_study_time/len(self.df)*100:.1f}%) have low study time (≤2 hours/week)")
            
        # Absence insights
        high_absences = len(self.df[self.df['absences'] > 10])
        if high_absences > 0:
            insights.append(f"{high_absences} students have high absence rates (>10 absences), which may impact performance")
            
        # Family support insights
        if 'famsup' in self.df.columns:
            family_support = len(self.df[self.df['famsup'] == 'yes'])
            insights.append(f"{family_support} students ({family_support/len(self.df)*100:.1f}%) have family educational support")
            
        # Confidence insights
        high_confidence = len(self.df[self.df['Confidence'] > 0.8])
        insights.append(f"{high_confidence} predictions ({high_confidence/len(self.df)*100:.1f}%) have high confidence (>80%)")
        
        return insights
        
    def create_visualizations_tab(self):
        """Create visualizations tab"""
        viz_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(viz_frame, text="📊 Visualizations")
        
        # Create scrollable frame
        canvas = tk.Canvas(viz_frame, bg=ModernStyles.COLORS['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(viz_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Main.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create various charts
        self.create_correlation_chart(scrollable_frame)
        self.create_feature_analysis_charts(scrollable_frame)
        
    def create_correlation_chart(self, parent):
        """Create correlation heatmap"""
        section_frame = WidgetFactory.create_card_frame(parent, padding=20)
        section_frame.pack(fill='x', pady=(0, 20), padx=20)
        
        title_label = ttk.Label(section_frame, text="🔥 Feature Correlation Heatmap", style='Subheading.TLabel')
        title_label.pack(anchor='w', pady=(0, 15))
        
        # Select numeric columns for correlation
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            fig, ax = plt.subplots(figsize=(12, 8))
            fig.patch.set_facecolor(ModernStyles.COLORS['surface'])
            
            corr_matrix = self.df[numeric_cols].corr()
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                       square=True, ax=ax, cbar_kws={'shrink': 0.8})
            ax.set_title('Feature Correlation Matrix', fontsize=14, fontweight='bold')
            
            plt.tight_layout()
            
            canvas_widget = FigureCanvasTkAgg(fig, section_frame)
            canvas_widget.draw()
            canvas_widget.get_tk_widget().pack(fill='both', expand=True)
        else:
            no_data_label = ttk.Label(section_frame, text="Insufficient numeric data for correlation analysis", 
                                     style='Secondary.TLabel')
            no_data_label.pack()
            
    def create_feature_analysis_charts(self, parent):
        """Create feature analysis charts"""
        section_frame = WidgetFactory.create_card_frame(parent, padding=20)
        section_frame.pack(fill='x', pady=(0, 20), padx=20)
        
        title_label = ttk.Label(section_frame, text="📈 Feature Analysis", style='Subheading.TLabel')
        title_label.pack(anchor='w', pady=(0, 15))
        
        # Create subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.patch.set_facecolor(ModernStyles.COLORS['surface'])
        
        # Chart 1: Age distribution by performance
        if 'age' in self.df.columns:
            good_perf_ages = self.df[self.df['Predicted_Performance'] == 1]['age']
            poor_perf_ages = self.df[self.df['Predicted_Performance'] == 0]['age']
            
            axes[0,0].hist([good_perf_ages, poor_perf_ages], bins=10, alpha=0.7, 
                          label=['Good Performance', 'Needs Support'],
                          color=[ModernStyles.COLORS['primary'], ModernStyles.COLORS['success']])
            axes[0,0].set_xlabel('Age')
            axes[0,0].set_ylabel('Number of Students')
            axes[0,0].set_title('Age Distribution by Performance')
            axes[0,0].legend()
            axes[0,0].grid(True, alpha=0.3)
            
        # Chart 2: Study time vs Performance
        if 'studytime' in self.df.columns:
            study_perf = self.df.groupby('studytime')['Predicted_Performance'].mean()
            axes[0,1].bar(study_perf.index, study_perf.values, 
                         color=ModernStyles.COLORS['accent'], alpha=0.7)
            axes[0,1].set_xlabel('Study Time (1-4)')
            axes[0,1].set_ylabel('Good Performance Rate')
            axes[0,1].set_title('Study Time vs Performance Rate')
            axes[0,1].grid(True, alpha=0.3)
            
        # Chart 3: Absences vs Performance
        if 'absences' in self.df.columns:
            axes[1,0].scatter(self.df['absences'], self.df['Predicted_Performance'], 
                             alpha=0.6, color=ModernStyles.COLORS['primary'])
            axes[1,0].set_xlabel('Number of Absences')
            axes[1,0].set_ylabel('Predicted Performance')
            axes[1,0].set_title('Absences vs Performance')
            axes[1,0].grid(True, alpha=0.3)
            
        # Chart 4: Previous grades distribution
        if 'G1' in self.df.columns and 'G2' in self.df.columns:
            axes[1,1].scatter(self.df['G1'], self.df['G2'], 
                             c=self.df['Predicted_Performance'], 
                             cmap='RdYlBu', alpha=0.7)
            axes[1,1].set_xlabel('G1 (First Period Grade)')
            axes[1,1].set_ylabel('G2 (Second Period Grade)')
            axes[1,1].set_title('Previous Grades Distribution')
            axes[1,1].grid(True, alpha=0.3)
            
        plt.tight_layout()
        
        canvas_widget = FigureCanvasTkAgg(fig, section_frame)
        canvas_widget.draw()
        canvas_widget.get
        canvas_widget.get_tk_widget().pack(fill='both', expand=True)
        
    def create_analysis_tab(self):
        """Create detailed analysis tab"""
        analysis_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(analysis_frame, text="🔍 Analysis")
        
        # Create scrollable frame
        canvas = tk.Canvas(analysis_frame, bg=ModernStyles.COLORS['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(analysis_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Main.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Risk analysis
        self.create_risk_analysis(scrollable_frame)
        
        # Recommendations
        self.create_recommendations_section(scrollable_frame)
        
    def create_risk_analysis(self, parent):
        """Create risk analysis section"""
        section_frame = WidgetFactory.create_card_frame(parent, padding=20)
        section_frame.pack(fill='x', pady=(0, 20), padx=20)
        
        title_label = ttk.Label(section_frame, text="⚠️ Risk Analysis", style='Subheading.TLabel')
        title_label.pack(anchor='w', pady=(0, 15))
        
        # Identify high-risk students
        high_risk_students = self.df[
            (self.df['Predicted_Performance'] == 0) & 
            (self.df['Confidence'] > 0.7)
        ]
        
        medium_risk_students = self.df[
            (self.df['Predicted_Performance'] == 0) & 
            (self.df['Confidence'] <= 0.7)
        ]
        
        low_confidence_predictions = self.df[self.df['Confidence'] < 0.6]
        
        # Risk summary
        risk_summary_frame = ttk.Frame(section_frame, style='Card.TFrame')
        risk_summary_frame.pack(fill='x', pady=(0, 15))
        
        risk_data = [
            ("🔴 High Risk", len(high_risk_students), "Students predicted to need support with high confidence"),
            ("🟡 Medium Risk", len(medium_risk_students), "Students predicted to need support with lower confidence"),
            ("🔵 Low Confidence", len(low_confidence_predictions), "Predictions with confidence below 60%")
        ]
        
        for i, (label, count, description) in enumerate(risk_data):
            risk_card = WidgetFactory.create_card_frame(risk_summary_frame, padding=15)
            risk_card.pack(fill='x', pady=5)
            
            header_frame = ttk.Frame(risk_card, style='Card.TFrame')
            header_frame.pack(fill='x')
            
            label_widget = ttk.Label(header_frame, text=f"{label}: {count} students", 
                                   style='Body.TLabel')
            label_widget.pack(side='left')
            
            percentage = (count / len(self.df)) * 100
            percent_widget = ttk.Label(header_frame, text=f"({percentage:.1f}%)", 
                                     style='Secondary.TLabel')
            percent_widget.pack(side='right')
            
            desc_widget = ttk.Label(risk_card, text=description, style='Secondary.TLabel')
            desc_widget.pack(anchor='w', pady=(5, 0))
            
        # Detailed risk factors
        if len(high_risk_students) > 0:
            risk_factors_frame = WidgetFactory.create_card_frame(section_frame, padding=15)
            risk_factors_frame.pack(fill='x', pady=(15, 0))
            
            factors_title = ttk.Label(risk_factors_frame, text="🎯 Common Risk Factors", 
                                    style='Subheading.TLabel')
            factors_title.pack(anchor='w', pady=(0, 10))
            
            risk_factors = self.analyze_risk_factors(high_risk_students)
            
            for factor in risk_factors:
                factor_label = ttk.Label(risk_factors_frame, text=f"• {factor}", 
                                       style='Body.TLabel', wraplength=800)
                factor_label.pack(anchor='w', pady=2)
                
    def analyze_risk_factors(self, high_risk_df):
        """Analyze common risk factors among high-risk students"""
        factors = []
        total_high_risk = len(high_risk_df)
        
        if total_high_risk == 0:
            return ["No high-risk students identified"]
            
        # Study time analysis
        low_study_time = len(high_risk_df[high_risk_df['studytime'] <= 2])
        if low_study_time > total_high_risk * 0.6:
            factors.append(f"{low_study_time}/{total_high_risk} high-risk students have low study time (≤2 hours/week)")
            
        # Absence analysis
        if 'absences' in high_risk_df.columns:
            high_absences = len(high_risk_df[high_risk_df['absences'] > 10])
            if high_absences > total_high_risk * 0.4:
                factors.append(f"{high_absences}/{total_high_risk} high-risk students have high absence rates (>10)")
                
        # Previous failures
        if 'failures' in high_risk_df.columns:
            past_failures = len(high_risk_df[high_risk_df['failures'] > 0])
            if past_failures > total_high_risk * 0.5:
                factors.append(f"{past_failures}/{total_high_risk} high-risk students have previous academic failures")
                
        # Family support
        if 'famsup' in high_risk_df.columns:
            no_family_support = len(high_risk_df[high_risk_df['famsup'] == 'no'])
            if no_family_support > total_high_risk * 0.4:
                factors.append(f"{no_family_support}/{total_high_risk} high-risk students lack family educational support")
                
        # School support
        if 'schoolsup' in high_risk_df.columns:
            no_school_support = len(high_risk_df[high_risk_df['schoolsup'] == 'no'])
            if no_school_support > total_high_risk * 0.6:
                factors.append(f"{no_school_support}/{total_high_risk} high-risk students don't receive extra school support")
                
        if not factors:
            factors.append("No clear common risk factors identified among high-risk students")
            
        return factors
        
    def create_recommendations_section(self, parent):
        """Create recommendations section"""
        section_frame = WidgetFactory.create_card_frame(parent, padding=20)
        section_frame.pack(fill='x', pady=(0, 20), padx=20)
        
        title_label = ttk.Label(section_frame, text="💡 Recommendations", style='Subheading.TLabel')
        title_label.pack(anchor='w', pady=(0, 15))
        
        recommendations = self.generate_batch_recommendations()
        
        for i, (category, recs) in enumerate(recommendations.items()):
            cat_frame = WidgetFactory.create_card_frame(section_frame, padding=15)
            cat_frame.pack(fill='x', pady=10)
            
            cat_title = ttk.Label(cat_frame, text=category, style='Body.TLabel')
            cat_title.pack(anchor='w', pady=(0, 10))
            
            for rec in recs:
                rec_label = ttk.Label(cat_frame, text=f"  • {rec}", style='Secondary.TLabel', 
                                    wraplength=800)
                rec_label.pack(anchor='w', pady=2)
                
    def generate_batch_recommendations(self):
        """Generate recommendations based on batch analysis"""
        recommendations = {
            "🎯 Immediate Actions": [],
            "📚 Academic Interventions": [],
            "👨‍👩‍👧‍👦 Family Engagement": [],
            "🏫 School Programs": []
        }
        
        high_risk_count = len(self.df[
            (self.df['Predicted_Performance'] == 0) & 
            (self.df['Confidence'] > 0.7)
        ])
        
        # Immediate actions
        if high_risk_count > 0:
            recommendations["🎯 Immediate Actions"].append(
                f"Prioritize {high_risk_count} high-risk students for immediate intervention"
            )
            
        low_study_time = len(self.df[self.df['studytime'] <= 2])
        if low_study_time > len(self.df) * 0.4:
            recommendations["🎯 Immediate Actions"].append(
                f"Address low study time issue affecting {low_study_time} students"
            )
            
        # Academic interventions
        if 'failures' in self.df.columns:
            students_with_failures = len(self.df[self.df['failures'] > 0])
            if students_with_failures > 0:
                recommendations["📚 Academic Interventions"].append(
                    f"Provide remedial support for {students_with_failures} students with past failures"
                )
                
        high_absences = len(self.df[self.df['absences'] > 10])
        if high_absences > 0:
            recommendations["📚 Academic Interventions"].append(
                f"Implement attendance improvement programs for {high_absences} students"
            )
            
        # Family engagement
        if 'famsup' in self.df.columns:
            no_family_support = len(self.df[self.df['famsup'] == 'no'])
            if no_family_support > len(self.df) * 0.3:
                recommendations["👨‍👩‍👧‍👦 Family Engagement"].append(
                    f"Increase family engagement for {no_family_support} students lacking support"
                )
                
        # School programs
        if 'schoolsup' in self.df.columns:
            no_school_support = len(self.df[self.df['schoolsup'] == 'no'])
            if no_school_support > len(self.df) * 0.5:
                recommendations["🏫 School Programs"].append(
                    f"Expand school support programs to cover {no_school_support} additional students"
                )
                
        # Add general recommendations if specific ones are limited
        for category in recommendations:
            if not recommendations[category]:
                if "Immediate" in category:
                    recommendations[category].append("Continue monitoring student progress regularly")
                elif "Academic" in category:
                    recommendations[category].append("Maintain current academic support programs")
                elif "Family" in category:
                    recommendations[category].append("Strengthen family-school communication")
                else:
                    recommendations[category].append("Evaluate and enhance existing programs")
                    
        return recommendations
        
    def create_data_tab(self):
        """Create data table tab"""
        data_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(data_frame, text="📋 Data Table")
        
        # Controls frame
        controls_frame = WidgetFactory.create_card_frame(data_frame, padding=15)
        controls_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        # Filter controls
        filter_frame = ttk.Frame(controls_frame, style='Card.TFrame')
        filter_frame.pack(fill='x')
        
        ttk.Label(filter_frame, text="Filter by Performance:", style='Body.TLabel').pack(side='left', padx=(0, 10))
        
        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var, 
                                   values=["All", "Good Performance", "Needs Support"],
                                   state='readonly', style='Modern.TCombobox')
        filter_combo.pack(side='left', padx=(0, 20))
        filter_combo.bind('<<ComboboxSelected>>', self.filter_data)
        
        # Export button
        export_btn = WidgetFactory.create_modern_button(
            filter_frame, "📤 Export Data", 
            command=self.export_data,
            style='Accent.TButton'
        )
        export_btn.pack(side='right')
        
        # Data table frame
        table_frame = ttk.Frame(data_frame)
        table_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Create treeview
        self.tree = ttk.Treeview(table_frame, show='headings')
        
        # Configure columns
        display_columns = ['age', 'sex', 'studytime', 'failures', 'absences', 
                          'Performance_Label', 'Confidence']
        
        # Add G1, G2 if available
        if 'G1' in self.df.columns:
            display_columns.insert(-2, 'G1')
        if 'G2' in self.df.columns:
            display_columns.insert(-2, 'G2')
            
        self.tree['columns'] = display_columns
        
        for col in display_columns:
            self.tree.heading(col, text=col.replace('_', ' ').title())
            if col in ['Confidence']:
                self.tree.column(col, width=100, minwidth=80)
            elif col in ['Performance_Label']:
                self.tree.column(col, width=150, minwidth=120)
            else:
                self.tree.column(col, width=80, minwidth=60)
                
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack everything
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Populate data
        self.populate_tree()
        
    def populate_tree(self, filtered_df=None):
        """Populate the treeview with data"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Use filtered data or full dataset
        df_to_show = filtered_df if filtered_df is not None else self.df
        
        # Get display columns
        display_columns = list(self.tree['columns'])
        
        # Add data (limit to first 1000 rows for performance)
        for index, row in df_to_show.head(1000).iterrows():
            values = []
            for col in display_columns:
                if col == 'Confidence':
                    values.append(f"{row[col]:.1%}")
                elif col in ['G1', 'G2'] and col in row:
                    values.append(f"{row[col]:.1f}")
                else:
                    values.append(str(row[col]))
            self.tree.insert('', 'end', values=values)
            
        # Update status
        if len(df_to_show) > 1000:
            status_text = f"Showing first 1000 of {len(df_to_show)} rows"
        else:
            status_text = f"Showing all {len(df_to_show)} rows"
            
    def filter_data(self, event=None):
        """Filter data based on performance selection"""
        filter_value = self.filter_var.get()
        
        if filter_value == "All":
            filtered_df = self.df
        elif filter_value == "Good Performance":
            filtered_df = self.df[self.df['Performance_Label'] == 'Good Performance']
        else:  # Needs Support
            filtered_df = self.df[self.df['Performance_Label'] == 'Needs Support']
            
        self.populate_tree(filtered_df)
        
    def create_footer(self, parent):
        """Create footer with action buttons"""
        footer_frame = ttk.Frame(parent, style='Main.TFrame')
        footer_frame.pack(fill='x', pady=(10, 0))
        
        # Left side - info
        info_frame = ttk.Frame(footer_frame, style='Main.TFrame')
        info_frame.pack(side='left', fill='x', expand=True)
        
        info_label = ttk.Label(info_frame, 
                              text=f"Analysis complete • {len(self.df)} students processed • {sum(self.predictions)} predicted to perform well",
                              style='Secondary.TLabel')
        info_label.pack(side='left')
        
        # Right side - buttons
        button_frame = ttk.Frame(footer_frame, style='Main.TFrame')
        button_frame.pack(side='right')
        
        export_btn = WidgetFactory.create_modern_button(
            button_frame, "📊 Export Report", 
            command=self.export_full_report,
            style='Accent.TButton'
        )
        export_btn.pack(side='right', padx=(10, 0))
        
        save_predictions_btn = WidgetFactory.create_modern_button(
            button_frame, "💾 Save Predictions", 
            command=self.save_predictions,
            style='Modern.TButton'
        )
        save_predictions_btn.pack(side='right', padx=(10, 0))
        
        close_btn = WidgetFactory.create_modern_button(
            button_frame, "✅ Close", 
            command=self.window.destroy,
            style='Success.TButton'
        )
        close_btn.pack(side='right')
        
    def export_data(self):
        """Export current data view to CSV"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="Export Data",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")]
            )
            
            if file_path:
                # Get current filter
                filter_value = self.filter_var.get()
                
                if filter_value == "All":
                    export_df = self.df
                elif filter_value == "Good Performance":
                    export_df = self.df[self.df['Performance_Label'] == 'Good Performance']
                else:
                    export_df = self.df[self.df['Performance_Label'] == 'Needs Support']
                    
                export_df.to_csv(file_path, index=False)
                messagebox.showinfo("Success", f"Data exported to: {file_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")
            
    def save_predictions(self):
        """Save predictions to CSV"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="Save Predictions",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")]
            )
            
            if file_path:
                # Create predictions summary
                predictions_df = self.df[['Predicted_Performance', 'Performance_Label', 'Confidence']].copy()
                predictions_df.to_csv(file_path, index=False)
                messagebox.showinfo("Success", f"Predictions saved to: {file_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save predictions: {str(e)}")
            
    def export_full_report(self):
        """Export comprehensive analysis report"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="Export Analysis Report",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if file_path:
                self.generate_report(file_path)
                messagebox.showinfo("Success", f"Report exported to: {file_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {str(e)}")
            
    def generate_report(self, file_path):
        """Generate comprehensive analysis report"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("STUDENT PERFORMANCE ANALYSIS REPORT\n")
            f.write("=" * 50 + "\n\n")
            
            # Summary statistics
            f.write("SUMMARY STATISTICS\n")
            f.write("-" * 20 + "\n")
            f.write(f"Total Students Analyzed: {len(self.df)}\n")
            f.write(f"Good Performance Predicted: {sum(self.predictions)} ({sum(self.predictions)/len(self.predictions)*100:.1f}%)\n")
            f.write(f"Students Needing Support: {len(self.predictions) - sum(self.predictions)} ({(len(self.predictions) - sum(self.predictions))/len(self.predictions)*100:.1f}%)\n")
            f.write(f"Average Prediction Confidence: {np.mean(self.df['Confidence']):.1%}\n\n")
            
            # Demographics
            f.write("DEMOGRAPHIC BREAKDOWN\n")
            f.write("-" * 22 + "\n")
            f.write(f"Average Age: {self.df['age'].mean():.1f} years\n")
            if 'sex' in self.df.columns:
                gender_dist = self.df['sex'].value_counts()
                f.write(f"Gender Distribution: {dict(gender_dist)}\n")
            f.write("\n")
            
            # Academic factors
            f.write("ACADEMIC FACTORS\n")
            f.write("-" * 16 + "\n")
            f.write(f"Average Study Time: {self.df['studytime'].mean():.1f}/4\n")
            f.write(f"Average Absences: {self.df['absences'].mean():.1f}\n")
            if 'failures' in self.df.columns:
                f.write(f"Students with Past Failures: {len(self.df[self.df['failures'] > 0])}\n")
            f.write("\n")
            
            # Risk analysis
            high_risk = self.df[(self.df['Predicted_Performance'] == 0) & (self.df['Confidence'] > 0.7)]
            f.write("RISK ANALYSIS\n")
            f.write("-" * 13 + "\n")
            f.write(f"High Risk Students: {len(high_risk)}\n")
            f.write(f"Medium Risk Students: {len(self.df[(self.df['Predicted_Performance'] == 0) & (self.df['Confidence'] <= 0.7)])}\n")
            f.write(f"Low Confidence Predictions: {len(self.df[self.df['Confidence'] < 0.6])}\n\n")
            
            # Key insights
            f.write("KEY INSIGHTS\n")
            f.write("-" * 12 + "\n")
            insights = self.generate_insights()
            for i, insight in enumerate(insights, 1):
                f.write(f"{i}. {insight}\n")
            f.write("\n")
            
            # Recommendations
            f.write("RECOMMENDATIONS\n")
            f.write("-" * 15 + "\n")
            recommendations = self.generate_batch_recommendations()
            for category, recs in recommendations.items():
                f.write(f"\n{category}:\n")
                for rec in recs:
                    f.write(f"  • {rec}\n")
            
            f.write(f"\n\nReport generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
