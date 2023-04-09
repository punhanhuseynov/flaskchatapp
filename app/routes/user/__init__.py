from app import app,render_template,redirect,request,flash,db,login_user
from app.models import Users
import random
@app.route("/login",methods=['GET',"POST"])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        data=Users().query.filter_by(email=email,password=password).first()
        login_user(data)
        if data is None:
            return "error"
        else:
            return redirect('/')
    return render_template('user/login.html')

@app.route("/register",methods=['GET',"POST"])
def register():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        job=request.form['job']
        img=request.files['img']

        filename=img.filename
        filetype=filename.rsplit('.')
        filename=filetype[0]
        type=filetype[1]
        filename=filename+str(random.randint(100,1000))
        data=Users(name=name,password=password,job=job,email=email,img=filename+"."+type)
        img.save('app/static/assets/img/'+filename+"."+type)
        db.session.add(data)
        db.session.commit()
        return redirect('login')

        
    return render_template('user/register.html')    
