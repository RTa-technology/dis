from typing import List

from .adapter import Adapter

__all__ = ['Transfer']


class Transfer:
  def __init__(self, adapter: Adapter) -> None:
    self._adapter = adapter

  def isnt_0_null(self, value) -> bool:
    if value == 0 or value == "" or value == "0":
      return False
    else:
      return True

  def is_str2int_null(self, value) -> int:
    if isinstance(value, int):
      return value
    elif value.isdigit():
      return int(value)
    else:
      return 0

  def is_additional_box2name(self, is_additional_box: bool, name: str, fixes_name: str) -> str:
    if is_additional_box and len(fixes_name) > 0:
      return name + "[" + fixes_name + "]"
    else:
      return name

  def skill_sum(self, num1, num2, num3, num4, num5) -> int:
    return self.is_str2int_null(num1) + self.is_str2int_null(num2) + self.is_str2int_null(num3) + \
           self.is_str2int_null(num4) + self.is_str2int_null(num5)

  def is_edit_skill(self, arr: dict) -> dict:
    """
    各skillの、profession_pointとinterest_pointとgrow_pointとother_pointのすべてが0か""以外の技能を返す
    :param arr:
    :return result:
    """
    result = {}
    for skill in arr:
      if self.isnt_0_null(skill['profession_point']) or self.isnt_0_null(skill['interest_point']) or \
          self.isnt_0_null(skill['grow_point']) or self.isnt_0_null(skill['other_point']):
        result[self.is_additional_box2name(skill['is_additional_box'], skill['name'], skill["fixed_name"])] = \
          self.skill_sum(skill['profession_point'], skill['interest_point'], skill['grow_point'], skill['other_point'], skill['default_value'])
    return result

  def is_skill(self, arr: dict) -> dict:
    result = {}
    for skill in arr:
      result[self.is_additional_box2name(skill['is_additional_box'], skill['name'], skill["fixed_name"])] = self.skill_sum(skill['profession_point'], skill['interest_point'],
                                             skill['grow_point'], skill['other_point'], skill['default_value'])
    return result

  def transfer(self) -> dict:
    return self._adapter.get_data()

  def get_parsonal_data(self) -> dict:
    return self._adapter.get_parsonal_data()

  def get_skill(self) -> dict:
    battle_skill = self.is_skill(self._adapter.get_battle_skill())
    search_skill = self.is_skill(self._adapter.get_search_skill())
    action_skill = self.is_skill(self._adapter.get_action_skill())
    negotiation_skill = self.is_skill(self._adapter.get_negotiation_skill())
    knowledge_skill = self.is_skill(self._adapter.get_knowledge_skill())

    return dict(**battle_skill, **search_skill, **action_skill, **negotiation_skill, **knowledge_skill)

  def get_edit_skill(self) -> dict:
    battle_skill = self.is_edit_skill(self._adapter.get_battle_skill())
    search_skill = self.is_edit_skill(self._adapter.get_search_skill())
    action_skill = self.is_edit_skill(self._adapter.get_action_skill())
    negotiation_skill = self.is_edit_skill(self._adapter.get_negotiation_skill())
    knowledge_skill = self.is_edit_skill(self._adapter.get_knowledge_skill())

    return dict(**battle_skill, **search_skill, **action_skill, **negotiation_skill, **knowledge_skill)

  def get_name(self) -> str:
    return self._adapter.get_result_name()

  def get_status(self) -> dict:
    result = {}
    ability_value = self._adapter.get_ability_value()
    for i, stu in enumerate(ability_value):
      try:
        result[stu] = self.is_str2int_null(ability_value[stu]["value"]) + self.is_str2int_null(ability_value[stu]["fixed_diff"]) + \
                                                self.is_str2int_null(ability_value[stu]["pre_fixed_diff"])
      except KeyError:
        result[stu] = self.is_str2int_null(ability_value[stu]["fixed_diff"]) + self.is_str2int_null(ability_value[stu]["pre_fixed_diff"])
    #hp, mp, san値修正
    result["hp"] = int((result["siz"]+result["con"])/10)
    result["mp"] = int(result["pow"]/5)
    result["san"] = result["pow"]
    return result

  def get_icon_url(self) -> str:
    return self._adapter.get_icon_url()

  def usage(self, id: int) -> dict:
    return self._adapter.get_usage()
