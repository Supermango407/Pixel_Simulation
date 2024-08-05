import pygame
import math

def black_and_white(color):
    r, g, b = color
    value = (r + g + b)/3
    return (value, value, value)

def border(x, y, time, command):
    gray_scale = black_and_white(command(x, y, time))[0]

    if black_and_white(command(x-1, y, time))[0] < gray_scale and black_and_white(command(x+1, y, time))[0] < gray_scale:
        return (0, 0, gray_scale)
    
    if black_and_white(command(x, y-1, time))[0] < gray_scale and black_and_white(command(x, y+1, time))[0] < gray_scale:
        return (0, 0, gray_scale)
    
    return (gray_scale, gray_scale, gray_scale)
