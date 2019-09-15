var agregatedData = [];
function logKeyEvent(){
    var now = new Date()
    entry = {"sourceid": event.srcElement.attributes.id.nodeValue, "type": event.type, "time": now.getTime(),
             "key": event.key};
    agregatedData.push(entry)
}

$('input').keydown(logKeyEvent);
$('input').keyup(logKeyEvent);

$( "#login" ).submit(function( event ) {
  url = '/save'
  data = { 'strikes': JSON.stringify(agregatedData)}
  $.post(url, data, function(data, status){
    console.log(`response status:  ${status}`)
    $("#login")[0].reset()
    resetAgregator()
  })
  event.preventDefault();
});

function resetAgregator(){
    agregatedData = [];
}