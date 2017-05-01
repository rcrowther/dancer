

//! simutaneous moves
//! storing/restoring pointer data for twirl
//! second twirl in bbreakdance fails?
//! opacity not resetting
//! do circles?
//! multiople go press?
// SVG drivers //

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

function twirl(dID, dir){
  // leaves a 1 px dot in the middle :)
  if (dID != ALL_DANCERS) {
    let e=pA[dID].pointer;
    e.setAttribute("x2", 17)
    e.setAttribute("y2", 17)
    e=pA[dID].body
    e.setAttribute("fill-opacity", 0.3)
  }
  else {
    let i = pA.length - 1; 
    while(i >= 0) {
      let e=pA[i].pointer
      e.setAttribute("x2", 17)
      e.setAttribute("y2", 17)
      e=pA[i].body
      e.setAttribute("fill-opacity", 0.3)
      i--;
    }
  }
}


function twirlReturn(dID, args){
  // leaves a 1 px dot in the middle :)
  if (dID != ALL_DANCERS) {
    let e=pA[dID].pointer;
    //e.setAttribute("x2", args[0])
    //e.setAttribute("y2",args[1])
    e=pA[dID].body
    e.setAttribute("fill-opacity", 1)
  }
  else {
    let i = pA.length - 1; 
    while(i >= 0) {
      let e=pA[i].pointer
      //e.setAttribute("x2", 17)
      //e.setAttribute("y2", 17)
      e=pA[i].body
      e.setAttribute("fill-opacity", 1)
      i--;
    }
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
  'point': point,
  'twirl': twirl,
  'twirlr': twirlReturn
})



