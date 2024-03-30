EXAMPLE = [{"position": (19, 13, 30), "velocity": (-2,  1, -2)},
           {"position": [18, 19, 22] , "velocity": [-1, -1, -2]},
            {"position": [20, 25, 34] , "velocity": [-2, -2, -4]},
             {"position": [12, 31, 28] , "velocity": [-1, -2, -1]},
              {"position": [20, 19, 15] , "velocity": [ 1, -5, -3]}]

def test_part_one():
    assert part_one(EXAMPLE, 7 , 27) == 2
