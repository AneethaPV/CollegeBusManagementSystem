from flask import *
from werkzeug.utils import secure_filename
import functools

import os
import folium

from src.dbconnectionnew import *
from datetime import datetime
app=Flask(__name__)
app.secret_key="12345"


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
    if res is None:
        return '''<script>alert("invaild");window.location="login_index"</script>'''
    elif res['usertype']=="admin":
        session['lid']=res['login_id']
        return '''<script>alert("vaild");window.location="adminhome"</script>'''
    elif res['usertype'] == "user":
        session['lid'] = res['login_id']
        return '''<script>alert("vaild");window.location="userhome"</script>'''
    elif res['usertype'] == "driver":
        session['lid'] = res['login_id']
        return '''<script>alert("vaild");window.location="driverhome"</script>'''
    else:
        return '''<scrpit>alert("invaild");window.location="login_index"</scrpit>'''


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
    qry="INSERT INTO `login` VALUES(NULL,%s,%s,'user')"
    val=(username,password)
    lid=iud(qry,val)
    qry="INSERT INTO `registration` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val=(lid,name,email,mobile,address,college,category,branch,semester)
    iud(qry,val)
    f.save("static/user_img/"+str(lid)+".jpg")
    return '''<script>alert("Registration Success");window.location="/" </script>'''


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
    qry = "SELECT * FROM bus"
    res = selectall(qry)
    return render_template('ViewBus.html', val=res)


@app.route('/add_bus', methods=['post'])
@login_required
def add_bus():
    return render_template('AddBus.html')


@app.route('/add_bus1', methods=['post'])
def add_bus1():
    bregno = request.form['textfield']
    bno = request.form['textfield2']
    bname = request.form['textfield3']
    bimage = request.files['textfield4']
    seat = request.form['textfield5']
    status = request.form['select']
    fn=datetime.now().strftime("%Y%m%d%H%M%S")+".jpg"
    bimage.save("static/bus/"+fn)
    qry = "INSERT INTO bus VALUES(null,%s,%s,%s,%s,%s,%s)"
    val=(bregno, bno, bname, fn, seat, status)
    iud(qry, val)
    return '''<script>alert("Inserted");window.location="view_bus"</script>'''


@app.route('/edit_bus')
@login_required
def edit_bus():
    id=request.args.get('id')
    session['edit_rid']=id
    qry="SELECT * FROM bus WHERE `bus_id`=%s"
    res=selectone(qry,id)
    return render_template('EditBus.html',data=res)


@app.route('/edit_bus1', methods=['post'])
def edit_bus1():
    try:
        bregno = request.form['textfield']
        bno = request.form['textfield2']
        bname = request.form['textfield3']
        seat = request.form['textfield5']
        status = request.form['select']
        img=request.files['f']
        fn=secure_filename(img.filename)
        img.save(os.path.join("static/bus",fn))
        bimage=fn
        qry = "UPDATE bus SET `bus_regno`=%s,`bus_no`=%s,`bus_name`=%s,`bus_image`=%s,`seat`=%s,`status`=%s WHERE `bus_id`=%s"
        val=(bregno,bno,bname,bimage,seat,status,str(session['edit_rid']))
        iud(qry, val)
        return '''<script>alert("Updated sucessfully with image");window.location="view_bus"</script>'''
    except:
        bregno = request.form['textfield']
        bno = request.form['textfield2']
        bname = request.form['textfield3']
        # bimage = request.form['textfield4']
        seat = request.form['textfield5']
        status = request.form['select']
        qry = "UPDATE bus SET `bus_regno`=%s,`bus_no`=%s,`bus_name`=%s,`seat`=%s,`status`=%s WHERE `bus_id`=%s"
        val = (bregno, bno, bname, seat, status, str(session['edit_rid']))
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
    dno = request.form['textfield']
    dname = request.form['textfield2']
    daddress = request.form['textfield3']
    dimage = request.files['textfield4']
    demail = request.form['textfield5']
    dmob = request.form['textfield6']
    dlicense = request.form['textfield7']
    dstatus = request.form['select']
    fn = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
    dimage.save("static/driver/" + fn)

    qry = "INSERT INTO driver VALUES(null,%s,%s,%s,%s,%s,%s,%s,%s)"
    val =(dno, dname, daddress, fn, demail, dmob, dlicense, dstatus)
    iud(qry, val)
    return '''<script>alert("Inserted");window.location="view_driver"</script>'''


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
        dno = request.form['textfield']
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
        qry = "UPDATE driver SET `driver_no`=%s,`driver_name`=%s,`driver_address`=%s,`driver_image`=%s,`driver_email`=%s,`driver_mobile`=%s,`driver_license`=%s,`status`=%s WHERE `driver_id`=%s"
        val=(dno, dname, daddress, dimage, demail, dmob, dlicense, dstatus, str(session['edit_rid']))
        res=iud(qry, val)
        return '''<script>alert("Updated sucessfully with image");window.location="view_driver"</script>'''

    except:
        dno = request.form['textfield']
        dname = request.form['textfield2']
        daddress = request.form['textfield3']
        demail = request.form['textfield5']
        dmob = request.form['textfield6']
        dlicense = request.form['textfield7']
        dstatus = request.form['select']
        qry = "UPDATE driver SET `driver_no`=%s,`driver_name`=%s,`driver_address`=%s,`driver_email`=%s,`driver_mobile`=%s,`driver_license`=%s,`status`=%s WHERE `driver_id`=%s"
        val = (dno, dname, daddress, demail, dmob, dlicense, dstatus, str(session['edit_rid']))
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
    qry = "SELECT `stop`.*,`route`.`route_name` FROM STOP JOIN route ON stop.`route_id`=`route`.`route_id`;"
    res = selectall(qry)
    return render_template('ViewStop.html', val=res)



