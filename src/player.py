# -*- coding: utf-8 -*-

"""
EasyLeague Player Class

This class stores the data about a player

Author: John Hsu

"""

class Player:

    def __init__(self):
        self.memberID = None
        self.lastName = None
        self.firstName = None
        self.middleName = None
        self.sex = None
        self.rating = None
        self.expiration = None
        self.lastPlayed = None
        self.email = None

    def __str__(self):
        return self.firstName + " " + self.lastName
