#!/usr/bin/env python

import webapp2
from models.course import Course

names = [
    'CS 445: Data Structures',
    'CS 447: Computer Organization and Assembly Language',
    'CS 1520: Web Applicaton Development',
    'CS 1550: Introduction to Operating Systems',
    'CS 1571: Introduction to Artificial Intelligence',
    'CS 1632: Software Quality Assurance',
    'CS 2730: Introduction to Natural Language Processing',
    'MATH 1000: Introduction to Statistics'
]


class SeedCourseHandler(webapp2.RequestHandler):

    def get(self):
        [Course.new(name) for name in names]
        self.response.write('Seed Complete!')
