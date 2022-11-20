import razorpay
from flask import *
from werkzeug.utils import secure_filename
import functools

import os
import folium

from src.dbconnectionnew import *
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail
app=Flask(__name__)
app.secret_key="12345"

mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'aneethawork@gmail.com'
app.config['MAIL_PASSWORD'] = 'AneethaAnu22'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True




def login_required(func):
    @functools.wraps(func)
    def secure_function():
        if "lid" not in session:
            return render_template('index_login.html')
        return func()
    return secure_function


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/')
def log():
    return render_template("index.html")


@app.route('/login_index')
def login_index():
    return render_template("index_login.html")


@app.route('/login', methods=['post'])
def login():
    username=request.form['un']
    password=request.form['pwd']
    qry=" SELECT * FROM `login`WHERE `username`=%s and`password`=%s"
    val=(username,password)
    res=selectone(qry,val)
    print(res)
    if res is None:
        return '''<script>alert("invaild");window.location="login_index"</script>'''
    elif res['username']==username and res['password']==password:
        if res['usertype']=="admin" :
            session['lid']=res['login_id']
            return '''<script>alert("vaild");window.location="adminhome"</script>'''
        elif res['usertype'] == "user":
            session['lid'] = res['login_id']
            q="SELECT `name` FROM `registration` WHERE `login_id`=%s "
            res1=selectone(q,res['login_id'])
            session['name'] = res1['name']
            return '''<script>alert("vaild");window.location="userhome"</script>'''
        elif res['usertype'] == "driver":
            session['lid'] = res['login_id']
            return '''<script>alert("vaild");window.location="driverhome"</script>'''
        else:
            return '''<script>alert("invaild");window.location="login_index"</script>'''

    else:
            return '''<script>alert("invaild");window.location="login_index"</script>'''



@app.route('/adminhome')
@login_required
def adminhome():
    return render_template('AdminHome.html')


@app.route('/admindash')
@login_required
def admindash():
    return render_template('AdminHome.html')


@app.route('/userhome')
@login_required
def userhome():
        return render_template('UserHome.html')


@app.route('/userdash')
@login_required
def userdash():
    return render_template('UserHome.html')


@app.route('/indexuser')
@login_required
def indexuser():
        return render_template('index_user.html')


@app.route('/reg')
def reg():
    return render_template('Registration.html')


@app.route('/reg_index')
def reg_index():
    return render_template('index_reg.html')



@app.route('/registration', methods=['post'])
def registration():
    name = request.form['nm']
    email = request.form['em']
    mobile = request.form['mob']
    address = request.form['add']
    college = request.form['clg']
    category = request.form['select']
    branch = request.form['brn']
    semester = request.form['sem']
    username = request.form['un']
    password = request.form['pwd']
    f = request.files['f']

    qry1="SELECT * FROM `registration` WHERE `email`=%s"
    res1 = selectone(qry1,email)

    if res1:
        return '''<script>alert("Email Already Exist");window.location="/" </script>'''
    else:
        qry2="SELECT * FROM `login` WHERE `username`=%s"
        res2 = selectone(qry2, username)

        if res2:
            return '''<script>alert("Username Already Exist");window.location="/" </script>'''
        else:
            qry = "INSERT INTO `login` VALUES(NULL,%s,%s,'user')"
            val = (username,password)
            lid = iud(qry,val)
            qry = "INSERT INTO `registration` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,'null')"
            val = (lid,name,email,mobile,address,college,category,branch,semester)
            iud(qry,val)
            f.save("static/user_img/"+str(lid)+".jpg")
            return '''<script>alert("Registration Success");window.location="/" </script>'''


    # lid=0
    # try:
    #     name = request.form['nm']
    #     email = request.form['em']
    #     mobile = request.form['mob']
    #     address = request.form['add']
    #     college = request.form['clg']
    #     category = request.form['select']
    #     branch = request.form['brn']
    #     semester = request.form['sem']
    #     username = request.form['un']
    #     password = request.form['pwd']
    #     f = request.files['f']
    #     qry = "INSERT INTO `login` VALUES(NULL,%s,%s,'user')"
    #     val = (username,password)
    #     lid = iud(qry,val)
    #     qry = "INSERT INTO `registration` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    #     val = (lid,name,email,mobile,address,college,category,branch,semester)
    #     iud(qry,val)
    #     f.save("static/user_img/"+str(lid)+".jpg")
    #     return '''<script>alert("Registration Success");window.location="/" </script>'''
    # except:
    #     if lid==0:
    #         qry = "DELETE FROM `login` WHERE login_id=%s"
    #         val = (lid)
    #         id = iud(qry, val)
    #         print("+++++++++++++++++++++++++++++++++++++++++++=")
    #         return '''<script>alert("Username already exists");window.location="/reg_index" </script>'''
    #     else:
    #         qry = "DELETE FROM `registration` WHERE login_id=%s"
    #         val = (lid)
    #         id = iud(qry, val)
    #         print("==================================================")
    #         return '''<script>alert("Email already exists");window.location="/reg_index" </script>'''



@app.route('/view_user')
@login_required
def view_user():
    qry = "SELECT * FROM registration"
    res = selectall(qry)
    return render_template('ViewUser.html', val=res)



@app.route('/view_route')
@login_required
def view_route():
    qry = "SELECT * FROM route"
    res = selectall(qry)
    return render_template('ViewRoute.html', val=res)


@app.route('/admin_view_route1')
def admin_view_route1():
    rid=request.args.get("id")

    qry="SELECT `stop_name`,`latitude`,`longitude`,`mrngtime`,`evngtime` FROM `stop` WHERE `route_id`=%s"
    res=selectall2(qry,rid)

    # my_map3 = folium.Map(location=[11.3400929,75.96622239999999], zoom_start=15)
    my_map3 = folium.Map(location=[11.3122, 75.9545], zoom_start=12)
    for i in res:
    # Pass a string in popup parameter
        folium.Marker([i['latitude'], i['longitude']], popup=i['stop_name']+"(M:"+str(i['mrngtime'])+",E:"+str(i['evngtime'])+")",icon=folium.Icon(color='red')).add_to(my_map3)


    #folium.Marker([i['latitude'], i['longitude']],popup=i['stop_name'] + "(M:" + str(i['mrngtime']) + ",E:" + str(i['evngtime']) + ")").add_to(my_map3)
    my_map3.save("templates/my_map31.html")

    return render_template('/my_map31.html')



