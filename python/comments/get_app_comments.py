#! /usr/bin/env python
# coding=utf8

import json
from urllib import request
from datetime import datetime
import xlsxwriter
import math
import time
import random
import os
import sys


class GetComments(object):

    def get_comments(self, app_id, country, app_file):
        from comments.comment import Comment
        file_name = './comments/app_comments_%s.xlsx' % app_file
        workbook = xlsxwriter.Workbook(file_name)
        worksheet = workbook.add_worksheet('comments')
        sheet_format = workbook.add_format()
        sheet_format.set_border(1)
        sheet_format.set_border(1)
        format_title = workbook.add_format()
        format_title.set_border(1)
        format_title.set_bg_color('#cccccc')
        format_title.set_align('left')
        format_title.set_bold()
        title = ['评分', '昵称', '评论内容', '时间', '国家']
        worksheet.write_row('A1', title, format_title)

        all_comments = []

        count = 0
        page = 50
        for cc in country:
            total = country[cc]
            page_count = math.ceil(country[cc] / page)
            for index in range(page_count):
                start = index * page
                end = (index + 1) * page
                if end > total:
                    end = total

                url = 'https://itunes.apple.com/WebObjects/MZStore.woa/wa/userReviewsRow?cc=%s&id=%s&displayable-kind=11' \
                      '&startIndex=%s&endIndex=%s&sort=0&appVersion=all' % (cc, app_id, start, end)

                print('[%s_get_comments] country: %s start : %s end: %s  load ...' % (app_file, cc, start, end))

                user_agent_list = [
                    "iTunes/11.0 (Windows; Microsoft Windows 7 Business Edition Service Pack 1 (Build 7601)) AppleWebKit/536.27.1",
                    "iTunes/11.0 (Windows; Microsoft Windows 8 Business Edition Service Pack 1 (Build 7601)) AppleWebKit/536.27.2",
                    "iTunes/11.0 (Windows; Microsoft Windows 7 Business Edition Service Pack 2 (Build 7603)) AppleWebKit/536.27.2",
                    "iTunes/12.0 (Windows; Microsoft Windows 7 Business Edition Service Pack 3 (Build 7601)) AppleWebKit/536.27.1",
                    "iTunes/11.0 (Windows; Microsoft Windows 8 Business Edition Service Pack 2 (Build 7701)) AppleWebKit/536.27.1"
                    ]
                user_agent = random.choice(user_agent_list)

                req = request.Request(
                    url,
                    data=None,
                    headers={
                        'User-Agent': user_agent
                    }
                )

                # load: {'userReviewList': [
                #     {'userReviewId': '5340579214', 'body': 'Everything&#39;s good! Outfits are perfect, but too much ads!!!',
                #      'date': '2019-12-31T00:24:34Z', 'name': 'raveilei', 'rating': 4, 'title': 'Too much ads!', 'voteCount': 0,
                #      'voteSum': 0, 'isEdited': False,
                #      'viewUsersUserReviewsUrl': 'https://itunes.apple.com/cn/reviews?userProfileId=477539462',
                #      'voteUrl': 'https://userpub.itunes.apple.com/WebObjects/MZUserPublishing.woa/wa/rateUserReview?userReviewId=5340579214',
                #      'reportConcernUrl': 'https://userpub.itunes.apple.com/WebObjects/MZUserPublishing.woa/wa/reportAConcernSubmit?cc=cn',
                #      'reportConcernExplanation': '请提供关于此篇“超级造型师”评论的详细信息。评论作者不会看到您的报告。', 'customerType': 'Customers',
                #      'reportConcernReasons': [{'reasonId': '0', 'name': '选取一个'},
                #                               {'reasonId': '1', 'name': '此评论含有令人反感的内容', 'upperCaseName': '此评论含有令人反感的内容'},
                #                               {'reasonId': '8', 'name': '此评论偏离主题', 'upperCaseName': '此评论偏离主题'},
                #                               {'reasonId': '111003', 'name': '疑似垃圾内容', 'upperCaseName': '疑似垃圾内容'},
                #                               {'reasonId': '7', 'name': '其他原因', 'upperCaseName': '其他原因'}]},
                #     ]}

                response = request.urlopen(req)
                json_data = json.loads(response.read().decode())

                # print('[get_comments]data: %s' % json_data)

                cur_dict = {}

                if 'userReviewList' in json_data:
                    count += len(json_data['userReviewList'])
                    for item in json_data['userReviewList']:
                        date = datetime.strptime(item['date'], '%Y-%m-%dT%H:%M:%SZ')
                        comment = Comment(item['name'], item['title'], item['body'], item['rating'], date, cc)
                        all_comments.append(comment)
                        cur_dict[item['userReviewId']] = comment
                else:
                    print("")
                    break

                sleep_time = random.randint(5, 7)
                time.sleep(sleep_time)

        all_comments.sort(key=lambda cm: cm.date, reverse=True)

        row = 1
        col = 0
        for comment in all_comments:
            worksheet.write(row, col, comment.rating, sheet_format)
            worksheet.write(row, col + 1, comment.name, sheet_format)
            worksheet.write(row, col + 2, comment.title + "\n" + comment.body, sheet_format)
            date = comment.date.strftime('%Y-%m-%d %H:%M:%S')
            worksheet.write(row, col + 3, date, sheet_format)
            worksheet.write(row, col + 4, comment.country, sheet_format)
            row += 1

        print("[%s_get_comments]finish! total: %s " % (app_file, count))
        workbook.close()


if __name__ == '__main__':
    path = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), os.path.pardir))
    os.chdir(path)
    # print(path)
    # print(os.getcwd())
    # print(sys.path)

    sys.path.append(path)

    if len(sys.argv) < 2:
        print('请输入App的名字(config文件的后缀)')
        pass

    app = sys.argv[1]

    # print('%s %s %s' % (app, mark, file))

    load_dict = {}

    print("[%s] begin ..." % app)
    with open('./comments/config_%s.json' % app, 'r') as load_f:
        load_dict = json.load(load_f)

    print("[%s] %s" % (app, load_dict))

    com = GetComments()
    com.get_comments(load_dict['app_id'], load_dict['country'], app)

    print("all done!")



# {
#   "country": {
#     "us": 20,
#     "cn": 10
#   },
#   "app_id": "1441648201"
# }