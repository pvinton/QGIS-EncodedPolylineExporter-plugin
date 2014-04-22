# Encoded Polyline - Plugin for QGIS
<br>
Encoded polylines are boundary definitions in a space-saving and efficient format.
<br>
They are used in many applications, from GIS tools to BI applications and more.
<br>
The **Encoded Polyline** plugin for QGIS allows you to export encoded polylines in a friendly CSV format for use in your applications.

___

## Installation

### Automatic
1. Install QGIS from [QGIS.org](http://www.qgis.org)
<br>
![Downloading QGIS](readme/img/1.png)
2. Load QGIS and go to Plugins -> Manage and Install Plugins
<br>
![Loading the Plugins window](readme/img/3.png)
3. Under the All tab, search for "encoded polyline" and click **Encoded Polyline Exporter** (your interface may differ slightly)
<br>
![Loading the Plugins window](readme/img/4b.png)
4. Click the *Install plugin* button and wait for installation to complete (an icon should appear on your top toolbar)
5. You're good to use the plugin!

### Manual
1. Install QGIS from [QGIS.org](http://www.qgis.org)
<br>
![Downloading QGIS](readme/img/1.png)
2. Download the Encoded Polyline source files from [Github](http://www.github.com/) (click the Download ZIP button in the lower right)
3. Extract the downloaded ZIP file
4. Cut or Copy the **encodedPolyline** folder from inside the **dist** folder
5. Paste or Move the **encodedPolyline** folder into your Plugin folder:
    + Windows - `%USERPROFILE%\.qgis2\python\plugins`
    + OSX/Unix - `~/.qgis2/python/plugins`
<br> ![After moving into Plugins folder](readme/img/2.png)
6. Load QGIS and go to Plugins -> Manage and Install Plugins
<br>
![Loading the Plugins window](readme/img/3.png)
7. Under the Installed tab, check the box next to the **Encoded Polyline Exporter** plugin (an icon should appear on your top toolbar)
<br>
![Checking the Encoded Polyline box](readme/img/4.png)
8. You're good to use the plugin!

___

## Usage

1. Load up a SHP or any file with boundary demarcations
2. Click the **Encoded Polyline** icon on your top toolbar
<br>
![After clicking the Encoded Polyline icon](readme/img/5.png)
3. Choose a Destination and column Prefix, then click OK
4. Open the created CSV in your spreadsheet application
<br>
![Your data with the encoded polylines in a single column](readme/img/6.png)
5. Use your data wherever you need it!

___

## Information about Encoded Polylines

+ [Google Developers Explanation](https://developers.google.com/maps/documentation/utilities/polylinealgorithm)
+ [Less Technical Explanation](http://www.danmandle.com/blog/what-is-an-encoded-polyline/)

___

## Created By
+ [Patrick Vinton](http://www.github.com/pvinton) at [Analytics8](http://www.analytics8.com)

## Maintained By
+ [Takeshi Takahashi](http://www.github.com/therealtakeshi) at [Analytics8](http://www.analytics8.com)