# Renin Kingsly Jose
# Hotplugging test using Avocado lib

import os
import time

from avocado import Test
from avocado.utils.process import run
from avocado.utils.ssh import Session

URI = "qemu:///system"          # Identifier
DOMAIN = "fedora"
HOST = "192.168.122.229"        # IP
USERNAME = "renin_l2"           
PASSWORD = "redhattest123"

DISK_PATH = f"/run/media/{USERNAME}/USB\ DISK"

class Libvirt(Test):

    def setUp(self):

        self.new_disk_path = os.path.join(self.workdir, "new_disk.raw")
        run(f"qemu-img create -f raw {self.new_disk_path} 1G")

        run(f"virsh -c {URI} start {DOMAIN}")                       # Boot up L2
        time.sleep(30)                                              # Needs 30s to boot up completely 

        self.session = Session(HOST, user=USERNAME, password=PASSWORD)

        if not self.session.connect():
            self.fail("Could not establish SSH connection")         

    def test(self):
        
        while(True):
            diskTarget = self.session.cmd(f"cd {DISK_PATH}", ignore_status=True)
            if diskTarget.exit_status == 0:
                # Disk detected
                self.log.debug("Disk detected")
                break
        
        pass

    def tearDown(self):
        
        self.session.quit()                                         # End ssh connection to L2

        run(f"virsh -c {URI} shutdown {DOMAIN}")                    # Shutdown L2

        pass