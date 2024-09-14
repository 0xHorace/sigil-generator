import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog  # Added for file dialogs
import random
import colorsys
import os  # Added to handle file paths

class SigilGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Sigil Generator")

        # Variables for user inputs
        self.num_layers_var = tk.IntVar(value=3)
        self.fractal_iterations_var = tk.IntVar(value=50)
        self.include_particles_var = tk.BooleanVar(value=True)
        self.include_sacred_geometry_var = tk.BooleanVar(value=True)
        self.include_fractal_var = tk.BooleanVar(value=True)
        self.include_parametric_var = tk.BooleanVar(value=True)
        self.include_relativity_var = tk.BooleanVar(value=True)
        self.color_theme_var = tk.StringVar(value='Random')

        # Flag to check if a sigil has been generated
        self.sigil_generated = False

        # Set up the GUI
        self.setup_gui()

        # Matplotlib figure and axis
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.ax.axis('off')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=9, column=0, columnspan=4)

    def setup_gui(self):
        ttk.Label(self.root, text="Number of Layers:").grid(row=0, column=0, sticky='w')
        ttk.Entry(self.root, textvariable=self.num_layers_var).grid(row=0, column=1)

        ttk.Label(self.root, text="Fractal Iterations:").grid(row=1, column=0, sticky='w')
        ttk.Entry(self.root, textvariable=self.fractal_iterations_var).grid(row=1, column=1)

        ttk.Checkbutton(self.root, text="Include Particles", variable=self.include_particles_var).grid(row=2, column=0, columnspan=2, sticky='w')
        ttk.Checkbutton(self.root, text="Include Sacred Geometry", variable=self.include_sacred_geometry_var).grid(row=3, column=0, columnspan=2, sticky='w')
        ttk.Checkbutton(self.root, text="Include Fractal", variable=self.include_fractal_var).grid(row=4, column=0, columnspan=2, sticky='w')
        ttk.Checkbutton(self.root, text="Include Parametric Equations", variable=self.include_parametric_var).grid(row=5, column=0, columnspan=2, sticky='w')
        ttk.Checkbutton(self.root, text="Include Relativity Concept", variable=self.include_relativity_var).grid(row=6, column=0, columnspan=2, sticky='w')

        ttk.Label(self.root, text="Color Theme:").grid(row=7, column=0, sticky='w')
        ttk.Combobox(self.root, textvariable=self.color_theme_var, values=['Random', 'Warm', 'Cool', 'Monochrome']).grid(row=7, column=1)

        ttk.Button(self.root, text="Generate Sigil", command=self.generate_sigil).grid(row=0, column=2, rowspan=2, padx=10)
        ttk.Button(self.root, text="Generate Animated Sigil", command=self.generate_animated_sigil).grid(row=2, column=2, rowspan=2, padx=10)
        ttk.Button(self.root, text="Save Sigil", command=self.save_sigil).grid(row=4, column=2, padx=10)  # Added Save Button
        ttk.Button(self.root, text="Clear", command=self.clear_canvas).grid(row=5, column=2, padx=10)

    def clear_canvas(self):
        self.ax.clear()
        self.ax.axis('off')
        self.canvas.draw()
        self.sigil_generated = False  # Reset the flag when cleared

    def generate_color(self, theme='Random'):
        if theme == 'Random':
            return np.random.rand(3,)
        elif theme == 'Warm':
            hue = random.uniform(0, 0.1)  # Red hues
            return colorsys.hsv_to_rgb(hue, 1, 1)
        elif theme == 'Cool':
            hue = random.uniform(0.5, 0.75)  # Blue hues
            return colorsys.hsv_to_rgb(hue, 1, 1)
        elif theme == 'Monochrome':
            shade = random.uniform(0, 1)
            return (shade, shade, shade)
        else:
            return np.random.rand(3,)

    def generate_sigil(self):
        self.clear_canvas()
        self.ax.set_aspect('equal')
        bg_color = 'black'
        self.fig.patch.set_facecolor(bg_color)
        self.ax.set_facecolor(bg_color)

        num_layers = self.num_layers_var.get()
        fractal_iterations = self.fractal_iterations_var.get()
        include_particles = self.include_particles_var.get()
        include_sacred_geometry = self.include_sacred_geometry_var.get()
        include_fractal = self.include_fractal_var.get()
        include_parametric = self.include_parametric_var.get()
        include_relativity = self.include_relativity_var.get()
        color_theme = self.color_theme_var.get()

        # Golden Ratio
        golden_ratio = (1 + np.sqrt(5)) / 2

        # Sacred Geometry: Flower of Life Pattern
        if include_sacred_geometry:
            for n in range(num_layers):
                radius = (n + 1) * golden_ratio * 0.5
                layer_color = self.generate_color(color_theme)
                for angle in np.linspace(0, 2 * np.pi, 6, endpoint=False):
                    x_center = radius * np.cos(angle)
                    y_center = radius * np.sin(angle)
                    circle = plt.Circle((x_center, y_center), radius, color=layer_color, fill=False, linewidth=0.5)
                    self.ax.add_artist(circle)

        # Fractal Pattern: Mandelbrot Set Overlay
        if include_fractal:
            fractal = self.mandelbrot(500, 500, fractal_iterations)
            extent = [-2.0, 1.0, -1.5, 1.5]
            cmap_options = ['magma', 'inferno', 'plasma', 'viridis', 'cividis']
            fractal_cmap = random.choice(cmap_options)
            self.ax.imshow(fractal, cmap=fractal_cmap, extent=extent, interpolation='bilinear', alpha=0.5)

        # Quantum Randomness: Particle Scatter
        if include_particles:
            num_points = random.randint(200, 500)
            x_points = np.random.uniform(-2, 2, num_points)
            y_points = np.random.uniform(-2, 2, num_points)
            particle_color = self.generate_color(color_theme)
            self.ax.scatter(x_points, y_points, color=particle_color, s=0.5, alpha=0.7)

        # Parametric Equations with Complex Numbers
        if include_parametric:
            t = np.linspace(0, 2 * np.pi, 1000)
            a = random.uniform(0.5, 1.5)
            b = random.uniform(0.5, 1.5)
            c = random.uniform(0.5, 1.5)
            param_color = self.generate_color(color_theme)
            x_param = np.cos(a * t) - np.cos(b * t) ** 3
            y_param = np.sin(c * t) - np.sin(b * t) ** 3
            self.ax.plot(x_param, y_param, color=param_color, linewidth=1)

        # General Relativity Concept: Light Bending Around a Mass
        if include_relativity:
            mass = random.uniform(0.5, 2.0)
            def light_bending(theta):
                return 1 / (1 + mass * np.cos(theta))
            theta_light = np.linspace(0, 2 * np.pi, 1000)
            r_light = light_bending(theta_light)
            x_light = r_light * np.cos(theta_light)
            y_light = r_light * np.sin(theta_light)
            relativity_color = self.generate_color(color_theme)
            self.ax.plot(x_light, y_light, color=relativity_color, linewidth=1, linestyle='--', alpha=0.7)

        self.canvas.draw()
        self.sigil_generated = True  # Set the flag to True when a sigil is generated

    def generate_animated_sigil(self):
        self.clear_canvas()
        self.ax.set_aspect('equal')
        bg_color = 'black'
        self.fig.patch.set_facecolor(bg_color)
        self.ax.set_facecolor(bg_color)

        num_layers = self.num_layers_var.get()
        fractal_iterations = self.fractal_iterations_var.get()
        include_particles = self.include_particles_var.get()
        include_sacred_geometry = self.include_sacred_geometry_var.get()
        include_fractal = self.include_fractal_var.get()
        include_parametric = self.include_parametric_var.get()
        include_relativity = self.include_relativity_var.get()
        color_theme = self.color_theme_var.get()

        # Pre-generate colors for consistency across frames
        sacred_colors = [self.generate_color(color_theme) for _ in range(num_layers)]
        param_color = self.generate_color(color_theme)
        particle_color = self.generate_color(color_theme)
        relativity_color = self.generate_color(color_theme)

        frames = 60  # Number of frames in the animation
        interval = 100  # Time between frames in milliseconds

        def animate(i):
            self.ax.clear()
            self.ax.axis('off')
            self.ax.set_aspect('equal')

            angle_offset = i * np.pi / 30  # Adjust rotation speed

            # Sacred Geometry
            if include_sacred_geometry:
                golden_ratio = (1 + np.sqrt(5)) / 2
                for n in range(num_layers):
                    radius = (n + 1) * golden_ratio * 0.5
                    layer_color = sacred_colors[n]
                    for angle in np.linspace(0, 2 * np.pi, 6, endpoint=False):
                        x_center = radius * np.cos(angle + angle_offset)
                        y_center = radius * np.sin(angle + angle_offset)
                        circle = plt.Circle((x_center, y_center), radius, color=layer_color, fill=False, linewidth=0.5)
                        self.ax.add_artist(circle)

            # Parametric Equations
            if include_parametric:
                t = np.linspace(0, 2 * np.pi, 1000)
                a = random.uniform(0.5, 1.5)
                b = random.uniform(0.5, 1.5)
                c = random.uniform(0.5, 1.5) + i * 0.1  # Animate by changing parameter

                x_param = np.cos(a * t) - np.cos(b * t + angle_offset) ** 3
                y_param = np.sin(c * t) - np.sin(b * t + angle_offset) ** 3
                self.ax.plot(x_param, y_param, color=param_color, linewidth=1)

            # Particles
            if include_particles:
                num_points = random.randint(200, 500)
                x_points = np.random.uniform(-2, 2, num_points)
                y_points = np.random.uniform(-2, 2, num_points)
                self.ax.scatter(x_points, y_points, color=particle_color, s=0.5, alpha=0.7)

            # General Relativity Concept
            if include_relativity:
                mass = random.uniform(0.5, 2.0)
                def light_bending(theta):
                    return 1 / (1 + mass * np.cos(theta + angle_offset))
                theta_light = np.linspace(0, 2 * np.pi, 1000)
                r_light = light_bending(theta_light)
                x_light = r_light * np.cos(theta_light)
                y_light = r_light * np.sin(theta_light)
                self.ax.plot(x_light, y_light, color=relativity_color, linewidth=1, linestyle='--', alpha=0.7)

            # Fractal Background
            if include_fractal and i % 10 == 0:
                fractal = self.mandelbrot(500, 500, fractal_iterations)
                extent = [-2.0, 1.0, -1.5, 1.5]
                cmap_options = ['magma', 'inferno', 'plasma', 'viridis', 'cividis']
                fractal_cmap = random.choice(cmap_options)
                self.ax.imshow(fractal, cmap=fractal_cmap, extent=extent, interpolation='bilinear', alpha=0.5)

            self.ax.set_facecolor(bg_color)

        # Create the animation
        self.ani = animation.FuncAnimation(self.fig, animate, frames=frames, interval=interval, blit=False, repeat=False)
        self.canvas.draw()
        self.sigil_generated = True  # Set the flag to True when an animation is generated

    def save_sigil(self):
        if not self.sigil_generated:
            tk.messagebox.showwarning("No Sigil", "Please generate a sigil before saving.")
            return

        # Ask the user where to save the file
        filetypes = [('PNG Image', '*.png'), ('All Files', '*.*')]
        filepath = filedialog.asksaveasfilename(defaultextension='.png', filetypes=filetypes)
        if not filepath:
            return  # User canceled the save dialog

        # Save the current figure
        try:
            # For static sigil
            if hasattr(self, 'ani'):
                # If an animation exists, save it as GIF
                self.ani.save(filepath, writer='pillow')
                tk.messagebox.showinfo("Saved", f"Animated sigil saved as {os.path.basename(filepath)}")
            else:
                self.fig.savefig(filepath, dpi=300, facecolor=self.fig.get_facecolor(), bbox_inches='tight')
                tk.messagebox.showinfo("Saved", f"Sigil saved as {os.path.basename(filepath)}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred while saving:\n{e}")

    def mandelbrot(self, h, w, max_iter):
        x = np.linspace(-2.0, 1.0, w)
        y = np.linspace(-1.5, 1.5, h)
        C = x + y[:, None]*1j
        Z = np.zeros(C.shape, dtype=complex)
        div_time = max_iter + np.zeros(Z.shape, dtype=int)

        for i in range(max_iter):
            mask = np.abs(Z) <= 10
            Z[mask] = Z[mask] ** 2 + C[mask]
            diverged = mask & (np.abs(Z) > 10)
            div_time[diverged] = i
            Z[diverged] = 10

        return div_time

def main():
    root = tk.Tk()
    app = SigilGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()