@app.route('/add_route', methods=['post'])
def add_route():
    return render_template('AddRoute.html')


@app.route('/add_route1', methods=['post'])
def add_route1():
    rno = request.form['textfield']
    rcode = request.form['textfield2']
    rname = request.form['textfield3']
    qry = "INSERT INTO route VALUES(null,%s,%s,%s)"
    val=(rno, rcode, rname)
    iud(qry, val)
    return '''<script>alert("Inserted");window.location="view_route"</script>'''



@app.route('/edit_route')
def edit_route():
    id=request.args.get('id')
    session['edit_rid']=id
    qry="SELECT * FROM route WHERE `route_id`=%s"
    res=selectone(qry,id)
    return render_template('EditRoute.html',data=res)


@app.route('/edit_route1', methods=['post'])
def edit_route1():
    rno = request.form['textfield']
    rcode = request.form['textfield2']
    rname = request.form['textfield3']
    qry = "UPDATE route SET `route_no`=%s,`route_code`=%s,`route_name`=%s WHERE `route_id`=%s"
    val=(rno, rcode, rname,str(session['edit_rid']))
    iud(qry, val)
    return '''<script>alert("Updated sucessfully");window.location="view_route"</script>'''


@app.route('/delete_route')
def delete_route():
    id=request.args.get('id')
    qry="DELETE FROM route WHERE `route_id`=%s"
    iud(qry,id)
    return '''<script>alert("Deleted sucessfully");window.location="view_route"</script>'''




@app.route('/view_bus')
@login_required
def view_bus():
    # qry = "SELECT * FROM bus"
    # qry = "SELECT `bus`.*,`route`.`route_name` FROM bus JOIN route ON bus.`route_id`=`route`.`route_id`"
    qry="SELECT * FROM `bus` LEFT JOIN `route` ON `bus`.`route_id`=`route`.`route_id` "
    res = selectall(qry)
    return render_template('ViewBus.html', val=res)


@app.route('/add_bus', methods=['post'])
@login_required
def add_bus():
    qry="select * from route"
    res=selectall(qry)
    return render_template('AddBus.html',val=res)


@app.route('/add_bus1', methods=['post'])
def add_bus1():
    rname = request.form['select']
    bregno = request.form['textfield']
    bno = request.form['textfield2']
    bname = request.form['textfield3']
    bimage = request.files['textfield4']
    seat = request.form['textfield5']
    status = request.form['select1']
    fn=datetime.now().strftime("%Y%m%d%H%M%S")+".jpg"
    bimage.save("static/bus/"+fn)
    qry = "INSERT INTO bus VALUES(null,%s,%s,%s,%s,%s,%s,%s)"
    val=(rname,bregno, bno, bname, fn, seat, status)
    iud(qry, val)
    return '''<script>alert("Inserted");window.location="view_bus"</script>'''


@app.route('/edit_bus')
@login_required
def edit_bus():
    id=request.args.get('id')
    session['edit_rid']=id
    qry="SELECT * FROM bus WHERE `bus_id`=%s"
    res=selectone(qry,id)
    q="SELECT * FROM route"
    res1=selectall(q)
    return render_template('EditBus.html',data=res,data1=res1)




@app.route('/edit_bus1', methods=['post'])
def edit_bus1():
    try:
        rname=request.form['select']
        bregno = request.form['textfield']
        bno = request.form['textfield2']
        bname = request.form['textfield3']
        seat = request.form['textfield5']
        status = request.form['select1']
        img=request.files['f']
        fn=secure_filename(img.filename)
        img.save(os.path.join("static/bus",fn))
        bimage=fn
        qry = "UPDATE bus SET `route_id`=%s,`bus_regno`=%s,`bus_no`=%s,`bus_name`=%s,`bus_image`=%s,`seat`=%s,`status`=%s WHERE `bus_id`=%s"
        val=(rname,bregno,bno,bname,bimage,seat,status,str(session['edit_rid']))
        iud(qry, val)
        return '''<script>alert("Updated sucessfully with image");window.location="view_bus"</script>'''
    except:
        rname = request.form['select']
        bregno = request.form['textfield']
        bno = request.form['textfield2']
        bname = request.form['textfield3']
        # bimage = request.form['textfield4']
        seat = request.form['textfield5']
        status = request.form['select1']
        qry = "UPDATE bus SET `route_id`=%s,`bus_regno`=%s,`bus_no`=%s,`bus_name`=%s,`seat`=%s,`status`=%s WHERE `bus_id`=%s"
        val = (rname,bregno, bno, bname, seat, status, str(session['edit_rid']))
        iud(qry, val)
        return '''<script>alert("Updated sucessfully without image");window.location="view_bus"</script>'''



@app.route('/delete_bus')
def delete_bus():
    id=request.args.get('id')
    qry="DELETE FROM bus WHERE `bus_id`=%s"
    iud(qry,id)
    return '''<script>alert("Deleted sucessfully");window.location="view_bus"</script>'''




@app.route('/view_driver')
@login_required
def view_driver():
    qry = "SELECT * FROM driver"
    res = selectall(qry)
    return render_template('ViewDriver.html', val=res)


@app.route('/add_driver', methods=['post'])
@login_required
def add_driver():
    return render_template('AddDriver.html')


@app.route('/add_driver1', methods=['post'])
def add_driver1():
    try:
        dname = request.form['textfield2']
        daddress = request.form['textfield3']
        dimage = request.files['textfield4']
        demail = request.form['textfield5']
        dmob = request.form['textfield6']
        dlicense = request.form['textfield7']
        dstatus = request.form['select']
        fn = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
        dimage.save("static/driver/" + fn)
        q="INSERT INTO `login` VALUES(NULL,%s,%s,'driver')"
        v=(demail,dmob)
        id=iud(q,v)
        qry = "INSERT INTO driver VALUES(null,%s,%s,%s,%s,%s,%s,%s,%s)"
        val =(str(id), dname, daddress, fn, demail, dmob, dlicense, dstatus)
        iud(qry, val)
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('aneethawork@gmail.com', 'wtmbqwyvrrdfjvdf')
        except Exception as e:
            print("Couldn't setup email!!" + str(e))
        msg = MIMEText("Hello" + dname + "\nYou can Login to Quickbus Account using the login credentials: \nUsername : " + demail+ "\nPassword : " + dmob)
        print(msg)
        msg['Subject'] = 'Driver Login'
        msg['To'] = demail
        msg['From'] = 'aneethawork@gmail.com'
        try:
            gmail.send_message(msg)
        except Exception as e:
            print("COULDN'T SEND EMAIL", str(e))

        return '''<script>alert("Inserted");window.location="view_driver"</script>'''

    except Exception as e:
        return '''<script>alert("Email already exist");window.location="view_driver"</script>'''



