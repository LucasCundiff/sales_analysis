import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

df = pd.read_csv('E:/Python Projects/sales_analysis/sales_data.csv')

# Function to plot total sales over time
def plot_total_sales():
    data = df.groupby(pd.to_datetime(df['Date']).dt.to_period('M')).agg({'Total_Sales': 'sum'}).reset_index()
    data['Date'] = data['Date'].dt.to_timestamp()
    plot_data(data, 'Date', 'Total_Sales', 'Total Sales Over Time')

# Function to plot sales by product
def plot_sales_by_product():
    data = df.groupby('Product').agg({'Total_Sales': 'sum'}).reset_index()
    plot_data(data, 'Product', 'Total_Sales', 'Sales by Product', kind='bar')

# Function to plot profit by product
def plot_profit_by_product():
    data = df.groupby('Product').agg({'Profit': 'sum'}).reset_index()
    plot_data(data, 'Product', 'Profit', 'Profit by Product', kind='bar')

# Generic function to plot data
def plot_data(data, x, y, title, kind='line'):
    # Clear previous figure in the Tkinter frame
    for widget in frame.winfo_children():
        widget.destroy()
        
    fig = Figure(figsize=(10, 4))
    ax = fig.add_subplot(111)
    if kind == 'line':
        ax.plot(data[x], data[y])
    elif kind == 'bar':
        ax.bar(data[x], data[y])
    ax.set_title(title)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    
    # Embed the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)
    canvas.draw()

# Main application window
app = tk.Tk()
app.geometry("800x600")
app.title('Sales Data Analysis')

# Dropdown for analysis type selection
options = ['Total Sales', 'Sales by Product', 'Profit by Product']
selected_option = tk.StringVar()
dropdown = ttk.Combobox(app, textvariable=selected_option, values=options, state="readonly")
dropdown.pack(pady=10)
dropdown.set(options[0])  # Default value

# Frame for plotting
frame = tk.Frame(app)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Button to trigger plotting based on selection
plot_button = ttk.Button(app, text="Plot", command=lambda: on_select(selected_option.get()))
plot_button.pack(pady=10)

# Function to handle selection
def on_select(value):
    if value == 'Total Sales':
        plot_total_sales()
    elif value == 'Sales by Product':
        plot_sales_by_product()
    elif value == 'Profit by Product':
        plot_profit_by_product()

app.mainloop()