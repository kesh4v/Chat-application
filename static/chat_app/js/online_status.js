const ws = new WebSocket('ws://' + window.location.host + '/ws/' + 'status/')

const Logged_username = JSON.parse(document.getElementById("logged_user").textContent)
const sender = JSON.parse(document.getElementById('sender').textContent)
console.log("Logged_username :",Logged_username)

ws.onopen = function(event){
    console.log("Online status Scoket connected..")

    ws.send(JSON.stringify({
        'user':Logged_username,
        'status':"online"
    }))
}


ws.onmessage = function(event){
    data = JSON.parse(event.data)
    console.log(data)

    // // Two separate send() method called from backend
    // // First is for all the Active Users present in the chatlist, type="active_users" 
    if (data.type == "active_users"){
        users = data.users

        users.forEach(user => {
            const update_users_status = document.getElementById(`${user}_status`)
            if(update_users_status){
                update_users_status.style.color = "green"
            }

            const sender_status = document.getElementById(`${sender_id}_id`);
            console.log("Found element:", user, sender, user== sender, "----", sender_status.innerHTML);
            
            if(user == sender){
                sender_status.innerHTML = "● Online"
                sender_status.style.color = "green";
            }
        })
    }


    // // If any user connected or disconnected, this is block will be executed. Here, activity status will be shown in chatlist.
    else if (data.type == "status_update"){
        user = data.user
        console.log(user, data.status)
        if (data.status){
            const update_users_status = document.getElementById(`${user}_status`)
            if(update_users_status){
                update_users_status.style.color = "green"
            }
        }
        else{
            const update_users_status = document.getElementById(`${user}_status`)
            if(update_users_status){
                update_users_status.style.color = "black"
            }
        }
    } 


    // const activity_status = document.getElementById(`${sender}_id`)
    // if 
    // if (activity_status){

    // }
}
    


ws.onclose = function(event){
    console.log("Online Status Connection Closed..")
}