@app.route('/edit_driver')
@login_required
def edit_driver():
    id=request.args.get('id')
    session['edit_rid']=id
    qry="SELECT * FROM driver WHERE `driver_id`=%s"
    res=selectone(qry,id)
    return render_template('EditDriver.html',data=res)


@app.route('/edit_driver1', methods=['post'])
def edit_driver1():
    try:
        # dno = request.form['textfield']
        dname = request.form['textfield2']
        daddress = request.form['textfield3']
        demail = request.form['textfield5']
        dmob = request.form['textfield6']
        dlicense = request.form['textfield7']
        dstatus = request.form['select']
        img=request.files['f']
        fn = secure_filename(img.filename)
        img.save(os.path.join("static/driver", fn))
        dimage=fn
        qry = "UPDATE driver SET `driver_name`=%s,`driver_address`=%s,`driver_image`=%s,`driver_email`=%s,`driver_mobile`=%s,`driver_license`=%s,`status`=%s WHERE `driver_id`=%s"
        val=(dname, daddress, dimage, demail, dmob, dlicense, dstatus, str(session['edit_rid']))
        res=iud(qry, val)
        return '''<script>alert("Updated sucessfully with image");window.location="view_driver"</script>'''

    except:
        # dno = request.form['textfield']
        dname = request.form['textfield2']
        daddress = request.form['textfield3']
        demail = request.form['textfield5']
        dmob = request.form['textfield6']
        dlicense = request.form['textfield7']
        dstatus = request.form['select']
        qry = "UPDATE driver SET `driver_name`=%s,`driver_address`=%s,`driver_email`=%s,`driver_mobile`=%s,`driver_license`=%s,`status`=%s WHERE `driver_id`=%s"
        val = (dname, daddress, demail, dmob, dlicense, dstatus, str(session['edit_rid']))
        iud(qry, val)
        return '''<script>alert("Updated sucessfully without image");window.location="view_driver"</script>'''



@app.route('/delete_driver')
def delete_driver():
    id=request.args.get('id')
    qry="DELETE FROM driver WHERE `driver_id`=%s"
    iud(qry,id)
    return '''<script>alert("Deleted sucessfully");window.location="view_driver"</script>'''




@app.route('/view_stop')
@login_required
def view_stop():
    q="SELECT * FROM `route`"
    r=selectall(q)
    return render_template('ViewStop.html',v=r)



@app.route('/add_stop', methods=['post','get'])
@login_required
def add_stop():
    qry="select * from route"
    res=selectall(qry)
    return render_template('AddStop.html',val=res)



@app.route('/add_stop1', methods=['post'])
def add_stop1():
    rname = request.form['select']
    sname = request.form['textfield1']
    sfees = request.form['textfield2']
    lat = request.form['textfield3']
    lon = request.form['textfield4']
    mrng = request.form['textfield5']
    evng = request.form['textfield6']
    qry = "INSERT INTO stop VALUES(null,%s,%s,%s,%s,%s,%s,%s)"
    val =(rname, sname, sfees, lat, lon, mrng, evng)
    iud(qry, val)
    return '''<script>alert("Inserted");window.location="view_stop"</script>'''



@app.route('/edit_stop')
def edit_stop():
    id=request.args.get('id')
    session['edit_rid']=id
    qry="SELECT * FROM stop WHERE `stop_id`=%s"
    res=selectone(qry,id)
    q="SELECT * FROM route"
    res1=selectall(q)
    return render_template('EditStop.html',data=res,data1=res1)


@app.route('/edit_stop1', methods=['post'])
def edit_stop1():
    rno = request.form['select']
    sname = request.form['textfield1']
    sfees = request.form['textfield2']
    lat = request.form['textfield3']
    lon = request.form['textfield4']
    mrng = request.form['textfield5']
    evng = request.form['textfield6']
    qry = "UPDATE stop SET `route_id`=%s,`stop_name`=%s,`stop_fees`=%s,`latitude`=%s,`longitude`=%s,`mrngtime`=%s,`evngtime`=%s WHERE `stop_id`=%s"
    val=(rno, sname, sfees, lat, lon, mrng, evng, str(session['edit_rid']))
    iud(qry, val)
    return '''<script>alert("Updated sucessfully");window.location="view_stop"</script>'''


@app.route('/delete_stop')
def delete_stop():
    id=request.args.get('id')
    qry="DELETE FROM stop WHERE `stop_id`=%s"
    iud(qry,id)
    return '''<script>alert("Deleted sucessfully");window.location="view_stop"</script>'''




@app.route('/search_stop',methods=['post'])
def search_stop():
    route=request.form['select']
    qry = "SELECT `stop`.*,`route`.`route_name` FROM STOP JOIN route ON stop.`route_id`=`route`.`route_id` WHERE `route`.`route_id`=%s"
    res = selectall2(qry,route)
    q = "SELECT * FROM `route`"
    r = selectall(q)
    return render_template('ViewStop.html', val=res,v=r)







@app.route('/view_payment')
@login_required
def view_payment():
    qry = "select * from bus where status='active'"
    res = selectall(qry)
    return render_template('ViewPayment.html', val=res)




@app.route('/view_payment1',methods=['post'])
@login_required
def view_payment1():
    bid=request.form['select']
    year = request.form['select1']
    month=request.form['select2']
    qry1 = "select * from bus where status='active'"
    res = selectall(qry1)
    qry = "SELECT `payment`.*,`registration`.`name`,`stop`.`stop_name` FROM  `payment` JOIN `registration` ON `registration`.`login_id`=`payment`.`login_id` JOIN `stop` ON `stop`.`stop_id`=`payment`.`stop_id` WHERE `payment`.`bus_id`=%s AND `payment`.`month`=%s AND `payment`.`year`=%s"
    v=(bid,month,year)
    res1=selectall2(qry,v)
    return render_template('ViewPayment.html',val1=res1,val=res)






