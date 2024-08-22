# Implement "A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system"
# https://link.springer.com/article/10.1007/s11432-023-4087-4

import numpy as np

# Required Input: Map vertex Matrix - 40 by 140m rectangle - "the matrix containing column-wise stacked polygon vertices"

# Final output: two sets of Waypoints - Wn and Wf - Wn is coordinates of straight line path primitives closert to UAS, Wf is the opposite


def main(V=np.array([[0, 0, 140, 140, 0], [0, 40, 40, 0, 0]])):
    M = V.shape[1] - 1  # this is the number of edges, which is less than the full loop
    # Output: d*, θ*, Vf

    print("Algorithm 1: Sweep Direction Optimization")
    # Algorithm 1
    # d, θ and Vf are labeled as OUTput for now
    dStar = 0
    thetaStar = 0
    Vf = 0
    iStar = 0

    # matlab code index 2 is actually index 1
    for i in range(1, M):

        theta = np.arctan2((V[1, i + 1] - V[1, i]), (V[0, i + 1] - V[0, i]))
        rotationMatrix = np.array(
            [
                [np.cos(theta), np.sin(theta)],
                [-np.sin(theta), np.cos(theta)],
            ]
        )
        Ṽ = rotationMatrix @ V
        d = np.amax(Ṽ[1]) - Ṽ[1, i]
        if i == 1 or d < dStar:
            dStar = d
            thetaStar = theta
            iStar = i  # ?
    Vs = np.array([])
    if iStar == M:
        Vs = np.hstack([V[:, M - 1 :], V[:, : M - 1]])  # possible place for error (M-1)
    else:
        Vs = np.hstack([V[:, iStar - 1 :], V[:, : iStar - 1]])
    rotationMatrix2 = np.array(
        [
            [np.cos(thetaStar), np.sin(thetaStar)],
            [-np.sin(thetaStar), np.cos(thetaStar)],
        ]
    )
    VStar = rotationMatrix2 @ Vs
    print("VStar", VStar)
    print()

    print("Algorithm 2: Waypoint Generation")
    # Algorithm #2
    # Input Ly, dStarP, VStar, Ns, M - all fake values for the next few lines
    Ly = 2  #! need
    Ns = 10  #! need
    dStarP = (dStar - Ly) / (Ns - 1)
    # I think Yn, Xn, Yf, Xf are two single dimension arrays
    yn = np.zeros(Ns)
    yf = np.zeros(Ns)
    xn = np.zeros(Ns)
    xf = np.zeros(Ns)

    # Output Wn, Wf
    # Line 1-2
    yn[0] = Ly / 2
    yf[0] = Ly / 2

    # Line 3
    for j in range(1, Ns):
        yn[j] = yn[j - 1] - dStarP
        yf[j] = yf[j - 1] - dStarP

    # Line 7
    for i in range(Ns):
        for j in range(
            M - 1, 0, -1
        ):  # might be troublesome, check if it should be M-1 or M and 0 or 2 and -1 (from j = M to 2)
            if VStar[1, j] >= yn[i]:
                k = (VStar[0, j] - VStar[0, j + 1]) / (VStar[1, j] - VStar[1, j + 1])
                xn[i] = k * (yn[i] - VStar[1, j]) + VStar[0, j]
    # Line 16
    for i in range(Ns):
        for j in range(1, M):
            if VStar[1, j] >= yf[i]:
                k = (VStar[0, j] - VStar[0, j - 1]) / (VStar[1, j] - VStar[1, j - 1])
                xf[i] = k * (yf[i] - VStar[1, j]) + VStar[0, j]

    # Line 25: Wn
    Wn = np.vstack((xn, yn))

    # Line 26: Wf
    Wf = np.vstack((xf, yf))

    return Wn, Wf


if __name__ == "__main__":
    V = np.array(
        input(
            "Enter the map vertex matrix (default: [[0, 0, 140, 140, 0], [0, 40, 40, 0, 0]]): "
        )
        or [[0, 0, 140, 140, 0], [0, 40, 40, 0, 0]]
    )
    Wn, Wf = main(V)
    print("Waypoints generated: ", Wn, Wf)
