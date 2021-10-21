from utils import APIException
"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class Base:
    # base class to inherit base methods
    
    # read-only: Use this method to generate random members ID's when adding members into the list
    def _generateId(self):
        return randint(0, 99999999)


class Member(Base):
    # represents a family member linked to a specific family
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', self._generateId())
        self.first_name = kwargs.get('first_name')
        self.age = kwargs.get('age')
        self.lucky_numbers = kwargs.get('lucky_numbers')
        self.family = kwargs.get('family')

    @classmethod
    def create(cls, family, **kwargs):
        # validate input
        if kwargs.get('first_name') is None:
            raise APIException('missing first name', 400)
        if kwargs.get('age') is None:
            raise APIException('missing age', 400)
        if (
            kwargs.get('lucky_numbers') is None or
            not isinstance(kwargs.get('lucky_numbers'), list) 
        ):
            kwargs.update(lucky_numbers=[])
        # create and return Member new instance
        return cls(
            **kwargs,
            family=family
        )

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.family.last_name,
            "age": self.age,
            "lucky_numbers": self.lucky_numbers
        }


class FamilyStructure(Base):
    def __init__(self, last_name):
        self.id = self._generateId()
        self.last_name = last_name
        self._members = []

    def add_member(self, member):
        # creates new member instance
        new_member = Member.create(self, **member)
        # updates class property _members
        self._members.append(new_member)
        # returns member added
        return new_member

    def delete_member(self, id):
        # fill this method and update the return
        # updates _members value ignoring member 
        # with id == id from the list
        self._members = list(filter(
            lambda member: int(member.id) != id,
            self._members
        ))
        # returns current length for _members property
        return len(self._members)

    def get_member(self, id):
        # fill this method and update the return
        for member in self._members:
            if member.id == id:
                return member
        # if no member with such id:
        raise APIException("no such member", 404)

    # this method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members
