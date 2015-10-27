function btnusr_onclick() 
{
	goto_you();
}

function handle_enter(e){
 var key=e.keyCode || e.which;
  if (key==13){
     goto_you();
  }
}

function goto_you(){
	var username = document.getElementById('username-input').value;
    window.location.href = "./you/"+username+"/";
}