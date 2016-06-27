/**
 * Created by steffen on 6/27/16.
 */
var PythonShell = require('python-shell');
var fs = require('file-system');
var pythonScripts;
var scriptIgnore = ["database","measurement_script","terminal_ui","__pycache__"];
$(document).ready(function(){
    // Searches through the 'python-scripts' folder for usable scripts
    pythonScripts = fs.readdirSync("./python-scripts");
    var scriptSelectHtml = []
    for(i=0; i<pythonScripts.length; i++){
        if(scriptIgnore.indexOf(pythonScripts[i].split(".")[0]) > -1){}
        else {
            scriptSelectHtml.push("<option>" + pythonScripts[i].split(".")[0] + "</option> ")
        }
    }
    // Fills the scriptSelect with all the names of the python scripts
    $('#scriptSelect').html(scriptSelectHtml)
    $('#startScript').click(function () {
    //     var pyshell = new PythonShell("/python-scripts/"+$('#scriptSelect').val()+'.py',{ mode: 'text '});
    //     pyshell.send('buildInstructions');
    //     pyshell.on('message', function (message) {
    //         // received a message sent from the Python script (a simple "print" statement)
    //         console.log(message);
    //     });


        var options = {
            mode: 'text',
            pythonPath: 'python3',
            args: ['value1']
        };

        PythonShell.run("/python-scripts/"+$('#scriptSelect').val()+'.py', options, function (err, results) {
            if (err) throw err;
            // results is an array consisting of messages collected during execution 
            console.log('results: %j', results);
        });
    });

});