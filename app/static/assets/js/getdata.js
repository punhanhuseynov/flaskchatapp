let http = new XMLHttpRequest()
let url = '/getusers'
http.open("GET", url)
http.send()

let userBar = document.getElementById('usersBar')
let messagesBar = document.getElementById('messages')
let userprofile = document.getElementsByClassName('user')
let confrimer // email confrimer 
let profilename //profile name

let message = document.getElementById("message")
let subbtn = document.getElementById('btn-submit')
let chat = document.getElementById('chatbar')

check=null

subbtn.addEventListener('click', () => {
    if( message.value==''|| message.value==null){
        window.alert('fill')
    }
    else{

        addMessage()
    }
        

})

http.onload = () => {

    user = http.responseText

    users = JSON.parse(user)

    for (let i = 0; i < users.length; i++) {

        userBar.innerHTML += `<a  class="d-block p-2 rounded-lg user " onclick="refreshMessages('${users[i].email}','${users[i].name}')" >
        <div class="d-flex p-2">
            <img alt="Image" src="/static/assets/img/${users[i].picture}" class="avatar shadow">
            <div class="ml-2">
                <div class="justify-content-between align-items-center">
                    <h4 class="text-blue mb-0 mt-1">${users[i].name}<span class="badge badge-success"></span>
                    </h4>
                    <p class="text-black mb-0 text-xs font-weight-normal">Job: ${users[i].job}</p>
                </div>
            </div>
        </div>
    </a>`
    }
}

recieverName=null

function refreshMessages(email, name) {
    clearInterval(check)
    document.getElementById('profilename').innerHTML = name
    confrimer = email
    profilename=name
    chat.style.width = '100%'

    writeMessages(email)

    recieverName=name
    console.log(recieverName,email)

    check=setInterval(()=>{
        refreshMessages(confrimer,profilename)
        console.log('called')
    },10000)
    

   
    

}   



for (let i = 0; i < userprofile.length; i++) {
    userprofile[i].addEventListener('onclick', () => {
        // refreshMessages()
        
    })
}


function addMessage() {
   
    let xhr = new XMLHttpRequest();
    let url = 'http://localhost:5000/send';
    let data = {
        name: message.value,
        email: confrimer
    };



    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onload = function () {
        callRefresh(confrimer,recieverName)
        messagesBar.scrollTop=messagesBar.scrollHeight

    };

    xhr.send(JSON.stringify(data));
    message.value = ''

    



}


function writeMessages(email) {
    let xhr = new XMLHttpRequest()
    let url = 'http://localhost:5000/getmessages'
    xhr.open('POST', url, true)
    xhr.setRequestHeader('Content-Type', 'application/json');
    data = {
        email: email
    }
    xhr.onload = () => {
        messagesBar.innerHTML = ''
        mes = JSON.parse(xhr.responseText)
        
        mes.sort((a,b)=>{return a.id-b.id})
     
        
        for (let i = 0; i < mes.length; i++) {
            messagesBar.innerHTML += `
            <div class="col-auto">
                 <div class="card ${mes[i].reciever_color}">

                    <div class="card-body p-2">

                        <p class="mb-1"> ${mes[i].message} </p>

                        <div class="d-flex align-items-center justify-content-${mes[i].content} text-sm opacity-6">

                                <i class="fa fa-check-double mr-1 text-xs" aria-hidden="true"></i>
                                <small>${mes[i].time}</small> 
                                ${
                                mes[i].sender==mes[i].current_id
                                   ? `<i onclick='deleteMessage(${mes[i].id})' class=" btn  fa fa-trash mr-1 text-xs" aria-hidden="true"></i>
                                    `
                                    :""
                                }

                        </div>
                    </div>
                 </div>
            </div>
            
            
          
          `
        }

    }
    xhr.send(JSON.stringify(data))
 
}



function callRefresh(email,name){
    setTimeout(2000,refreshMessages(email,name))  
}


function deleteMessage(id){
    xhr=new XMLHttpRequest()
    url="http://localhost:5000/deletemessage/"+id

    xhr.open('delete',url)
    xhr.onload=()=>{
        console.log(xhr.responseText)
        refreshMessages(confrimer,profilename)
    }
    xhr.send()
    
}


