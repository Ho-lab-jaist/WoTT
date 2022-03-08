
# WoTT

Open and Standardized interfaces for Tactile Things via W3C Web of Things

  

## For Developers

Developers must check the <a  href="docs/workflows.md">Workflow</a> before working in this repository!

## About The WoTT Haptic Interface

 - This project implements:

   1. A module, namely *WoTTServer*, to expose a *tactile device* as a W3C *Thing* so that W3C Web of Things clients can interact with the *tactile device* via WoT APIs
   2. A WoT client that consumes the exposed thing to communicate with *haptic jacket* (vibration modules) via WoT APIs and HapTic APIs
   
## Built With
- WoTTServer
  - python
  - wotpy
  - pytorch
  - torchvision
  - opencv
- WoT Client
	- python
	- WoTpy
	- hapticAPI
## Getting Started
Please make sure to add the domain name of the server machine to your local computer (Linux):
```
$ sudo nano /etc/hosts
```
Then add:
```
$ 150.65.152.91  	ho-lab
```
[150.65.152.91] is the ip address of JAIST WoTT server.
Then run:
```
$ python codes/WoTTClientHapticJacketInterface.py
```
This program have been tested to interface with the GUI Visualization of the Haptic JacKet. Please modify according to your needs.

The hapticAPI module is invoked every time the Deformed Event of tactile device is detected. This event is captured and processed for communication with vibration modules using ```utils/SensingCells``` class

## Contributing


Any contributions you make are **greatly appreciated**.
1. Fork the Project

2. Create your Feature Branch (`git checkout -b feature/aFeature`)

3. Commit your Changes (`git commit -m 'commit string'`)

4. Push to the Branch (`git push origin feature/aFeature`)

5. Open a Pull Request
## License
Distributed under the MIT License. See `LICENSE` for more information.
## Contact
- Project Manager
	- Ho Anh Van - [van-ho@jaist.ac.jp](mailto:van-ho@jaist.ac.jp)
- Advisors
	- Tan Yasuo -  [ytan@jaist.ac.jp](mailto:ytan@jaist.ac.jp)
	- Pham Van Cu - [cupham@jaist.ac.jp](mailto:cupham@jaist.ac.jp)
- Developers
	- Luu Khanh Quan - [quan-luu@jaist.ac.jp](mailto:quan-luu@jaist.ac.jp)
	- Nguyen Tai Tuan - [tuan-nguyen@jaist.ac.jp](mailto:tuan-nguyen@jaist.ac.jp)
## Acknowledgements
This work was supported in part by JSPS KAKENHI under Grant 18H01406 and JST Precursory Research for Embryonic Science and Technology PRESTO under Grant JPMJPR2038.
