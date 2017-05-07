
//! = Event shcheduling
//! While not running events, we need to be doing things like get more 
//! data(online), or uilding new parameters for queues
//! timing will be very off. Maybe use a double event seq, load while
//!  one is processing, then switch?
//! Control feels backwards? Currently, we load data, then run the
//! engine.  It controls the stops. But we maybe need the engine running,
//! then feed it data? And it idles itself?
//! = Events
//! simutaneous moves
//! do circles?
//! = Data
//! faster to store the position/display data, update that, then
//! show, rather than getting data from the DOM?
//! can always store pointer directions, say, not absolute positions 
//! (then calculate)
//! but ms examples use the DOM?
//! = particulars
//! f (!svgSupported()) { // Bail if the browser doesn't support HTML5 with inline SVG. alert("Inline SVG in HTML5 is not supported. This document requires a browser that supports HTML5 and inline SVG."); 
//! setAttribute is slow?
//! https://msdn.microsoft.com/en-us/library/gg193979(v=vs.85).aspx
//! mySquare.transform.baseVal.getItem(0).setRotate(mySquare.currentTheta, 0, 0);
//! yes, direct access can be faster
//! baseVal.appendItem
//! zoom
//! look at setInterval()/clearInterval(),
//! and requestAnimationFrame/cancelAnimationFrame
//! - not sure if repaint delay works on svg?
//! - have to rejig code for variable timing
//! - doesn't stop when hidden on my Firefox?
//! - will sync with GPU, though
//! - look at greensock? Or just do it?
//! - will have to rewrite for current time...
//! SIML, XML presentation of multimedia. Not interesting.
/*
 * 

 */
// SVG drivers //

const NORTH = 0
const EAST = 1
const SOUTH = 2
const WEST = 3


const compassToEnum = Object.freeze({
  "N": NORTH,
  "E": EAST,
  "S": SOUTH,
  "W": WEST
})




// offsets array of [xOff, yOff] +- allowed
//? wish this didn't change both offsets
//? pass pA in
function move(dID, offsets){
  let d = pA[dID]
  let x=d.svg.x.baseVal
  x.value=x.value + offsets[0]
  let y=d.svg.y.baseVal
  y.value=y.value + offsets[1]
}

//! must all be different offsets for different dancers?
function moveAbsolute(dID, args){
  let d = pA[dID]
  let i = 0
  // All different params, so must detect
  // wether params is two elements, or seq of pairs 
  if (dID == ALL_DANCERS) i = dID << 1
  let x = d.svg.x.baseVal
  x.value = x.value + args[i]
  //d.svg.setAttribute("x", x)
  let y=d.svg.y.baseVal
  y.value = y.value + args[i + 1]
}

//! must all be different offsets for different dancers?
function offsetToPos(dID, args){
  let d = pA[dID]
  let i = dID << 1
  d.svg.setAttribute("x", args[i])
  d.svg.setAttribute("y", args[i + 1])
}


const pointerDisp = [[16, 0], [32, 16], [16, 32], [0, 16]]

// @args compasEnum
function point(dID, args){
  let d = pA[dID]
  // by N/E/S/W
  let disp = pointerDisp[args]
  let e=d.pointer
  e.setAttribute("x2", disp[0])
  e.setAttribute("y2", disp[1])
}

// args is null
function twirl(dID, args){
  let d = pA[dID]
  // leaves a 1 px dot in the middle :)
  let e=d.pointer;
  e.setAttribute("x2", 17)
  e.setAttribute("y2", 17)
  e=d.body
  e.setAttribute("fill-opacity", 0.2)
}

// args is pair/seq of [x y]
function twirlReturn(dID, args){
  // leaves a 1 px dot in the middle :)
  let d = pA[dID]
  let e=d.pointer
  e.setAttribute("x2", args[0])
  e.setAttribute("y2",args[1])
  e=d.body
  e.setAttribute("fill-opacity", 1)
}

// args = directionEnum
function kick(dID, args){
  let d = pA[dID]
  // vertical
  let a = "translate(16 16) scale(0.5 1) translate(-16 -16)"
  if (args == NORTH || args == SOUTH) {
     // orientate horizontally
     a = "translate(16 16) scale(1 0.5) translate(-16 -16)"
  }

  let e=d.body
  e.setAttribute( "transform", a)
}

function kickr(dID, args){
  let d = pA[dID]
  let e=d.body
  e.setAttribute("transform", "scale(1 1)")
}

function jump(dID, args){
  let d = pA[dID]
  let e=d.body
  e.r.baseVal.value=10
}

