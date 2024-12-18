from typing import Dict, Any
import logging
from ..models import LightData
from ..config import LIGHT_STATE, LIGHT_PARAMS
from ..credentials import Credentials

logger = logging.getLogger(__name__)

class Light:
    """Represents a Haven light device."""

    def __init__(self, credentials: Credentials, location_id: int, light_id: int, data: Dict[str, Any]) -> None:
        self._credentials = credentials
        self.location_id = location_id
        self._data = LightData(
            light_id=int(data["lightId"]),
            name=data["name"],
            status=data.get("lightingStatusId", LIGHT_STATE["OFF"]),
            brightness=data.get("brightness", LIGHT_PARAMS["BRIGHTNESS"]),
            color=data.get("color", LIGHT_PARAMS["COLOR"]),
            pattern_speed=data.get("patternSpeed", LIGHT_PARAMS["PATTERN_SPEED"])
        )
        logger.debug("Initialized Light: %s (ID: %d)", self.name, self.id)

    @property
    def id(self) -> int:
        return self._data.light_id

    @property
    def name(self) -> str:
        return self._data.name

    @property
    def is_on(self) -> bool:
        return self._data.status == LIGHT_STATE["ON"]

    def turn_on(self) -> None:
        """Turn the light on."""
        logger.debug("Turning on light: %s (ID: %d)", self.name, self.id)
        try:
            self._send_command(LIGHT_STATE["ON"])
            self._data.status = LIGHT_STATE["ON"]
            logger.info("Light turned on successfully: %s", self.name)
        except Exception as e:
            logger.error("Failed to turn on light %s: %s", self.name, str(e))
            raise

    def turn_off(self) -> None:
        """Turn the light off."""
        logger.debug("Turning off light: %s (ID: %d)", self.name, self.id)
        try:
            self._send_command(LIGHT_STATE["OFF"])
            self._data.status = LIGHT_STATE["OFF"]
            logger.info("Light turned off successfully: %s", self.name)
        except Exception as e:
            logger.error("Failed to turn off light %s: %s", self.name, str(e))
            raise
        
    def _send_command(self, status_id: int) -> None:
        """Send a command to the light."""
        self._credentials.make_request(
            "POST",
            "/Light/CommandV1",
            params={"locationId": self.location_id},
            json={
                "lightingStatusId": status_id,
                "lightBrightnessId": LIGHT_PARAMS["BRIGHTNESS"],
                "lightColorId": LIGHT_PARAMS["COLOR"],
                "patternSpeedId": LIGHT_PARAMS["PATTERN_SPEED"],
                "selectedLightIds": [self.id],
                "locationId": self.location_id
            }
        )