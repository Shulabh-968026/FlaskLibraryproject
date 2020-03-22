function B()
{
    var a=document.forms["form2"]["password"].value;
    var b=document.forms["form2"]["cpassword"].value;
    /*if(a=="")
    {
    document.getElementbyid('message').innerHTML="**please fill this field";
    return false;
    }
    if(a.length<5)
    {
    document.getElementbyid('message').innerHTML="**password is too short";
    return false;
    }*/
    if(a!=b)
    {
     alert("password are not same");
     a.focus();
     return false;
    }
}
	/*if(matchpass(f.password,f.cpassword,"password does not match")==false)
	{
		f.password.value="";
		f.cpassword.value="";
		f.password.focus='()';
		return false;
	}
}
function matchpass(ele1,ele2,msg)
{
	if(ele1.value!=ele2.value)
	{
		alert(msg);
		return false;
	}
	else
	{
		return true;
	}
}*/