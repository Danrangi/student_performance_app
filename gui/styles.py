"""
Modern UI Styles and Themes for Student Performance App
"""

import tkinter as tk
from tkinter import ttk

class ModernStyles:
    # Color Palette
    COLORS = {
        'primary': '#2E86AB',      # Ocean Blue
        'secondary': '#A23B72',    # Deep Pink
        'accent': '#F18F01',       # Orange
        'success': '#C73E1D',      # Red Orange
        'background': '#F5F5F5',   # Light Gray
        'surface': '#FFFFFF',      # White
        'text_primary': '#2C3E50', # Dark Blue Gray
        'text_secondary': '#7F8C8D', # Gray
        'border': '#E0E0E0',       # Light Border
        'hover': '#3498DB',        # Light Blue
        'gradient_start': '#667eea',
        'gradient_end': '#764ba2'
    }
    
    # Fonts
    FONTS = {
        'heading': ('Segoe UI', 24, 'bold'),
        'subheading': ('Segoe UI', 16, 'bold'),
        'body': ('Segoe UI', 11),
        'body_bold': ('Segoe UI', 11, 'bold'),
        'small': ('Segoe UI', 9),
        'button': ('Segoe UI', 10, 'bold')
    }
    
    @staticmethod
    def configure_styles():
        """Configure ttk styles for modern appearance"""
        style = ttk.Style()
        
        # Configure main frame style
        style.configure('Main.TFrame', 
                       background=ModernStyles.COLORS['background'])
        
        # Configure card frame style
        style.configure('Card.TFrame',
                       background=ModernStyles.COLORS['surface'],
                       relief='flat',
                       borderwidth=1)
        
        # Configure modern button style
        style.configure('Modern.TButton',
                       background=ModernStyles.COLORS['primary'],
                       foreground='white',
                       font=ModernStyles.FONTS['button'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10))
        
        style.map('Modern.TButton',
                 background=[('active', ModernStyles.COLORS['hover']),
                           ('pressed', ModernStyles.COLORS['secondary'])])
        
        # Configure accent button style
        style.configure('Accent.TButton',
                       background=ModernStyles.COLORS['accent'],
                       foreground='white',
                       font=ModernStyles.FONTS['button'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=(15, 8))
        
        # Configure success button style
        style.configure('Success.TButton',
                       background=ModernStyles.COLORS['success'],
                       foreground='white',
                       font=ModernStyles.FONTS['button'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=(15, 8))
        
        # Configure modern entry style
        style.configure('Modern.TEntry',
                       fieldbackground=ModernStyles.COLORS['surface'],
                       borderwidth=2,
                       relief='solid',
                       bordercolor=ModernStyles.COLORS['border'],
                       font=ModernStyles.FONTS['body'],
                       padding=(10, 8))
        
        style.map('Modern.TEntry',
                 bordercolor=[('focus', ModernStyles.COLORS['primary'])])
        
        # Configure modern combobox style
        style.configure('Modern.TCombobox',
                       fieldbackground=ModernStyles.COLORS['surface'],
                       borderwidth=2,
                       relief='solid',
                       bordercolor=ModernStyles.COLORS['border'],
                       font=ModernStyles.FONTS['body'],
                       padding=(10, 8))
        
        # Configure modern label style
        style.configure('Heading.TLabel',
                       background=ModernStyles.COLORS['background'],
                       foreground=ModernStyles.COLORS['text_primary'],
                       font=ModernStyles.FONTS['heading'])
        
        style.configure('Subheading.TLabel',
                       background=ModernStyles.COLORS['surface'],
                       foreground=ModernStyles.COLORS['text_primary'],
                       font=ModernStyles.FONTS['subheading'])
        
        style.configure('Body.TLabel',
                       background=ModernStyles.COLORS['surface'],
                       foreground=ModernStyles.COLORS['text_primary'],
                       font=ModernStyles.FONTS['body'])
        
        style.configure('Secondary.TLabel',
                       background=ModernStyles.COLORS['surface'],
                       foreground=ModernStyles.COLORS['text_secondary'],
                       font=ModernStyles.FONTS['small'])
        
        # Configure modern notebook style
        style.configure('Modern.TNotebook',
                       background=ModernStyles.COLORS['background'],
                       borderwidth=0)
        
        style.configure('Modern.TNotebook.Tab',
                       background=ModernStyles.COLORS['surface'],
                       foreground=ModernStyles.COLORS['text_primary'],
                       font=ModernStyles.FONTS['body_bold'],
                       padding=(20, 10),
                       borderwidth=0)
        
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', ModernStyles.COLORS['primary']),
                           ('active', ModernStyles.COLORS['hover'])],
                 foreground=[('selected', 'white')])
        
        # Configure modern progressbar
        style.configure('Modern.Horizontal.TProgressbar',
                       background=ModernStyles.COLORS['primary'],
                       troughcolor=ModernStyles.COLORS['border'],
                       borderwidth=0,
                       lightcolor=ModernStyles.COLORS['primary'],
                       darkcolor=ModernStyles.COLORS['primary'])
        
        return style

class WidgetFactory:
    """Factory class for creating styled widgets"""
    
    @staticmethod
    def create_card_frame(parent, **kwargs):
        """Create a card-style frame"""
        frame = ttk.Frame(parent, style='Card.TFrame', **kwargs)
        return frame
    
    @staticmethod
    def create_gradient_frame(parent, width, height):
        """Create a gradient background frame using Canvas"""
        canvas = tk.Canvas(parent, width=width, height=height, highlightthickness=0)
        
        # Create gradient effect
        for i in range(height):
            ratio = i / height
            r1, g1, b1 = int(ModernStyles.COLORS['gradient_start'][1:3], 16), \
                        int(ModernStyles.COLORS['gradient_start'][3:5], 16), \
                        int(ModernStyles.COLORS['gradient_start'][5:7], 16)
            r2, g2, b2 = int(ModernStyles.COLORS['gradient_end'][1:3], 16), \
                        int(ModernStyles.COLORS['gradient_end'][3:5], 16), \
                        int(ModernStyles.COLORS['gradient_end'][5:7], 16)
            
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, width, i, fill=color, width=1)
        
        return canvas
    
    @staticmethod
    def create_modern_button(parent, text, command=None, style='Modern.TButton', **kwargs):
        """Create a modern styled button"""
        button = ttk.Button(parent, text=text, command=command, style=style, **kwargs)
        return button
    
    @staticmethod
    def create_icon_button(parent, text, icon=None, command=None, **kwargs):
        """Create a button with icon (placeholder for now)"""
        # For now, just create a modern button
        # In a full implementation, you'd add icon support
        return WidgetFactory.create_modern_button(parent, text, command, **kwargs)