@app.route('/view_notification')
@login_required
def view_notification():
    qry = "SELECT * FROM notification ORDER BY `notification_id` DESC"
    res = selectall(qry)
    return render_template('ViewNotification.html', val=res)


@app.route('/add_notification', methods=['post'])
@login_required
def add_notification():
    return render_template('AddNotification.html')



@app.route('/add_notification1', methods=['post'])
def add_notification1():
    noti = request.form['textfield']
    qry = "INSERT into notification VALUES(null,%s,curdate())"
    val =(noti)
    iud(qry, val)
    return '''<script>alert("Inserted sucessfully");window.location="view_notification"</script>'''



@app.route('/edit_notification')
@login_required
def edit_notification():
    id=request.args.get('id')
    session['edit_rid']=id
    qry="SELECT * FROM notification WHERE `notification_id`=%s"
    res=selectone(qry,id)
    return render_template('EditNotification.html',data=res)



@app.route('/edit_notification1', methods=['post'])
def edit_notification1():
    noti = request.form['textfield']
    qry = "UPDATE notification SET `notification`=%s,`date`=curdate() WHERE `notification_id`=%s"
    val=(noti,str(session['edit_rid']))
    iud(qry, val)
    return '''<script>alert("Updated sucessfully");window.location="view_notification"</script>'''



@app.route('/delete_notification')
def delete_notification():
    id=request.args.get('id')
    qry="DELETE FROM notification WHERE `notification_id`=%s"
    iud(qry,id)
    return '''<script>alert("Deleted sucessfully");window.location="view_notification"</script>'''


@app.route('/view_feedback')
@login_required
def view_feedback():
        return render_template('ViewFeedback.html')



@app.route('/view_feedback1',methods=['post'])
@login_required
def view_feedback1():
    user=request.form['select']
    if user=="user":
        qry = "SELECT `feedback`.*,`registration`.`name` FROM `feedback` JOIN `registration` ON `feedback`.`login_id`=`registration`.`login_id`"
        res = selectall(qry)
        return render_template('ViewFeedback.html', val=res)

    elif user=="driver":
        qry = "SELECT `feedback`.*,`driver`.`driver_name` AS `name` FROM `feedback` JOIN `driver` ON `feedback`.`login_id`=`driver`.`login_id`"
        res = selectall(qry)
        return render_template('ViewFeedback.html', val=res)
    elif user=='None':
        return render_template('ViewFeedback.html', status="ok")


@app.route('/reply_feedback')
@login_required
def reply_feedback():
    feedback_id=request.args.get('id')
    session['fid']=feedback_id
    return render_template('ReplyFeedback.html')




@app.route('/insert_reply',methods=['post'])
def insert_reply():
    # feedback_id=session['fid']
    response=request.form['textarea']
    qry = "UPDATE feedback SET `response`=%s WHERE `feedback_id`=%s"
    val=(response,session['fid'])
    iud(qry,val)
    return '''<script>alert("Replied");window.location="view_feedback"</script>'''



@app.route('/viewdriverbus')
@login_required
def viewdriverbus():
    qry = "SELECT `bus`.`bus_name`,`driver`.*,`driverbus`.`driverbus_id`,`driverbus`.`from`,`driverbus`.`to` FROM `bus` JOIN `driverbus` ON `bus`.`bus_id`=`driverbus`.`bus_id` JOIN `driver` ON `driver`.`login_id`=`driverbus`.`driver_id`"
    #Here DriverBus - Driverid is Driver - Loginid
    res = selectall(qry)
    return render_template('ViewDriverBus.html',val=res)




@app.route('/adddriverbus',methods=['post'])
@login_required
def adddriverbus():
    d=datetime.now().strftime("%Y-%m-%d")
    qry = "select * from bus where status='active'"
    res = selectall(qry)
    qry1 = "select * from driver"
    res1 = selectall(qry1)
    return render_template('AddDriverBus.html', val=res,val1=res1,d=d)



@app.route('/adddriverbus1',methods=['post'])
@login_required
def adddriverbus1():
    bname = request.form['select']
    dname = request.form['select1']
    frm=request.form['from']
    to=request.form['to']

    q = "SELECT * FROM `bus` WHERE `bus_id`=%s"
    r = selectone(q,bname)
    print(r)
    busno=r['bus_no']
    regno=r['bus_regno']
    bus=r['bus_name']

    q="SELECT * FROM `driverbus` WHERE `driver_id`=%s or `bus_id`=%s"
    val=(dname,bname)
    res=selectone(q,val)
    if res is None:
        qr = "SELECT * FROM `driver` WHERE `login_id`=%s"
        re = selectone(qr, dname)
        email=re['driver_email']
        name=re['driver_name']
        if re is None:
            return '''<script>alert("invalid mail");window.location="viewdriverbus"</script>'''
        else:
            try:
                gmail = smtplib.SMTP('smtp.gmail.com', 587)
                gmail.ehlo()
                gmail.starttls()
                gmail.login('aneethawork@gmail.com', 'wtmbqwyvrrdfjvdf')
            except Exception as e:
                print("Couldn't setup email!!" + str(e))
            msg = MIMEText(
                "Hello " + name + "\nYou are Assigned to the bus: \nBusno : " + str(busno) + "\nBus Regno : " + str(regno) + "\nBusname : " + str(bus) + "\n You can login to view route and bus details")
            print(msg)
            msg['Subject'] = 'Driver Login'
            msg['To'] = str(email)
            msg['From'] = 'aneethawork@gmail.com'
            try:
                gmail.send_message(msg)
            except Exception as e:
                print("COULDN'T SEND EMAIL", str(e))

            qry = "INSERT INTO driverbus VALUES(null,%s,%s,%s,%s)"
            val = (dname,bname,frm,to)
            iud(qry, val)
            return '''<script>alert("Inserted");window.location="viewdriverbus"</script>'''
    else:
        return '''<script>alert("Already Assigned");window.location="viewdriverbus"</script>'''



