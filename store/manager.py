from core.exceptions.exceptions import DuplicationException

from .models import Facility
from .messages import FacilityMessages


class FacilityManager:
    def exists_check(self, data):
        category = data["category"]
        name = data["name"]
        facility = Facility.objects.filter(name=name, category=category)

        if facility.exists():
            raise DuplicationException(
                FacilityMessages.ALREADY_EXISTS_ERROR.format(category, name)
            )
