import tkinter as tk
from tkinter import ttk
from openpyxl import Workbook
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def calculate():
    num_slabs = int(entry_num_slabs.get())
    length = float(entry_length.get())
    width = float(entry_width.get())
    height = float(entry_height.get())
    spacing_main = float(entry_spacing_main.get()) / 1000  # Convert mm to meters
    dia_main = float(entry_dia_main.get())
    spacing_dist = float(entry_spacing_dist.get()) / 1000  # Convert mm to meters
    dia_dist = float(entry_dia_dist.get())
    earthwork_thickness = float(entry_earthwork_thickness.get())
    clearance = float(entry_clearance.get())
    
    # Calculate slab volume
    volume = num_slabs * length * width * height
    
    # Calculate earthwork volume
    earthwork_volume = num_slabs * length * width * earthwork_thickness

    # Calculate number and weight of main bars
    num_main_bars = round(width / spacing_main) + 1
    weight_main_bars = num_main_bars * (dia_main ** 2) / 162

    # Calculate number and weight of distribution bars
    num_dist_bars = round(length / spacing_dist) + 1
    weight_dist_bars = num_dist_bars * (dia_dist ** 2) / 162

    # Total reinforcement quantity
    reinforcement_qty = weight_main_bars + weight_dist_bars

    result.set(f"Total Volume: {volume:.2f} m³\n"
               f"Earthwork Volume: {earthwork_volume:.2f} m³\n"
               f"Total Reinforcement: {reinforcement_qty:.2f} kg")
    
    # Create Excel file
    wb = Workbook()
    ws = wb.active
    ws.append(["S.N", "Number", "Description of Item", "Length (m)", "Width (m)", "Height (m)", "Quantity (m³)", "Remarks"])
    ws.append([1, num_slabs, "RCC Slab", length, width, height, volume, ""])
    ws.append([2, num_slabs, "Earthwork", length, width, earthwork_thickness, earthwork_volume, ""])
    wb.save("RCC_Road_Earthwork_StoneSoling_Calculation.xlsx")

    # Create a section drawing with earthwork, stone soling, and reinforcement bars
    fig, ax = plt.subplots()

    # Draw slab
    ax.add_patch(Rectangle((0, 0), length, width, edgecolor='black', facecolor='none', label='Slab'))

    # Draw stone soling (0.15m thickness)
    ax.add_patch(Rectangle((0, -0.15), length, width, edgecolor='brown', facecolor='none', label='Stone Soling (0.15m)'))

    # Draw main bars
    for i in range(num_main_bars):
        x = i * spacing_main
        ax.plot([0, length], [x, x], 'r--', label='Main Bars' if i == 0 else "")

    # Draw distribution bars
    for i in range(num_dist_bars):
        y = i * spacing_dist
        ax.plot([y, y], [0, width], 'b--', label='Distribution Bars' if i == 0 else "")

    # Add earthwork clearance
    ax.add_patch(Rectangle((-clearance, -0.15-earthwork_thickness), length + 2*clearance, width + 2*clearance, edgecolor='green', facecolor='none', linestyle='--', label='Earthwork & Clearance'))

    ax.set_aspect('equal')
    plt.title("RCC Slab Section with Stone Soling, Bars, and Earthwork")
    plt.xlabel("Length (m)")
    plt.ylabel("Height/Depth (m)")
    plt.legend()
    plt.savefig("RCC_Slab_Section_Drawing.png")
    plt.show()

# GUI setup
root = tk.Tk()
root.title("RCC Slab with Earthwork and Stone Soling Calculator")

# Input fields for slab details
ttk.Label(root, text="Number of Slabs:").grid(column=0, row=0)
entry_num_slabs = ttk.Entry(root)
entry_num_slabs.grid(column=1, row=0)

ttk.Label(root, text="Length (m):").grid(column=0, row=1)
entry_length = ttk.Entry(root)
entry_length.grid(column=1, row=1)

ttk.Label(root, text="Width (m):").grid(column=0, row=2)
entry_width = ttk.Entry(root)
entry_width.grid(column=1, row=2)

ttk.Label(root, text="Height (m):").grid(column=0, row=3)
entry_height = ttk.Entry(root)
entry_height.grid(column=1, row=3)

# Input fields for reinforcement details
ttk.Label(root, text="Spacing of Main Bars (mm):").grid(column=0, row=4)
entry_spacing_main = ttk.Entry(root)
entry_spacing_main.grid(column=1, row=4)

ttk.Label(root, text="Diameter of Main Bars (mm):").grid(column=0, row=5)
entry_dia_main = ttk.Entry(root)
entry_dia_main.grid(column=1, row=5)

ttk.Label(root, text="Spacing of Distribution Bars (mm):").grid(column=0, row=6)
entry_spacing_dist = ttk.Entry(root)
entry_spacing_dist.grid(column=1, row=6)

ttk.Label(root, text="Diameter of Distribution Bars (mm):").grid(column=0, row=7)
entry_dia_dist = ttk.Entry(root)
entry_dia_dist.grid(column=1, row=7)

# Input fields for earthwork and clearance
ttk.Label(root, text="Earthwork Thickness (m):").grid(column=0, row=8)
entry_earthwork_thickness = ttk.Entry(root)
entry_earthwork_thickness.grid(column=1, row=8)

ttk.Label(root, text="Clearance (sqm):").grid(column=0, row=9)
entry_clearance = ttk.Entry(root)
entry_clearance.grid(column=1, row=9)

# Output display
result = tk.StringVar()
ttk.Label(root, textvariable=result).grid(column=0, row=10, columnspan=2)

# Button to trigger calculation
ttk.Button(root, text="Calculate", command=calculate).grid(column=0, row=11, columnspan=2)

# Run the GUI loop
root.mainloop()
