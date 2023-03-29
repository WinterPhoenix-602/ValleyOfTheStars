# Date: 2023-03-28
# Description: Contains classes for questlines and quests

from CustomMessages import *

class Questline:
    def __init__(self, name, description, quests, completed = False):
        self._name = name
        self._description = description
        self._quests = quests
        self._completed = completed

    # Getters
    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._description
    
    @property
    def quests(self):
        return self._quests
    
    @property
    def completed(self):
        return self._completed
    
    # Setters
    @name.setter
    def name(self, name):
        self._name = name

    @description.setter
    def description(self, description):
        self._description = description

    @quests.setter
    def quests(self, quests):
        self._quests = quests

    @completed.setter
    def completed(self, completed):
        for quest in self._quests:
            if quest.completed == False:
                completed = False
        self._completed = completed

    # Sets attributes from input dictionary
    def reader(self, input_dict):
        for key in input_dict:
            try:
                setattr(self, key, input_dict[key])
            except Exception:
                print("No such attribute, please consider adding it in init.")
        # If the description is not an empty string
        if self._description != "":
            formatForTable(self._description)

class Quest:
    def __init__(self, name, description, reward, requirements, completed = False):
        self.name = name
        self.description = description
        self.reward = reward
        self.requirements = requirements
        self.completed = completed

    # Getters
    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description
    
    @property
    def reward(self):
        return self._reward

    @property
    def requirements(self):
        return self._requirements
    
    @property
    def completed(self):
        return self._completed
    
    # Setters
    @name.setter
    def name(self, name):
        self._name = name

    @description.setter
    def description(self, description):
        self._description = description

    @reward.setter
    def reward(self, reward):
        self._reward = reward

    @requirements.setter
    def requirements(self, requirements):
        self._requirements = requirements

    @completed.setter
    def completed(self, completed):
        self._completed = completed
