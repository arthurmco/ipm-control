/* Load clients via AJAx by name.

   A text field with id = client_name must be present there to grab the name,
also an element with id = client_search with an ul as a child should be present
too, to show the results */
function load_clients(){
    var clientul = document.getElementById('client_search').getElementsByTagName('ul')[0];
    var clientname = document.getElementById('client_name').value;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
	if (this.readyState == 4 && this.status == 200) {
	    clients = JSON.parse(this.responseText);
	    console.log(clients)
	    
	    clientul.innerHTML = "";
	    
	    for(var i = 0; i < clients.length; i++) {
		var li = document.createElement("li");
		var li_text = document.createTextNode(clients[i].name);
		li.appendChild(li_text);
		clientul.appendChild(li);
	    }
	    
	}
    };
    
    xhttp.open("GET", "/api/client/search/?name=" + clientname,
	       true);
    xhttp.send();
}

/* Load client by ID. Shows name in element with id=client_name */
function load_client(client_id){

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
	if (this.readyState == 4 && this.status == 200) {
	    client = JSON.parse(this.responseText);
	    console.log(client)
	    
	    document.getElementById("client_name").innerHTML = client.name;
	    
	}
    };
    
    xhttp.open("GET", "/api/client/" + client_id, true);
    xhttp.send();
}
