import lEventWriterFile, lEventWriterConsole, lTimer, lStatistics

EventsToFile = {
'dancer' : [],
'dancerGroup' : [],
'score' : [],
'global' : [lEventWriterFile]
  }
  
EventsToConsole = {
'dancer' : [],
'dancerGroup' : [],
'score' : [],
'global' : [lEventWriterConsole]
  }


GlobalStatistics = {
'dancer' : [lTimer],
'dancerGroup' : [],
'score' : [],
'global' : []
#lStatistics
}


LocalStatistics = {
'dancer' : [lTimer],
'dancerGroup' : [],
'score' : [],
'global' : []
}
