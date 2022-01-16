let utter = new SpeechSynthesisUtterance();
utter.lang = 'en-US';
// utter.text = 'Hello World';
utter.volume = 0.5;

// event after text has been spoken
// utter.onend = function() {
// 	alert('Speech has finished');
// }

function onConnectionLost(){
	console.log("connection lost");
	document.getElementById("status").innerHTML = "Connection Lost";
	document.getElementById("status-box").style.backgroundColor = "#f78989d3";
	document.getElementById("messages").innerHTML ="Connection Lost";
	connected_flag=0;
}

function onFailure(message) {
	console.log("Failed");
	document.getElementById("status").innerHTML = "Connection Lost";
	document.getElementById("status-box").style.backgroundColor = "#f78989d3";
	document.getElementById("messages").innerHTML = "Connection Failed- Retrying";
	setTimeout(MQTTconnect, reconnectTimeout);
}

function onMessageArrived(r_message){
	// out_msg = "Message received " + r_message.payloadString + "<br>";
	out_msg = r_message.payloadString;
	utter.text = r_message.payloadString;
	// speak
	window.speechSynthesis.speak(utter);
	// out_msg = out_msg + "Message received Topic " + r_message.destinationName;
	//console.log("Message received ",r_message.payloadString);
	console.log(out_msg);
	document.getElementById("messages").innerHTML = out_msg;
}

function onConnected(recon,url){
	console.log(" in onConnected " + reconn);
}

function onConnect() {
	// Once a connection has been made, make a subscription and send a message.
	document.getElementById("messages").innerHTML = "Connected to " + host + " on port " + port;
	connected_flag = 1
	document.getElementById("status").innerHTML = "Connected";
	document.getElementById("status-box").style.backgroundColor = "#93f193cb";
	console.log("on Connect " + connected_flag);
	//mqtt.subscribe("sensor1");
	//message = new Paho.MQTT.Message("Hello World");
	//message.destinationName = "sensor1";
	//mqtt.send(message);
}

function MQTTconnect() {
	document.getElementById("messages").innerHTML = "";
	var s = document.forms["connform"]["server"].value;
	var p = document.forms["connform"]["port"].value;
	if (p != "") {
		console.log("ports");
		port = parseInt(p);
		console.log("port" + port);
	}
	if (s != "") {
		host = s;
		console.log("host");
	}
	console.log("connecting to " + host + " " + port);
	var x = Math.floor(Math.random() * 10000); 
	var cname = "orderform-" + x;
	mqtt = new Paho.MQTT.Client(host, port, cname);
	//document.write("connecting to "+ host);
	var options = {
		timeout: 3,
		onSuccess: onConnect,
		onFailure: onFailure,
	};

	mqtt.onConnectionLost = onConnectionLost;
	mqtt.onMessageArrived = onMessageArrived;
	//mqtt.onConnected = onConnected;

	// mqtt.tls_set('./ca.crt', tls_version=2)
	mqtt.connect(options);
	return false;
}

function sub_topics(){
	document.getElementById("messages").innerHTML = "";
	if (connected_flag == 0) {
		out_msg = "<b>Not Connected so can't subscribe</b>"
		console.log(out_msg);
		document.getElementById("messages").innerHTML = out_msg;
		return false;
	}
	var stopic = document.forms["subs"]["Stopic"].value;
	console.log("Subscribing to topic = " + stopic);
	mqtt.subscribe(stopic);
	return false;
}
