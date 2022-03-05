import os
import yaml

from utils.logger import *
from control import *

""" modes """
BROWS = 1
VIEW = 2
TAG = 3
NOTES = 4
EXIT = -1

PROJ_DIR = "subjectA/projectA"
# PROJ_DIR = "subject1/2021/project"


""" current framework environment """
class Environment:
    def __init__(self, screens, windows, conf):

        """ screens and windows """
        self.screens = screens
        self.windows = windows

        self.win_center_pos = conf['window']['position']
        self.win_left_edge, self.win_right_edge = conf['window']['left_edge'], conf['window']['right_edge']
        self.win_top_edge, self.win_bottom_edge = conf['window']['top_edge'], conf['window']['bottom_edge']
        self.windows.set_edges(self.win_left_edge, self.win_right_edge, self.win_top_edge, self.win_bottom_edge)
        self.windows.center.set_position(self.win_center_pos)


        """ environment """
        self.mode = conf['env']['mode']
        self.quick_view = conf['env']['quick_view']
        self.edit_allowed = conf['env']['edit_allowed'] # TODO: REMOVE
        self.show_tags = conf['env']['edit_allowed'] # TODO: edit_allowed --> show_tags
        self.note_highlight = conf['env']['note_highlight']
        self.show_cached_files = conf['env']['show_cached_files']
        self.start_with_line_numbers = conf['env']['start_with_line_numbers']

        self.tab_size = conf['editor']['tab_size']
        self.messages = conf['messages'] # {'empty_path_filter': txt, 'empty_tag_filter': txt, ... }

        self.file_edit_mode = False # file edit or file management
        self.show_menu = False
        self.line_numbers = None # None or str(number_of_lines_in_buffer)
        self.note_management = False
        self.specific_line_highlight = None # (line_number, color)

        self.file_to_open = None
        self.cwd = None # Directory(path, dirs, files)
        self.buffer = None # Buffer(path, lines)
        self.tags = None # Tags(path, data)

        """ filter """
        self.filter = None # Filter()
        self.filter_mode = False

        self.menu_mode = False
        self.user_input_mode = False

        self.report = None # Report(path, data)

        """ reports """
        self.code_review = None # Report(path, data) for current file
        # self.other_notes = None # Report(path, data) for current project TODO
        # self.auto_notes = None # Report(path, data) for current project TODO
        # self.auto_report = None # TODO

        self.typical_notes = [] # [notes] all saved typical notes (from all projects)

        self.control = Control()

    def set_user_control(self, contr):
        self.control.set_file_functions(contr)
        self.control.set_brows_functions(contr)
        self.control.set_tags_functions(contr)
        self.control.set_notes_functions(contr)
        self.control.set_filter_functions(contr)
        self.control.set_menu_functions(contr)
        self.control.set_user_input_functions(contr)


    # TODO: get current project dir
    def get_project_path(self):
        return os.path.join(HOME, PROJ_DIR)

    def get_project_name(self):
        return PROJ_DIR

    def set_file_to_open(self, file_to_open):
        if self.file_to_open != file_to_open:
            self.file_to_open = file_to_open
            # if self.show_tags:
            if self.edit_allowed:
                self.windows.edit.reset()
            else:
                self.windows.view.reset()
            self.windows.tag.reset(0,0)
            self.windows.notes.reset(0,0)
            self.report = None

    def get_screen_for_current_mode(self):
        if self.is_brows_mode():
            return self.screens.left, self.windows.brows
        if self.is_view_mode():
            # if self.show_tags:
            if self.edit_allowed:
                return self.screens.right, self.windows.edit
            else:
                return self.screens.right_up, self.windows.view
        if self.is_tag_mode():
            return self.screens.right_down, self.windows.tag
        if self.is_notes_mode():
            return self.screens.left, self.windows.notes

    def update_win_for_current_mode(self, win):
        if self.is_brows_mode():
            self.windows.brows = win
        if self.is_view_mode():
            # if self.show_tags:
            if self.edit_allowed:
                self.windows.edit = win
            else:
                self.windows.view = win
        if self.is_tag_mode():
            self.windows.tag = win
        if self.is_notes_mode():
            self.windows.notes = win

    def update_center_win(self, win):
        self.windows.center = win


    def get_center_win(self, reset=False, row=None, col=None):
        if reset:
            self.windows.center.set_position(self.win_center_pos, screen=self.screens.center)
            self.windows.center.reset(row=row, col=col)
        return self.screens.center, self.windows.center


    """ filter """
    def filter_not_empty(self):
        if self.filter is not None:
            return not self.filter.is_empty()
        else:
            return False

    def path_filter_on(self):
        if self.filter is not None:
            if self.filter.path:
                return True
        return False

    def content_filter_on(self):
        if self.filter is not None:
            if self.filter.content:
                return True
        return False

    def tag_filter_on(self):
        if self.filter is not None:
            if self.filter.tag:
                return True
        return False
    
    def prepare_browsing_after_filter(self):
        if not self.is_exit_mode():
            self.set_brows_mode()
            self.disable_note_management()
            self.quick_view = True
            self.windows.brows.reset(0,0)


    """ update data """
    def update_browsing_data(self, win, cwd):
        self.windows.brows = win
        self.cwd = cwd

    def update_viewing_data(self, win, buffer, report=None):
        # if self.show_tags:
        if self.edit_allowed:
            self.windows.edit = win
        else:
            self.windows.view = win
        self.buffer = buffer
        if report:
            self.report = report

    def update_tagging_data(self, win, tags):
        self.windows.tag = win
        self.tags = tags

    def update_report_data(self, win, report):
        self.windows.notes = win
        self.report = report


    """ file management """
    def change_to_file_edit_mode(self):
        self.file_edit_mode = True

    def change_to_file_management(self):
        self.file_edit_mode = False


    # TO REMOVE
    def enable_file_edit(self):
        self.edit_allowed = True
        self.quick_view = False # TODO ???

    # TO REMOVE
    def disable_file_edit(self):
        self.edit_allowed = False


    """ note management """
    def enable_note_management(self):
        self.note_management = True

    def disable_note_management(self):
        self.note_management = False


    """ line numbers """
    def enable_line_numbers(self, buffer):
        self.line_numbers = str(len(buffer))

    def disable_line_numbers(self):
        self.line_numbers = None


    """ set mode """
    def set_brows_mode(self):
        self.mode = BROWS

    def set_view_mode(self):
        self.mode = VIEW

    def set_tag_mode(self):
        self.mode = TAG

    def set_notes_mode(self):
        self.mode = NOTES

    def set_exit_mode(self):
        self.mode = EXIT

    """ cycling between modes """
    def switch_to_next_mode(self):
        if self.is_brows_mode():
            self.mode = VIEW # Brows -> View
        elif self.is_view_mode():
            # if self.show_tags:
            if self.edit_allowed:
                if self.note_management:
                    self.mode = NOTES # View -> Notes
                else:
                    self.mode = BROWS # View -> Brows
            else:
                self.mode = TAG # View -> Tag
        elif self.is_tag_mode():
            if self.note_management:
                self.mode = NOTES # Tag -> Notes
            else:
                self.mode = BROWS # Tag -> Brows
        elif self.is_notes_mode():
            self.mode = VIEW # Notes -> View


    """ check mode """
    def is_brows_mode(self):
        return self.mode == BROWS

    def is_view_mode(self):
        return self.mode == VIEW

    def is_tag_mode(self):
        return self.mode == TAG

    def is_notes_mode(self):
        return self.mode == NOTES

    def is_exit_mode(self):
        return self.mode == EXIT

    def is_filter_mode(self):
        return self.filter_mode

    def is_menu_mode(self):
        return self.menu_mode

    def is_user_input_mode(self):
        return self.user_input_mode
