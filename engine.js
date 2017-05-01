

//! simutaneous moves
//! storing/restoring pointer data for twirl
//! second twirl in breakdance fails?
//! opacity not resetting
//! do circles?
//! setAttribute is slow?
//! zoom
//! make those ALL_DANCER rotations somewhere near the call, so not 
//! repeating every effect call
//! kick should have direction crossways

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

// args is null
function twirl(dID, args){
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

// args is pair/seq of [x y]
function twirlReturn(dID, args){
  // leaves a 1 px dot in the middle :)
  if (dID != ALL_DANCERS) {
    let e=pA[dID].pointer
    e.setAttribute("x2", args[0])
    e.setAttribute("y2",args[1])
    e=pA[dID].body
    e.setAttribute("fill-opacity", 1)
  }
  else {
    //args are unmarked x1 y1 x2 y2 ...
    let i = pA.length - 1
    let j = 0
    while(i >= 0) {
      let e=pA[i].pointer
      e.setAttribute("x2", args[j])
      j++
      e.setAttribute("y2", args[j])
      j++
      e=pA[i].body
      e.setAttribute("fill-opacity", 1)
      i--;
    }
  }
}


function kick(dID, args){
  if (dID != ALL_DANCERS) {
    let e=pA[dID].body
    e.setAttribute("transform", "translate(16 16) scale(0.5 1) translate(-16 -16)")
  }
  else {
    let i = pA.length - 1
    while(i >= 0) {
      e=pA[i].body
      e.setAttribute("transform", "translate(16 16) scale(0.5 1) translate(-16 -16)")
      i--
    }
  }
}

function kickr(dID, args){
  if (dID != ALL_DANCERS) {
    let e=pA[dID].body
    e.setAttribute("transform", "scale(1 1)")
  }
  else {
    let i = pA.length - 1
    while(i >= 0) {
      e=pA[i].body
      e.setAttribute("transform", "scale(1 1)")
      i--
    }
  }
}

function jump(dID, args){
  if (dID != ALL_DANCERS) {
    //will do, not now
    let e=pA[dID].body
    e.r.baseVal.value=10
  }
  else {
    let i = pA.length - 1
    while(i >= 0) {
      e=pA[i].body
      e.r.baseVal.value=10
      i--
    }
  }
}

function jumpr(dID, args){
  if (dID != ALL_DANCERS) {
    //will do, not now
    let e=pA[dID].body
    e.r.baseVal.value=16
  }
  else {
    let i = pA.length - 1
    while(i >= 0) {
      e=pA[i].body
      e.r.baseVal.value=16
      i--
    }
  }
}

function clap(dID, args){
  if (dID != ALL_DANCERS) {
    //will do, not now
    let e=pA[dID].body 
    e.style.fill="url(#rg)"
  }
  else {
    let i = pA.length - 1
    while(i >= 0) {
      e=pA[i].body
      e.style.fill="url(#rg)"
      i--
    }
  }
}
  
  function clapr(dID, args){
  if (dID != ALL_DANCERS) {
    //will do, not now
    let e=pA[dID].body
    e.style.fill="#ffeeb8"
  }
  else {
    let i = pA.length - 1
    while(i >= 0) {
      e=pA[i].body
      e.style.fill="#ffeeb8"
      i--
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
  'kick': kick,
  'kickr': kickr,
  'clap': clap,
  'clapr': clapr,
  'jump': jump,
  'jumpr': jumpr,
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

const ES_IDLE = 1
const ES_DANCING = 2
const ES_CANCELLED = 3
let engineStatus = ES_IDLE



// Event Loop //
// used for frame animations
//Event loop items
// [call, dancerId, params]
const EL_CALL = 0;
const EL_DANCERID = 1;
const EL_PARAMS = 2;

let frameAnimationCalls = []
let frameCountdown = 0

let beatEndCalls = []

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

    
    //send notify
    notifyBeatFinshed.call()
  }
}


// needs defending against multicalls
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
  
//? now these are fixed, but if we introduce distance a dancer moves,
//? they will vary.
function moveOffsets(m) {
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


// 'all' args returned as undifferentiated seq
function pointerData(m) {
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

function posDataAsParams(m) {
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
/*
// make a easily callable data for animation
function pushFrameCall(m) {
  let action = m[D_ACTION]
  let call = actionCalls[action]
  let id = m[D_TARGET]
  // currently only handling 'step' here, so
  // calculate offsets
  // switch (action) {
  //case 'step'
  let params = moveOffsets(m[D_PARAMS])
  frameAnimationCalls.push([call, id, params])
}

// make a easily callable data for animation
function pushBeatEndCall(m) {
  let action = m[D_ACTION]
  let call = actionCalls[action + 'r']
  let id = m[D_TARGET]
  // currently only handling 'twirl' here, so
  // calculate offsets
  // switch (action) {
  //case 'twirl'
  let params = pointerData(m)
  beatEndCalls.push([call, id, params])
}

function pushBeatStartCall(m) {
  let action = m[D_ACTION]
  let call = actionCalls[action]
  let id = m[D_TARGET]
  // currently only handling 'twirl' here, so
  // calculate offsets
  // switch (action) {
  //case 'twirlr'
  let params = pointerData(m)
  beatStartCalls.push([call, id, params])
}
*/

function paramsForCall(m, action) {
  switch(action) {
  case 'step': return moveOffsets(m)
  case 'twirlr': return pointerData(m)
  case 'point': return m[D_PARAMS]
  case 'twirl':
  case 'clap' :
  case 'clapr' : 
  case 'kick': 
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
      //pushFrameCall(m)
      frameAnimationCalls.push([call, id, params])
      break
    case AT_ISANIMATED:
      beatStartCalls.push([call, id, params])

      //pushBeatStartCall(m)

      break
    case AT_RETURNANIMATED:
      //pushBeatStartCall(m)
      //pushBeatEndCall(m)
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
      c[EL_CALL](c[EL_DANCERID], c[EL_PARAMS])
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
      c[EL_CALL](c[EL_DANCERID], c[EL_PARAMS])
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

    //? TMP show moves
    //? D_ISMANYBEAT
    setMovesDisplay( m[D_ACTION])
    
    doBeatStartCalls()
    //? junk code if no animations?
    startAnimations()
    beatI++
  }
  else notifyDanceEnded.call()
}



function startBeats(moves) {
    beatI = 0
    beatMoves = moves
    //?
    beatStartCalls = []
    beatEndCalls = []
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
    
    setStatus('hush')
  
    updateDancers(dance.dancerCount)
  
    toStartPositions(dance.start)
    
    startBeats(dance.moves)
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
  
  //! Din't use filters. They're expensive, complex,
  //! don't add helpful effects, and not yet browser agnostic.
  /*
  	<defs>
		<filter id="blur" x="0" y="0">
			<feGaussianBlur in="SourceGraphic" stdDeviation="5" />
		</filter>
	</defs>
  * filter="url(#blur)"
  */

/*
 * in =
    SourceGraphic
    SourceAlpha
    BackgroundImage
    BackgroundAlpha
    FillPaint
    StrokePaint
 */ 
  // Only works on the first following element?
  // Thanks for telling me...
  //var df=document.createElementNS(NS,"defs")
  //var f=document.createElementNS(NS,"filter")
  //f.setAttribute("id", "blur")
  //f.setAttribute("x", 2)
  //f.setAttribute("y", 2)
  //f.setAttribute("width", 28)
  //f.setAttribute("height", 28)
  
  //df.appendChild(f)
  //var gb=document.createElementNS(NS,"feGaussianBlur")
  //gb.setAttribute("in", "StrokePaint")
  //gb.setAttribute("stdDeviation", "1")
  //f.appendChild(gb)
  //is.appendChild(df)

/*
<radialGradient id="g">
  <stop offset="0" stop-color="white"/>
  <stop offset="1" stop-color="black"/>
</radialGradient>
https://dev.w3.org/SVG/modules/vectoreffects/master/SVGVectorEffectsPrimer.html
*/
  // Gradient could be useful for effects, though.
  //? How expensive is it?
  var rg=document.createElementNS(NS,"radialGradient")
  rg.setAttribute("id", "rg")
  var s1=document.createElementNS(NS,"stop")
  s1.setAttribute("offset", "0")
  s1.setAttribute("stop-color", "#ffdd00")
  rg.appendChild(s1)

  var s2=document.createElementNS(NS,"stop")
  s2.setAttribute("offset", "1")
  s2.setAttribute("stop-color", "#ffeeb8")
  rg.appendChild(s2)

  svg.appendChild(rg)

    
  let b=document.createElementNS(NS,"circle");
  //b.setAttribute("filter", "url(#blur)")


  //transform='translate(140 105) scale(2 1.5) translate(-140 -105)
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

function toStartPositions(desc){
  switch(desc) {
    case 'vline':
      setAsVLine(pA, 64);
      point(ALL_DANCERS, EAST)
    break;
    default:
      // default is hline
      setAsHLine(pA, 64);
      point(ALL_DANCERS, SOUTH)
  }
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
  ['step', ALL_DANCERS, false, NORTH],
  ['point', ALL_DANCERS, false, WEST],
  ['kick', ALL_DANCERS, false, NORTH],
  ['point', ALL_DANCERS, false, EAST],
  ['kick', ALL_DANCERS, false, NORTH],
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
    ['kick', ALL_DANCERS, false, EAST],

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
  ['step', 0, false, EAST],
  ['kick', 0, false, null],
  ['step', 0, false, SOUTH],
  ['jump', 0, false, null],  
  ['twirl', 0, false, null],
  ['point', 0, false, SOUTH],
  ['step', 0, false, EAST],
  ['kick', 0, false, null],
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
