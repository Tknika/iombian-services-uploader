# IoMBian Services Uploader

This service scans the IoMBian services announced through Avahi (mDNS) and uploads them to the IoMBian Configurator platform.


## Installation

- Clone the repo into a temp folder:

> ```git clone https://github.com/Tknika/iombian-services-uploader.git /tmp/iombian-services-uploader && cd /tmp/iombian-services-uploader```

- Create the installation folder and move the appropiate files (edit the user):

> ```sudo mkdir /opt/iombian-services-uploader```

> ```sudo cp requirements.txt /opt/iombian-services-uploader```

> ```sudo cp -r src/* /opt/iombian-services-uploader```

> ```sudo cp systemd/iombian-services-uploader.service /etc/systemd/system/```

> ```sudo chown -R iompi:iompi /opt/iombian-services-uploader```

- Create the virtual environment and install the dependencies:

> ```cd /opt/iombian-services-uploader```

> ```python3 -m venv venv```

> ```source venv/bin/activate```

> ```pip install --upgrade pip```

> ```pip install -r requirements.txt```

- Start the script

> ```sudo systemctl enable iombian-services-uploader.service && sudo systemctl start iombian-services-uploader.service```


## Author

(c) 2022 [Aitor Iturrioz Rodríguez](https://github.com/bodiroga)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.