import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Window 2.1
ApplicationWindow{
	width : 600
	height : 400
	function createDialog()
	{
		var component = Qt.createComponent("warning.qml")
		if(component.status == Component.Ready)
		{
			var dialog = component.createObject(root,{"x":100,'y':100})
			if(dialog == null)
			{
				console.log("create object error")
			}
			else if(component.status == Component.Error)
			{
				console.log("component error")
			}
			else
			{
				console.log('component not ready');
			}
		}
		
	}
Rectangle
{
	id : root
	color : 'beige'
	anchors.fill: parent
	Image
	{
		id : img
		width : root.width
		height : root.height-200
		anchors.centerIn: parent
		DropArea
		{
			id : fileDocker
			anchors.fill: parent
			onDropped : {
				console.log(drop.urls)
				var filename = drop.urls[0]
				var cols = filename.split('.')
				console.log(cols[0])
				img.source = filename
			}

		}
	}
    Component.onCompleted: visible = true
}
}
