# # names = [
# #     "Number of wedges",
# #     "Epoxy low bound",
# #     "Highlight cutoff",
# #     "CF top bound",
# #     "CF bottom bound",
# #     "CF thickness",
# #     "Highlight thickness",
# #     "Interpolation threshold",
# #     "Epoxy interpolation threshold",
# # ]
# # vals = [50, 40, 210, 70, 173, 7, 9, 0.7, 0]


# # def thing(name, val):
# #     return "<label>{}:</label> \n <textarea>{}</textarea>\n<br>".format(name, val)


# # for i in range(len(names)):
# #     print(thing(names[i], vals[i]))

# # Side A
# A_onextwo_x = [77.33, 86.825, 113.36, 146.75, 174.525]
# A_onextwo_y = [-1, 29.9, 49.8, 50.085, 30.68]
# A_onextwo_theta = [1.570796327, 0.825143493, 0.145918828, -0.517723842, -1.221555058]

# A_twoxtwo_x = [26.37, 37.68, 73.465, 124.855, 178.685, 220.765]
# A_twoxtwo_y = [127.65, 179.455, 219.43, 236.73, 226.295, 190.245]
# A_twoxtwo_theta = [
#     1.570796327,
#     0.999651777,
#     0.428354869,
#     -0.142902471,
#     -0.713975145,
#     -1.285029653,
# ]

# # Side B
# B_onextwo_x = [-170.835, -160.51, -140.92, -114.98, -86.52, -59.81, -38.905, -27]
# B_onextwo_y = [12.67, 38.87, 59.26, 70.72, 71.465, 61.295, 41.67, 15.48]
# B_onextwo_theta = [
#     78.00711748,
#     54.01320436,
#     29.99915084,
#     6.003503097,
#     -18.00697322,
#     -41.99795448,
#     -65.99214726,
#     -90,
# ]

# B_twoxtwo_x = [-236.835, -218.18, -181.41, -131.81, -76.81, -25.02, 15.86, 39.48]
# B_twoxtwo_y = [-75.125, -24.39, 15.81, 39.24, 41.495, 22.515, -14.685, -64.64]
# B_twoxtwo_theta = [
#     77.99426418,
#     54.01320436,
#     29.99915084,
#     6.003503097,
#     -17.98197792,
#     -41.99795448,
#     -65.91297265,
#     -90,
# ]

# clean_str = '\n{"pattern": "clean big", "absolute loc?": true, "location (default rel to fid 1)": [683.153, 365.306, 53.69], "orientation": 0 }'


# def print_positions(xlst, ylst, theta_lst, name, cleaning):
#     str = ""
#     for i, (x, y, theta) in enumerate(zip(xlst, ylst, theta_lst)):
#         s = f'{{ "pattern": "{name}", "location (default rel to fid 1)": [ {-y}, {x}, -10 ],  "orientation": {theta} }},'
#         if cleaning:
#             s += clean_str
#             if i < len(xlst) - 1:
#                 s = s + ","
#         str += s + "\n"
#     return str


# # print_positions(A_onextwo_x, A_onextwo_y, A_onextwo_theta, "1x2", cleaning=True)
# # print_positions(A_twoxtwo_x, A_twoxtwo_y, A_twoxtwo_theta, "2x2", cleaning=True)
# print('"pattern positions": [')
# print(print_positions(B_onextwo_x, B_onextwo_y, B_onextwo_theta, "1x2", cleaning=False))
# print(print_positions(B_twoxtwo_x, B_twoxtwo_y, B_twoxtwo_theta, "2x2", cleaning=False))
# print("]")

import os
from os.path import join
import cv2

base_path = "D:\\Documents\\Dragonfly data\\Junior fall\\Diamond plaquette 1"
files_path = join(base_path, "A tubing")
left_path = join(base_path, "A\\Left\\Left tube")
right_path = join(base_path, "A\\Right\\Right tube")
files = os.listdir(files_path)
for i, file in enumerate(files):
    raw = cv2.imread(join(files_path, file))
    # cv2.imshow("img", raw)
    # cv2.waitKey(0)
    left = cv2.imwrite(
        join(left_path, "tube " + str(i) + ".png"), raw[160:280, 100:265]
    )
    right = cv2.imwrite(
        join(right_path, "tube " + str(i) + ".png"), raw[160:260, 370:510]
    )