@app.route('/deletedriverbus')
def deletedriverbus():
    # id = request.args.get('id')

    # q = "SELECT `driverbus`.* ,`driver`.`driver_name`,`driver_email` FROM `driverbus` JOIN `driver` ON `driverbus`.`driver_id`=`driver`.`driver_id` WHERE `driverbus`.`driverbus_id`=%s"
    # res = selectone(q, id)
    #
    # if res is None:
    #     qq=" SELECT * FROM `driverbus` WHERE `driverbus_id`=%s"
    #     drrid=selectall2(qq,id)
    #     print(drrid,"======================================================================")
    #
    #     qr = "SELECT * FROM `driver` WHERE `login_id`=%s"
    #     re = selectone(qr,drrid['driver_id'])
    #
    #     email = re['driver_email']
    #     name = re['driver_name']
    #     if re is None:
    #         return '''<script>alert("invalid mail");window.location="viewdriverbus"</script>'''
    #     else:
    #         try:
    #             gmail = smtplib.SMTP('smtp.gmail.com', 587)
    #             gmail.ehlo()
    #             gmail.starttls()
    #             gmail.login('aneethawork@gmail.com', 'wtmbqwyvrrdfjvdf')
    #         except Exception as e:
    #             print("Couldn't setup email!!" + str(e))
    #         msg = MIMEText(
    #             "Hello " + name + "\nYour Assigned schedule is cancelled. Will update with new information")
    #         print(msg)
    #         msg['Subject'] = 'Driver Schedule Cancelled'
    #         msg['To'] = str(email)
    #         msg['From'] = 'aneethawork@gmail.com'
    #         try:
    #             gmail.send_message(msg)
    #         except Exception as e:
    #             print("COULDN'T SEND EMAIL", str(e))
    qry="DELETE FROM driverbus WHERE `driverbus_id`=%s"
    iud(qry,id)
    return '''<script>alert("Deleted sucessfully");window.location="viewdriverbus"</script>'''




@app.route('/editdriverbus')
def editdriverbus():
    id=request.args.get('id')
    session['edit_rid']=id
    qry="SELECT * FROM driverbus WHERE `driverbus_id`=%s"
    res=selectone(qry,id)
    q="select * from bus where status='active'"
    r=selectall(q)
    qry1 = "select * from driver"
    res1 = selectall(qry1)
    return render_template('EditDriverBus.html',data=res,data1=r,data2=res1)



@app.route('/editdriverbus1', methods=['post'])
def editdriverbus1():
    bname = request.form['select']
    dname = request.form['select1']
    f=request.form['from']
    t=request.form['to']
    q = "SELECT * FROM `bus` WHERE `bus_id`=%s"
    r = selectone(q, bname)
    print(r)
    busno = r['bus_no']
    regno = r['bus_regno']
    bus = r['bus_name']

    q = "SELECT * FROM `driverbus` WHERE `driver_id`=%s or `bus_id`=%s"
    val = (dname, bname)
    res = selectone(q, val)
    if res is None:
        qr = "SELECT * FROM `driver` WHERE `login_id`=%s"
        re = selectone(qr, dname)
        email = re['driver_email']
        name = re['driver_name']
        if re is None:
            return '''<script>alert("invalid mail");window.location="viewdriverbus"</script>'''
        else:
            try:
                gmail = smtplib.SMTP('smtp.gmail.com', 587)
                gmail.ehlo()
                gmail.starttls()
                gmail.login('aneethawork@gmail.com', 'wtmbqwyvrrdfjvdf')
            except Exception as e:
                print("Couldn't setup email!!" + str(e))
            msg = MIMEText(
                "Hello " + name + "\nYou are Re-Assigned to the bus: \nBusno : " + str(busno) + "\nBus Regno : " + str(
                    regno) + "\nBusname : " + str(bus) + "\n You can login to view route and bus details")
            print(msg)
            msg['Subject'] = 'Driver Login'
            msg['To'] = str(email)
            msg['From'] = 'aneethawork@gmail.com'
            try:
                gmail.send_message(msg)
            except Exception as e:
                print("COULDN'T SEND EMAIL", str(e))

            qry = "UPDATE driverbus SET `bus_id`=%s,`driver_id`=%s,`from`=%s,`to`=%s WHERE `driverbus_id`=%s"
            val = (bname, dname, f, t, str(session['edit_rid']))
            iud(qry, val)
            return '''<script>alert("Updated sucessfully");window.location="viewdriverbus"</script>'''

    else:
        return '''<script>alert("Already Assigned");window.location="viewdriverbus"</script>'''






@app.route('/leave_request')
@login_required
def leave_request():
    # qry = "SELECT `leave`.*,`driver`.`driver_name` FROM `leave` JOIN `driver` ON `driver`.`login_id`=`leave`.`driver_id`"
    qry = "SELECT `leave`.*,`driver`.`driver_name`,`driverbus`.`driver_id`,`bus_id` FROM `leave` JOIN `driver` ON `driver`.`login_id`=`leave`.`driver_id` JOIN `driverbus` ON `leave`.`driver_id`=`driverbus`.`driver_id` ORDER BY `leave_id` DESC"
    res = selectall(qry)
    return render_template('ViewDriverLeave.html',val=res)





@app.route('/leave_request1')
@login_required
def leave_request1():
    id=request.args.get('id')
    session['leaveid']=id
    qry = "UPDATE `leave` SET `status`='verified' WHERE `leave_id`=%s"
    iud(qry,str(id))
    return '''<script>alert("Updated sucessfully");window.location="leave_request"</script>'''



@app.route('/leave_assign')
@login_required
def leave_assign():
    id=request.args.get('id')
    session['busid']=id

    qry="SELECT * FROM `leave` WHERE `leave_id`=%s"
    res=selectone(qry,str(session['leaveid']))

    qry1="SELECT * FROM `driver` WHERE `status`='backup'"
    res1=selectall(qry1)

    return render_template('LeaveAssign.html',data=res1,val=res)


@app.route('/leave_assign1',methods=['post'])
@login_required
def leave_assign1():
    drid=request.form['select1']
    f = request.form['textfield']
    t = request.form['textfield2']
    qry = "INSERT INTO driverbus VALUES(null,%s,%s,%s,%s)"
    val = (drid, str(session['busid']), f, t)
    iud(qry, val)

    qry1="UPDATE `leave` SET `status`='Assigned' WHERE `leave_id`=%s"
    iud(qry1,str(session['leaveid']))
    return '''<script>alert("Assigned sucessfully");window.location="leave_request"</script>'''





