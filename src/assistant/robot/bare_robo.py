import speech_recognition as sr
from typing import Optional, Dict, Any


class BARE_ROBO:
    """
    Basic robot class with fundamental properties.

    This is the foundation class that provides basic robot functionality
    like naming and identification.
    """

    def __init__(self, name: str = "Default Robot"):
        self._name = name
        self._is_active = True
        self._created_at = None  # Can be set by subclasses

    @property
    def name(self) -> str:
        """Get the robot's name"""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the robot's name"""
        if not value or not value.strip():
            raise ValueError("Robot name cannot be empty")
        self._name = value.strip()

    @property
    def is_active(self) -> bool:
        """Check if the robot is active"""
        return self._is_active

    def activate(self) -> None:
        """Activate the robot"""
        self._is_active = True

    def deactivate(self) -> None:
        """Deactivate the robot"""
        self._is_active = False

    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the robot"""
        return {
            'name': self.name,
            'active': self.is_active,
            'type': self.__class__.__name__
        }

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', id={self.robot_id})"

    def __repr__(self) -> str:
        return self.__str__()

