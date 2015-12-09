#!/usr/bin/env python

import webapp2
from models.course import Course

names = [
    'CS 1520: Web Applicaton Development',
    'CS 1550: Introduction to Operating Systems',
    'MATH 1000: Introduction to Statistics'
]


class SeedCourseHandler(webapp2.RequestHandler):

    def get(self):
        [Course.new(name) for name in names]
        self.response.write('Seed Complete!')
