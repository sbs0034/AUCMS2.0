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
        if(pythonScripts[i].split(".")[0] == "__pycache__"){}
        else {
            scriptSelectHtml.push("<option>" + pythonScripts[i].split(".")[0] + "</option> ")
        }
    }
    // Fills the scriptSelect with all the names of the python scripts
    $('#scriptSelect').html(scriptSelectHtml)
    $('#buildGUI').click(function () {

            var options = {
            mode: 'text',
            pythonPath: 'python',
            args: ['buildGUI']
        };

        PythonShell.run("/python-scripts/"+$('#scriptSelect').val()+'/script.py', options, function (err, results) {
            if (err) throw err;
            // results is an array consisting of messages collected during execution
            console.log(results);
            var scriptGUIFill = []
            for(i=1; i<results.length; i++){
                scriptGUIFill.push(results[i])
            }
            $('#scriptGUI').html(scriptGUIFill)
            $('.addDevice').click(function(){
                console.log(scriptGUIFill)
                $('.tableRow').last().after("<tr class='tableRow'>"+$('.tableRow').html()+"</tr>")
            })
        });
    });
    $('#runScript').click(function(){
        for(i=0; i< document.getElementsByClassName('scriptInput').length; i++){
            console.log(document.getElementsByClassName('scriptInput')[i].value)
            console.log(document.getElementsByClassName('scriptInput')[i].id)
        }
        deviceID=[]
        for(i=0; i < document.getElementsByClassName('deviceID').length; i++){
            deviceID.push(document.getElementsByClassName('deviceID')[i].value)}

        inputLow=[]
        for(i=0; i < document.getElementsByClassName('inputLow').length; i++){
            inputLow.push(document.getElementsByClassName('inputLow')[i].value)}

        inputHigh=[]
        for(i=0; i < document.getElementsByClassName('inputHigh').length; i++){
            inputHigh.push(document.getElementsByClassName('inputHigh')[i].value)}

        currentSteps=[]
        for(i=0; i < document.getElementsByClassName('currentSteps').length; i++){
            currentSteps.push(document.getElementsByClassName('currentSteps')[i].value)}

        currentLimit=[]
        for(i=0; i < document.getElementsByClassName('currentLimit').length; i++){
            currentLimit.push(document.getElementsByClassName('currentLimit')[i].value)}

        voltageLimit=[]
        for(i=0; i < document.getElementsByClassName('voltageLimit').length; i++){
            voltageLimit.push(document.getElementsByClassName('voltageLimit')[i].value)}

        var options = {
            mode: 'text',
            pythonPath: 'python',
            args: ['measureDevice',"deviceID@"+deviceID,"inputHigh@"+inputHigh,"inputLow@"+inputLow,"currentLimit@"+currentLimit,"currentSteps@"+currentSteps,"userName@"+$('#userName').val(),"chipID@"+$('#chipID').val(),"notes@"+$('#notes').val(),"voltageLimit@"+voltageLimit]
        };

        var shell = new PythonShell("/python-scripts/"+$('#scriptSelect').val()+'/script.py', options);
        console.log("Exicuting python script")
        shell.on('message', function (message) {
            console.log(message)
            $('#dataStream').html(message)
        });
    })
});