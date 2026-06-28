import marimo

__generated_with = "0.17.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import math
    import random

    return math, random


@app.cell
def _():
    n_steps = 100
    dt = 0.02
    diffusion = 1.0
    return diffusion, dt, n_steps


@app.cell
def _(diffusion, dt, math, n_steps, random):
    x = 0.0
    y = 0.0 
    z = 0.0

    step_size = math.sqrt(2*diffusion*dt)


    for i in range(n_steps):
        dx = random.gauss(0, step_size)
        dy = random.gauss(0, step_size)
        dz = random.gauss(0, step_size)
    
        x = x+dx
        y = y+dy
        z = z+dz
        print(1)
        print("comment")
        print("I", x, y, z)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