@app.route('/add_stop', methods=['post'])
@login_required
def add_stop():
    qry="select * from route"
    res=selectall(qry)
    return render_template('AddStop.html',val=res)



@app.route('/add_stop1', methods=['post'])
def add_stop1():
    rno = request.form['select']
    sname = request.form['textfield1']
    sfees = request.form['textfield2']
    lat = request.form['textfield3']
    lon = request.form['textfield4']
    mrng = request.form['textfield5']
    evng = request.form['textfield6']
    qry = "INSERT INTO stop VALUES(null,%s,%s,%s,%s,%s,%s,%s)"
    val =(rno, sname, sfees, lat, lon, mrng, evng)
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



@app.route('/view_payment')
@login_required
def view_payment():
    qry = "SELECT * FROM payment"
    res = selectall(qry)
    return render_template('ViewPayment.html', val=res)




@app.route('/view_notification')
@login_required
def view_notification():
    qry = "SELECT * FROM notification"
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
    qry = "SELECT * FROM feedback"
    res = selectall(qry)
    return render_template('ViewFeedback.html', val=res)



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



@app.route('/report')
@login_required
def report():
    return render_template('Report.html')



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

    my_map3 = folium.Map(location=[11.3400929,75.96622239999999], zoom_start=15)
    for i in res:
    # Pass a string in popup parameter
        folium.Marker([i['latitude'], i['longitude']], popup=i['stop_name']+"(M:"+str(i['mrngtime'])+",E:"+str(i['evngtime'])+")",icon=folium.Icon(color='red')).add_to(my_map3)


    #folium.Marker([i['latitude'], i['longitude']],popup=i['stop_name'] + "(M:" + str(i['mrngtime']) + ",E:" + str(i['evngtime']) + ")").add_to(my_map3)
    my_map3.save("templates/my_map31.html")

    return render_template('/my_map31.html')



@app.route('/user_payment')
def user_payment():
    return render_template('UserPayment.html')



@app.route('/user_pay_history')
def pay_history():
    return render_template('UserPaymentHistory.html')




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
    val = ( session['lid'],feed)
    iud(qry, val)
    return '''<script>alert("Send sucessfully");window.location="user_feedback"</script>'''





@app.route('/user_feedbackres')
def user_feedbackres():
    qry = "SELECT * FROM `feedback`"
    res = selectall(qry)
    return render_template('UserFeedbackResponse.html',val=res)













#Driver

@app.route('/driverhome')
def driverhome():
        return render_template('DriverHome.html')


@app.route('/driver_profile')
def driver_profile():
    return render_template('DriverViewProfile.html')




app.run(debug=True)