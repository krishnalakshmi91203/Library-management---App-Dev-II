from flask import *
import dbase as db
import backend as rem
import os
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_mail import Mail, Message 
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta,date
import atexit
from flask_caching import Cache

def delete_pdf(filename):
      filepath = os.path.join(app.root_path, 'static', filename)
      if os.path.exists(filepath):
            os.remove(filepath)
            
app = Flask(__name__)
mail = Mail(app) 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'krishnalakshmi91203@gmail.com'
app.config['MAIL_PASSWORD'] = 'cxuwnqcprltlldvc'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  
app.config['CACHE_TYPE'] = 'SimpleCache'  
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  

cache = Cache(app)
jwt = JWTManager(app)
mail = Mail(app)

@app.route('/',methods=['GET','POST'])
def home():
      return render_template('home.html')

@app.route('/userlogin',methods=['GET','POST'])
#@cache.cached(timeout=60) 
def user():
      if (request.form.get("userreq")=="das"):
            a1=request.form.get('uname')
            a2=request.form.get('pwd')
            k=db.userchk(a1,a2)
            if k!=[]:
                  access_token = create_access_token(identity={"username": a1,"role":k[0][1]}, expires_delta=timedelta(hours=1))
                  print(k[0][1])
                  return jsonify(access_token=access_token)
            return jsonify({"msg": "Bad username or password"}), 401
      return render_template('user.html')

@app.route('/librarian_dashboard',methods=['GET','POST'])
def libr():
      if (request.method=="POST") :
            search_name = request.form.get('name')
            search_type = request.form.get('search')
            delete_section_id = request.form.get('form')
            if delete_section_id:
                  # Delete section and associated files
                  deleted_sections = db.delesec(delete_section_id)
                  for section in deleted_sections:
                        delete_pdf(section[0])
            if request.form.get('same') == "search1":
                  search_results = db.fun(0, [search_name, search_type])
                  return jsonify(search_results)
      return render_template('libdash.html',k=db.fun(0,0))

@app.route('/<section_id>/books',methods=['GET','POST'])
def books(section_id):
      if (request.method=="POST") :
            a3=request.form.get('name')
            a4=request.form.get('search')
            a1=request.form.get('del')
            print(a1,a4,a3)
            if a1:
                  k=db.delebook(a1)
                  for i in k:
                       delete_pdf(i[0]) 
            if request.form.get('same')=="search1":
                  (k,b)=db.fun1(section_id,[a3,a4])
                  return render_template('libdashbook.html',k=k,b=b,a=section_id)
      (k,b)=db.fun1(section_id,0)
      return render_template('libdashbook.html',k=k,b=b,a=section_id)

@app.route('/sectionform/<req>',methods=['GET','POST'])
#@cache.cached(timeout=60) 
def sectionform(req):
      if str(req)=="new":
            a1=request.form.get('title')
            a2=date.today()
            a3=request.form.get('desc')
            if (request.form.get("libdas")=="j"):
                  db.addsection(a1,a2,a3)
                  return redirect(url_for('libr'))
            return render_template('sectionform.html',aa=str(req),a=a2)
      else:
            k=db.fun2(int(req),0)
            a1=request.form.get('title')
            a2=request.form.get('date')
            a3=request.form.get('desc')
            if (request.form.get("libdas")=="j"):
                  db.update(a1,a2,a3,req,0,0,0)
                  return redirect(url_for('libr'))
            return render_template('sectionform.html',aa=req,aa1=k[0],aa2=k[1],aa3=k[2])
      
@app.route('/<section_name>/bookform/<req>',methods=['GET','POST'])
def bookform(section_name,req):
      b2=db.fun(section_name,0)
      print(section_name,b2)
      if req == "new":
              if request.method == "POST":
                  a1 = request.form.get('title')
                  a3 = request.form.get('auth')
                  a2 = request.files.get("content")
                  a4 = request.form.get('price')
                  if request.method == "POST" and request.form.get('libdas') == 'j':
                      if a2:
                            e = a2.filename
                            t = f"static/{e}"
                            a2.save(t)
                            a2 = e
                      db.addbook(a1, a2, a3, section_name, a4)
                      (k, b1) = db.fun1(b2[0][0], 0)
                      return render_template('libdashbook.html', k=k, b=b1)
              return render_template('bookform.html', b=b2[0][0], a=section_name, aa=req)
      else:
          k = db.fun2(int(req), 1)
          a1 = request.form.get('title')
          a2 = request.form.get('auth')
          a3 = request.files.get("content")
          a4 = request.form.get('price')
          if request.method == "POST" and request.form.get('libdas') == 'j':
              if a3:
                    e = a3.filename
                    t = f"static/{e}"
                    a3.save(t)
                    a3 = e
              db.update(a1, a2, a3, section_name, 1, req, a4)
              k1, b1 = db.fun1(b2[0][0], 0)
              return render_template('libdashbook.html', k=k1, b=b1)
          return render_template('bookform.html', b=b2[0][0], a=section_name, aa=req, aa1=k[0], aa2=k[1], aa3=k[2], aa4=k[3])

@app.route('/user_dashboard/<uname>',methods=['GET','POST'])
def usdash(uname):
      a3=request.form.get('name')
      a4=request.form.get('search')
      a1=request.form.get('book')
      if a1!=None:
            if db.chk(uname):
                  db.req(int(a1),uname)
            t=f'/user_dashboard/{uname}'
            return redirect(t)
      if request.form.get('same')=="search1":
            k=db.search(a3,a4,uname)
            return render_template('usdash.html',k=k,a=uname)
      return render_template('usdash.html',k=db.userdash(uname),a=uname)