@app.route('/report')
@login_required
def report():
    amt = []
    m=['January', 'February', 'March', 'April', 'May', 'June', 'July','Aug','Sep','Oct','Nov','Dec']
    for i in m:
        qry="SELECT `month`,SUM(`amount`) AS amt FROM `payment` where month=%s and year=year(curdate())"
        res=selectone(qry,i)
        try:
            amt.append(int(res['amt']))
        except:
            amt.append(0)
    print(amt)
    return render_template('Report.html',a=amt)








#User


@app.route('/user_profile')
@login_required
def user_profile():
    qry = "SELECT * FROM registration WHERE `login_id`=%s"
    res = selectone(qry,session['lid'])
    return render_template('UserViewProfile.html', val=res)



@app.route('/edit_profile',methods=['post'])
def edit_profile():
    name = request.form['nm']
    email = request.form['em']
    mobile = request.form['mob']
    address = request.form['add']
    college = request.form['clg']
    category = request.form['select']
    branch = request.form['brn']
    semester = request.form['sem']
    # username = request.form['un']
    # password = request.form['pwd']
    # f = request.files['f']
    qry = "UPDATE registration SET `name`=%s,`email`=%s,`mobile`=%s,`address`=%s,`college`=%s,`category`=%s,`department`=%s,`designation`=%s WHERE `login_id`=%s"
    val = (name, email, mobile, address, college, category, branch,semester, str(session['lid']))
    iud(qry, val)
    return '''<script>alert("Updated sucessfully");window.location="user_profile"</script>'''



@app.route('/change_pwd',methods=['post'])
def change_pwd():
    cpwd = request.form['password']
    npwd = request.form['newpassword']
    rnpwd = request.form['renewpassword']
    qry="SELECT * FROM `login` WHERE `password`=%s AND `login_id`=%s"
    val=(cpwd,session['lid'])
    res=selectone(qry,val)
    if res is not None:
        if npwd==rnpwd:
            qry = "UPDATE login SET `password`=%s WHERE `login_id`=%s"
            val = (npwd, str(session['lid']))
            iud(qry, val)
            return '''<script>alert("Password Updated sucessfully");window.location="user_profile"</script>'''
        else:
            return '''<script>alert("Password mismatch");window.location="user_profile"</script>'''
    else:
        return '''<script>alert("Current Password is Wrong");window.location="user_profile"</script>'''



@app.route('/user_viewroute')
def user_viewroute():
    qry="SELECT * FROM `route`"
    res=selectall(qry)
    return render_template('UserViewRoute.html', val=res)




@app.route('/view_route1')
def view_route1():
    rid=request.args.get("id")

    qry="SELECT `stop_name`,`latitude`,`longitude`,`mrngtime`,`evngtime` FROM `stop` WHERE `route_id`=%s"
    res=selectall2(qry,rid)

    # my_map3 = folium.Map(location=[11.3400929,75.96622239999999], zoom_start=15)
    my_map3 = folium.Map(location=[11.3122, 75.9545], zoom_start=12)
    for i in res:
    # Pass a string in popup parameter
        folium.Marker([i['latitude'], i['longitude']], popup=i['stop_name']+"(M:"+str(i['mrngtime'])+",E:"+str(i['evngtime'])+")",icon=folium.Icon(color='red')).add_to(my_map3)


    #folium.Marker([i['latitude'], i['longitude']],popup=i['stop_name'] + "(M:" + str(i['mrngtime']) + ",E:" + str(i['evngtime']) + ")").add_to(my_map3)
    my_map3.save("templates/my_map31.html")

    return render_template('/my_map31.html')





@app.route('/user_payment1', methods=['post'])
@login_required
def user_payment1():
    qry = "select * from route"
    res = selectall(qry)
    return render_template('UserPayment.html',val=res)




@app.route('/user_payment',methods=['get','post'])
@login_required
def user_payment():
    if request.method=="POST":
        route = request.form['route']
        stop = request.form['stop']
        bus = request.form['bus']
        year = request.form['year']
        month = request.form['select2']
        amt1 = request.form['amt1']

        session['amt']=int(amt1)*100

        re = selectone("SELECT * FROM `bus` WHERE `bus_id`=%s", bus)
        ree = selectone("SELECT COUNT(`pay_id`) as count1 FROM `payment` WHERE `bus_id`=%s AND `month`=%s AND `status`='notpaid'",(bus, month))
        av_seat = re['seat']

        if int(ree['count1']) <= int(av_seat):
            session['route']=route
            session['stop']=stop
            session['bus']=bus
            session['year']=year
            session['month']=month
            session['amt1']=amt1

            res1 = selectone("SELECT * FROM `route` WHERE `route_id`=%s",route)
            res2 = selectone("SELECT * FROM `bus` WHERE `bus_id`=%s",bus)
            res3 = selectone("SELECT * FROM `stop` WHERE `stop_id`=%s",stop)
            return render_template('UserPaySummary.html',data1=res1,data2=res2,data3=res3)
        else:
            return '''<script>alert("full");window.location="user_pay_proceed"</script>'''

    else:
        qry = "select * from route"
        res = selectall(qry)
        return render_template('UserPayment.html',val=res)





@app.route('/pay_proceed', methods=['post'])
@login_required
def pay_proceed():
    qry = "select * from payment"
    res = selectall(qry)
    return render_template('UserPaySummary.html',data=res)


@app.route('/pay_proceed1', methods=['post'])
@login_required
def pay_proceed1():
    route = session['route']
    stop = session['stop']
    bus = session['bus']
    year = session['year']
    month = session['month']
    amt = session['amt1']

    re = selectone("SELECT * FROM `bus` WHERE `bus_id`=%s",bus)
    ree = selectone("SELECT COUNT(`pay_id`) as count1 FROM `payment` WHERE `bus_id`=%s AND `month`=%s AND `status`='paid'",(bus,month))
    av_seat=re['seat']


    q="UPDATE registration SET bus_id=%s WHERE login_id=%s"
    v=(bus,session['lid'])
    iud(q,v)

    qry = "INSERT INTO payment VALUES(null,%s,%s,%s,%s,%s,%s,now(),'notpaid','ps')"
    val = (session['lid'], stop, bus, year, month, amt)
    res=iud(qry, val)
    session['paymentnumber']=str(res)

    if int(ree['count1'])<=int(av_seat):
        # iud("UPDATE `bus` SET `available_seat`=%s where bus_id=%s",(ree['count1'],bus))
        return '''<script>alert("Directed to payment gateway");window.location="user_pay_proceed"</script>'''
    else:
        return '''<script>alert("Seats are full");window.location="user_pay_proceed"</script>'''



