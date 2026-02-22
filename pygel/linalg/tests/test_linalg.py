from pygel.linalg import Array

data1 = [[1.0, 2.0], [3.0, 4.0]]
data2 = [[5.0, 6.0], [7.0, 8.0]]

a = Array(data1)
b = Array(data2)

def test_matrix_addition_simple():

    c = a + b

    assert c[0, 0] == 6.0
    assert c[0, 1] == 8.0
    assert c[1, 0] == 10.0
    assert c[1, 1] == 12.0


def test_matrix_matmul_simple():
    c = a @ b

    assert c[0, 0] == 19.0
    assert c[0, 1] == 22.0
    assert c[1, 0] == 43.0
    assert c[1, 1] == 50.0

