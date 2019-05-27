var outputField = document.getElementById("timestamps")
function logKeyEvent(){
    var now = new Date()
    entry = {"sourceid": event.srcElement.attributes.id.nodeValue, "type": event.type, "time": now.getTime(),
             "key": event.key, "fieldvalue": event.srcElement.value};
    outputField.value += JSON.stringify(entry) + "\n";
    outputField.scrollTop = outputField.scrollHeight;
}

$('input').keydown(logKeyEvent);
$('input').keyup(logKeyEvent);