@app.route('/user_pay_proceed')
def user_pay_proceed():
    client = razorpay.Client(auth=("rzp_test_edrzdb8Gbx5U5M", "XgwjnFvJQNG6cS7Q13aHKDJj"))
    print(client)
    payment = client.order.create({'amount': session['amt'], 'currency': "INR", 'payment_capture': '1'})
    return render_template('UserPayProceed.html',p=payment)


@app.route('/user_pay_complete',methods=['post'])
def user_pay_complete():
    print(request.form)
    print(request.json)
    print(request.args)
    pid=request.form['razorpay_payment_id']
    route = session['route']
    stop = session['stop']
    bus = session['bus']
    year = session['year']
    month = session['month']
    amt = session['amt1']
    q="SELECT `email` FROM `registration` WHERE `login_id`=%s"
    res=selectone(q,session['lid'])
    email=res['email']
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('aneethawork@gmail.com', 'wtmbqwyvrrdfjvdf')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText(
        "Hello\nYour Payment is successfull for : \nYear : " + str(year) +"\nMonth : " + str(month) + "\nAmount : " + str(amt) + "\nPayment_id : " + str(pid) +  "\n You can login to view payment details")
    print(msg)
    msg['Subject'] = 'Payment'
    msg['To'] = str(email)
    msg['From'] = 'aneethawork@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))

    qry = "UPDATE `payment` SET `status`='paid',`pid`=%s WHERE `pay_id`=%s"
    # qry = "INSERT INTO payment VALUES(null,%s,%s,%s,%s,%s,%s,now(),'paid',%s)"
    val = (pid,str(session['paymentnumber']))
    # val = (session['lid'], stop, bus, year, month, amt,pid)
    iud(qry, val)

    return '''<script>alert("payment successful");window.location="user_pay_history"</script>'''




# @app.route('/razorpay',methods=['post','get'])
# def q():
#     client=razorpay.Client(auth=("rzp_test_edrzdb8Gbx5U5M","XgwjnFvJQNG6cS7Q13aHKDJj"))
#     print(client)
#     payment =client.order.create({'amount':10000,'currency':"INR",'payment_capture':'1'})
#     print(payment)
#     # payment={}
#     # qry="SELECT * FROM contact"
#     # res=selectall(qry)
#     return payment
#     # return render_template('view_contact.html',p=payment,payment=payment)





@app.route('/user_pay_history')
@login_required
def user_pay_history():
    qry = "SELECT *,DATE_FORMAT(`datetime`,'%d-%m-%Y') AS nd  FROM payment WHERE `login_id`="+str(session['lid'])+" AND `payment`.`status`='paid' ORDER BY `pay_id` DESC"
    res = selectall(qry)
    print(res)
    return render_template('UserPaymentHistory.html',val=res)



@app.route('/user_pay_history1')
@login_required
def user_pay_history1():
    id=request.args.get('id')
    qry = "SELECT * FROM `payment` JOIN `bus` ON `bus`.`bus_id`=`payment`.`bus_id` JOIN `stop` ON `stop`.`stop_id`=`payment`.`stop_id` JOIN `route` ON `route`.`route_id`=`stop`.`route_id` JOIN `registration` ON `registration`.`login_id`=`payment`.`login_id` WHERE `payment`.`pay_id`=%s"
    # qry = "SELECT * FROM `payment` JOIN `bus` ON `bus`.`bus_id`=`payment`.`bus_id` JOIN `stop` ON `stop`.`stop_id`=`payment`.`stop_id` JOIN `route` ON `route`.`route_id`=`stop`.`route_id` WHERE `payment`.`pay_id`=%s"
    res = selectone(qry,id)
    print(res)
    return render_template('UserPaymentHistory1.html',i=res)



@app.route('/current_details')
def current_details():
    q="SELECT `bus_id` FROM `registration` WHERE `login_id`=%s"
    r=selectone(q,session['lid'])
    qry = "SELECT `route`.`route_name`,`stop`.`stop_name`,`bus`.*,`driver`.*,`payment`.`amount`,`payment`.`month` FROM `payment` JOIN `stop` ON `payment`.`stop_id`=`stop`.`stop_id` JOIN `route` ON `route`.`route_id`=`stop`.`route_id` JOIN `driverbus` ON `driverbus`.`bus_id`=`payment`.`bus_id` JOIN `bus` ON `bus`.`bus_id`=`payment`.`bus_id` JOIN `driver` ON `driver`.`login_id`=`driverbus`.`driver_id` WHERE `payment`.`bus_id`=%s and `payment`.`login_id`=%s"
    v=(r['bus_id'],session['lid'])
    res = selectone(qry,v)
    print(res)
    return render_template('UserCurrentDetails.html',val=res)



@app.route('/details')
def details():
    qry = "SELECT `route`.`route_name`,`stop`.`stop_name`,`bus`.*,`driver`.*,`payment`.`amount`,`payment`.`month` FROM `payment` JOIN `stop` ON `payment`.`stop_id`=`stop`.`stop_id` JOIN `route` ON `route`.`route_id`=`stop`.`route_id` JOIN `driverbus` ON `driverbus`.`bus_id`=`payment`.`bus_id` JOIN `bus` ON `bus`.`bus_id`=`payment`.`bus_id` JOIN `driver` ON `driver`.`login_id`=`driverbus`.`driver_id` WHERE `payment`.`login_id`=%s"
    res = selectall2(qry,session['lid'])
    return render_template('UserDetails.html',val=res)




@app.route('/user_notification')
def user_notification():
    qry = "SELECT * FROM `notification` ORDER BY `notification_id` DESC"
    res = selectall(qry)
    return render_template('UserNotification.html',val=res)



@app.route('/user_feedback')
def user_feedback():
    return render_template('UserFeedback.html')


