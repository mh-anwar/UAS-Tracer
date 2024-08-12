# Implement "A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system"
# https://link.springer.com/article/10.1007/s11432-023-4087-4

# Algorithm 1: Sweep direct optimization
import numpy as np

# Input: Map vertex Matrix - 40 by 140m rectangle - "the matrix containing column-wise stacked polygon vertices"

input = np.array([[0, 0, 0, 40, 140], [40, 140, 0, 0, 0]])
# ([[0, 0], [0, 40], [140, 40], [140, 0], [0, 0]])
# do I use 2x5 or 5x2


# Output: d*, θ*, Vf
def main():
    # d, θ and Vf are labeled as OUTput for now
    dOut = 0
    angleOut = 0
    vfOut = 0
    iOut = 0

    # matlab code index 2 is actually index 1
    for i in range(len(input) - 1):  # this is messed up?
        # fmt: off
        angle = np.arctan2(
            (input[1, i + 1] - input[1, 0]), 
            (input[0, i + 1] - input[0, i])
        )
        # fmt: on

        V = np.dot(
            np.array(
                [
                    [np.cos(angle), np.sin(angle)],
                    [np.sin(-angle), np.cos(angle)],
                ]
            ),
            input,
        )
        d = np.amax(V[1]) - V[1, i]
        if i == 1 or d < dOut:
            dOut = d
            angleOut = angle
            iOut = i  # ?
            print(dOut, angleOut, iOut)
            break
    Vs = np.array([])
    if iOut == len(input):  # what is M?
        # this makes 0 sense "[col(V )M col(V )1 · · · col(V )M ];"
        for i in range(len(input) - 1):
            col = input[:i]
            np.append(Vs, col)
    else:
        # different Vs
        for i in range(len(input) - 1):
            col = input[: iOut + 1]
            np.append(Vs, col)
        for i in range(len(input) - 1):
            col = input[: iOut - 1]
            np.append(Vs, col)
    print(Vs)
    VPrime = np.dot(
        np.array(
            [
                [np.cos(angleOut), np.sin(angleOut)],
                [np.sin(-angleOut), np.cos(angleOut)],
            ]
        ),
        Vs,
    )


if __name__ == "__main__":
    main()
