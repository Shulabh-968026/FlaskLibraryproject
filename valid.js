function A(f)
{

   	if(matchpass(f.t1,f.t2,"password does not match")==false)
	{
		f.t1.value="";
		f.t2.value="";
		f.t1.focus='()';
		return false;
	}
}
function matchpass(ele1,ele2,msg)
{
	if(ele1.value!=ele2.value)
	{
		alert(msg)
		return false;
	}
	else
	{
		return true;
	}
}