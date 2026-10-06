import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="Discrete-Time Signals", layout="centered")
st.title("Discrete-Time Signal Transformations")

# ==========================================
# DATA & HELPERS
# ==========================================
# Original coordinates
n_orig = np.arange(-6, 9)
x_orig = np.array([0, 0, 0, 2, -1, 0, 3, -2, 1, 2, 0, -1, 0, 0, 0])

def get_x(n_target):
    x_dict = dict(zip(n_orig, x_orig))
    return np.array([x_dict.get(ni, 0) for ni in n_target])

u = lambda n: np.heaviside(n, 1)
delta = lambda n: np.where(n == 0, 1, 0)

# ==========================================
# UI CONTROLS
# ==========================================
col1, col2 = st.columns([2, 1])

with col1:
    plot_choice = st.selectbox(
        "Select Problem Part:",
        [
            "Original Signal x[n]",
            "1.1: x[2n]",
            "1.2: x[-n/2]",
            "1.3: x[1 + n/3]",
            "1.4: 3x[n] - 2",
            "1.5: 2x[n+4] - 1",
            "2.1: x[-n]u[n+1]",
            "2.2: x[n]u[-n]",
            "2.3: x[n]u[n-3]",
            "2.4: x[n]u[3-n]",
            "2.5: x[n]δ[n-2]",
            "2.6: x[n](δ[n] + δ[n-3])"
        ]
    )

with col2:
    x_range = st.slider(
        "X-Axis Viewing Range",
        min_value=-20,
        max_value=20,
        value=(-10, 10)
    )

# ==========================================
# TRANSFORMATION LOGIC
# ==========================================
# Generate a wide domain to safely compute expansive transformations
n_full = np.arange(-30, 31)

if plot_choice == "Original Signal x[n]":
    n_vals, x_vals = n_orig, x_orig
elif plot_choice == "1.1: x[2n]":
    n_vals = n_full
    x_vals = get_x(2 * n_vals)
elif plot_choice == "1.2: x[-n/2]":
    n_vals = n_full
    x_vals = np.where(n_vals % 2 == 0, get_x(-n_vals // 2), 0)
elif plot_choice == "1.3: x[1 + n/3]":
    n_vals = n_full
    x_vals = np.where(n_vals % 3 == 0, get_x(1 + n_vals // 3), 0)
elif plot_choice == "1.4: 3x[n] - 2":
    n_vals = n_full
    x_vals = 3 * get_x(n_vals) - 2
elif plot_choice == "1.5: 2x[n+4] - 1":
    n_vals = n_full
    x_vals = 2 * get_x(n_vals + 4) - 1
elif plot_choice == "2.1: x[-n]u[n+1]":
    n_vals = n_full
    x_vals = get_x(-n_vals) * u(n_vals + 1)
elif plot_choice == "2.2: x[n]u[-n]":
    n_vals = n_full
    x_vals = get_x(n_vals) * u(-n_vals)
elif plot_choice == "2.3: x[n]u[n-3]":
    n_vals = n_full
    x_vals = get_x(n_vals) * u(n_vals - 3)
elif plot_choice == "2.4: x[n]u[3-n]":
    n_vals = n_full
    x_vals = get_x(n_vals) * u(3 - n_vals)
elif plot_choice == "2.5: x[n]δ[n-2]":
    n_vals = n_full
    x_vals = get_x(n_vals) * delta(n_vals - 2)
elif plot_choice == "2.6: x[n](δ[n] + δ[n-3])":
    n_vals = n_full
    x_vals = get_x(n_vals) * (delta(n_vals) + delta(n_vals - 3))

# ==========================================
# FILTER & PLOT
# ==========================================
# Mask data to fit strictly within the slider boundaries
mask = (n_vals >= x_range[0]) & (n_vals <= x_range[1])
n_plot = n_vals[mask]
x_plot = x_vals[mask]

fig, ax = plt.subplots(figsize=(10, 5))

# Draw stem plot
if len(n_plot) > 0:
    ax.stem(n_plot, x_plot, basefmt="black")

# Formatting matching the previous grid style
ax.set_title(plot_choice, fontsize=14, fontweight='bold')
ax.set_xlabel("n", fontsize=12)
ax.set_ylabel("Amplitude", fontsize=12)

# Dynamic Y-axis scaling based on visible points
y_min = min(x_plot) if len(x_plot) > 0 else -2
y_max = max(x_plot) if len(x_plot) > 0 else 2
ax.set_ylim(y_min - 1.5, y_max + 1.5)

ax.grid(True, linestyle='--', alpha=0.6)
ax.axhline(0, color='black', linewidth=1.2)
ax.axvline(0, color='black', linewidth=1.2)

# Render plot in Streamlit
st.pyplot(fig)