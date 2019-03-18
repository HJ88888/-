import pymysql
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
pymysql.install_as_MySQLdb()
import json

import re
import os
import urllib.request
import requests
from bs4 import BeautifulSoup
import threading


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:123456@localhost:3306/douban"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
db = SQLAlchemy(app)
class Book_info(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    book_type = db.Column(db.String(30))   # 书籍类别
    r_name = db.Column(db.String(50))      # 书名
    t_name = db.Column(db.String(50))      # 别名
    url = db.Column(db.String(80))         # 书链接
    img_name = db.Column(db.String(80))    # 图片文件名
    info = db.Column(db.Text)              # 书籍信息
    score = db.Column(db.String(30))       # 评分
    nums = db.Column(db.Integer)        # 评价人数
    ds = db.Column(db.Text)                # 描述
    # img_url = db.Column(db.String(80))     # 图片链接
    # pictute = db.Column(db.Text)         # 图片二进制格式
    # book_intro = db.Column(db.Text)      # 书籍简介
    # author_intro = db.Column(db.Text)    # 内容简介
    def add_book(self,book_type,r_name,t_name,url,img_name,info,score,nums,ds):
        self.book_type = book_type
        self.r_name = r_name
        self.t_name = t_name
        self.url = url
        self.img_name = img_name
        self.info = info
        self.score = score
        self.nums = nums
        self.ds = ds
        # book.img_url = img_url
        # book.pictute = pictute
        # book.book_intro = b_intro
        # book.author_intro = a_intro
        db.session.add(self)
        db.session.commit()
        return "添加成功"
    def to_dict(self):
        book_dict={'id':self.id,"r_name":self.r_name,"t_name":self.t_name,"url":self.url,
        "img_name":self.img_name,"info":self.info,"score":self.score,"nums":self.nums,"ds":self.ds}
        return  book_dict

db.create_all()


def book(tmp_url,target_url):
    book = requests.get(target_url) #使用requests返回网页的整体结构
    soup = BeautifulSoup(book.text,'lxml') # 使用lxml作为解析器，返回一个Beautifulsoup对象
    li = soup.findAll('li', {"class": "subject-item"}) #找到其中所有class=subjec-item的li标签），即找到所有的书
    if len(li) == 0:
        return False
    for item in li: #遍历li，一个item代表一本书
        name = item.find('div',{"class":"info"}).a.text.strip() #找到书名
        r_name = name.replace("\n","").replace(' ','') #通过看通过看网页的HTML结构，可以发现书名后是有换行以及空格的，将这些全部通过replace替换去除
        url = item.find('div',{"class":"info"}).a['href'] #获取书的链接
        if ":" in r_name:  #判断是否存在别名
            s_name = r_name.split(':')
            r_name = s_name[0]
            t_name = s_name[1] #因为是通过div.span判断别名 有些书的别名前面有个冒号，比如《三体系列》
        else:
            t_name = '' #无别名就使用原始的名称
        img_url = item.div.img["src"] #获取图片链接
        img_name = img_url.split('/')[-1] #得到图片名
        result = urllib.request.urlopen(img_url)  #发送图片请求
        pictute = result.read()  #得到二进制形式的图片
        get_img(tmp_url,img_name, pictute)    #保存图片到本地
        info = item.find('div',{"class":"pub"}).text.replace("\n","").replace(' ','') #获取书的信息
        score = item.find('div', {'class': 'star clearfix'}).find('span',{'class': 'rating_nums'})
        if not score:
            score = 0
        else:
            score = score.text.strip()   #获取评价分数
        # score = item.find('div',{'class':'star clearfix'}).find('span',
        #                             {'class':'rating_nums'}).text.strip() #获取评价分数
        nums = item.find('div',{'class':'info'}).find('span',{'class':'pl'})
        if nums:
            nums = nums.text.strip().replace('(','').replace(')','')  # 获取评价人数
            nums = int(re.sub(r"\D", '', nums))  # 替换掉非数字字符,得到评价人数的整数
        else:
            nums = 0
        ds = item.find('div', {'class': 'info'}).p  #获得描述
        if ds: # 判断是否存在描述
            ds = ds.text.strip().replace("\n","").replace('"',"")
        else:
            ds = ''
        book_type = tmp_url

        # sql = "insert into books(book_type,r_name,t_name,url,img_name,info,score,nums,ds) values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (book_type,r_name,t_name,url,img_name,info,score,nums,ds)
        # try:
        #     cursor.execute(sql)
        #     db.commit()
        # except:
        #     db.rollback()
        u = Book_info.query.filter_by(url=url).first()
        if u:
            print('已存在')

        bookl = Book_info()
        bookl.add_book(book_type,r_name,t_name,url,img_name,info,score,nums,ds)
        print("成功添加一本书籍")

def seek(tmp_url,url_number=None):
    for n in range(2):
        url1 = 'https://book.douban.com/tag/'+tmp_url+'?start=' + str(n*20)  #网页，每页20本书，共100页，“start=”后面从0开始，以20递增
        book(tmp_url,url1)
    # t1_url = 'https://book.douban.com/tag/'+tmp_url+'?start=' + str((url_number-2)*20)
    # t2_url = 'https://book.douban.com/tag/' + tmp_url + '?start=' + str((url_number - 1) * 20)
    # t1 = threading.Thread(target=book,args=(tmp_url,t1_url,))
    # t2 = threading.Thread(target=book, args=(tmp_url,t2_url,))
    # t1.start()
    # t2.start()
    return 'OK'

def seek1(tmp_url,book_N,st):
    ns = book_N*30
    bkN = len(bks) // 20 + 1
    while True:
        bks = Book_info.query.filter_by(book_type=tmp_url).all()
        if len(bks)<ns:
            url1 = 'https://book.douban.com/tag/' + tmp_url + '?start=' + str(bkN * 20)
            book(tmp_url, url1)
            bkN += 1
        else:
            if st != None and not st:
                ob = st + " desc"
                bk = Book_info.query.filter_by(book_type=tmp_url).order_by(ob).limit(30).offset(ns).all()
            else:
                bk = Book_info.query.filter_by(book_type=tmp_url).limit(30).offset(ns).all()
    return bk


def get_img(tmp_url,img_name,pictute):
    url_path = "./static/images/"+tmp_url
    if not os.path.exists(url_path):
        os.makedirs(url_path)
    with open(url_path+"/"+img_name,'wb') as f:
        f.write(pictute)

# @app.route('/',methods=["GET","POST"])
@app.route('/book',methods=["GET","POST"])
def look_book():
    if request.method == "GET":
        if not Book_info.query.filter_by(book_type="小说").first():
            seek("小说")
        books = Book_info.query.filter_by(book_type="小说").order_by("id asc").limit(30).all()
        return render_template('books.html', books=books)
    else:
        type = request.form.get("book_type")
        if not Book_info.query.filter_by(book_type=type).first():
            seek(type)
        bk = Book_info.query.filter_by(book_type=type).order_by("id asc").limit(30).all()
        books = []
        for book in bk:
            books.append(book.to_dict())
        jsonStr = json.dumps(books)
        return jsonStr

@app.route('/book_TN',methods=["GET","POST"])
def look_book_TN():
    if request.method == "GET":
        type = request.args.get('b_type')
        T = request.args.get('T')
        if T == 'S':
            bk = Book_info.query.filter_by(book_type=type).order_by("score desc").limit(30).all()
        else:
            bk = Book_info.query.filter_by(book_type=type).order_by("nums desc").limit(30).all()
    else:
        type = request.form.get('book_type')
        papg = request.form.get('pape')
        book_N = int(request.form.get('book_N'))
        st = request.form.get('st')
        print(type,papg,book_N,st)
        if papg == 'previous':
            ns = (book_N-1)*30
            if st != 'D':
                ob = st + " desc"
                bk = Book_info.query.filter_by(book_type=type).order_by(ob).limit(30).offset(ns).all()
            else:
                bk = Book_info.query.filter_by(book_type=type).limit(30).offset(ns).all()
        else:
            ns = book_N * 30
            bks1 = Book_info.query.filter_by(book_type=type).all()
            bkN = len(bks1)//20 + 1
            while True:
                bks2 = Book_info.query.filter_by(book_type=type).all()
                if len(bks2) < ns:
                    url1 = 'https://book.douban.com/tag/' + type + '?start=' + str(bkN * 20)
                    book(type,url1)
                    bkN += 1
                else:
                    if st == 'S':
                        bk = Book_info.query.filter_by(book_type=type).order_by('score desc').limit(30).offset(ns-30).all()
                    elif st == "C":
                        bk = Book_info.query.filter_by(book_type=type).order_by('nums desc').limit(30).offset(ns-30).all()
                    else:
                        bk = Book_info.query.filter_by(book_type=type).limit(30).offset(ns-30).all()
                    break
    books = []
    for book1 in bk:
        books.append(book1.to_dict())
    jsonStr = json.dumps(books)
    return jsonStr






@app.route('/add')
def add():
    seek1('小说',3,'score')
    # bk = Book_info.query.filter_by(book_type='小说').order_by('score desc').limit(30).offset(1).all()
    print(bk)
    return 'ok'

@app.route('/s')
def ss():
    # books = Book_info.query.filter_by(book_type="小说").order_by("score desc").limit(30).all()
    # for book in books:
    book = Book_info.query.filter_by(id=1).first()
    print(book.to_dict())
    return '显示成功'

def f1():
    f2 = [lambda x:x+i for i in range(4)]
    return f2
# for xm in f1():
#     print(xm(3))



def a():
    L = []
    for i in range(4):
        def b(ax):
           return ax+i
        L.append(b)
    return L
# for xy in a():
#     print(xy(3))




if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
