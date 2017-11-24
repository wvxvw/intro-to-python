# -*- coding: utf-8 -*-


def area_of_triangle(base, height):
    '''
    Computes area of triangle in Euclidean geometry.
    :param base: An integer or a float, the base of the triangle
    :param height: An integer or a float, the height of the triangle
    '''
    # This ignores the fact that neither float nor integer division
    # commutes with multiplication, this is why the result may not
    # be what you expect it to be.  If you expected the division
    # to happen first, you should roll your own area_of_triangle
    # function.
    area = base * height / 2
    # The extra line added here is for the purposes of debugging.
    return area
