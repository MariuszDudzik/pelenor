import control_obj
import kolor
import pygame
import hexagon
import camera
import play_handler
import gamelogic
import hexagon
from functools import partial # Powoduje, że funkcja x() jest wywoływana bez argumentów
import dictionary
import support
import math

class Play(object):

    def __init__(self, screen, game_controller, connection, game):

        self.screen = screen
        self.game_controller = game_controller
        self.connection = connection
        self.game = game
        self.camera = camera.Camera()
        self.base_hex_size = self.screen.get_height() * 0.024
        self.world_origin_x = 0
        self.world_origin_y = 0
        self.hex_size = screen.get_height() * (0.024 + self.camera.get_camera_scale() * self.camera.get_zoom_speed())
        self.stage_fields = []
        self.phaze_fields = []
        self.hex = {}
        self.units = {}
        self.reinforcement = {}
        self.left_menu_graphics = pygame.sprite.LayeredDirty()
        self.right_menu_graphics = pygame.sprite.LayeredDirty()
        self.map_view = pygame.sprite.LayeredDirty()
        self.manage_graphics = pygame.sprite.LayeredDirty()
        self.stage_phaze_graphics = pygame.sprite.LayeredDirty()
        self.tooltip_graphics = pygame.sprite.LayeredDirty()
        self.mouse_dragging = False
        self.last_mouse_pos = None 
        self.last_click_time = 0
        self.click_cooldown = 200

        self.player_w_field = control_obj.Label(0, 0, screen.get_width() * 0.1, screen.get_height() // 2,
                            kolor.GREEN, "", None, int(screen.get_height() * 0.035), kolor.WHITE, None, None, None, None)
        self.player_w_login = control_obj.Label(3, 3, int(self.player_w_field.get_width()  - 6), 
                            int(self.player_w_field.get_height() * 0.06), kolor.WHITE, self.game.player_w.get_login(), 
                            self.game_controller.get_default_font(), int(self.player_w_field.get_height() * 0.06 * 0.8), 
                            kolor.BLACK, None, None, None, None, None, None)
        self.player_w_photo = control_obj.Label(3, self.player_w_login.get_height() + 6, 
                            int((self.player_w_field.get_width() - 9) / 2), int((self.player_w_field.get_width()  - 9) / 2), kolor.BLUE, "", None, int(screen.get_height() * 0.035), kolor.WHITE, None, None, None, None, None, None)
        self.player_w_demoralization_1 = control_obj.Label(self.player_w_photo.get_width() + 6, 
                            self.player_w_login.get_height() + 6, int((self.player_w_photo.get_width() - 3) / 2), int((self.player_w_photo.get_height() - 3) / 2), kolor.WHITE, str(self.game.player_w.get_demoralization_threshold_2()), self.game_controller.get_default_font(), int(self.player_w_field.get_height() * 0.06 * 0.8),
                            kolor.BLACK, None, None, None, None, None, None)
        self.player_w_demoralization_2 = control_obj.Label(self.player_w_photo.get_width() + 9 
                            + self.player_w_demoralization_1.get_width(), self.player_w_login.get_height() + 6, 
                            int((self.player_w_photo.get_width() - 3) / 2), int((self.player_w_photo.get_height() - 3) / 2), kolor.WHITE, str(self.game.player_w.get_demoralization_threshold_3()), 
                            self.game_controller.get_default_font(), int(self.player_w_field.get_height() * 0.06 * 0.8), 
                            kolor.BLACK, None, None, None, None, None, None)
        self.player_w_spell_power = control_obj.Label(self.player_w_photo.get_width() + 6, 
                            self.player_w_login.get_height() + self.player_w_demoralization_1.get_height() + 9, int((self.player_w_photo.get_width() - 3) / 2), int((self.player_w_photo.get_height() - 3) / 2), kolor.WHITE, str(self.game.player_w.get_spell_power()), self.game_controller.get_default_font(), int(self.player_w_field.get_height() * 0.06 * 0.8), kolor.BLACK, None, None, None, None, None, None) 
        self.player_s_field = control_obj.Label(0, self.player_w_field.get_height(), screen.get_width() * 0.1, 
                            screen.get_height() // 2, kolor.RED, "", None, int(screen.get_height() * 0.035), kolor.WHITE, None, None, None, None, None, None)
        self.player_s_login = control_obj.Label(3, self.player_s_field.get_height() + 3, 
                            int(self.player_s_field.get_width() - 6), int(self.player_s_field.get_height() * 0.06), kolor.WHITE, self.game.player_s.get_login(), self.game_controller.get_default_font(), int(self.player_s_field.get_height() * 0.06 * 0.8), kolor.BLACK, None, None, None, None, None, None)
        self.player_s_photo = control_obj.Label(3, self.player_s_login.get_height() + 6 + 
                            self.player_s_field.get_height(), int((self.player_s_field.get_width()  - 9) / 2), int((self.player_s_field.get_width()  - 9) / 2), kolor.BLUE, "", None, int(screen.get_height() * 0.035), kolor.WHITE, None, None, None, None, None, None)
        self.player_s_demoralization = control_obj.Label(self.player_s_photo.get_width() + 6, 
                            self.player_s_login.get_height() + 6 + self.player_s_field.get_height() , 
                            int((self.player_s_photo.get_height() - 3) / 2), int((self.player_s_photo.get_height() - 3) / 2), kolor.WHITE, str(self.game.player_s.get_demoralization_threshold_1()), 
                            self.game_controller.get_default_font(), int(self.player_s_field.get_height() * 0.06 * 0.8), 
                            kolor.BLACK, None, None, None, None, None, None)
        self.player_s_spell_power = control_obj.Label(self.player_s_photo.get_width() + 6, 
                            self.player_s_login.get_height() + self.player_s_demoralization.get_height() + 9 + 
                            self.player_s_field.get_height(), int((self.player_s_photo.get_width() - 3) / 2), 
                            int((self.player_s_photo.get_height() - 3) / 2), kolor.WHITE, 
                            str(self.game.player_s.get_spell_power()), self.game_controller.get_default_font(), 
                            int(self.player_s_field.get_height() * 0.06 * 0.8), kolor.BLACK, None, None, None, None, None, None)
        self.player_s_heads = control_obj.Label(self.player_s_photo.get_width() + 9 + 
                            self.player_s_spell_power.get_width(), self.player_s_login.get_height() + 6 + self.player_s_field.get_height(), int((self.player_s_photo.get_width() - 3) / 2), int((self.player_s_photo.get_height() - 3) / 2), kolor.WHITE, str(self.game.player_s.get_heads()), self.game_controller.get_default_font(), int(self.player_s_field.get_height() * 0.06 * 0.8), kolor.BLACK, None, None, None, None, None, None)
        self.state_field = control_obj.Label(screen.get_width() - screen.get_width() * 0.1, 0, screen.get_width() * 0.101 
                            ,screen.get_height(), kolor.BLUE, "", None, int(screen.get_height() * 0.035), kolor.WHITE, None, None, None, None, None, None)
        self.map = control_obj.Label(self.player_w_field.get_width(), 0, self.screen.get_width() - 
                            self.player_w_field.get_width() - self.state_field.get_width(), self.screen.get_height(), 
                            kolor.ORANGE, "", None,  int(screen.get_height() * 0.035), kolor.WHITE, None, None,
                            partial(play_handler.ZoomHandler.handle_in, self.get_camera, self), 
                            partial(play_handler.ZoomHandler.handle_out, self.get_camera, self), None, None)
        self.zoom_in_button = control_obj.Button(self.state_field.get_position_x() + (screen.get_height() * 0.0028), 
                            screen.get_height() * 0.0028, screen.get_height() * 0.028, screen.get_height() * 0.028, 
                            kolor.GREY, "+", self.game_controller.get_default_font(), int(screen.get_height() * 0.03), kolor.BLACK, partial(play_handler.ZoomHandler.handle_in, self.get_camera, self), None, None, None, play_handler.PlayHandler.on_hover, play_handler.PlayHandler.un_hover)
        self.zoom_out_button = control_obj.Button(self.state_field.get_position_x() + (screen.get_height() * 0.033),
                            screen.get_height() * 0.0028, screen.get_height() * 0.028, screen.get_height() * 0.028, 
                            kolor.GREY, "-", self.game_controller.get_default_font(), int(screen.get_height() * 0.03), kolor.BLACK, partial(play_handler.ZoomHandler.handle_out, self.get_camera, self), None, None, None, play_handler.PlayHandler.on_hover, play_handler.PlayHandler.un_hover)
        self.dice_button = control_obj.Button(self.state_field.get_position_x() + 
                            (self.state_field.get_width() // 3 // 3),len(self.game.get_stages_list()) * (self.state_field.get_height() / 24) + screen.get_height() * 0.033 + screen.get_height() * 0.028 + 26, self.state_field.get_width() // 3, self.state_field.get_width() // 3, kolor.GREY, "", self.game_controller.get_default_font(),int(screen.get_height() * 0.03), kolor.BLACK, None, None, None, None, None, None)
        self.result_field = control_obj.Label(self.dice_button.get_position_x() + self.dice_button.get_width() 
                            + (self.state_field.get_width() // 3 // 3), self.dice_button.get_position_y(),self.state_field.get_width() // 3, self.state_field.get_width() // 3, kolor.WHITE,  "",  self.game_controller.get_default_font(), int(screen.get_height() * 0.03), kolor.BLACK, None, None, None, None, None, None)
        self.message_field = control_obj.Label(self.state_field.get_position_x() + (screen.get_height() * 0.0028),  
                            self.dice_button.get_position_y() + self.dice_button.get_height() + 10,  self.state_field.get_width() - (screen.get_height() * 0.0028 * 2), screen.get_height() * 0.100, kolor.WHITE, "", self.game_controller.get_default_font(), int(screen.get_height() * 0.016), kolor.BLACK, None, None, None, None, None, None)
        self.action_button = control_obj.Button(self.state_field.get_position_x() + (screen.get_height() * 0.0028), 
                            self.message_field.get_position_y() + self.message_field.get_height() + 3, self.state_field.get_width() - (screen.get_height() * 0.0028 * 2), screen.get_height() * 0.045, kolor.GREY, "Zakończ turę", self.game_controller.get_default_font(), int(screen.get_height() * 0.045 * 0.6), kolor.BLACK, partial(play_handler.PlayHandler.action_left_click, play_obj=self), None, None, None, play_handler.PlayHandler.on_hover, play_handler.PlayHandler.un_hover)
        self.tooltip = control_obj.Tooltip(0, 0, 0, 0, kolor.WHITE, "", self.game_controller.get_default_font()
                            , int(screen.get_height() * 0.015), kolor.BLACK, None, None, None, None, None, None)

        self._init_stage_and_phaze_fields()
        self._prepare_graphics()
        self.set_map_view()
        self.camera.set_min_x(-0.066 * self.screen.get_height() * 44)
        self.camera.set_min_y(-0.066 * self.screen.get_height() * 31)
        self.tooltip.dirty = 0
        self.set_message()


    def _apply_camera_to_hexgraphic(self, hexG):
        sx, sy = self._world_to_screen(hexG.base_center.x, hexG.base_center.y)
        hexG.current_center = hexagon.Point(sx, sy)
        hexG.current_size   = self.base_hex_size * self.camera.get_camera_scale()
        hexG.zoom_level     = self.camera.get_camera_scale()
        hexG.set_dirty()


    def _hex_to_world_center(self, q, r, s):
        bs = self.base_hex_size
        wx = bs * (1.5 * q) + self.world_origin_x + bs
        wy = bs * (math.sqrt(3)/2 * q + math.sqrt(3) * r) + self.world_origin_y + bs
        return wx, wy

    def _world_to_screen(self, wx, wy):
        cam = self.camera
        scale = cam.get_camera_scale()
        ui_x = self.map.get_position_x()
        ui_y = self.map.get_position_y()
        sx = ui_x + (wx - cam.get_camera_x()) * scale
        sy = ui_y + (wy - cam.get_camera_y()) * scale
        return sx, sy


    def set_message(self, message=dictionary.message[0]):
        self.message_field.wrapped_lines = support.Wrap.wrap_text(message,pygame.font.SysFont(self.message_field.font_style, self.message_field.font_size), int(self.message_field.get_width() * 0.9))

    def set_hex_base_size(self):
        self.hex_size = self.screen.get_height() * (0.017 + self.camera.get_camera_scale() * self.camera.get_zoom_speed())


    def set_map_view(self):
        self.map_view.empty()
        self.map_view.add(self.map, layer=1)

        visible_hexes = self.get_visible_hexagons(
            self.get_map(), self.get_camera(), self.game.get_board().get_hexes()
        )

        self.hex = hexagon.Hexagon.create_hex_graphics_dict(
            self.get_camera(), visible_hexes, self.get_map(), play_obj=self
        )

        self.map_view.add(*self.hex.values(), layer=3)

        for unit in self.game.player_w.get_units().values():
            if unit.get_qrs() is not None and tuple(unit.get_qrs()) in self.hex:
                self.add_unit('Z', unit.id, unit.get_qrs())

        for unit in self.game.player_s.get_units().values():
            if unit.get_qrs() is not None and tuple(unit.get_qrs()) in self.hex:
                self.add_unit('C', unit.id, unit.get_qrs())


    def _prepare_graphics(self):
        for sprite in [self.player_w_field, self.player_s_field]:
            self.left_menu_graphics.add(sprite, layer=1)
        for sprite in [self.player_w_login, self.player_w_photo, self.player_w_demoralization_1, self.player_w_demoralization_2,
                    self.player_w_spell_power, self.player_s_login, self.player_s_photo, self.player_s_demoralization, self.player_s_spell_power, self.player_s_heads]:
            self.left_menu_graphics.add(sprite, layer=2)
        self.right_menu_graphics.add(self.state_field, layer=1)
        self.manage_graphics.add(self.zoom_in_button, self.zoom_out_button, self.dice_button, self.result_field,
                                self.message_field, self.action_button, layer=4)
        for sprite in self.stage_fields:
            self.stage_phaze_graphics.add(sprite, layer=2)
        for sprite in self.phaze_fields:
            self.stage_phaze_graphics.add(sprite, layer=3)
        self.tooltip_graphics.add(self.tooltip, layer=5)


    def add_reinforcement_graphics(self):
        self.left_menu_graphics.add(*self.reinforcement.values(), layer=4)


    def remove_reinforcement(self, unit_id):
        unit = self.reinforcement.get(unit_id)
        if unit:
            self.left_menu_graphics.remove(unit)
            del self.reinforcement[unit_id]


    def remove_unit(self, unit_id):
        unit = self.units.get(unit_id)
        if unit:
            self.map_view.remove(unit)
            del self.units[unit_id]


    def _init_stage_and_phaze_fields(self):
        stages = self.game.get_stages_list()
        phazes = self.game.get_phazes_list()
        width = self.state_field.get_width()
        height = self.state_field.get_height()
        con_stage_height = int(height / 24)
        stage_height = int(height / 24)
        phaze_width = (width - 6) // 9
        phaze_height = con_stage_height * 0.96 // 2
        max_line_width = self.screen.get_width() * 0.1
        tooltip_x = self.screen.get_width() - self.state_field.get_width() - max_line_width - 10

        self.stage_fields.clear()
        self.phaze_fields.clear()

        for stage in stages:
            text =  f"ETAP {stage.get_nr_stage()}: {stage.get_season()} \n {stage.get_text()}"
            stage_field = control_obj.StageGraph(
                self.state_field.get_position_x() + 3,
                stage_height,
                width - 6,
                con_stage_height,
                stage.get_colour(),
                "",
                None,
                int(height * 0.035),
                kolor.WHITE,
                None,
                None,
                None,
                None,
                partial(play_handler.ToolTipHandler.on_hover, get_tooltip=self.get_tooltip, tool_x=tooltip_x, tool_y=stage_height, max_line_width=max_line_width),
                partial(play_handler.ToolTipHandler.un_hover, play_obj=self),
                stage,

            )
            stage_field.tiptext = text
            self.stage_fields.append(stage_field)
            stage_height += con_stage_height + 2

        stage_height = int(height / 24)
        i = 0
        for phaze in phazes:
            text = f"Faza {phaze.get_nr_phaze()}: {phaze.get_name()}"
            i += 1
            phaze_field = control_obj.PhazeGraph(
                4.8 + self.state_field.get_position_x() + (phaze_width + 2.0) * (i - 1),
                stage_height + con_stage_height * 0.08,
                phaze_width,
                phaze_height,
                phaze.get_colour(),
                "",
                None,
                int(height * 0.035),
                kolor.BLACK,
                None,
                None,
                None,
                None,
                partial(play_handler.ToolTipHandler.on_hover, get_tooltip=self.get_tooltip, tool_x=tooltip_x, tool_y=stage_height, max_line_width=max_line_width),
                partial(play_handler.ToolTipHandler.un_hover, play_obj=self),
                phaze,
            )
            phaze_field.tiptext = text
            self.phaze_fields.append(phaze_field)
            if i % 8 == 0:
                i = 0
                stage_height += con_stage_height + 2


    """
    def checkReinforcement(self):
        if self.gameController.getDeploy():
            self.addReinforcement()
    """

    def add_unit(self, site, id, qrs):
        qrs = tuple(qrs)

        if site == 'C':
            units = self.game.get_player_s_units()
            colour = kolor.REDJ
        elif site == 'Z':
            units = self.game.get_player_w_units()
            colour = kolor.LIME
        else:
            return

        unit = units[id]
        unit.set_deploy()
        unit.set_qrs(qrs)

        board_hex = self.game.get_board().get_hexes()[qrs]
        if id not in board_hex.pawn_list:
            board_hex.pawn_list.append(id)
        if id not in board_hex.pawn_graph_list:
            board_hex.pawn_graph_list.append(id)
        index = board_hex.pawn_graph_list.index(id)

        q, r, s = qrs
        wx, wy = self._hex_to_world_center(q, r, s)
        sx, sy = self._world_to_screen(wx, wy)

        size = self.base_hex_size * 1.2 * self.camera.get_camera_scale()

        pos_x = sx - size / 2
        pos_y = sy - size / 2

        offset_px = max(1, int(1 * self.camera.get_camera_scale()))
        pos_x += index * offset_px
        pos_y += index * offset_px

        layernr = 10 + index

        max_line_width = self.screen.get_width() * 0.08
        unitG = control_obj.UnitGraph(pos_x, pos_y, size, size, colour, "",self.game_controller.get_default_font(),
                int(size * 0.85 / 3), kolor.BLACK, None, None, None, None, partial(play_handler.ToolTipHandler.on_hover_unit,get_tooltip=self.get_tooltip, tool_x=pos_x, tool_y=pos_y - 75,max_line_width=max_line_width, play_obj=self),
                partial(play_handler.ToolTipHandler.un_hover_unit, play_obj=self), unit.get_board_colour(), self.get_map(), unit=unit)
        unitG.wrapped_lines = gamelogic.GameLogic.unit_full_string(unit, self.game_controller.get_chosen_site())
        text = f"{unit.name}\n {unit.nationality}\n {unitG.wrapped_lines[2]}"
        unitG.set_tip_text(text)
        self.units[id] = unitG
        self.map_view.add(unitG, layer=layernr)


    def change_unit_on_hex(self, first_gunit):
        qrs = first_gunit.unit.get_qrs()
        graph_list = self.game.get_board().get_hexes()[qrs].pawn_graph_list

        if len(graph_list) <= 1:
            return

        graph_list.append(graph_list.pop(0))

        if qrs in self.hex:

            l = len(graph_list) - 1

            for idx in range(len(graph_list) - 1, -1, -1):
                layernr = 10 + idx
                if idx > 0:
                    self.units[graph_list[idx]].position_x, self.units[graph_list[idx-1]].position_x = self.units[graph_list[idx-1]].position_x, self.units[graph_list[idx]].position_x
                    self.units[graph_list[idx]].position_y, self.units[graph_list[idx-1]].position_y = self.units[graph_list[idx-1]].position_y, self.units[graph_list[idx]].position_y
                    self.units[graph_list[idx]].rect.x = self.units[graph_list[idx]].get_position_x()
                    self.units[graph_list[idx]].rect.y = self.units[graph_list[idx]].get_position_y()
                    self.units[graph_list[idx-1]].rect.x = self.units[graph_list[idx-1]].get_position_x()
                    self.units[graph_list[idx-1]].rect.y = self.units[graph_list[idx-1]].get_position_y()

                sprite_id = graph_list[idx]
                unit_sprite = self.units[sprite_id]
                self.map_view.change_layer(unit_sprite, layernr)

                self.units[graph_list[idx]].set_dirty()
                if idx < l:
                    unit_sprite.set_visible(0)
                else:
                    unit_sprite.set_visible(1)

            max_line_width = self.screen.get_width() * 0.08
            play_handler.ToolTipHandler.on_hover_unit(button=self.units[graph_list[l]], get_tooltip=self.get_tooltip,
                                                             tool_x=self.units[graph_list[l]].get_position_x(), tool_y=self.units[graph_list[l]].get_position_y() - 75, max_line_width=max_line_width, play_obj=self)

    def add_reinforcement(self):
        max_line_width = self.screen.get_width() * 0.08
        tooltip_x = self.player_w_field.get_position_x() + 5
        unit_w = self.game.get_player_w_units()
        unit_s = self.game.get_player_s_units()

        width = (self.player_w_field.get_width() - 15) // 4
        height = width
        margin = 3
        quantity_in_row = int(self.player_w_field.get_width() // (width + margin))

        self.reinforcement = {}

        in_row = 0
        column = 0

        for unit in unit_w.values():
            if unit.get_stage_deploy() <= self.game_controller.get_akt_stage() and unit.get_deploy() == False:
                if in_row <= quantity_in_row:

                    position_x = self.player_w_field.get_position_x() + 3 + (width + margin) * in_row
                    position_y = self.player_w_photo.get_position_y() + self.player_w_photo.get_height() + 3 + (height + margin) * column
                    unit_g = control_obj.UnitGraph(
                        position_x, position_y, width, height, kolor.LIME,"",self.game_controller.get_default_font(),
                        int(height * 0.85 / 3), kolor.BLACK, partial(play_handler.PlayHandler.reinforcement_left_click,
                        play_obj=self, unit=unit), None, None, None,
                        partial(play_handler.ToolTipHandler.on_hover_reinforcement, get_tooltip=self.get_tooltip, tool_x=tooltip_x, tool_y=position_y - 75, max_line_width=max_line_width),
                        partial(play_handler.ToolTipHandler.un_hover_reinforcement, play_obj=self), unit.get_board_colour(), None, unit)
                    unit_g.wrapped_lines = gamelogic.GameLogic.unit_full_string(unit, self.game_controller.get_chosen_site())

                    text = f"{gamelogic.GameLogic.change_pot_name(unit, self.game_controller.get_chosen_site())}\n {unit.nationality}\n {unit_g.wrapped_lines[2]}"
                    unit_g.set_tip_text(text)
                    self.reinforcement[unit.id] = unit_g
                    in_row += 1
                    if in_row == quantity_in_row:
                        in_row = 0
                        column += 1

        in_row = 0
        column = 0
    
        for unit in unit_s.values():
            if unit.get_stage_deploy() <= self.game_controller.get_akt_stage() and unit.get_deploy() == False:
                if in_row <= quantity_in_row:
                    position_x = self.player_w_field.get_position_x() + 3 + (width + margin) * in_row
                    position_y = self.player_s_photo.get_position_y() + self.player_s_photo.get_height() + 3 + (height + margin) * column
                    unit_g = control_obj.UnitGraph(
                        position_x, position_y, width, height, kolor.REDJ,"", self.game_controller.get_default_font(),
                        int(height * 0.85 / 3), kolor.BLACK, partial(play_handler.PlayHandler.reinforcement_left_click,
                        play_obj=self, unit=unit), None, None, None,
                        partial(play_handler.ToolTipHandler.on_hover_reinforcement, get_tooltip=self.get_tooltip, tool_x=tooltip_x, tool_y=position_y - 85, max_line_width=max_line_width),
                        partial(play_handler.ToolTipHandler.un_hover_reinforcement, play_obj=self), unit.get_board_colour(), None, unit)
                    unit_g.wrapped_lines = gamelogic.GameLogic.unit_full_string(unit, self.game_controller.get_chosen_site())
                    text = f"{unit.name}\n {unit.nationality}\n {unit_g.wrapped_lines[2]}"
                    unit_g.set_tip_text(text)
                    self.reinforcement[unit.id] = unit_g
                    in_row += 1
                    if in_row == quantity_in_row:
                        in_row = 0
                        column += 1


    def set_all_dirty(self):
        for sprite in self.left_menu_graphics:
            sprite.set_dirty()
        self.set_right_menu_dirty()
        for sprite in self.map_view:
            sprite.set_dirty()

    def set_right_menu_dirty(self):
        for sprite in self.right_menu_graphics.sprites():
            sprite.set_dirty()
        for sprite in self.manage_graphics.sprites():
            sprite.set_dirty()
        for sprite in self.stage_phaze_graphics.sprites():
            sprite.set_dirty()

    
    def render(self, mouse_position):
        all_dirty_rects = []

        self.map_view.update(mouse_position)
        for sprite in self.map_view:
            if sprite.dirty:
                sprite.draw(self.screen.get_screen())
                all_dirty_rects.append(sprite.rect.copy())

        self.left_menu_graphics.update(mouse_position)
        dirty_rects = self.left_menu_graphics.draw(self.screen.get_screen())
        all_dirty_rects.extend(dirty_rects)

        self.right_menu_graphics.update(mouse_position)
        dirty_rects = self.right_menu_graphics.draw(self.screen.get_screen())
        all_dirty_rects.extend(dirty_rects)

        self.manage_graphics.update(mouse_position)
        dirty_rects = self.manage_graphics.draw(self.screen.get_screen())
        all_dirty_rects.extend(dirty_rects)

        self.stage_phaze_graphics.update(mouse_position)
        dirty_rects = self.stage_phaze_graphics.draw(self.screen.get_screen())
        all_dirty_rects.extend(dirty_rects)

        self.tooltip_graphics.update(mouse_position)
        dirty_rects = self.tooltip_graphics.draw(self.screen.get_screen())
        all_dirty_rects.extend(dirty_rects)

        if all_dirty_rects:
            pygame.display.update(all_dirty_rects)


    def get_camera(self):
        return self.camera

    def get_hex_size(self):
        return self.hex_size

    def get_hexes(self):
        return self.hex

    def get_map(self):
        return self.map

    def get_tooltip(self):
        return self.tooltip

    def get_game(self):
        return self.game


    def get_visible_hexagons(self, map_area, camera, hexes):
       
        visible_hexes = {}

        view_left   = map_area.get_position_x()
        view_top    = map_area.get_position_y()
        view_right  = view_left + map_area.get_width()
        view_bottom = view_top  + map_area.get_height()

        scale = camera.get_camera_scale()
        screen_hex_radius = self.base_hex_size * scale

        for pos, hex_obj in hexes.items():
            q, r, s = pos

            wx, wy = self._hex_to_world_center(q, r, s)
            sx, sy = self._world_to_screen(wx, wy)

            hex_left   = sx - screen_hex_radius
            hex_right  = sx + screen_hex_radius
            hex_top    = sy - screen_hex_radius
            hex_bottom = sy + screen_hex_radius

            if (hex_right >= view_left and hex_left <= view_right and
                hex_bottom >= view_top and hex_top <= view_bottom):

                clip_info = {
                    'clip_left':   hex_left   < view_left,
                    'clip_right':  hex_right  > view_right,
                    'clip_top':    hex_top    < view_top,
                    'clip_bottom': hex_bottom > view_bottom,
                }
                clip_info['fully_visible'] = not (
                    clip_info['clip_left'] or clip_info['clip_right'] or
                    clip_info['clip_top']  or clip_info['clip_bottom']
                )

                if not clip_info['fully_visible']:
                    clip_info['clip_rect'] = {
                        'left':   max(int(hex_left),   view_left),
                        'right':  min(int(hex_right),  view_right),
                        'top':    max(int(hex_top),    view_top),
                        'bottom': min(int(hex_bottom), view_bottom),
                    }

                visible_hexes[pos] = {
                    'hex_obj':   hex_obj,
                    'pixel_pos': hexagon.Point(sx, sy),
                    'world_pos': hexagon.Point(wx, wy),
                    'clip_info': clip_info,
                }

        return visible_hexes

   
    def _clamp_camera(self):
        cam = self.camera
        if cam.get_camera_x() < cam.get_min_x():
            cam.set_camera_x(cam.get_min_x())
        elif cam.get_camera_x() > cam.get_max_x():
            cam.set_camera_x(cam.get_max_x())
        if cam.get_camera_y() < cam.get_min_y():
            cam.set_camera_y(cam.get_min_y())
        elif cam.get_camera_y() > cam.get_max_y():
            cam.set_camera_y(cam.get_max_y())


    def handle_event(self, mouse_position, event):
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_click_time < self.click_cooldown:
                return
            self.last_click_time = current_time
            if event.button == 1:
                self.mouse_dragging = True
                self.last_mouse_pos = mouse_position
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.mouse_dragging = False
                self.last_mouse_pos = None

        self.zoom_in_button.handle_event(mouse_position, event)
        self.zoom_out_button.handle_event(mouse_position, event)
        self.map.handle_event(mouse_position, event)
        self.tooltip.handle_event(mouse_position, event)
        self.action_button.handle_event(mouse_position, event)
        for unitG in self.reinforcement.values():
            unitG.handle_event(mouse_position, event)
        for unitG in self.units.values():
            unitG.handle_event(mouse_position, event)
        for hexG in self.hex.values():
            hexG.handle_event(mouse_position, event)


    def handle_mouse_motion(self, mouse_position, event):
        if not (self.mouse_dragging and self.last_mouse_pos):
            return

        dx = mouse_position[0] - self.last_mouse_pos[0]
        dy = mouse_position[1] - self.last_mouse_pos[1]

        drag_factor = 1.0 / self.camera.get_camera_scale()
        camx = self.camera.get_camera_x()
        camy = self.camera.get_camera_y()

        camx -= dx * drag_factor
        camy -= dy * drag_factor

        self.camera.set_camera_x(camx)
        self.camera.set_camera_y(camy)
      #  self._clamp_camera()
        self.set_map_view()

        self.last_mouse_pos = mouse_position


    def update_movement(self, keys):
        moved = False
        spd = self.camera.get_camera_speed()
        camx = self.camera.get_camera_x()
        camy = self.camera.get_camera_y()

        if keys[pygame.K_LEFT]:
            camx -= spd
            moved = True
        if keys[pygame.K_RIGHT]:
            camx += spd
            moved = True
        if keys[pygame.K_UP]:
            camy -= spd
            moved = True
        if keys[pygame.K_DOWN]:
            camy += spd
            moved = True

        if moved:
            self.camera.set_camera_x(camx)
            self.camera.set_camera_y(camy)
         #   self._clamp_camera()
            self.set_map_view()
            play_handler.Refresh.refresh_right(play_obj=self)


    def handle_keyboard_event(self, mouse_position, event):
            if event.key == pygame.K_ESCAPE:
                self.connection.close_connection()
                pygame.quit()
                quit()
            if event.key == pygame.K_c:
                for qrs, hex_sprite in self.hex.items():
                    if hex_sprite.rect.collidepoint(mouse_position):
                        if self.game.get_board().get_hexes()[qrs].pawn_graph_list:

                            first_unit_id = self.game.get_board().get_hexes()[qrs].pawn_graph_list[0]
                            unit = self.units[first_unit_id]
                    
                            self.change_unit_on_hex(unit)

                        break
