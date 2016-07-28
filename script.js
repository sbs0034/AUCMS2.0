/**
 * Created by steffen on 6/27/16.
 * Script for building a user interface for the AUCMS Python modules
 */
var PythonShell = require('python-shell');
var fs = require('file-system');
var pythonScripts;
var scriptIgnore = ["database","measurement_script","terminal_ui","__pycache__"];

// Build GUI for selected module
function BuildScriptGUI() {
  stuff = {}
  stuff['action']='buildGUI'

    var options = {
    mode: 'text',
    pythonPath: 'python',
    args: [JSON.stringify(stuff)]
    };
    var scriptGUIFill = []
    PythonShell.run("/python-scripts/"+$('#scriptSelect').val()+'/script.py', options, function (err, results) {
        if (err) throw err;
        // results is an array consisting of messages collected during execution
        console.log(results);
        for(i=1; i<results.length; i++){
            scriptGUIFill.push(results[i])
        }
        $('#scriptGUI').html(scriptGUIFill)
        $('#scriptGUI').show(800)
        $('body').append('<button class="btn btn-raised btn-success" onclick="RunScript()">Run Script</button>')
        $.material.init()
    });
}

// Build Initial Gui for launching scripts.
function BuildInitialGui(){
  // File input button
  $('body').append('<label for="scriptSelect">Choose Module</label> <select id="scriptSelect" class="form-control scriptInput"></select>')
  $('body').append('<button id="buildGUI" class="btn btn-raised btn-primary" onclick="BuildScriptGUI()">Build GUI</button>')
  $('body').append('<div id="scriptGUI" style="display: none"></div>')
  $('body').append('<div id="dataStream" style="padding-top: 20px; padding-bottom: 20px;"></div>')
}

// Searches through the 'python-scripts' folder for usable scripts
function ScriptSelectorFill(){
  pythonScripts = fs.readdirSync("./python-scripts");
  var scriptSelectHtml = []
  for(i=0; i<pythonScripts.length; i++){
      if(pythonScripts[i].split(".")[0] == "__pycache__"){}
      else {
          scriptSelectHtml.push("<option>" + pythonScripts[i].split(".")[0] + "</option> ")
      }
    }
      $('#scriptSelect').append(scriptSelectHtml)
  }

// Run selected script and gather all script inputs
function RunScript(){
  pythonArguments = {}
    for(i=0; i< document.getElementsByClassName('scriptInput').length; i++){
      pythonArguments[document.getElementsByClassName('scriptInput')[i].id]=[]
    }
    for(i=0; i< document.getElementsByClassName('scriptInput').length; i++){
      pythonArguments[document.getElementsByClassName('scriptInput')[i].id].push(document.getElementsByClassName('scriptInput')[i].value)
    }
    pythonArguments["action"]="measureDevice"
    console.log(pythonArguments)
    var options = {
        mode: 'text',
        pythonPath: 'python',
        args: [JSON.stringify(pythonArguments)]
    };
    console.log(options["args"][0])
    var shell = new PythonShell("/python-scripts/"+$('#scriptSelect').val()+'/script.py', options);
    console.log("Exicuting python script")
    var layout = {
      width: 700,
      height: 600,
        xaxis: {
            showgrid: true,
            showline: true,
            mirror: 'ticks',
            gridcolor: '#bdbdbd',
            linecolor: '#636363',
            linewidth: 2,
            autotick: true,
            ticks: 'inside',
            tick0: 0,
            ticklen: 8,
            tickwidth: 4,
            tickcolor: '#000'
        },
        yaxis: {
            showgrid: true,
            showline: true,
            mirror: 'ticks',
            gridcolor: '#bdbdbd',
            linecolor: '#636363',
            linewidth: 2,
            autotick: true,
            ticks: 'inside',
            tick0: 0,
            ticklen: 8,
            tickwidth: 4,
            tickcolor: '#000'
        },
        font: {
      family:"Droid Serif, serif",
      size: 18,
        },
        showlegend:true,
        title:"Data Stream Graph"
    }
    x_data = []
    y_data = []
    counter=0
    shell.on('message', function (message) {
      counter++
      if($('#dataGraph').length == 0){
        $('#dataStream').html(message.split(",")[0])
      }
      else{
        x_data.push(message.split(",")[0])
        y_data.push(message.split(",")[1])
        dataToGraph = []
        if($('#dataGraph').html()==""){
          dataToGraph.push({
              x: x_data,
              y: y_data,
              mode: 'lines+markers',
              type: 'scatter',
          });
          Plotly.newPlot('dataGraph', dataToGraph, layout);
        }
        if(counter < 15){}
        else{
          dataToGraph.x=x_data
          dataToGraph.y=y_data
          Plotly.redraw("dataGraph")
          counter=0

        }

      }
    });
}

// Waits untill the page is fully loaded
$(document).ready(function(){
    BuildInitialGui()
    ScriptSelectorFill()
    $.material.init()
});
