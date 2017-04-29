
function pointN(p){
e=p.pointer;
e.setAttribute("x1", "16");
e.setAttribute("y1", "0");
e.setAttribute("x2", "16");
e.setAttribute("y2", "16");
}

function pointS(p){
e=p.pointer;
e.setAttribute("x1", "16");
e.setAttribute("y1", "16");
e.setAttribute("x2", "16");
e.setAttribute("y2", "24");
}

function pointE(p){
e=p.pointer;
e.setAttribute("x1", "16");
e.setAttribute("y1", "16");
e.setAttribute("x2", "32");
e.setAttribute("y2", "16");
}

function pointW(p){
e=p.pointer;
e.setAttribute("x1", "0");
e.setAttribute("y1", "16");
e.setAttribute("x2", "16");
e.setAttribute("y2", "16");
}



function pointAllN(pa){
var i = pa.length - 1; 
while(i >= 0) {
e=pa[i].pointer;
e.setAttribute("x1", "16");
e.setAttribute("y1", "0");
e.setAttribute("x2", "16");
e.setAttribute("y2", "16");
i -= 1;
}
}

function pointAllS(pa){
var i = pa.length - 1; 
while(i >= 0) {
e=pa[i].pointer;
e.setAttribute("x1", "16");
e.setAttribute("y1", "16");
e.setAttribute("x2", "16");
e.setAttribute("y2", "32");
i -= 1;
}
}

function pointAllE(pa){
var i = pa.length - 1; 
while(i >= 0) {
e=pa[i].pointer;
e.setAttribute("x1", "16");
e.setAttribute("y1", "16");
e.setAttribute("x2", "32");
e.setAttribute("y2", "16");
i -= 1;
}
}

function pointAllW(pa){
var i = pa.length - 1; 
while(i >= 0) {
e=pa[i].pointer;
e.setAttribute("x1", "0");
e.setAttribute("y1", "16");
e.setAttribute("x2", "16");
e.setAttribute("y2", "16");
i -= 1;
}
}

function moveN(p){
y=p.svg.y.baseVal;
y.value=y.value - 8;
}

function moveE(p){
x=p.svg.x.baseVal;
x.value=x.value + 8;
}

function moveS(p){
y=p.svg.y.baseVal;
y.value=y.value + 8;
}

function moveW(p){
x=p.svg.x.baseVal;
x.value=x.value - 8;
}


function moveAllN(pa){
var i = pa.length - 1; 
while(i >= 0) {
y=pa[i].svg.y.baseVal;
y.value=y.value - 8;
i--;
}
}

function moveAllE(pa){
var i = pa.length - 1; 
while(i >= 0) {
x=pa[i].svg.x.baseVal;
x.value=x.value + 8;
i--;
}
}

function moveAllS(pa){
var i = pa.length - 1; 
while(i >= 0) {
y=pa[i].svg.y.baseVal;
y.value=y.value + 8;
i--;
}
}

function moveAllW(pa){
var i = pa.length - 1; 
while(i >= 0) {
x=pa[i].svg.x.baseVal;
x.value=x.value - 8;
i--;
}
}

function setAsHLine(pa, spacing){
  var l = pa.length;
  var i = 0; 
  var x = 100;
  var y = 100; 
  while(i < l) {
    //? why not work?
    //pa[i].svg.x.baseVal = x;
    pa[i].svg.setAttribute("x", x);
    //pa[i].svg.y.baseVal = y;
    pa[i].svg.setAttribute("y", y);

    x += spacing;
    i++;
  }
}

function setAsVLine(pa, spacing){
  var l = pa.length;
  var i = 0; 
  var x = 100;
  var y = 100; 
  while(i < l) {
    //? why not work?
    //pa[i].svg.x.baseVal = x;
    pa[i].svg.setAttribute("x", x);
    //pa[i].svg.y.baseVal = y;
    pa[i].svg.setAttribute("y", y);
    y += spacing;
    i++;
  }
}

////////////////////////////////////////////////////////

var createPerson=function(svg, x,y){
 var NS="http://www.w3.org/2000/svg";

 var is = document.createElementNS(NS,"svg");
 is.x.baseVal.value=x;
 is.y.baseVal.value=y;
 is.width.baseVal.value=32;
 is.height.baseVal.value=32;

 var b=document.createElementNS(NS,"circle");
 b.cx.baseVal.value=16;
 b.cy.baseVal.value=16;
 b.r.baseVal.value=16;
 b.style.fill="#ffeeb8";
 is.appendChild(b);

 var d=document.createElementNS(NS,"line");
 d.x1.baseVal.value=16;
 d.y1.baseVal.value=0;
 d.x2.baseVal.value=16;
 d.y2.baseVal.value=16;
 d.style.stroke="#000000";
 d.style.strokeWidth="2";
 is.appendChild(d);

 svg.appendChild(is);
 return {svg: is, body:b, pointer:d};
}




var moveToAction = {
 'S': moveAllS,
 'E' : moveAllE,
 'S': moveAllS,
 'W': moveAllW
/*
 'TurnL': moveTurnL,
 'TurnR': moveTurnR,
*/


}



