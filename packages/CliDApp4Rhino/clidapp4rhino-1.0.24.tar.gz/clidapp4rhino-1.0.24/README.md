# CliDApp4Rhino

## Overview

CliDApp4Rhino package is a Python package with the plugin for the [Rhinoceros](https://www.rhino3d.com/) program developed by [CliMA](https://clima.caltech.edu/) that enables users to download weather files into the Rhinoceros environment from the CliDApp API.

### Requirements

Before installing the CliDApp4Rhino plugin, ensure that you have the following:

- Rhinoceros 5 and above
- Python 3 or later installed on your device
- Internet connection: to download weather files

### Installation

To install the CliDApp4Rhino plugin, follow the steps below:

1. Close Rhinoceros (Rhino) if opened
2. Navigate to the terminal and enter the following to install the package

```shell
pip install CliDApp4Rhino
```

3. After running the following command to install the package to the correct directory.

```shell
clidapp4rhino
```

4. Open Rhino and enter the following in the command-line

```shell
CliDApp4Rhino
```

If Rhino suggests this command, then you have successfully installed the plugin.

### Usage

After installing the plugin and launching the CliDApp4Rhino command, you will now see the dialog box below:

<div align="center">
<img src="https://clidapp.s3.amazonaws.com/static/server/img/dialog.png" alt="CliDApp4Rhino Dialog Box" width="35%" height="35%">
</div>

Begin by selecting a city from the dropdown

<div align="center">
<img src="https://clidapp.s3.amazonaws.com/static/server/img/city_selection.png" alt="CliDApp4Rhino City Selection" width="35%" height="35%">
</div>

Then select a weather file from the following three options:

- Typical Meteorological Year (TMY)
- Future Meteorological Year (FTMY)
- Actual Meteorological Year (AMY)

Next, select a data type. Currently, only observational data is available.

The start/end-year ranges will differ depending on the weather file selected. Currently, for AMY and TMY files, the start-year and end-year range starts from 1979 and ends in 2022. For FTMY files, the baseline years run from 1979 to 2023, and they are projected to 2050 to 2070.

Afterwards, select your desired file type. Then, enter the path where you want to download the file. If the text box for Download Path is left empty, the default path will be Downloads/clidapp/epw. Lastly, click on **OK** to begin downloading the weather file.

### Example

Here we use the CliDApp4Rhino plugin to download an EPW weather file. Then, we use the ImportEPW and WindRose Ladybug module to visualise the data as a wind rose chart.

As shown in the form inputs below, the following file was downloaded.

<div align="center">
    <img src="https://clidapp.s3.amazonaws.com/static/server/img/form_inputs.png" alt="CliDApp4Rhino Form Input" width="35%" height="35%" style="display: inline-block; margin-right: 10px;">
    <img src="https://clidapp.s3.amazonaws.com/static/server/img/file.png" alt="CliDApp4Rhino File" width="35%" height="35%" style="display: inline-block;">
</div>

We get the following chart using a Panel, the ImportEPW Ladybug module, and the WindRose Ladybug module.

<div align="center">
<img src="https://clidapp.s3.amazonaws.com/static/server/img/ladybug_inputs.png" alt="CliDApp4Rhino Ladybug Input" width="35%" height="35%">
</div>
<br>
<div align="center">
<img src="https://clidapp.s3.amazonaws.com/static/server/img/wind_rose.png" alt="CliDApp4Rhino Wind Rose" width="35%" height="35%">
</div>
