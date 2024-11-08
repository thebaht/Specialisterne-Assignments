# PDF Downloader: Guide

* When running the program, select the .xlsx file when prompted.
* Afterwards the program will start gathering the download links from the file.

  When "Download: *Getting ready..*" changes to "Download: *In Progress..*", the will start downloading the files.

  You can keep track of the download status of each document by the icon next to their ID.

  * Blue arrow: download still ongoing
  * Green checkmark: download completed
  * Red X: download failed

    Use the filter buttons in the top right, to only display files of a specific status.
* Once "Download: *In Progress..*" changes to "Download: *Complete!*" the program has finished downloading all the files it could.

  The downloaded pdf-files are saved in the directory "pdf-files", which is created in the directory the program was run from.

  An overview of the status of each file can be found in the file "_status.txt" generated in the same directory as the pdf-files.
