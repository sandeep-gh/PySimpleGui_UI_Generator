# TODO: ToggleExclusive


class ToggleExclusive:
    pass
#     def __init__(self, attr, active_val, inactive_val, curr_active_elem):
#         '''
#         get_updater: a functor that returns the update function
#         '''
#         # self.gelems = gelems
#         self.attr = attr
#         self.curr_active_elem = curr_active_elem
#         self.curr_active_elem = None
#         self.active_val = active_val
#         self.inactive_val = inactive_val

#     def set_active(self, window, event):
#         window.Element(event).Update(**{self.attr: self.active_val})
#         if self.curr_active_elem is not None:
#             window.Element(self.curr_active_elem).Update(
#                 **{self.attr: self.inactive_val})
#         self.curr_active_elem = event


class ToggleExclusiveOther:
    pass
#     def __init__(self, attr, active_val, inactive_val, curr_active_elem):
#         '''
#         get_updater: a functor that returns the update function
#         '''
#         # self.gelems = gelems
#         self.attr = attr
#         self.curr_active_elem = curr_active_elem
#         self.curr_active_elem = None
#         self.active_val = active_val
#         self.inactive_val = inactive_val

#     def set_active(self, window, event):
#         oevent = get_key_from_label("_".join(event.split("_")[1:]))
#         #print("toggle called for event=", "_".join(event.split("_")[1:]))
#         # print(window.Element(oevent))
#         window.Element(oevent).Update(**{self.attr: self.active_val})
#         if self.curr_active_elem is not None:
#             window.Element(self.curr_active_elem).Update(
#                 **{self.attr: self.inactive_val})
#         self.curr_active_elem = oevent
