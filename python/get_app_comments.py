#! /usr/bin/env python
#coding=utf8

import urllib.request
import json
import xlsxwriter
print("这是一个在线获取appstore里任意app的评论列表工具")
print("运行完毕后 将生成一个名为“app评论.xlsx”的文件")

#appid=input("请输入应用id号:");
appid=1441648201
workbook = xlsxwriter.Workbook('app评论.xlsx')
count=0
for cc in ["cn","us","sa"]:
    worksheet = workbook.add_worksheet(cc)
    format=workbook.add_format()
    format.set_border(1)
    format.set_border(1)
    format_title = workbook.add_format()    
    format_title.set_border(1)   
    format_title.set_bg_color('#cccccc')
    format_title.set_align('left')
    format_title.set_bold()    
    title=['昵称','标题','评论内容','评分','时间']
    worksheet.write_row('A1',title,format_title)
    row=1
    col=0

    myurl="https://itunes.apple.com/WebObjects/MZStore.woa/wa/userReviewsRow?cc="+str(cc)+"&id="+str(appid)+"&displayable-kind=11&startIndex=0&endIndex=100&sort=0&appVersion=all"
    
    req = urllib.request.Request(
        myurl, 
        data=None, 
        headers={
            'User-Agent': 'iTunes/11.0 (Windows; Microsoft Windows 7 Business Edition Service Pack 1 (Build 7601)) AppleWebKit/536.27.1'
        }
    )

    #myurl="https://itunes.apple.com/rss/customerreviews/page="+str(page)+"/id="+str(appid)+"/sortby=mostrecent/json?l=en&&cc="+str(cc)
    response = urllib.request.urlopen(req)
    myjson = json.loads(response.read().decode())
    print("["+str(cc)+"]正在生成数据文件，请稍后......")
    if 'userReviewList' in myjson:
        count+=len(myjson["userReviewList"])
        for item in myjson["userReviewList"]:
            worksheet.write(row,col,item["name"],format)
            worksheet.write(row,col+1,item["title"],format)
            worksheet.write(row,col+2,item["body"],format)
            worksheet.write(row,col+3,item["rating"],format)
            worksheet.write(row,col+4,item["date"],format)
            row+=1
    else:
        print("")
        break

if count==0:
    print("运行完毕，未获取到任何数据。请检查是否输入正确！")
else:
    print("生成完毕，请查阅相关文件,共获取到"+str(count)+"条数据")
workbook.close()
