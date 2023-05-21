# Date: 2023-03-28
# Description: Contains classes for questlines and quests

from CustomMessages import *

class Questline:
    def __init__(self, name="", active=False, description="", quests=None, complete = False):
        self._name = name
        self._active = active
        self._description = description
        self._quests = [] if quests is None else quests
        self._complete = complete

    # Getters
    @property
    def name(self):
        return self._name
    
    @property
    def active(self):
        return self._active
    
    @property
    def description(self):
        return self._description
    
    @property
    def quests(self):
        return self._quests
    
    @property
    def complete(self):
        return self._complete
    
    # Setters
    @name.setter
    def name(self, name):
        self._name = name

    @active.setter
    def active(self, active):
        self._active = active

    @description.setter
    def description(self, description):
        self._description = description

    @quests.setter
    def quests(self, quests):
        self._quests = quests

    @complete.setter
    def complete(self, complete):
        for quest in self._quests:
            if quest.complete == False:
                complete = False
        self._complete = complete

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
        # If there are quests
        if len(self._quests) > 0:
            # Iterate over each quest
            for quest in self._quests:
                a = Quest(quest)
                a.reader(self._quests[quest])
                self._quests[quest] = a

class Quest:
    def __init__(self, name="", description="", reward_text="", reward=None, complete = False, requires = False):
        self._name = name
        self._description = description
        self._reward_text = reward_text
        self._reward = {} if reward is None else reward
        self._complete = complete
        self._requires = requires

    # Getters
    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description
    
    @property
    def reward_text(self):
        return self._reward_text
    
    @property
    def reward(self):
        return self._reward
    
    @property
    def complete(self):
        return self._complete
    
    @property
    def requires(self):
        return self._requires
    
    # Setters
    @name.setter
    def name(self, name):
        self._name = name

    @description.setter
    def description(self, description):
        self._description = description

    @reward_text.setter
    def reward_text(self, reward_text):
        self._reward_text = reward_text

    @reward.setter
    def reward(self, reward):
        self._reward = reward

    @complete.setter
    def complete(self, complete):
        self._complete = complete

    @requires.setter
    def requires(self, active):
        self._requires = active

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
