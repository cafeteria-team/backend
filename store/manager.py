from core.exceptions.exceptions import DuplicationException

from .models import Facility
from .messages import FacilityMessages


class FacilityManager:
    def exists_check(self, data, facility_id=None):
        category = data["category"]
        name = data["name"]
        if facility_id == None:
            facility = Facility.objects.filter(name=name, category=category)
        else:
            facility = Facility.objects.exclude(id=facility_id).filter(
                name=name, category=category
            )

        if facility.exists():
            raise DuplicationException(
                FacilityMessages.ALREADY_EXISTS_ERROR.format(category, name)
            )
