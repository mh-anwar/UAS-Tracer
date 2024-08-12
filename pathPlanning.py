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
    VPrime = np.cross(
        np.array(
            [
                [np.cos(thetaStar), np.sin(thetaStar)],
                [np.sin(-thetaStar), np.cos(thetaStar)],
            ]
        ),
        Vs,
    )
    # Algorithm #2


if __name__ == "__main__":
    main()
