const NORTH = 0
const EAST = 1
const SOUTH = 2
const WEST = 3

//x now unused
const compassToEnum = Object.freeze({
  "N": NORTH,
  "E": EAST,
  "S": SOUTH,
  "W": WEST
})

const pointerDisp = [[16, 0], [32, 16], [16, 32], [0, 16]]

// dir = compasEnum
function point(dID, dir){
  // by N/E/S/W
  let disp = pointerDisp[dir]
  
  if (dID != ALL_DANCERS) {
    e=pA[dID].pointer;
    e.setAttribute("x2", disp[0]);
    e.setAttribute("y2", disp[1]);
  }
  else {
    let i = pA.length - 1; 
    while(i >= 0) {
      e=pA[i].pointer
      e.setAttribute("x2", disp[0]);
      e.setAttribute("y2", disp[1]);
      i--;
    }
  }
}

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

// offsets array of [xOff, yOff] +- allowed
//? wish this didn't change both offsets
//? pass pA in
function move(dID, offsets){
  if (dID != ALL_DANCERS) {
    x=pA[dID].svg.x.baseVal;
    x.value=x.value + offsets[0]
    y=pA[dID].svg.y.baseVal;
    y.value=y.value + offsets[1]
  }
  else {
    let i = pA.length - 1; 
    while(i >= 0) {
      x=pA[i].svg.x.baseVal;
      x.value=x.value + offsets[0]
      y=pA[i].svg.y.baseVal;
      y.value=y.value + offsets[1]
      i--;
    }
  }
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




const actionCalls = Object.freeze({
 'step': move,
 'point': point
})



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
const NS="http://www.w3.org/2000/svg";
var svg = null;
// person array
var pA = [];

// Magic number for 'all dancers'
const ALL_DANCERS = -1

// enum for a dance move
//x
/*
var action = 0
var duration = 1
var target = 2
var direction = 3
*/

// 4 frames/sec?
let frameRate = 4
// in MS
//? should be fly/per dance calculated?
let frameTimeSize = 1000/frameRate
// In MS. Modified by tempo.
let beatTimeSize = null

//! Done not showing
//! applause always showing (needs callback)
//! animation not fluid
//! animation not with duration
//! hush not showing
//! swan lake not working
//! cancel not working
//! have to refresh for options





// Perform/UI //

var movesTotal = null
var movesI = 0
var moves = null




// Event Loop //
//Event loop items
// [call, dancerId, params]
const EL_CALL = 0;
const EL_DANCERID = 1;
const EL_PARAMS = 2;
let frameAnimationCalls = []

let frameCountdown = 0
//probably exceesive, but we need something
let notifyBeatFinshed = doNextBeat


function doFrame() {
  let i = frameAnimationCalls.length - 1
  while (i >= 0) {
    let c = frameAnimationCalls[i]
    // call!
    c[EL_CALL](c[EL_DANCERID], c[EL_PARAMS])
    i--
    }
  
  frameCountdown--
  
  if (frameCountdown > 0) {
      setTimeout(function() { doFrame(); }, (frameTimeSize));
  }
  else {
    frameAnimationCalls = []
    notifyBeatFinshed.call()
  }
}


function cancelAnimations() {
  frameCountdown = 0
}

//? needs defending against multicalls
function startAnimations() {
  // if running, don't bother
  if (!frameCountdown) {
    frameCountdown = famesPerBeat 
    setTimeout(function() { doFrame(); }, (frameTimeSize));
  }
}





// animation handling //

let famesPerBeat = null



function setTiming(tempo) {
  // time of the animation in ms
  //? lossy
  //? ceil upwards, not down
  //? errors make the dance too long
  famesPerBeat = Math.ceil(frameRate * (60/tempo))
  beatTimeSize = 1000 * (60/tempo)
}
  
//? now these are fixed, but if we introduce distance a dancer moves,
//? they will vary.
function calculateMoveOffsets(direction) {
  //! temp for now
  var distance = 96
  //? floor = errors go short, not long
  var moveSize = Math.floor(distance/famesPerBeat)
  switch (direction) {
    case NORTH: return [0, -moveSize]
    case EAST: return [moveSize, 0]
    case SOUTH: return [0, moveSize]
    case WEST: return [-moveSize, 0]
  }
  alert('d' + direction)
}

// make a easily callable data for animation
function pushFrameCall(m) {
  let action = m[D_ACTION]
  let call = actionCalls[action]
  let dancerId = m[D_TARGET]
  let id = (dancerId == 'All') ? ALL_DANCERS : Number(dancerId)
  // currently only handling 'step' here, so
  // calculate offsets
  // switch (action) {
  //case 'step'
  let params = calculateMoveOffsets(m[D_PARAMS])
  frameAnimationCalls.push([call, id, params])
}


// beat based //

let beatI = 0
let beatMoves = null
let notifyDanceEnded = endDance


//? should this load everything?
//? i.e. needs to be loop-based for multiple events?
function performBeat(m) {
  let ma = m[D_ACTION]

  let mad = moveAnimationType[ma]

  // show most moves
  //? D_ISMANYBEAT
  setMovesDisplay(ma)
  
  switch (mad) {
    case AT_ISFRAMEBASED:
      pushFrameCall(m)
      startAnimations()
      break
    case AT_ISANIMATED:
      // do it now?
      //! duplication with pushFrameCall 
      let dancerId = m[D_TARGET]
      let id = (dancerId == 'All') ? ALL_DANCERS : Number(dancerId)
      // call!
      actionCalls[m[D_ACTION]](id, m[D_PARAMS])
      // delay, continue
      setTimeout(function() { notifyBeatFinshed(); }, (beatTimeSize))
      break
    default:
      // AT_UNANIMATED this engine - nothing
      // delay, continue
      setTimeout(function() { notifyBeatFinshed(); }, (beatTimeSize))
  }
}

function doNextBeat(){
  if (beatI < beatMoves.length) {
    m = beatMoves[beatI]
    performBeat(m)
    beatI++
  }
  else notifyDanceEnded.call()
}

function startBeats(moves) {
    beatI = 0
    beatMoves = moves
    doNextBeat()
}

/////////////////////////////////////////////

// Dance-based //

function cancelDance() {
  cancelAnimations()
  // Scatter dancers? kill dancers?
  setStatus('bewildered audience')
}

function endDance() {
  setStatus('applause')
}

function startDance(dance) {
  setTiming(dance.tempo)
  
  setStatus('hush')

  updateDancers(dance.dancerCount)

  toStartPositions(dance.start)
  
  startBeats(dance.moves)
}

////////////////////////////////////////////


// Control //

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




//? may want to animate changes in dancer numbers,
//? and moving to start positions
function updateDancers(count) {

  // be nice, respect current dancers
  l = pA.length
  if (count < l) {
    var i = l - 1;
    while(i >= count) {
      svg.removeChild(pA[i].svg);
      d = pA.pop();
      //? popping seems to affect the dom, too?
      i--;
    }
  }
  else {
    if (count > l) {
      var i = count - l;
  
      while(i>0) {
        var d = createDancer()
        pA.push(d);
        svg.appendChild(d.svg);
        i--;
    }}
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


function cancelPerformance() {
  //This causes the performance section to think we
  //are on the last move
  //? could be more sophisticated, killing handles and spilling messages
movesI = movesTotal
//  setStatus('[audience] bewildered')

 
}


function perform(dance){
  setStatus('hush')

  updateDancers(dance.dancerCount);

  toStartPositions(dance.start);

  startMoves(dance.moves);
}


// Data //

// Also, [isAnimated, isFrameAnimated]
// isFrameAnimated means 'do we need frame animation or beat'. Here, a 
// clap is beat-animated, but mvement is frame-animated.
// this is an anomoly, specific to the engine? A triplet tap may e fully 
// animated by some engines, but beat-animated in a simple engine
// (like this)
// P.S. freeze ought to be faster. In some browsers (Chrome) it 
// currently is.
const AT_UNANIMATED = 0
const AT_ISANIMATED = 1
const AT_ISFRAMEBASED = 2
var moveAnimationType = Object.freeze({
  'step' : 2,
  'clap' : 0,
  'point' : 1
})

// params may include direction, weight, etc?
// simulation of helpful marrkup, so may include enums.
// format [action, target, isManyBeat,  optional[params]]
//? are we sticking with this? the only param is direction?
//! convert 'All'
const D_ACTION = 0;
const D_TARGET = 1;
const D_ISMANYBEAT = 2;
const D_PARAMS = 3;

const dance1 = {
  title: 'Coconutters',
  tempo: 30,
  //tempo: 64,
  dancerCount: 3,
  start: 'hline',
  moves: [
  ['step', 'All', false, SOUTH],
  ['step', 'All', false, NORTH],
  ['clap', 'All', false, NORTH],
  ['point', 'All', false, WEST],
  ['point', 'All', false, EAST],
  ['point', 'All', false, SOUTH],
  ['step', 'All', false, SOUTH],
  ['step', 'All', false, NORTH]
  ]
}

const dance4 = {
  title: 'Meeting Human Resources',
  tempo: 64,
  dancerCount: 5,
  start: 'vline',
  moves: [
  ['step', 'All', false, EAST],
  ['step', 'All', false, EAST],
  ['step', 'All', false, EAST],
  ['step', 'All', false, EAST],
  ['step', 'All', false, EAST],
  ['step', 'All', false, EAST],
  ['step', 'All', false, EAST],
  ['step', 'All', false, EAST]
  ]
}

const dance5 = {
  title: 'Swan Lake',
  tempo: 64,
  dancerCount: 1,
  start: 'hline',
  moves: [
  ['step', 'All', false, SOUTH],
  ['step', 'All', false, EAST],
  ['step', 'All', false, SOUTH],
  ['step', 'All', false, EAST],
  ['step', 'All', false, SOUTH],
  ['step', 'All', false, SOUTH]
  ]
}

const danceData = [dance1, dance1,  dance1, dance4, dance1, dance5]


// Control/UI //

//! enable
function validDance(d) {
  if(d.dancerCount > 6) {
    setStatus('Too many dancers for your browser. count:' + count)
    return false
  }
  return true
}

function setStatus(msg) {
    document.getElementById("status").textContent = msg;
}

function setMovesDisplay(msg) {
    document.getElementById("moves-display").textContent = msg;
}

//! dynamically build options
function getDanceFromWidget(){
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
  

  
  document.getElementById("stop").addEventListener("click", function () {
      //alert('stop')
    //cancelPerformance()
    cancelDance()
  }, false);
      
  document.getElementById("go").addEventListener("click", function () {
   // protect
  //       if (frameCount == 0) {
  //frameCount = 12;
    // get dance
    dance = getDanceFromWidget();
    setStatus('dance: ' + dance.title);
  
    //perform(dance);
    startDance(dance)
  }, false);
}