/*
window.onload = function (){

var pCount = 3;
//milliseconds
// don't go under 1/60 sec framerate i.e. 17.
// fix as framerate?
// 40 - 25f/sec
var frameRate = 40;

var stepTime = 64;

//var movDist = 96;
// 96/8 = 12 frames
// fastest this will be is 3/2 sec (2 * 80 to the bar)
var callrate = (120/stepTime * 1000)/12



var currentMove = moveAllE





//


pointN(pA[0]);
pointE(pA[0]);

moveE(pA[0]);
moveS(pA[0]);

// suspendRedraw  requestAnimationFrame 
var svgPersonDirections = svgContainer.getElementsByClassName("person-direction");
 var svgPaths = svgContainer.getElementsByTagNameNS(ns,"path");
var svgDoc = svgPersonDirections[0].contentDocument;

var svgPath = svgContainer.getElementsByTagNameNS(ns,"line");
svgPersons[0].attributes[1].value = "12"
svgPersons[0].attributes[1].value = "0"
document.getElementById("svg_image_id").getSVGDocument().get‌​ElementById("circle_‌​id").style.fill="blu‌​e"; 



function renderLoop(first, action) {
   if (first) {
   frameCount = 12;
   } 
   action(pA);
   frameCount--;
   //window.requestAnimationFrame(renderLoop);
if (frameCount > 0) {
setTimeout(function() {
          renderLoop(false, action);
}, (callrate));
        }
}




// document.getElementById("go").addEventListener("click", function () {
 //       if (frameCount == 0) {
//frameCount = 12;

          renderLoop(true, currentMove);


// document.getElementById("stop").addEventListener("click", function () {

          //alert('stop')
  //    }, false);
}
*/
/////////////////////////////////////////////////////////////////////////



// global data
var NS="http://www.w3.org/2000/svg";
var svg = null;
// person array
var pA = [];


function performMove(){
}



// Perform/UI //
function createDancer() {
  // Doesn't create a position?
  
  var is = document.createElementNS(NS,"svg");
  is.x.baseVal.value=100;
  is.y.baseVal.value=100;
  //is.width.baseVal.value="32px";
  is.setAttribute("width", "32px");

  //is.height.baseVal.value="32px";
  is.setAttribute("height", "32px");
  
  var b=document.createElementNS(NS,"circle");
  b.cx.baseVal.value=16;
  b.cy.baseVal.value=16;
  b.r.baseVal.value=16;
  b.style.fill="#ffeeb8";
  is.appendChild(b);
  
  var d=document.createElementNS(NS,"line");
  d.x1.baseVal.value=16;
  d.y1.baseVal.value=0;
  d.x2.baseVal.value=16;
  d.y2.baseVal.value=16;
  d.style.stroke="#000000";
  d.style.strokeWidth="2";
  is.appendChild(d);
  
  return {svg: is, body: b, pointer: d}
}


// Control //


//? may want to animate changes in dancer numbers,
//? and moving to start positions
function updateDancers(count) {

  // be nice, respect current dancers
  if (count < pA.length) {
    var i= r.length;
    while(i>0) {
      d = pA.pop(p);
      svg.removeChild(d.is);
      i--;
    }
  }
  else {
    var i= count - pA.length;

    while(i>0) {
      var d = createDancer()
      pA.push(d);
      svg.appendChild(d.svg);
      i--;
    }
  }
}

function toStartPositions(desc){
  switch(desc) {
    case 'vline':
      setAsVLine(pA, 64);
      pointAllE(pA);
    break;
    default:
       // default is hline
       setAsHLine(pA, 64);
       pointAllS(pA);
  }
}


function cancelPerformance () {

}

function perform(dance){

  updateDancers(dance.dancerCount);

  toStartPositions(dance.start);
  /*
  var moves = dance.moves
  i= moves.length-1;
  while(i >=0) {
    currentMove = moves[i];
    performMove()
    i--;
  }
*/
}



// Data //
var dance1 = {
  title: 'Coconutters',
  speed: 64,
  dancerCount: 3,
  start: 'hline',
  moves: [
  'S All 2',
  'N All 2',
  'Turn All W',
  'Turn All S',
  'S All 2',
  'N All 2'
  ]
}

var dance4 = {
  title: 'Meeting Human Resources',
  speed: 64,
  dancerCount: 5,
  start: 'vline',
  moves: [
  'E All 8'
  ]
}

var dance5 = {
  title: 'Swan Lake',
  speed: 64,
  dancerCount: 1,
  start: 'hline',
  moves: [
  'E All 8'
  ]
}

var danceData = [dance1, dance1,  dance1, dance4, dance1, dance5]


// Control/UI //

function setStatus(msg) {
    document.getElementById("status").textContent = msg;
}

//! dynamically build options
function getDance(){
  var e = document.getElementById("dance-id")
  var o = e.options[e.selectedIndex];
  var danceId = o.value;
  var danceName = o.text;
  //! tmp, offer options
   
  return danceData[danceId];
}

window.onload = function (){
  // set the container
  svg = document.getElementById("svg");
  var ns = "http://www.w3.org/2000/svg";
  svg.style.minWidth="600px";
  svg.style.minHeight="600px";
  
  // get dance
  dance = getDance();
  setStatus('dance: ' + dance.title);
  
  perform(dance);
}
