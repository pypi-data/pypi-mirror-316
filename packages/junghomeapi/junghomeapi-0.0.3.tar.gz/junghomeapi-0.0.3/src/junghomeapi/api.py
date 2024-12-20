"""Python library for Junghome Openapi."""

from __future__ import annotations

import aiohttp

def mapSubscriptionDatapoints(datapoint) -> dict:
    """Map datapoints to fit createSubscriptions."""
    try:
        ret_val = {"id": datapoint["id"], "type": "datapoint"}
    except KeyError:
        return {}
    return ret_val

class JunghomeApi:
    """JunghomeApi class."""

    _junghome_url: str
    _token: str

    _api_version: str
    _api_base: str

    _session = None

    def __init__(self, junghome_url: str, token: str) -> None:
        """Init JunghomeApi class."""
        self._junghome_url = junghome_url
        self._token = token

    async def __aenter__(self):
        """Aenter JunghomeApi class."""
        if not self._session:
            self._session = aiohttp.ClientSession()
        try:
            #Check api version and path.
            async with self._session.get(
                self._junghome_url + "/.well-known/knx", data={}, headers={}
            ) as resp:
                status = resp.status
                if status != 200:
                    raise Exception("Error getting api.")
                response = await resp.json()
                try:
                    self._api_version = response["api"]["version"]
                    self._api_base = response["api"]["base"]
                except KeyError:
                    raise Exception("Unexpected return value on init.")
            #Get Location on init, to check if the token ist valid. /.well-known/knx ist working without authoration
            url = self._junghomeApiUrl() + "/locations"
            async with self._session.get(
                url,
                data={},
                headers=self._headers(),
            ) as resp:
                status = resp.status
                if status == 401:            
                    raise Exception("Wrong token.")
                if status != 200:
                    raise Exception("Error getting locations.")
                response = await resp.json()
                self.getLocations = list(response.get("data", [])) 
        except Exception as ex:
            await self.__aexit__()
            raise ex
        return self

    async def __aexit__(self, *args):
        """Aexit JunghomeApi class."""
        await self._session.close()

    def _junghomeApiUrl(self) -> str:
        """Return the current Api Url."""
        return self._junghome_url + "/" + self._api_base

    def _headers(self):
        """Build the header for requests"""
        return {
            "Authorization": "Bearer " + self._token,
            "Content-Type": "application/vnd.api+json",
        }

    def getApiBase(self) -> str:
        """Return the current api base."""
        return self._api_base
    
    def getApiVersion(self) -> str:
        """Return the current api version."""
        return self._api_version

    def getLocations(self) -> str:
        """Return locations."""
        return self._locations
    
    async def getFunctions(self) -> list[dict]:
        """Get all functions fom Junghome."""
        async with self._session.get(
            self._junghomeApiUrl() + "/functions", data={}, headers=self._headers()
        ) as resp:
            status = resp.status
            if status != 200:
                return {}
            response = await resp.json()
            return list(response.get("data", []))
            #return list(map(mapAttributes, response.get("data", [])))

    async def getFunctionDatapoints(self, function_id) -> list[dict]:
        """Get all datapoints to given functions fom Junghome."""
        async with self._session.get(
            self._junghomeApiUrl() + "/functions/" + function_id + "/datapoints",
            data={},
            headers=self._headers(),
        ) as resp:
            response = await resp.json()
            return list(response.get("data", []))
            #return list(map(mapAttributes, response.get("data", [])))

    async def getDevices(self) -> list[dict]:
        """Get all devcices fom Junghome."""
        async with self._session.get(
            self._junghomeApiUrl() + "/devices", data={}, headers=self._headers()
        ) as resp:
            status = resp.status
            if status != 200:
                return {}
            response = await resp.json()
            return list(response.get("data", []))

    async def getDeviceDatapoints(self, function_id) -> list[dict]:
        """Get all datapoints to given devcice fom Junghome."""
        async with self._session.get(
            self._junghomeApiUrl() + "/devices/" + function_id + "/datapoints",
            data={},
            headers=self._headers(),
        ) as resp:
            response = await resp.json()
            return list(response.get("data", []))

    async def getSubscriptions(self, callback_url) -> list[dict]:
        """Get subscriptions from Junghome."""
        subscriptions = []
        async with self._session.get(
            self._junghomeApiUrl() + "/subscriptions",
            data={},
            headers=self._headers(),
        ) as resp:
            response = await resp.json()
            for subscription in response.get("data", []):
                try:
                    if subscription['attributes']['url'] == callback_url:
                        subscriptions.append(subscription)
                except Exception:
                    continue
            return list(subscriptions)

    async def getSubscriptionDatapoints(self, subscription_id) -> list[dict]:
        """Get all datapoints to given subscription fom Junghome."""
        async with self._session.get(
            self._junghomeApiUrl()
            + "/subscriptions/"
            + subscription_id
            + "/datapoints",
            data={},
            headers=self._headers(),
        ) as resp:
            response = await resp.json()
            return list(response.get("data", []))

    async def getDatapoint(self, id) -> dict:
        """Get datapoint from Junghome."""
        async with self._session.get(
            self._junghomeApiUrl() + "/datapoints/" + id,
            data={},
            headers=self._headers(),
        ) as resp:
            status = resp.status
            if status != 200:
                return None
            response = await resp.json()
            return list(response.get("data", []))

    async def sendCommand(self, datapoint_id: str, command: str):
        """Send command to Junghome."""
        data = {
            "data": [
                {
                    "id": datapoint_id,
                    "type": "datapoint",
                    "attributes": {"value": str(command)},
                }
            ]
        }
        async with self._session.put(
            self._junghomeApiUrl() + "/datapoints/values",
            json=data,
            headers=self._headers(),
        ) as resp:
            status = resp.status
            if status not in (200, 204):
                return False
        return True

    async def createSubscription(self, callback_url, datapoints) -> bool:
        """Create subscriptions."""
        subscriptions = await self.getSubscriptions(callback_url)
        data = {
            "data": {
                "type": "subscription",
                "relationships": {
                    "subscriptionDatapoints": {
                        "data": list(map(mapSubscriptionDatapoints, datapoints))
                    },
                },
                "attributes": {"url": callback_url},
            }
        }
        if not subscriptions:
            # If there is no subscription cretea a subscription
            async with self._session.post(
                self._junghomeApiUrl() + "/subscriptions",
                json=data,
                headers=self._headers(),
            ) as resp:
                status = resp.status
                if status not in (200, 204):
                    return False
        else:
            # If there are on or more subscriptions patch the first one an delete the others
            first = True
            for subscription in subscriptions:
                if first:
                    data["data"]["id"] = subscription["id"]
                    async with self._session.patch(
                        self._junghomeApiUrl() + "/subscriptions/" + subscription["id"],
                        json=data,
                        headers=self._headers(),
                    ) as resp:
                        status = resp.status
                        if status not in (200, 204):
                            return False
                    first = False
                else:
                    async with self._session.delete(
                        self._junghomeApiUrl() + "/subscriptions/" + subscription["id"],
                        json={},
                        headers=self._headers(),
                    ) as resp:
                        status = resp.status
                        if status not in (200, 204):
                            return False
        return True