from pygel.linalg import Array


def test_matrix_addition_simple():
    data1 = [[1.0, 2.0], [3.0, 4.0]]
    data2 = [[5.0, 6.0], [7.0, 8.0]]

    a = Array(data1)
    b = Array(data2)

    c = a + b

    assert c[0, 0] == 6.0
    assert c[0, 1] == 8.0
    assert c[1, 0] == 10.0
    assert c[1, 1] == 12.0
