$(function (){
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.hose +"/chat/stream/";
    console.log("Connecting to "+ws_path)
    var socket = new ReconnectingWebSocket(ws_path);
    
    socket.onopen = function() {
        console.log("Connected to chat socket");
    };
    
    socket.onclose = function () {
        console.log("Disconnected from chat socket");
    }


	inRoom = function (roomId) {
			return $("#room-" + roomId).length > 0;
	};
	
	socket.onmessage = function (message) {
		
		console.log("Got websocket message " + message.data);
		var data = JSON.parse(message.data);
		
		if(data.error){
			alert(data.error);
			return;
		}
		//Handles joining?
		if(data.join){
			console.log("Joining room "+data.join);
			var roomdiv = $(
				"<div class='room' id='room-"+ data.join +"'>" +
				"<h2>" + data.title + "</h2>" +
				"<div class='messages'></div>" +
				"<input><button>Send</button>" +
				"</div>"
			);
			$("#chats").append(roomdiv);
			
		//Handles leaving?
		} else if(data.leave) {
			console.log("Leaving room "+ data.leave);
			$("#room-"+data.leave).remove();
		} else if(data.message){
			var msgdiv = $("#room-" + data.room + ".messages");
			var ok_msg = "<div class='message'" +
				"<span class='username'>" + data.username +"</span>"
				"<span class='body'>" + data.message + "</span>"
				"</div>";
			msgdiv.append(ok_msg);
			msdiv.scrollTop(msgdiv.prop("scrollHeight"));
		} else {
			console.log("Cannot handle message");
		}
	}
	
	roomdiv.find("button").on("click", function(){
		socket.send(JSON.stringify({
			"command": "send",
			"room": data.join,
			"message": roomdiv.find("inut").val()
		}));
		roomdiv.find("input").val("");
		return false;
	});
	
	//Should probably study all of this cause I dont really
	//know javascript....
	$("li.room-link").click(function () {
		roomId = $(this).attr("data-room-id");
		if(inRoom(roomId)) {
			$(this).removeClass("joined");
			socket.send(JSON.stringify({
				"command": "leave",
				"room": roomId
			}));
		} else {
			$(this).addClass("joined");
			socket.send(JSON.stringify({
				"command": "join",
				"room": roomId
			}));
		}
	});
});