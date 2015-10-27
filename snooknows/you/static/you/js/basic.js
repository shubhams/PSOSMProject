function btnusr_onclick() 
{
	var username = document.getElementById('username-input').value;
    window.location.href = "./you/"+username+"/";
}