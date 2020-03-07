"""Platform for JAP Firmware integration."""
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import urllib3
import logging

from homeassistant.helpers.entity import Entity


REQUIREMENTS = ['beautifulsoup4>=4.4.1','urllib3']
_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([JAPFirmwareSensor()])


class JAPFirmwareSensor(Entity):

    def __init__(self):
        self._state = None
        self._updated = datetime.now() - timedelta(days=2)

    @property
    def name(self):
        return 'JAP Firmware'

    @property
    def state(self):
        return self._state

    def update(self):
        if self._updated <= datetime.now() - timedelta(days=1):
            url = "https://support.justaddpower.com/kb/article/257-list-of-firmware-versions-for-2g-3g/"
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            r = requests.get(url + "/kb", verify=False)
            soup = BeautifulSoup(r.content, features="html.parser")

            tables = soup.findAll("table")
            versions = ""

            for table in tables:
                table_rows = table.find_all('tr')
                fw_name = ""
                fw_date = ""
                for tr in table_rows:
                    td = tr.find_all('td')
                    if len(td) >= 1:
                        fw_name = td[0].text.strip()
                        fw_date = td[1].text.strip()
                versions = f"{fw_name}: {fw_date}\n" + versions

            _LOGGER.debug("State: [%s]", versions)

            self._state = versions
            self._updated = datetime.now()
