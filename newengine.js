let nextTime = 0
let delay = 1000

function eventLoop(currentTime) {
    if(currentTime < nextTime){requestAnimationFrame(eventLoop); return;}
    nextTime = currentTime + delay
    // do stuff every 1000ms
    requestAnimationFrame(looper)
}



window.onload = function (){
  // set the container
  svg = document.getElementById("svg");
  var ns = "http://www.w3.org/2000/svg";
  //svg.style.minWidth="600px";
  //svg.style.minHeight="600px";
  

  document.getElementById("stop").addEventListener("click", function () {
    cancelDance()
  }, false);
      
  document.getElementById("go").addEventListener("click", function () {
    // get dance
    dance = getDanceFromWidget()
    
    //? doing nothing? immediately removed...
    //setStatus('dance: ' + dance.title);
    
    startDance(dance)

  }, false);
}