function jumpr(dID, args){
  let d = pA[dID]
  let e=d.body
  e.r.baseVal.value=16
}

function clap(dID, args){
  let d = pA[dID]
  let e=d.body 
  e.style.fill="url(#rg)"
}
  
function clapr(dID, args){
  let d = pA[dID]
  let e=d.body
  e.style.fill="#ffeeb8"
} 


// start pos //
//x
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

//x
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

/* Move dancers
 * Brute runs a move. Will not work for return-animated or 
 * frame-animated moves, only beat start moves.
 */
 // This is inlined into the event seq,
 // but here for one-offs, like startup.
function mkMove(dID, func, args) {
    if (dID != ALL_DANCERS) {
      func(dID, args)
    }
    else {
      let i = pA.length - 1
      while(i >= 0) {
        func(i, args) 
        i--
      }
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
  'moveAbsolute' : moveAbsolute,
  'huddleAbsolute' : offsetToPos,
  'point': point,
  'kick': kick,
  'kickr': kickr,
  'clap': clap,
  'clapr': clapr,
  'jump': jump,
  'jumpr': jumpr,
  'twirl': twirl,
  'twirlr': twirlReturn
})


/////////////////////////////////////////////////////////////////////////



// global data
const NS="http://www.w3.org/2000/svg";
var svg = null;
// person array
var pA = [];

// Magic number for 'all dancers'
const ALL_DANCERS = -1


// 4 frames/sec?
let frameRate = 4
// in MS
//? should be fly/per dance calculated?
let frameTimeSize = 1000/frameRate
// In MS. Modified by tempo.
let beatTimeSize = null




//! animation not fluid
//! animation not with duration
//! have to refresh for options
// Perform/UI //

var movesTotal = null
var movesI = 0
var moves = null

const ES_IDLE = 1
const ES_DANCING = 2
const ES_CANCELLED = 3
let engineStatus = ES_IDLE



// Event Loop //
// used for frame animations

// event loop element format
// [call, dancerId, params]
const EL_CALL = 0
const EL_DANCERID = 1
const EL_PARAMS = 2

let frameAnimationCalls = []
let frameCountdown = 0

let beatEndCalls = []

//probably excesive, but we need something
const notifyBeatFinshed = doNextBeat


function doFrame() {
  let i = frameAnimationCalls.length - 1
  while (i >= 0) {
    let c = frameAnimationCalls[i]
    // call!
    //c[EL_CALL](c[EL_DANCERID], c[EL_PARAMS])
    let dID = c[EL_DANCERID]
    if (dID != ALL_DANCERS) {
          c[EL_CALL](dID, c[EL_PARAMS])
    }
    else {
      let i = pA.length - 1
      while(i >= 0) {
        c[EL_CALL](i, c[EL_PARAMS]) 
        i--
      }
    }
    i--
  }
  
  frameCountdown--
  
  if (frameCountdown > 0) {
      setTimeout(function() { doFrame(); }, (frameTimeSize));
  }
  else {
    frameAnimationCalls = []

    //send notify
    notifyBeatFinshed.call()
  }
}


function startAnimations() {
  // if running, don't bother
  if (!frameCountdown) {
    frameCountdown = famesPerBeat 
    setTimeout(function() { doFrame(); }, (frameTimeSize));
  }
}



// Beat-based animation handling //

let famesPerBeat = null
let beatStartCalls = []


// utilities //
function setTiming(tempo) {
  // time of the animation in ms
  //? lossy
  //? ceil upwards, not down
  //? errors make the dance too long
  famesPerBeat = Math.ceil(frameRate * (60/tempo))
  beatTimeSize = 1000 * (60/tempo)
}
  
  
// return offsets to an absolute point
// can make dancers run fast, if they must cover the floor.
// args [x, y] target
function moveAbsoluteParams(m) {
  let targetPos = m[D_PARAMS]
  let x = targetPos[0]
  let y = targetPos[1]
  let dID = m[D_TARGET]
  if (dID != ALL_DANCERS) {
    let e = pA[dID].svg
    return [Math.floor((x - e.x.baseVal.value)/famesPerBeat),  Math.floor((y - e.y.baseVal.value)/famesPerBeat)]
  }
  else {
    let args = []
    let i = 0
    let l = pA.length
    while(i < l) {
      let e = pA[i].svg
      args.push(Math.floor((x - e.x.baseVal.value)/famesPerBeat))
      args.push(Math.floor((y - e.y.baseVal.value)/famesPerBeat))
      i++
    }
    return args
  }
}


