#!/usr/bin/python3


danceEventClasses = {
#'CreateContext': 1,
#'DeleteContext': 2,
#'MergeProperty': 3,
#'DeleteProperty': 4,
#'MomentStart': 5,
#'MomentEnd': 6,
#'Finish': 7,

'Move': 10,
'Rest': 11,
'BeatsPerBarChange': 20,
'TempoChange': 21
}

danceEventClassesToString = {v:k for k, v in danceEventClasses.items()}
