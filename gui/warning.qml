import QtQuick 2.3
import QtQuick.Dialogs 1.1
MessageDialog
{
	id : messageDialog
	title : "warning!"
	text : "file format incorrect!"
	icon : StandardIcon.Critical
	//standardButtons : StandardButtons.Yes
	Component.onCompleted : visible=true
	onYes : console.log("yes")
}