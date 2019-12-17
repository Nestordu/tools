/*

@@@BUILDINFO@@@ Export Layer.jsx 1.0.0.0

*/
//#target photoshop
var doc_path = app.activeDocument.path;
var doc = app.activeDocument.duplicate("temp",false);

//savePngFowWeb('testt');

// alert(doc.layerSets.length);
// alert(doc.artLayers.length);
// var newLayer = activeDocument.artLayers.getByName('My Layer'); // Create a new ArtLayer object newLayer.name = "My Layer";
// newLayer.visible = true;

(function main(){
    var data = [];
    for (var i = 0; i < doc.layerSets.length; i++) {
        var set = doc.layerSets[i];
        if(set.visible == true)
            data.push(set);
    }

    for (var i = 0; i < data.length; i++) {
        var set = data[i];
        set.visible = true;
        for (var j = 0; j < doc.layerSets.length; j++) {
            var set1 = doc.layerSets[j];
            if(set != set1){
                set1.visible = false;
            }
        }
        dealLayerSet(set);
    }

    //doc.close();
})();

function dealLayerSet(set){
    var layers = [];
    for (var i = 0; i < set.artLayers.length; i++) {
        var layer = set.artLayers[i];
        if(layer.visible == true)
            layers.push(layer);
    }
    
    for (var i = 0; i < layers.length; i++) {
        var layer = layers[i];
        layer.visible = true;
        for (var j = 0; j < set.artLayers.length; j++) {
            var layer1 = set.artLayers[j];
            if(layer != layer1){
                layer1.visible = false;
            }
        }
        savePngFowWeb(layer.name);
    }
}

function savePngFowWeb(name){
   // alert(doc_path + '/output/' + name + '.png');
    var file = new File(doc_path + '/output/' + name + '.png');

    var opts = new ExportOptionsSaveForWeb();
    opts.format = SaveDocumentType.PNG;
    opts.PNG8 = false;
    opts.quality = 10;

    doc.exportDocument(file, ExportType.SAVEFORWEB, opts);
}