// JavaScript Document

function changeNavbar() {
	//alert("small");
	if(screen.width < 1000) {
		
		(document.getElementsByClassName)[0].style.padding = "0px";
		(document.getElementsByClassName)[1].style.padding = "0px";
		(document.getElementsByClassName)[2].style.padding = "0px";
  }
}

window.onresize = changeNavbar;