@app.route('/user_feedback1', methods=['post'])
def user_feedback1():
    feed = request.form['textfield']
    qry = "INSERT into feedback VALUES(null,%s,%s,curdate(),'pending')"
    val = (session['lid'],feed)
    iud(qry,val)
    return '''<script>alert("Send sucessfully");window.location="user_feedback"</script>'''



@app.route('/user_feedbackres')
def user_feedbackres():
    qry = "SELECT * FROM `feedback` WHERE login_id=%s"
    res = selectall2(qry,session['lid'])
    return render_template('UserFeedbackResponse.html',val=res)




@app.route('/select_stop/<eid>')
def select_stop(eid):
    res1 = selectall2("SELECT * FROM `stop` WHERE `route_id`=%s",eid)
    res2 = selectall2("SELECT * FROM `bus` WHERE `route_id`=%s",eid)
    print(res1,"aaaaaaaaaaaaa")
    return render_template('get_stop.html',val2=res1,val3=res2)




@app.route('/index',methods=['post','get'])
def index():
    print(request.form)
    rid=request.form['brand']
    qry="SELECT `bus_id`,`bus_no`,`bus_name` FROM `bus` WHERE `route_id`=%s"
    res=selectall2(qry,rid)

    qry="SELECT `stop_name`,`stop_id` FROM `stop` WHERE `route_id`=%s"
    res1=selectall2(qry,rid)

    lis=["","Select"]

    for i in res:
        lis.append(i['bus_id'])
        lis.append(i['bus_name']+" - "+str(i['bus_no']))
    lis.append("")
    lis.append("Select")
    for i in res1:
        lis.append(i['stop_id'])
        lis.append(i['stop_name'] )

    resp = make_response(jsonify(lis))

    resp.status_code = 200
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp







@app.route('/index1',methods=['post','get'])
def index1():
    print(request.form)
    sid=request.form['brand']
    qry="SELECT `stop_fees` FROM `stop` WHERE `stop_id`=%s"
    res=selectone(qry,sid)
    return str(res['stop_fees'])





#Driver


@app.route('/driverhome')
@login_required
def driverhome():
        return render_template('DriverHome.html')


@app.route('/driverdash')
@login_required
def driverdash():
    return render_template('DriverHome.html')



@app.route('/indexdriver')
@login_required
def indexdriver():
    qry="SELECT * FROM `driver` WHERE `login_id`=%s"
    res=selectone(qry,str(session['lid']))
    return render_template('index_driver.html',val=res)



@app.route('/driver_profile')
@login_required
def driver_profile():
    qry = "SELECT * FROM driver WHERE `login_id`=%s"
    res = selectone(qry, session['lid'])
    return render_template('DriverViewProfile.html',val=res)




@app.route('/driver_viewroute')
def driver_viewroute():
    qry="SELECT * FROM `route`"
    res=selectall(qry)
    return render_template('DriverViewRoute.html', val=res)



@app.route('/driver_schedule')
def driver_schedule():
    qry = "SELECT `route`.`route_name`,`bus`.*,`driverbus`.`from`,`driverbus`.`to` FROM bus JOIN `driverbus` ON `driverbus`.`bus_id`=`bus`.`bus_id` JOIN `route` ON `route`.`route_id`=`bus`.`route_id` WHERE `driverbus`.`driver_id`=%s"
    res = selectone(qry, session['lid'])
    print(res)
    return render_template('DriverSchedule.html', val=res)




@app.route('/view_travellers')
@login_required
def view_travellers():
    bid=request.args.get('id')
    qry = "SELECT `registration`.`name`,`category`,`stop`.`stop_name`,`stop_fees`,`payment`.`status`,`payment`.`month` FROM `registration` JOIN `payment` ON `payment`.`login_id`=`registration`.`login_id` JOIN `stop` ON `stop`.`stop_id`=`payment`.`stop_id` WHERE  `registration`.`bus_id`=%s AND `payment`.`month`=MONTHNAME(CURDATE())"
    res = selectall2(qry,bid)
    print(res)
    return render_template('DriverViewTravellers.html', val=res)





@app.route('/driver_leave')
def driver_leave():
    qry = "SELECT * FROM `leave` WHERE driver_id=%s"
    res = selectall2(qry,str(session['lid']))
    return render_template('DriverLeave.html',val=res)



@app.route('/req_leave', methods=['post','get'])
def req_leave():
    d = datetime.now().strftime("%Y-%m-%d")
    qry = "SELECT * FROM `leave`"
    res = selectall(qry)
    return render_template('DriverRequestLeave.html',val=res,d=d)



@app.route('/req_leave1', methods=['post'])
def req_leave1():
    r = request.form['rsn']
    f = request.form['frm']
    t = request.form['to']
    qry = "INSERT INTO `leave`(`driver_id`,`reason`,`from`,`to`,`status`) VALUES (%s,%s,%s,%s,'pending')"
    val = (session['lid'],r,f,t)
    iud(qry,val)
    return '''<script>alert("Send sucessfully");window.location="driver_leave"</script>'''





# @app.route('/user_feedback1', methods=['post'])
# def user_feedback1():
#     feed = request.form['textfield']
#     qry = "INSERT into feedback VALUES(null,%s,%s,curdate(),'pending')"
#     val = (session['lid'],feed)
#     iud(qry,val)
#     return '''<script>alert("Send sucessfully");window.location="user_feedback"</script>'''




@app.route('/driver_notification')
def driver_notification():
    qry = "SELECT * FROM `notification` ORDER BY `notification_id` DESC"
    res = selectall(qry)
    return render_template('DriverNotification.html',val=res)



@app.route('/driver_feedback')
def driver_feedback():
    return render_template('DriverFeedback.html')


@app.route('/driver_feedback1', methods=['post'])
def driver_feedback1():
    feed = request.form['textfield']
    qry = "INSERT into feedback VALUES(null,%s,%s,curdate(),'pending')"
    val = (session['lid'],feed)
    iud(qry,val)
    return '''<script>alert("Send sucessfully");window.location="driver_feedback"</script>'''



@app.route('/driver_feedbackres')
def driver_feedbackres():
    qry = "SELECT * FROM `feedback` WHERE login_id=%s "
    res = selectall2(qry, session['lid'])
    return render_template('DriverFeedbackResponse.html',val=res)




app.run(debug=True)