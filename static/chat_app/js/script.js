const sender_id = document.getElementById('sender_id').textContent
const current_user_data = document.getElementById('logged_user').textContent
current_user = JSON.parse(current_user_data)

console.log("sender_id", sender_id)
console.log("logged_user", current_user)


const socket = new WebSocket('ws://' + window.location.host + '/ws/' + sender_id +'/')

socket.onopen = function(event){
    console.log("Websocket Connnected...")
}

socket.addEventListener('message', (event)=>{
    data = JSON.parse(event['data'])
    console.log("Message from server :", data)

    let msg = data['message']
    let sender = data['username']




    // const msgContainer = document.querySelector(".chat-messages")
    // const messageElement = document.createElement('div')
    // messageElement.classList.add('message');

    // if(current_user == sender){
    //     messageElement.classList.add('sent'); // Use the 'sent' class
    //     messageElement.innerHTML = `
    //         <div class="message-content">${msg}</div>
    //     `
    // }
    // else{
    //     messageElement.classList.add('received'); // Use the 'received' class
    //     messageElement.innerHTML = `
    //         <div class="message-content">${msg}</div>
    //     `
    // }

    // msgContainer.appendChild(messageElement);



    if(current_user == sender){
        document.querySelector('#message-body').innerHTML += `<div class="message outgoing">
                                ${msg}<div class="timestamp"></div>
                            </div>
        
        `
    }
    else{
        document.querySelector('#message-body').innerHTML += `<div class="message incoming">
                                ${msg}<div class="timestamp"></div>
                            </div>
        
        `
    }


})

socket.addEventListener('close', ()=>{
    console.log("Connection closed...")
})  



function getInput(){
    let messsage_input = document.getElementById("message-input")
    message = messsage_input.value
    console.log("Typed message", message)
    socket.send(JSON.stringify({
        'message': message,
        'username': current_user,
    }))
    messsage_input.value = ""
}






// // Auto-scroll to bottom
// const messagesDiv = document.getElementById("messages");
// function scrollToBottom() {
//     messagesDiv.scrollTop = messagesDiv.scrollHeight;
// }
// scrollToBottom();

// // Add new message
// function sendMessage(event) {
//     event.preventDefault();
//     const input = document.getElementById("msgInput");
//     if (input.value.trim() !== "") {
//     const newMsg = document.createElement("div");
//     newMsg.className = "message outgoing";
//     newMsg.innerHTML = input.value + `<div class="timestamp">${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>`;
//     messagesDiv.appendChild(newMsg);
//     input.value = "";
//     scrollToBottom();
//     }
// }