// return fixed step length based on frames
//? now these are fixed distance, but if we introduce distance 
//? a dancer moves,
//? they will vary.
function stepParams(m) {
  let direction = m[D_PARAMS]
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

// return offset, random within a given area
// args must be [x,y,width,height] for bounding box
//! this looks expensive?
function randomPosParams(m) {
  let args = m[D_PARAMS]
  let x = args[0]
  let y = args[1]
  let width = args[2]
  let height = args[3]
  
  if (m[D_TARGET] != ALL_DANCERS) {
    let xr = Math.floor(Math.random()*(width + 1)) + x
    let yr = Math.floor(Math.random()*(height + 1)) + y
    return [x, y]
  }
  else {
    let args = []
    let xa = width + 1
    let ya = height + 1
    
    let i = pA.length - 1
    while(i >= 0) {
      let xr = Math.floor(Math.random()*xa) + x
      let yr = Math.floor(Math.random()*ya) + y
      args.push(xr)
      args.push(yr)
      i--
    }
    return args
  }
}


// return current pointer positions
function pointerParams(m) {
  if (m[D_TARGET] != ALL_DANCERS) {
    e = pA[m[D_TARGET]].pointer
    return [e.getAttribute("x2"), e.getAttribute("y2")]
  }
  else {
    let args = []
    let i = pA.length - 1
    while(i >= 0) {
      e = pA[i].pointer
      args.push(e.getAttribute("x2"))
      args.push(e.getAttribute("y2"))
      i--
    }
    return args
  }
}

// return params for current positions
function posParams(m) {
  if (m[D_TARGET] != ALL_DANCERS) {
    e = pA[m[D_TARGET]].svg
    return [e.x.baseVal, e.y.baseVal]
  }
  else {
    let args = []
    let i = pA.length - 1
    while(i >= 0) {
      e = pA[i].svg
      args.push(e.x.baseVal)
      args.push(e.y.baseVal)
      i--
    }
    return args
  }
}

function paramsForCall(m, action) {
  switch(action) {
  case 'step': return stepParams(m)
  case 'huddleAbsolute': return randomPosParams(m)
  case 'twirlr': return pointerParams(m)
  // pass direction
  case 'point': 
  case 'kick': return m[D_PARAMS]
  case 'moveAbsolute': return moveAbsoluteParams(m)
  case 'twirl':
  case 'clap' :
  case 'clapr' : 
  case 'kickr': 
  case 'jump': 
  case 'jumpr': 
  default:
  return null
  }
}



// beat-based event handling //

let beatI = 0
let beatMoves = null
let notifyDanceEnded = endDance


//? should this load everything?
//? i.e. needs to be loop-based for multiple events?
function loadMove(m) {
  let a = m[D_ACTION]
  let call = actionCalls[a]
  //! all junk code if non animated command?
  //if (!call) alert('unrecognised command:' + a)
  let id = m[D_TARGET]
  let params = paramsForCall(m, a)

  let mad = moveAnimationType[a]

  switch (mad) {
    case AT_ISFRAMEBASED:
      frameAnimationCalls.push([call, id, params])
      break
    case AT_ISANIMATED:
      beatStartCalls.push([call, id, params])
      break
    case AT_RETURNANIMATED:
      beatStartCalls.push([call, id, params])
      let ar = a + 'r'
      let callr = actionCalls[ar]
      let paramsr = paramsForCall(m, ar) 
      beatEndCalls.push([callr, id, paramsr])
      break
    default:
      // do nothing (may show elsewhere)
  }
}


function doBeatStartCalls() {
    // do return calls
    //? done without timeout isolation/async will slow
    //? the clock, but is linear synced.
    let i = beatStartCalls.length - 1
    while (i >= 0) {
      let c = beatStartCalls[i]
      
      // call!      
      //c[EL_CALL](c[EL_DANCERID], c[EL_PARAMS])
      let dID = c[EL_DANCERID]
      if (dID != ALL_DANCERS) {
            c[EL_CALL](dID, c[EL_PARAMS])
      }
      else {
        let i = pA.length - 1
        while(i >= 0) {
          c[EL_CALL](i, c[EL_PARAMS]) 
          i--
        }
      }
      
      i--
    }
    
    // clear
    beatStartCalls = []
}

function doBeatEndCalls() {
    // do return calls
    //? done without timeout isolation will slow
    //? the clock, but is linear synced.
    let i = beatEndCalls.length - 1
    while (i >= 0) {
      let c = beatEndCalls[i]
      
      // call!
      //c[EL_CALL](c[EL_DANCERID], c[EL_PARAMS])
      let dID = c[EL_DANCERID]
      if (dID != ALL_DANCERS) {
            c[EL_CALL](dID, c[EL_PARAMS])
      }
      else {
        let i = pA.length - 1
        while(i >= 0) {
          c[EL_CALL](i, c[EL_PARAMS]) 
          i--
        }
      }
      
      i--
    }

    // clear
    beatEndCalls = []
}

function doNextBeat(){
  doBeatEndCalls()

  if (beatI < beatMoves.length && engineStatus == ES_DANCING) {
    m = beatMoves[beatI]
    loadMove(m)

    //? TMP: show moves
    //? D_ISMANYBEAT
    setMovesDisplay(m[D_ACTION])
    
    doBeatStartCalls()
    //? junk code if no animations?
    startAnimations()
    beatI++
  }
  else notifyDanceEnded.call()
}



function startBeats(moves, endCall) {
    beatI = 0
    beatMoves = moves
    // ensure this, as single beats can reset it.
    notifyDanceEnded = endCall
    doNextBeat()
}

/////////////////////////////////////////////

// Dance-based //

function cancelDance() {
  //? currently kills beat based. This takes maybe up to a second
  //? and a half to work, but has huge advantages...
  //? it allows current frame-animation to run it's course, clean up
  //? and notify. It is also only one flag point, and puts
  //? no extra code in frame-animation (both good).
  //? could also kill callback handlers
  if (engineStatus == ES_DANCING)  {
    engineStatus = ES_CANCELLED
  }
}

//? aside from messages, repetitive
function endStartPositioning() {
  if (engineStatus != ES_CANCELLED) {
    setStatus('hush')
  }
  else {
    // Scatter dancers? kill dancers?
    setStatus('what happened?')
  }
  // done, so start dance
  //!? Why does this work?
  startBeats(dance.moves, endDance)
}


function endDance() {
  setMovesDisplay('')
  if (engineStatus != ES_CANCELLED) {
    setStatus('applause')
  }
  else {
    // Scatter dancers? kill dancers?
    setStatus('bewildered audience')
  }
  // done, so reset
  engineStatus = ES_IDLE
}

function startDance(dance) {
  //validDance
  if (engineStatus != ES_DANCING) {
    engineStatus = ES_DANCING
    
    setTiming(dance.tempo)
    setStatus('clink, rustle')
    updateDancers(dance.dancerCount)
  
    toStartPositions(dance)
   // startBeats(dance.moves, endDance)
  }
}

////////////////////////////////////////////


// Control //

function createDancer() {
  // Doesn't create a position?
  var is = document.createElementNS(NS,"svg");
  //! script forces size, to ensure dancefllor?
  //? use viewport?
  //is.width.baseVal.value="32px";
  is.setAttribute("width", "32px");
  //is.height.baseVal.value="32px";
  is.setAttribute("height", "32px");
  
  //! Don't use filters. They're expensive, complex,
  //! don't add helpful effects, and not yet browser 
  //! agnostic.
  /*
  <radialGradient id="g">
    <stop offset="0" stop-color="white"/>
    <stop offset="1" stop-color="black"/>
  </radialGradient>
  https://dev.w3.org/SVG/modules/vectoreffects/master/SVGVectorEffectsPrimer.html
  */
  // Gradient could be useful for effects, though.
  //? How expensive is it?
  // this puts a yellow dot in the middle
  var rg=document.createElementNS(NS,"radialGradient")
  rg.setAttribute("id", "rg")
  var s1=document.createElementNS(NS,"stop")
  s1.setAttribute("offset", "0")
  // yellow
  s1.setAttribute("stop-color", "#ffdd00")
  rg.appendChild(s1)

  var s2=document.createElementNS(NS,"stop")
  s2.setAttribute("offset", "0.5")
  s2.setAttribute("stop-color", "#ffeeb8")
  rg.appendChild(s2)

  svg.appendChild(rg)

    
  let b=document.createElementNS(NS,"circle")
  b.cx.baseVal.value=16;
  b.cy.baseVal.value=16;
  b.r.baseVal.value=16;
  b.style.fill="#ffeeb8";
  is.appendChild(b);  

  let d=document.createElementNS(NS,"line")
  d.x1.baseVal.value=16
  d.y1.baseVal.value=16
  d.x2.baseVal.value=16
  d.y2.baseVal.value=32
  d.style.stroke="#000000"
  d.style.strokeWidth="2"
  is.appendChild(d)
  
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


//! beter centring of x positions  
function toStartPositions(dance){
  let l = pA.length
  let i = 0 
  let initMoves = []

  switch(dance.start) {
    case 'walkToHLine':
      initMoves.push(['huddleAbsolute', ALL_DANCERS, false, [8, 8, 128, 128]])
      let x = Math.ceil(300 -((l * 70) >> 1))
      while(i < l) {
        initMoves.push(['moveAbsolute', i, false, [x, 128]])
        initMoves.push(['point', i, false, SOUTH])
        x += 70
        i++
      }
      break
    case 'vline':
      //setAsVLine(pA, 64);
      //point(ALL_DANCERS, EAST)
      //mkMove(ALL_DANCERS, point, EAST)
      let y = 128
      while(i < l) {
        initMoves.push(['moveAbsolute', i, false, [128, y]])
        initMoves.push(['point', i, false, EAST])
        y += 70
        i++
      }
      break
    default:
      // default is hline
      //setAsHLine(pA, 64);
      //point(ALL_DANCERS, SOUTH)
      //mkMove(ALL_DANCERS, point, SOUTH)
      let x1 = Math.ceil(300 -((l * 70) >> 1))
      while(i < l) {
        initMoves.push(['moveAbsolute', i, false, [x1, 128]])
        initMoves.push(['point', i, false, SOUTH])
        x1 += 70
        i++
      }
  }
  startBeats(initMoves, endStartPositioning)
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
  'moveAbsolute' : 3,
  'huddleAbsolute': 1,
  'clap' : 2,
  'kick' : 2,
  'jump' : 2,
  'point' : 1,
  'twirl' : 2
})

// params may include direction, weight, etc?
// simulation of helpful marrkup, so may include enums.
// format [action, target, isManyBeat,  optional[params]]
//? are we sticking with this? the only param is direction?
//? include specifics like : moveAnimationType, actionCalls, paramsForCall?
const D_ACTION = 0
const D_TARGET = 1
const D_ISMANYBEAT = 2
const D_PARAMS = 3
  

const dance0 = {
  title: 'Coconutters',
  //tempo: 30,
  tempo: 64,
  dancerCount: 3,
  //start: 'hline',
  start: 'walkToHLine',
  moves: [
  ['point', ALL_DANCERS, false, EAST],
  ['point', ALL_DANCERS, false, WEST],
  ['point', ALL_DANCERS, false, SOUTH],
  ['step', ALL_DANCERS, false, SOUTH],
  ['step', ALL_DANCERS, false, NORTH],
  ['clap', ALL_DANCERS, false, NORTH],
  ['point', ALL_DANCERS, false, WEST],
  ['point', ALL_DANCERS, false, EAST],
  ['point', ALL_DANCERS, false, SOUTH],
  ['step', ALL_DANCERS, false, SOUTH],
  ['step', ALL_DANCERS, false, NORTH],
  ['point', ALL_DANCERS, false, WEST],
  ['kick', ALL_DANCERS, false, WEST],
  ['point', ALL_DANCERS, false, EAST],
  ['kick', ALL_DANCERS, false, EAST],
  ['point', ALL_DANCERS, false, SOUTH]
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
    ['point', 1, false, SOUTH],
    ['twirl', 1, false, null],
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
  ['step', 3, false, SOUTH],
  ['point', 4, false, NORTH],
  ['point', 3, false, SOUTH],
  ['point', 5, false, WEST],
  ['step', 3, false, SOUTH],
  ['point', 4, false, WEST],
  ['point', 5, false, EAST],
  ['point', 3, false, EAST],
  ['point', 2, false, NORTH],
  ['step', 3, false, EAST],
  ['point', 1, false, SOUTH],
  ['step', 3, false, EAST],
  ['point', 1, false, EAST],
  ['point', 3, false, WEST]
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
  //['kick', ALL_DANCERS, false, EAST],
  ['step', ALL_DANCERS, false, EAST]
  ]
}

const dance4 = {
  title: 'War Games',
  tempo: 60,
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
  ['step', 0, false, EAST],
  ['kick', 0, false, NORTH],
  ['step', 0, false, SOUTH],
  ['jump', 0, false, null],  
  ['twirl', 0, false, null],
  ['kick', 0, false, WEST],
  ['point', 0, false, SOUTH],
  ['step', 0, false, EAST],
  ['kick', 0, false, WEST],
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
  let e = document.getElementById("dance-id")
  let o = e.options[e.selectedIndex]
  let danceId = o.value
  let danceName = o.text
  return danceData[danceId]
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
