### Scrapping xing.com
  For run `xing.py` you must build docker image and run container (assumed that docker  is already installed).
  Go to directory with Docerfile and execute following commands for this (take in mind that for linux users may be required `sudo`):
  ```
  docker build -t <image name> .
  docker run <image name>
 ```
  Add flad `-d` if you want start container in daemon mode.
  If you want check your all existing containers execute:
  ``` 
  docker ps -a
  ```
  existing images:
  ``` 
  docker images
  ```
  For coping logfile and result files from conteiners to host execute:
  ```
  docker cp <container id>:/code/.xing.log <path where you want to save>
  docker cp <container id>:/code/xing_com_result.csv <path where you want to save>
  ```
  