@app.route('/user_dashboard/<uname>/mybook',methods=['GET','POST'])
def usreq(uname):
      a1=db.userreq(uname,'request')
      a2=db.userreq(uname,'granted')
      a3=db.userreq(uname,'completed')
      a4=request.form.get('select')
      a5=request.form.get('sub')
      if a5=='i':
            a6=request.form.get('book')
            a7=request.form.get('rate')   
            db.uprate(a6,a7)
            f=f'/user_dashboard/{uname}/mybook'
            return redirect(f)
      if a4:
            db.revoke(int(a4),uname)
            f=f'/user_dashboard/{uname}/mybook'
            return redirect(f)
      return render_template('usmybook.html',k1=a1,k2=a2,k3=a3,a=uname)

@app.route('/Registerform/<req>',methods=['GET','POST'])
def regform(req):
      if (request.method=="POST") :
            a1=request.form.get('name')
            a2=request.form.get('role')
            a3=request.form.get('uname')
            a4=request.form.get('pwd')
            a6=request.form.get('email')
            a5=request.form.get('num')
            print(a1,a2)
            if str(req)=='new':
                  db.adduser(a1,a2,a3,a4,a5,a6)
                  return redirect('/userlogin')
            else:
                  print(a1,a2)
                  db.deluser(req)
                  db.adduser(a1,a2,a3,a4,a5,a6) 
                  t=f'/user_dashboard/{a3}'
                  return redirect(t)     
      if  str(req)=='new':   
            return render_template('regform.html',aa=req)
      else:
            return render_template('regform.html',aa=req,k=db.userdetail(req))

      
@app.route('/librarian_dashboard/status',methods=['GET','POST'])
def libstatus():
      a3=request.form.get('grant')
      a4=request.form.get('grant1')
      if a3:
            a3=a3.split(',')
            db.libchoice(int(a3[0]),str(a3[1]))
            return redirect('/librarian_dashboard/status')
      if a4:
            a4=a4.split(',')
            db.reject(int(a4[0]),str(a4[1]))
            return redirect('/librarian_dashboard/status')
      a3=request.form.get('revoke')
      if a3!=None:
            a3=a3.split(',')
            db.revoke(int(a3[0]),str(a3[1]))
            return redirect('/librarian_dashboard/status')
      a1=db.libreq("request")
      a2=db.libreq("granted")
      return render_template('libstatus.html',k1=a1,k2=a2)

@app.route('/<uname>/profile',methods=['GET','POST'])
#@cache.cached(timeout=60) 
def profile(uname):
      return render_template('profile.html',a=uname,k=db.userdetail(uname))
@app.route('/<uname>/user_detail',methods=['GET','POST'])
#@cache.cached(timeout=60) 
def userdet(uname):
      k,k1=db.bookdet(uname)
      return render_template('userdet.html',a=uname,k=k,k1=k1)
@app.route('/<bookid>/status',methods=['GET','POST'])
#@cache.cached(timeout=60) 
def bookstat(bookid):
      k,k1,k2,k3=db.bookstat(int(bookid))
      return render_template('bookstat.html',a=bookid,k=k,k1=k1,k2=k2,k3=k3)

def generate_monthly_report():
    with app.app_context():
        a,b=rem.fetch()
        print("..................Monthly Report.................\n" ,a,b)
        report_html = render_template_string(rem.REPORT_TEMPLATE,issued_books=a,book_ratings=b)
        msg = Message(
            'Monthly Activity Report',
            sender='krishnalakshmi91203@gmail.com',
            recipients=['krishnalakshmi91203@gmail.com']
        )
        msg.html = report_html
        mail.send(msg)

#....................................monthly report mail.........................
from apscheduler.triggers.cron import CronTrigger
scheduler = BackgroundScheduler(daemon=True)
'''run_time = datetime.now() + timedelta(minutes=1)
scheduler.add_job(func=generate_monthly_report, trigger='date', run_date=run_time)'''
scheduler.add_job(func=generate_monthly_report, trigger=CronTrigger(day=1))

#..................................... reminder sms................................
'''another_run_time = datetime.now() + timedelta(minutes=2)  
scheduler.add_job(func=rem.reminder, trigger='date', run_date=another_run_time)'''
hour = 18  
minute = 0
scheduler.add_job(func=rem.reminder, trigger=CronTrigger(hour=hour, minute=minute))
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

#.......................User Triggered Async Job - Export as CSV.......................
from rq import Queue
from redis import Redis
redis_conn = Redis(port=6380)
q = Queue(connection=redis_conn)

@app.route('/export-ebooks', methods=['POST'])
def export_ebooks():
    job = q.enqueue(rem.export_ebook_data)
    return jsonify({'job_id': job.get_id()}), 202

@app.route('/job-status/<job_id>')
def job_status(job_id):
    job = q.fetch_job(job_id)
    if job.is_finished:
        return jsonify({'status': 'finished'})
    elif job.is_failed:
        return jsonify({'status': 'failed'})
    else:
        return jsonify({'status': 'pending'})

if __name__ == '__main__':
   db.default()
   app.run(debug=True)
