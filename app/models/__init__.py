from app import db,login_manager,redirect,UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Users().query.filter_by(id=user_id).first()

@login_manager.unauthorized_handler
def unlogin():
    return redirect('/login')


class Users(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    email=db.Column(db.String,nullable=False)
    password=db.Column(db.String,nullable=False)
    job=db.Column(db.String,nullable=False)
    img=db.Column(db.String,nullable=False)
    message=db.relationship('Messages',foreign_keys="Messages.user1",backref='us')
    message2=db.relationship('Messages',foreign_keys="Messages.user2",backref='us2')
    


class Messages(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    message=db.Column(db.Text)
    time=db.Column(db.String)
    user1=db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    user2=db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    
    

    
