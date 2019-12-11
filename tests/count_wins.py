#!/usr/bin/python3

file = open('results.log', 'r').read()
print("Black wins:", file.count("Black wins"))
print("White wins:", file.count("White wins"))
print("Games drawn:", file.count("Game drawn"))
