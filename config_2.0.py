circuit1=[
    [
     [
    """
    R3 0 1 ;up
    W 1 2 ;up
    W 2 3 ;right
    W 3 4 ;right
    W 4 5 ;down
    R2 5 6 ;down
    W 6 7 ;left
    SW 7 0  no 0;left=1
    C 3 8 ;down
    R1 8 7 ;down
    W 5 9 ;right
    W 6 10 ;right
    V 9 10 ;down
        """
     ]








    ]

]

circuit2 = [
    [
        [
            """
            R1 0 1 ;up
            SW 1 2  no 0;up=1
            W 2 3 ;right
            W 3 4 ;right
            W 4 5 ;down
            R2 5 6 ;down
            W 6 7 ;left
            L 7 0 ;left
            C 3 8 ;down
            R3 8 7 ;down
            W 5 9 ;right
            W 6 10 ;right
            V 9 10 ;down
                """
        ],

    ]

]