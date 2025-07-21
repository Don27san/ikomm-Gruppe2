import QtQuick
import QtQuick.Controls

RowLayout { spacing: 8
    Rectangle { width: 60; height: 36; color: "#eeeeee"; radius: 16
        AnimatedImage { source: "images/typing_indicator.gif"; anchors.centerIn: parent; width: 50 }
    }
}