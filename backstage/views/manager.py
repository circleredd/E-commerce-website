from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from link import *
from api.sql import *
import imp, random, os, string
from werkzeug.utils import secure_filename
from flask import current_app
import os
import cv2
import numpy as np

UPLOAD_FOLDER = 'static/product'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

manager = Blueprint('manager', __name__, template_folder='../templates')

def config():
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    config = current_app.config['UPLOAD_FOLDER'] 
    return config

@manager.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return redirect(url_for('manager.productManager'))

@manager.route('/productManager', methods=['GET', 'POST'])
@login_required
def productManager():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))
        
    if 'delete' in request.values:
        pid = request.values.get('delete')
        data = Record.delete_check(pid)
        
        if(data != None):
            flash('failed')
        else:
            data = Product.get_product(pid)
            img_path = data[5]
            if(img_path != ""): ###檢查picture欄位是否有值，若有就把該路徑的圖片檔刪除
                try:
                    os.remove(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + img_path) ###將該商品圖片從server端刪除
                except:
                    pass

            Product.delete_product(pid) #刪除該商品值
    
    elif 'edit' in request.values:
        pid = request.values.get('edit')
        return redirect(url_for('manager.edit', pid=pid))
    
    book_data = book()
    return render_template('productManager.html', book_data = book_data, user=current_user.name)

def book():
    book_row = Product.get_all_product()
    book_data = []
    for i in book_row:
        book = {
            '商品編號': i[0],
            '商品名稱': i[1],
            '商品售價': i[2],
            '商品類別': i[3],
            '商品圖片': i[5],       ###新增回傳商品圖片
        }
        book_data.append(book)
    return book_data

@manager.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = ""
        #令img為空
        img = ""
        while(data != None):
            number = str(random.randrange( 10000, 99999))
            en = random.choice(string.ascii_letters)
            pid = en + number
            data = Product.get_product(pid)

        name = request.values.get('name')
        price = request.values.get('price')
        category = request.values.get('category')
        description = request.values.get('description')
        
        ####################儲存圖片到server端####################
        img = request.files['file']
        img_path = ""
        #若有接收到圖片，將它儲存到server端指定路徑
        if(img.filename != ""):
            #path = '/static/uploads/xxx.jpg'
            img_path = save_img(img, pid)
            crop_img(img_path)

        if (len(name) < 1 or len(price) < 1):
            return redirect(url_for('manager.productManager'))
        
        Product.add_product(
            {'pid' : pid,
             'name' : name,
             'price' : price,
             'category' : category,
             'description':description,
             'picture':img_path
            }
        )

        return redirect(url_for('manager.productManager'))

    return render_template('productManager.html')

####用來上傳的商品圖片名稱加上pid後儲存到server端指定資料夾，並回傳路徑
def save_img(img, pid):
    imgname = secure_filename(img.filename)
    #path = '/static/uploads/xxx.jpg'
    img_path = 'static/uploads/'+pid+'_'+imgname
    img.save(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), img_path))
    return '/' + img_path

####將商品圖品裁切至1:1
def crop_img(img_path):
    img = cv2.imread(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + img_path)
    x_mid, y_mid = int(img.shape[1]/2), int(img.shape[0]/2) #找出長度寬度中點
    if(y_mid > x_mid):  
        crop_img = img[y_mid-x_mid:y_mid+x_mid, 0:x_mid*2]  #若長>寬，將長度裁切成和寬度一樣
    else:
        crop_img = img[0:y_mid*2, x_mid-y_mid:x_mid+y_mid]  #若寬>長，將寬度裁切成和長度一樣
    cv2.imwrite(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + img_path, crop_img) 

@manager.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('bookstore'))
    
    #######################增加picture#########################
    if request.method == 'POST':
        pid = request.values.get('pid')
        img = request.files['file']
        ####如果有修改picture就update新的，並將舊的img檔案刪除，若img.filename為空值就用舊的###
        img_path = Product.get_picture(pid)
        if(img.filename != ""):
            if(img_path != ""):
                try:
                    os.remove(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + img_path) #將舊的圖片從server端刪除 
                except:
                    pass         
            img_path = save_img(img, pid)
            crop_img(img_path)
        else:
            pass

        Product.update_product(
            {
            'name' : request.values.get('name'),
            'price' : request.values.get('price'),
            'category' : request.values.get('category'), 
            'description' : request.values.get('description'),
            'pid' : request.values.get('pid'),
            'picture' : img_path
            }
        )        
        
        return redirect(url_for('manager.productManager'))

    else:
        product = show_info()
        return render_template('edit.html', data=product)


def show_info():    #新增商品照片
    pid = request.args['pid']
    data = Product.get_product(pid)
    pname = data[1]
    price = data[2]
    category = data[3]
    description = data[4]
    picture = data[5]

    product = {
        '商品編號': pid,
        '商品名稱': pname,
        '單價': price,
        '類別': category,
        '商品敘述': description,
        '商品照片': picture
    }
    return product


@manager.route('/orderManager', methods=['GET', 'POST'])
@login_required
def orderManager():
    # if request.method == 'POST':
    #     pass
    #else:
    order_row = Order_List.get_order()
    order_data = []
    for i in order_row:
        order = {
            '訂單編號': i[0],   
            '訂購人': i[1],
            '訂單總價': i[2],
            '訂單時間': i[3],
            '交易編號': i[4]
        }
        order_data.append(order)
        
    orderdetail_row = Order_List.get_orderdetail()
    order_detail = []

    for j in orderdetail_row:
        pid = j[5]
        picture = Product.get_picture(pid)
        orderdetail = {
            '訂單編號': j[0],   
            '商品名稱': j[1],
            '商品單價': j[2],
            '訂購數量': j[3],
            '交易編號': j[4],
            '商品圖片': picture
        }
        order_detail.append(orderdetail)

    if 'deleteOrder' in request.values:
        tno = request.values.get('deleteOrder')
        deleteOrder(tno)
        #重新載入頁面
        order_row = Order_List.get_order()
        order_data = []
        for i in order_row:
            order = {
                '訂單編號': i[0],   
                '訂購人': i[1],
                '訂單總價': i[2],
                '訂單時間': i[3],
                '交易編號': i[4]
            }
            order_data.append(order)
            
        orderdetail_row = Order_List.get_orderdetail()
        order_detail = []

        for j in orderdetail_row:
            pid = j[5]
            picture = Product.get_picture(pid)
            orderdetail = {
                '訂單編號': j[0],   
                '商品名稱': j[1],
                '商品單價': j[2],
                '訂購數量': j[3],
                '交易編號': j[4],
                '商品圖片': picture
            }
            order_detail.append(orderdetail)

    
    return render_template('orderManager.html', orderData = order_data, orderDetail = order_detail, user=current_user.name)


def deleteOrder(tno):    
    for i in range(50):
        print(tno)
    Order_List.delete_order(tno)
    Record.delete_order(tno)  
        