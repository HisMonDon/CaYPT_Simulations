import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import numpy as np
import tkinter as tk

class RayleighScatteringSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Rayleigh Scattering Simulation")
        
        # Setup matplotlib figure
        self.fig = plt.figure(figsize=(10, 6))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(-2, 2)
        self.ax.set_ylim(-2, 2)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        
        # Create GUI components
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.start_button = tk.Button(self.root, text="Start", command=self.start_animation)
        self.start_button.pack(side=tk.BOTTOM)
        
        # Animation control
        self.anim = None
        self.is_animating = False
        
        # Initialize elements
        self.init_elements()
    
    def init_elements(self):
        # Laser beam
        self.laser_line, = self.ax.plot([], [], lw=2)
        
        # Styrofoam molecule (polystyrene structure)
        self.molecule = self.ax.add_patch(plt.Circle((0, 0), 0.2, color='#FFD700', ec='black', lw=1))
        
        # Scattering points
        self.scatter_points = self.ax.scatter([], [], s=40, alpha=0.6, edgecolors='none')
        
        # Wavelength bar
        self.wavelength_bar = self.ax.add_patch(plt.Rectangle((-1.5, -1.8), 3, 0.3, 
                                            fc='none', ec='black', lw=1))
        self.current_wavelength = self.ax.add_patch(plt.Rectangle((-1.5, -1.8), 0, 0.3, 
                                            fc='blue', alpha=0.8))
        
        # Text label for Rayleigh scattering
        self.text = self.ax.text(0, 1.5, '', ha='center', va='center', 
                                fontsize=12, color='red', weight='bold')
    
    def update(self, frame):
        elements = [self.laser_line, self.scatter_points, self.current_wavelength, self.text]
        
        if frame < 30:  # Laser approaching phase
            x = np.linspace(-2, 0, 30)[frame]
            self.laser_line.set_data([-2, x], [0, 0])
            self.laser_line.set_color(plt.cm.rainbow(0))
        else:  # Scattering phase
            progress = (frame - 30) / 70
            wavelength = 400 + 300 * progress
            color = plt.cm.rainbow(progress)
            
            # Update laser and wavelength bar
            self.laser_line.set_color(color)
            self.laser_line.set_data([-2, 0], [0, 0])
            self.current_wavelength.set_width(3 * progress)
            self.current_wavelength.set_facecolor(color)
            
            # Generate new scattering points
            if frame % 3 == 0:
                angles = np.random.uniform(0, 2*np.pi, 15)
                radius = np.random.uniform(0.3, 1.2, 15)
                x = np.cos(angles) * radius
                y = np.sin(angles) * radius
                self.scatter_points.set_offsets(np.column_stack((x, y)))
                self.scatter_points.set_color(color)
                self.scatter_points.set_alpha(0.6)
            
            # Update text
            self.text.set_text('Rayleigh Scattering\n' + 
                             f'Wavelength: {wavelength:.1f} nm')
        
        return elements
    
    def init_anim(self):
        self.laser_line.set_data([], [])
        self.scatter_points.set_offsets(np.empty((0, 2)))  # Fix: Initialize with empty 2D array
        self.current_wavelength.set_width(0)
        self.text.set_text('')
        return [self.laser_line, self.scatter_points, self.current_wavelength, self.text]
    
    def start_animation(self):
        if not self.is_animating:
            self.anim = FuncAnimation(self.fig, self.update, frames=100,
                                    init_func=self.init_anim, interval=50, blit=True)
            self.is_animating = True

if __name__ == "__main__":
    root = tk.Tk()
    app = RayleighScatteringSimulation(root)
    root.mainloop()
