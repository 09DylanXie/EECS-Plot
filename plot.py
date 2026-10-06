import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="EECS Online Plotter", layout="centered")
st.title("EECS Online Plotter")

# ==========================================
# DATA & SIGNAL FUNCTIONS
# ==========================================
n_orig = np.arange(-6, 9)
x_orig = np.array([0, 0, 0, 2, -1, 0, 3, -2, 1, 2, 0, -1, 0, 0, 0])
x_dict = dict(zip(n_orig, x_orig))

def x_func(n_target):
    """Evaluates x[n]. Returns 0 if n is not an integer or out of bounds."""
    n_target = np.asarray(n_target)
    # Check which elements are integers (handles fractional shifts like n/2)
    is_int = np.isclose(n_target, np.round(n_target))
    result = np.zeros_like(n_target, dtype=float)
    for i, val in enumerate(n_target):
        if is_int[i]:
            result[i] = x_dict.get(int(np.round(val)), 0)
    return result

# Standard signal functions
u_func = lambda n: np.heaviside(n, 1)
delta_func = lambda n: np.where(np.isclose(n, 0), 1.0, 0.0)

# ==========================================
# UI CONTROLS
# ==========================================
col1, col2 = st.columns([2, 1])

with col1:
    equation_str = st.text_input(
        "Signal Equation:",
        value="x(n)",
        placeholder="e.g., x(-n) * u(n+1)"
    )

with col2:
    x_range = st.slider(
        "X-Axis Viewing Range",
        min_value=-30,
        max_value=30,
        value=(-6, 8)
    )

# ==========================================
# EVALUATION & PLOT
# ==========================================
# Compute over a wide invisible domain to allow for large shifts
n_vals = np.arange(-50, 51) 

# Dictionary of allowed functions and variables for the eval() parser
eval_dict = {
    "n": n_vals,
    "x": x_func,
    "u": u_func,
    "delta": delta_func,
    "np": np
}

try:
    # Safely evaluate the text input as a mathematical expression
    x_vals = eval(equation_str, {"__builtins__": {}}, eval_dict)
    
    # Handle edge case where user types a constant (e.g., "0")
    if isinstance(x_vals, (int, float)):
        x_vals = np.full_like(n_vals, x_vals, dtype=float)

    # Filter data to only show what is inside the slider window
    mask = (n_vals >= x_range[0]) & (n_vals <= x_range[1])
    n_plot = n_vals[mask]
    x_plot = x_vals[mask]

    fig, ax = plt.subplots(figsize=(10, 5))

    if len(n_plot) > 0:
        ax.stem(n_plot, x_plot, basefmt="black")

    ax.set_title(f"y[n] = {equation_str}", fontsize=14, fontweight='bold')
    ax.set_xlabel("n", fontsize=12)
    ax.set_ylabel("Amplitude", fontsize=12)

    # Dynamically scale Y-axis bounds based on the active equation
    y_min = min(x_plot) if len(x_plot) > 0 else -2
    y_max = max(x_plot) if len(x_plot) > 0 else 2
    ax.set_ylim(y_min - 1.5, y_max + 1.5)

    ax.grid(True, linestyle='--', alpha=0.6)
    ax.axhline(0, color='black', linewidth=1.2)
    ax.axvline(0, color='black', linewidth=1.2)

    st.pyplot(fig)

except Exception as e:
    st.error("Syntax Error. Please check your equation. Remember to use standard Python math operations (e.g., `x(n/2)` or `x(n) * delta(n-3)`).")