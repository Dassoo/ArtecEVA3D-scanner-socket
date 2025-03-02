# Artec EVA 3D Scanner SDK remote scanning

This readme provides a comprehensive setup for establishing a socket connection between your system and the Artec EVA 3D Scanner, enabling remote control and seamless scanning operations. By utilizing the C++ Artec SDK alongside Python, you'll be able to effortlessly interface with the scanner, automate tasks, and streamline your 3D scanning workflow.

Whether the task is to integrate the scanner into a larger application or simply control it remotely for enhanced convenience, this setup will walk you through the necessary steps to get up and running quickly. 

> <b>Note</b>: In addition to the computer that will be used as the main body for the scanning and postprocessing activities, another computer is needed in order to handle scanning control (in our case, also through robotic arms movements and commands). From now on, we will refer to the the computer on which the scanner is directly connected as "server", and to the other pc as "client".

## Setup

Install on both client and server the basic requirements in an environment (actually on the server side you would only need everything inside the `socket_server` folder and the execution links (`server.bat/server_linux.sh` in the main folder), just make sure that the required libraries are installed:

```bash
  cd scanner_socket
  
  conda create --name eva_remote -y python=3.11
  conda activate eva_remote
  
  python -m pip install --upgrade pip
  pip install -r requirements.txt
```

> <b>IMPORTANT</b>: Server and client have to be connected to the same network. Additionally, make sure that neither Artec Studio is open nor that other existing connections may cause trouble (ex. Ethernet + Wi-Fi) before starting the scans. 

### Server
To open the socket connection on the server just run the platform-corresponding executable: 
- On Windows: run `server.bat`;
- On Linux: `./server_linux.sh`.

By leaving the current CMD/Terminal window open, the server will be listening to any command coming from any connecting client.


### Client

Changing the settings in `settings.toml` is needed in order to establish the connection with the server. It is very important to update with the right configuration and paths.

```
[server]
ip = "insert server ip here"                        # Server IP
port = 3000                                         # Server port (default)

[paths]
base = "C:/Users/iit_c/Desktop/scanner_socket"      # Path to the "scanner_socket" folder on server pc
folder = "test_5_11"                                # Project/folder name

[data]
auth_token = "token_serial"                         # Authentication Token for the upload to the postproduction platform (not publicly available)
```

The `ext_scanner.py` file groups up the fundamental activity parts of the scanner into functions, which could easily be implemented into any additional script.


## Scanning

The default methods will start acquiring the frames until the entire process is finished (producing `.png`, `.mtl` and `.obj` results for every single scan/frame), zipping the results and sending them into the client, finally unzipping them locally. 
In this script, the scans were also originally uploaded into a dedicated cloud repository using an authentication token, on which they will be automatically used for the postprocessing and 3D reconstruction.

> <b>Note</b>: It may happen that the scanner will be not able to capture a frame and that it won't get registered due to not having enough distance from the scanning area, for which is required a minimum of 60cm. In the default code the scanner will attempt to scan up to 5 times before eventually failing the single acquisition.

You can find locally the scanning results in the subfolder you chose in the settings inside the `projects` folder. The same folders tree will also be replicated on the server side.


## SDK Reference

The C++ code which use the Artec SDK has been already compiled, and it is included in the `socket_server/app/cpp` folder.
The main file is `scanprocess.cpp` which, if edited, needs to be re-compiled with the prompt command written in `compile.txt`. The resulting `scanExec.exe` executable will be automatically used as the new reference.

To do so, you may need to set up your C++ compiler: https://code.visualstudio.com/docs/cpp/config-mingw

More info about Artec SDK here: https://docs.artec-group.com/sdk/2.0/index.html
