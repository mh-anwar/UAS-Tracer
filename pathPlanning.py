# Implement "A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system"
# https://link.springer.com/article/10.1007/s11432-023-4087-4

# Algorithm 1: Sweep direct optimization
import numpy as np

# Input: Map vertex Matrix - 40 by 140m rectangle - "the matrix containing column-wise stacked polygon vertices"
# fmt: off
input = np.array(
    [
        [0, 0, 0, 40, 140], 
        [40, 140, 0, 0, 0]
    ]
)
# ([[0, 0], [0, 40], [140, 40], [140, 0], [0, 0]])
# do I use 2x5 or 5x2
# fmt: on
dimensions = input.shape
rows, M = dimensions  # row and columns of input matrix
print(dimensions)


# Output: d*, θ*, Vf
def main():
    # Algorithm 1
    # d, θ and Vf are labeled as OUTput for now
    dStar = 0
    thetaStar = 0
    Vf = 0
    iStar = 0

    # matlab code index 2 is actually index 1
    for i in range(M):

        theta = np.arctan2(
            (input[1, i + 1] - input[1, i]), (input[0, i + 1] - input[0, i])
        )
        rotationMatrix = np.array(
            [
                [np.cos(theta), np.sin(theta)],
                [-np.sin(theta), np.cos(theta)],
            ]
        )
        Ṽ = np.cross(
            rotationMatrix,
            input,
        )
        d = np.amax(Ṽ[1]) - Ṽ[1, i]
        if i == 1 or d < dStar:
            dStar = d
            thetaStar = theta
            iStar = i  # ?
            print(dStar, thetaStar, iStar)
    Vs = np.array([])
    if iStar == M:
        # this makes 0 sense "[col(Ṽ )M col(Ṽ )1 · · · col(Ṽ )M ];"
        np.append(Vs, input[:M])
        for i in range(M):
            col = input[:i]
            np.append(Vs, col)
    else:
        # different Vs
        np.append(Vs, input[:iStar])
        for i in range(M):
            col = input[: iStar + 1]
            np.append(Vs, col)
        np.append(Vs, input[:0])
        for i in range(M):
            col = input[: iStar - 1]
            np.append(Vs, col)
        np.append(Vs, input[:iStar])
    VStar = np.cross(
        np.array(
            [
                [np.cos(thetaStar), np.sin(thetaStar)],
                [np.sin(-thetaStar), np.cos(thetaStar)],
            ]
        ),
        Vs,
    )
    # Algorithm #2
    # Input Ly, dStarP, VStar, Ns, M - all fake values for the next few lines
    dStarP = 0
    Ly = 2
    Ns = 10
    y = []  # I think this is some multi-dimension array
    x = 0
    n = 0
    f = 0
    # Output Wn, Wf

    for _ in range(len(y)):
        # I think this is populating n rows of y with Ly/2?
        y[n, 1] = Ly / 2
        y[f, 1] = Ly / 2
    # Line 3
    for j in range(2, Ns):
        y[n, j] = y[n, j - 1] + dStarP
        y[f, j] = y[f, j - 1] + dStarP

    # Line 7
    for i in range(len(Ns)):
        for j in range(M, 2):
            if VStar[2, j] >= y[n, i]:
                k = (VStar[1, j] - VStar[1, j + 1]) / (VStar[2, j] - VStar[2, j + 1])
                x[n, i] = (
                    k * (y[n, i] - VStar[2, j]) + VStar[1, j]
                )  # where does x come from
    # Line 16
    for i in range(len(Ns)):
        for j in range(2, M):
            if VStar[2, j] >= y[f, i]:
                k = (VStar[1, j] - VStar[1, j - 1]) / (VStar[2, j] - VStar[2, j - 1])
                x[f, i] = (
                    k * (y[f, i] - VStar[2, j]) + VStar[1, j]
                )  # where does x come from

    # Line 25: Wn
    Wn = np.array([])
    np.append(Wn, x[n, 1])
    np.append(Wn, y[n, 1])
    for i in range(2, Ns):
        np.append(Wn, x[n, i])
        np.append(Wn, y[n, i])

    # Line 26: Wf
    Wf = np.array([])
    np.append(Wf, x[n, 1])
    np.append(Wf, y[n, 1])
    for i in range(2, Ns):
        np.append(Wf, x[n, i])
        np.append(Wf, y[n, i])


if __name__ == "__main__":
    main()
