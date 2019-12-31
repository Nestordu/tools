#! /usr/bin/env python
# coding=utf8

# worksheet.write(row, col, item["name"], sheet_format)
# worksheet.write(row, col + 1, item["title"], sheet_format)
# worksheet.write(row, col + 2, item["body"], sheet_format)
# worksheet.write(row, col + 3, item["rating"], sheet_format)
# worksheet.write(row, col + 4, item["date"], sheet_format)
import json


class Comment(object):
    def __init__(self, name, title, body, rating, date, country):
        self.name = name
        self.title = title
        self.body = body
        self.rating = rating
        self.date = date
        self.country = country

    def print_msg(self):
        print("%s %s" % (self.name, self.title))

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
