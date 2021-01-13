import test_bld_event_actions
everything_bagel_dict = {}
test_bld_dict = {'button1a': test_bld_event_actions, 'button1b': test_bld_event_actions, 'button2a': test_bld_event_actions, 'button2b': test_bld_event_actions}
everything_bagel_dict = {**everything_bagel_dict, **test_bld_dict}
test_bld_dict = {'text1a': test_bld_event_actions, 'text1b': test_bld_event_actions, 'text2a': test_bld_event_actions, 'text2b': test_bld_event_actions}
everything_bagel_dict = {**everything_bagel_dict, **test_bld_dict}
def everything_bagel(window, event):

    	if event in everything_bagel_dict:

    		everything_bagel_dict[event].on_event(window, event)