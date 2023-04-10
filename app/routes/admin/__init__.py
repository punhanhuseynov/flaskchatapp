from app import app,render_template,redirect,login_required,logout_user,current_user,request,db
from app.models import Users,Messages
from flask import jsonify
from datetime import datetime

@app.route('/')
@login_required
def index():
    
    return render_template('/profile/index.html',user=current_user)


@app.route('/getusers')
@login_required
def getdata():
    data=Users().query.filter(id!=current_user.id).all()
    jsdata=[]
    for i in data :
        if i.id !=current_user.id:
            jsdata.append(
                {
                'name':i.name,
                'email':i.email,
                "job":i.job,
                "picture":i.img
                }
            )
    print(jsdata)
    jsdata=jsonify(jsdata)
    
    return jsdata

@app.route('/send',methods=['POST'])
@login_required
def sendmessage():
    now=datetime.now()
    if request.method=='POST':
        sender=Users.query.filter_by(email=request.json['email']).first()
        data=Messages(message=request.json['name'],time=str(now.strftime("%H:%M")),user1=current_user.id,user2=sender.id)
        
        db.session.add(data)
        db.session.commit()
   
        print(request.json['name'])
        return request.json['email']

  

@app.route('/getmessages',methods=['POST'])
@login_required
def getmessage():
    if request.method=='POST':
        email=request.json['email']
    
        reciever=Users().query.filter_by(email=email).first()
    
        send_messages=Messages().query.filter_by(user1=current_user.id,user2=reciever.id).all()
        reci_messages=Messages().query.filter_by(user1=reciever.id,user2=current_user.id).all()
       
        all_messages_json=[]
        for i in send_messages:
            all_messages_json.append(
                {
                    "id":i.id,
                    "message":i.message,
                    "time":i.time,
                    "sender":i.user1,
                    "reciever":i.user2,
                    "current_id":current_user.id,
                    "reciever_color":'bg-gradient-primary text-white',
                    "content":'end',
                }
            )
        
        for i in reci_messages:
            all_messages_json.append(
                {
                    "id":i.id,
                    "message":i.message,
                    "time":i.time,
                    "sender":i.user1,
                    "reciever":i.user2,
                    "content":"start"
                  
                    
                }
            )
        
        return jsonify(all_messages_json)
    
@app.route('/deletemessage/<id>',methods=['DELETE'])
@login_required
def delete_message(id):
    
    if request.method=='DELETE':
        data=Messages.query.filter_by(id=id).first()
        db.session.delete(data)
        db.session.commit()
        response={
            "message":"silindi"
        }
        return jsonify(response)

        
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')
