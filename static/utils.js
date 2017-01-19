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

		var text_link = "<a href='/dashboard/client/" +
		    clients[i].id + "'>" + clients[i].name + "</a>";
		var license_link = "<a href='/api/client/" + clients[i].id +
		    "/license_file'>Baixar arquivo de licença</a>";
		
		var li_text = document.createTextNode("");
		li.appendChild(li_text);
		li.innerHTML = text_link + " | " + license_link;
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

function print_client_status(type, el, message) {
    if (type === 'ERROR') {
	el.style.color = "red";
    } else if (type === 'SUCCESS') {
	el.style.color = "green";
    }

    el.innerHTML = message;
}


function add_client() {
    
    var status = document.getElementById("client_status");
    var clientname = document.getElementById("cli_name").value;
    
    if (clientname == "") {
	print_client_status('ERROR', status, "Digite o nome do cliente");
	return;
    }
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
	if (this.readyState == 4 && this.status == 200) {
	    client = JSON.parse(this.responseText);
	    console.log(client)

	    if (client.name == clientname) {
		print_client_status('SUCCESS', status, "Cliente adicionado com sucesso!");
	    } else {
		print_client_status('ERROR', status, "Erro: Inconsistência");
	    }
	    
	} else if (this.readyState == 4 && this.status >= 400) {
	    print_client_status('ERROR', status, "Algo de errado ocorreu no servidor");
	}
    };
    
    xhttp.open("GET", "/api/client/add?name=" + clientname, true);
    xhttp.send();
}