/*
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
let cancelled = false



// Event Loop //
// used for frame animations
//Event loop items
// [call, dancerId, params]
const EL_CALL = 0;
const EL_DANCERID = 1;
const EL_PARAMS = 2;

let frameAnimationCalls = []
let frameCountdown = 0
//probably excesive, but we need something
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
    // do return calls
    let i = returnAnimationCalls.length - 1
    while (i >= 0) {
      let c = returnAnimationCalls[i]
      // call!
      c[EL_CALL](c[EL_DANCERID], c[EL_PARAMS])
      i--
    }
    // clear
    returnAnimationCalls = []
    
    //send notify
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
let returnAnimationCalls = []



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
  // Should never be here
  //alert('d' + direction)
}



// beat based //

let beatI = 0
let beatMoves = null
let notifyDanceEnded = endDance


// make a easily callable data for animation
function pushFrameCall(m) {
  let action = m[D_ACTION]
  let call = actionCalls[action]
  let id = m[D_TARGET]
  //let id = (dancerId == 'All') ? ALL_DANCERS : Number(dancerId)
  // currently only handling 'step' here, so
  // calculate offsets
  // switch (action) {
  //case 'step'
  let params = calculateMoveOffsets(m[D_PARAMS])
  frameAnimationCalls.push([call, id, params])
}

// make a easily callable data for animation
function pushReturnCall(m) {
  let action = m[D_ACTION]
  let call = actionCalls[action + 'r']
  let id = m[D_TARGET]
  //let id = (dancerId == 'All') ? ALL_DANCERS : Number(dancerId)
  // currently only handling 'twirl' here, so
  // calculate offsets
  // switch (action) {
  //case 'twirl'
  let params = null //calculateMoveOffsets(m[D_PARAMS])
  returnAnimationCalls.push([call, id, params])
}



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
    case AT_RETURNANIMATED:
      pushReturnCall(m)
      let id = m[D_TARGET]
      //let id = (dancerId == 'All') ? ALL_DANCERS : Number(dancerId)
      // call!
      actionCalls[m[D_ACTION]](id, m[D_PARAMS])
      setTimeout(function() { notifyBeatFinshed(); }, (beatTimeSize))
      break
    case AT_ISANIMATED:
      // do it now?
      //! duplication with pushFrameCall 
      let id2 = m[D_TARGET]
      // call!
      actionCalls[m[D_ACTION]](id2, m[D_PARAMS])
      // delay, continue
      setTimeout(function() { notifyBeatFinshed(); }, (beatTimeSize))
      break
    default:
      // AT_UNANIMATED this engine - no animate
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

function cancelBeats(){
  beatI = beatMoves.length
}

function startBeats(moves) {
    beatI = 0
    beatMoves = moves
    doNextBeat()
}

/////////////////////////////////////////////

// Dance-based //

function cancelDance() {
  //? currently maxing globals, yuch.
  //? could also kill callback handlers
  //? for immediacy?
  cancelled = true
  cancelBeats()
  cancelAnimations()
}

function endDance() {
  setMovesDisplay('')
  if (!cancelled) {
    setStatus('applause')
  }
  else {
    // Scatter dancers? kill dancers?
    setStatus('bewildered audience')
    // done, so reset
    cancelled = false
  }
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
  //! script forces size, to ensure dancefllor?
  //? use viewport?
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
  d.y1.baseVal.value=16;
  d.x2.baseVal.value=16;
  d.y2.baseVal.value=32;
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
      //pointAllE(pA);
      point(ALL_DANCERS, EAST)
    break;
    default:
      // default is hline
      setAsHLine(pA, 64);
      //pointAllS(pA);
      point(ALL_DANCERS, SOUTH)
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

// Animation types
// AT_UNANIMATED is not animated, though the information is prpocessed and
// here shown in a progressing text display. Clap is currently 
// unanimated.
// AT_ISANIMATED is a one-shot this-to-that. Pointer is 
// animated. 
// AT_RETURNANIMATED is animated only for the beat.
// AT_ISFRAMEBASED means 'frame animation'. Step/move is frame-animated.
// P.S. freeze ought to be faster. In some browsers (Chrome) it 
// currently is.
const AT_UNANIMATED = 0
const AT_ISANIMATED = 1
const AT_RETURNANIMATED = 2
const AT_ISFRAMEBASED = 3
var moveAnimationType = Object.freeze({
  'step' : 3,
  'clap' : 0,
  'point' : 1,
  'twirl' : 2
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

const dance0 = {
  title: 'Coconutters',
  //tempo: 30,
  tempo: 64,
  dancerCount: 3,
  start: 'hline',
  moves: [
  ['point', ALL_DANCERS, false, EAST],
  ['step', ALL_DANCERS, false, EAST],
  ['point', ALL_DANCERS, false, SOUTH],
  ['step', ALL_DANCERS, false, SOUTH],
  ['step', ALL_DANCERS, false, NORTH],
  ['clap', ALL_DANCERS, false, NORTH],
  ['point', ALL_DANCERS, false, WEST],
  ['point', ALL_DANCERS, false, EAST],
  ['point', ALL_DANCERS, false, SOUTH],
  ['step', ALL_DANCERS, false, SOUTH],
  ['step', ALL_DANCERS, false, NORTH]
  ]
}

const dance1 = {
  title: 'Breakdance',
  //tempo: 30,
  tempo: 64,
  dancerCount: 3,
  start: 'hline',
  moves: [
    ['point', ALL_DANCERS, false, EAST],
    ['step', ALL_DANCERS, false, EAST],
    ['step', ALL_DANCERS, false, EAST],
    ['point', ALL_DANCERS, false, SOUTH],
    ['point', 2, false, EAST],
    ['step', 2, false, EAST],
    ['point', 2, false, WEST],
    ['point', 1, false, EAST],
    ['step', 1, false, EAST],
    ['point', 1, false, WEST],
    ['twirl', 0, false, null],
    ['point', 0, false, EAST],
    ['step', 0, false, EAST],
    ['twirl', 1, false, null]
    ['point', 1, false, NORTH],
    ['point', 1, false, SOUTH]
  ]
}

const dance2 = {
  title: 'Nightclub Moves',
  tempo: 90,
  dancerCount: 6,
  start: 'hline',
  moves: [
  ['point', 0, false, WEST],
  ['point', 4, false, WEST],
  ['point', 3, false, EAST],
  ['point', 0, false, EAST],
  ['point', 1, false, WEST],
  ['point', 2, false, EAST],
  ['point', 1, false, EAST],
  ['point', 2, false, WEST],
  ['point', 4, false, WEST],
  ['point', 5, false, EAST],
  ['step', 3, false,SOUTH],
  ['point', 4, false, NORTH],
  ['point', 5, false, WEST],
  ['step', 3, false,SOUTH],
  ['point', 4, false, WEST],
  ['point', 5, false, EAST],
  ['step', 3, false, EAST],
  ['point', 1, false, SOUTH],
  ['step', 3, false, EAST],
  ['point', 1, false, EAST]
  ]
}

const dance3 = {
  title: 'Meeting Human Resources',
  tempo: 30,
  dancerCount: 6,
  start: 'vline',
  moves: [
  ['step', ALL_DANCERS, false, EAST],
  ['step', ALL_DANCERS, false, EAST],
  ['step', ALL_DANCERS, false, EAST],
  ['step', ALL_DANCERS, false, EAST]
  ]
}

const dance4 = {
  title: 'War Games',
  tempo: 80,
  dancerCount: 2,
  start: 'hline',
  moves: [
  ['point', 0, false, WEST],
  ['point', 1, false, EAST],
  ['step', 0, false, WEST],
  ['step', 1, false, EAST],
  ['step', 1, false, EAST],
  ['point', 0, false, EAST],
  ['point', 1, false, WEST],
  ['step', 1, false, WEST],
  ['step', 0, false, EAST],
  ['point', 0, false, SOUTH],
  ['step', 0, false, SOUTH],
  ['point', 1, false, EAST],
  ['point', 0, false, NORTH],
  ['step', 0, false, NORTH],
  ['point', 0, false, SOUTH],
  ['point', 1, false, WEST],
  ['point', 1, false, EAST]
  ]
}

const dance5 = {
  title: 'Swan Lake',
  tempo: 64,
  dancerCount: 1,
  start: 'hline',
  moves: [
  ['step', 0, false, SOUTH],
  ['step', 0, false, EAST],
  ['step', 0, false, SOUTH],
  ['twirl', 0, false, null],
  ['point', 0, false, SOUTH],
  ['step', 0, false, EAST],
  ['step', 0, false, SOUTH],
  ['step', 0, false, SOUTH]
  ]
}

const danceData = [dance0, dance1,  dance2, dance3, dance4, dance5]


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
  //svg.style.minWidth="600px";
  //svg.style.minHeight="600px";
  

  
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
