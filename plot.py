import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="EECS Plotter")
st.title("EECS Plotter")

st.write("- use `x(n)` for the main signal, `u(n)` for unit step, and `delta(n)` for impulse.")
st.write("- type it out like python math: `3 * x(n)` not `3x(n)`. use parentheses like `x(n/2)` not brackets.")
st.write("- examples: `x(-n / 2)` or `x(n) * u(3 - n)`")

n_orig = np.arange(-6, 9)
x_orig = np.array([0, 0, 0, 2, -1, 0, 3, -2, 1, 2, 0, -1, 0, 0, 0])
x_dict = dict(zip(n_orig, x_orig))

def x_func(n_target):
    n_target = np.asarray(n_target)
    is_int = np.isclose(n_target, np.round(n_target))
    result = np.zeros_like(n_target, dtype=float)
    for i, val in enumerate(n_target):
        if is_int[i]:
            result[i] = x_dict.get(int(np.round(val)), 0)
    return result

u_func = lambda n: np.heaviside(n, 1)
delta_func = lambda n: np.where(np.isclose(n, 0), 1.0, 0.0)

equation_str = st.text_input("type equation here:", value="x(n)")

x_range = st.slider("x-axis range", -30, 30, (-6, 8))

n_vals = np.arange(-50, 51) 

eval_dict = {
    "n": n_vals,
    "x": x_func,
    "u": u_func,
    "delta": delta_func,
    "np": np
}

try:
    x_vals = eval(equation_str, {"__builtins__": {}}, eval_dict)
    
    if isinstance(x_vals, (int, float)):
        x_vals = np.full_like(n_vals, x_vals, dtype=float)

    mask = (n_vals >= x_range[0]) & (n_vals <= x_range[1])
    n_plot = n_vals[mask]
    x_plot = x_vals[mask]

    fig, ax = plt.subplots(figsize=(10, 5))

    if len(n_plot) > 0:
        ax.stem(n_plot, x_plot, basefmt="black")

    ax.set_title(f"y[n] = {equation_str}")
    ax.set_xlabel("n")
    ax.set_ylabel("amplitude")

    y_min = min(x_plot) if len(x_plot) > 0 else -2
    y_max = max(x_plot) if len(x_plot) > 0 else 2
    ax.set_ylim(y_min - 1.5, y_max + 1.5)

    ax.grid(True, linestyle='--', alpha=0.6)
    ax.axhline(0, color='black')
    ax.axvline(0, color='black')

    st.pyplot(fig)

except Exception:
    st.error("uh oh, something is wrong with the equation. check your math and try again.")