
import kolor
import pygame
import gamelogic
import hexagon
import dictionary


class ZoomHandler(object):
   
    @staticmethod
    def handle_in(get_camera, play_obj, mouse_position=None):
        camera = get_camera()
        if camera.get_camera_scale() <= camera.get_max_scale():
            camera.set_camera_scale(camera.get_camera_scale() + camera.get_zoom_speed())
            play_obj.set_hex_base_size()
            play_obj.set_map_view()

    @staticmethod
    def handle_out(get_camera, play_obj, mouse_position=None):
        camera = get_camera()
        if camera.get_camera_scale() > camera.get_min_scale():
            camera.set_camera_scale(camera.get_camera_scale() - camera.get_zoom_speed())
            play_obj.set_hex_base_size()
            play_obj.set_map_view()


    @staticmethod
    def on_hover(button):
        button.colour = kolor.RGREY

    @staticmethod
    def un_hover(button):
        button.colour = kolor.GREY


class ToolTipHandler(object):

    @staticmethod
    def on_hover(button, get_tooltip, tool_x, tool_y, max_line_width):
        tooltip = get_tooltip()
        tooltip.set_position_x(tool_x)
        tooltip.set_position_y(tool_y)
        text = button.get_tip_text()
        tooltip.set_text_wrapped(text, max_line_width)


    @staticmethod
    def un_hover(button, play_obj):

        play_obj.map.set_dirty()
        for hex_obj in play_obj.hex.values():
            hex_obj.set_dirty()
        for unit in play_obj.units.values():
            unit.set_dirty()
        #Refresh.refresh_under_tooltip(play_obj)

    @staticmethod
    def on_hover_reinforcement(button, get_tooltip, tool_x, tool_y, max_line_width):
        if button.unit.get_site() == 'Z':
            button.set_colour(kolor.RLIME)
        elif button.unit.get_site() == 'C':
            button.set_colour(kolor.RREDJ)
        ToolTipHandler.on_hover(button, get_tooltip, tool_x, tool_y, max_line_width)


    @staticmethod
    def un_hover_reinforcement(button, play_obj):
        if button.unit.get_site() == 'Z':
            button.set_colour(kolor.LIME)
        elif button.unit.get_site() == 'C':
            button.set_colour(kolor.REDJ)
        for sprite in play_obj.left_menu_graphics.sprites():
            sprite.set_dirty()


    @staticmethod
    def on_hover_unit(button, get_tooltip, tool_x, tool_y, max_line_width, play_obj):
        qrs = button.unit.get_qrs()
        unit_list = play_obj.game.board.hexes[qrs].pawn_graph_list
        l = len(unit_list) - 1
        for idx, id in enumerate(unit_list):
            if idx < l:
                play_obj.units[id].set_visible(0)

        if button.unit.get_site() == 'Z':
            button.set_colour(kolor.RLIME)
        elif button.unit.get_site() == 'C':
            button.set_colour(kolor.RREDJ)
        play_obj.units[unit_list[l]].set_dirty()
        if tool_x > play_obj.map.get_position_x() and tool_x + max_line_width + 4 < play_obj.map.get_position_x() + play_obj.map.get_width():
            ToolTipHandler.on_hover(play_obj.units[unit_list[l]], get_tooltip, tool_x, tool_y, max_line_width)


    @staticmethod
    def un_hover_unit(button, play_obj):
        if button.unit.get_site() == 'Z':
            button.set_colour(kolor.LIME)
        elif button.unit.get_site() == 'C':
            button.set_colour(kolor.REDJ)
        qrs = button.unit.get_qrs()
        unit_list = play_obj.game.board.hexes[qrs].pawn_graph_list
        for idx, id in enumerate(unit_list):
                play_obj.units[id].set_visible(1)
        Refresh.refresh_under_tooltip(play_obj)
        for sprite in play_obj.map_view.sprites():
            sprite.set_dirty()
        # Refresh.refreshRight(play_obj)


class Refresh(object):

    @staticmethod
    def refresh_login(play_obj):
        play_obj.player_w_login.set_text(play_obj.game.player_w.login)
        play_obj.player_s_login.set_text(play_obj.game.player_s.login)
        play_obj.player_w_login.set_dirty()
        play_obj.player_s_login.set_dirty()

    @staticmethod
    def refresh_right(play_obj):
        x = play_obj.tooltip.get_position_x() + play_obj.tooltip.get_width()
        x2 = play_obj.state_field.get_position_x()
        if x >= x2:
            play_obj.set_right_menu_dirty()


    @staticmethod
    def refresh_under_tooltip(play_obj):
        tooltip_rect = play_obj.get_tooltip().get_rect()
        for hit_hex in PlayHandler.get_hexes_under_rect(tooltip_rect, play_obj.hex):
            play_obj.hex[hit_hex].set_dirty()
            Refresh.refresh_unit_graphics_list(play_obj, hit_hex)


    @staticmethod
    def refresh_unit_graphics_list(play_obj, qrs):
        for unit in play_obj.game.board.hexes[qrs].pawn_graph_list:
            play_obj.units[unit].set_dirty()


class PlayHandler(object):

    @staticmethod
    def get_hexes_under_rect(rect, hex_graphics_dict, sampling_step=5):
        
        hit_hexes = set()

        for x in range(rect.left, rect.right, sampling_step):
            for y in range(rect.top, rect.bottom, sampling_step):
                for hex_pos, hex_sprite in hex_graphics_dict.items():
                    if hex_sprite.rect.collidepoint(x, y):
                        hit_hexes.add(hex_pos)
        return hit_hexes
    

    @staticmethod
    def change_hex_colour(play_obj, flag, matching):
        for qrs in matching:
            Lhex = play_obj.game.board.hexes[tuple(qrs)]
            Lhex.set_colour_flag(flag)
            if qrs in play_obj.hex:
                hex_tile = play_obj.hex[qrs]
                colour = Lhex.get_colour() if flag else Lhex.get_dark_colour()
                hex_tile.set_fill_colour(kolor.colour_hex.get(colour))
                hex_tile.set_dirty()
                Refresh.refresh_unit_graphics_list(play_obj, qrs)


    @staticmethod
    def change_hex_colour_handler(play_obj, flag, site, stage):
        
        if stage == 0 and site == 'C':
            matching = gamelogic.GameLogic.get_matching_coords(play_obj.game.board.hexes, gamelogic.GameLogic.deploy0_right_hex_S)
        elif stage == 0 and site == 'Z':
            matching = gamelogic.GameLogic.get_matching_coords(play_obj.game.board.hexes, gamelogic.GameLogic.deploy0_right_hex_W)
        else:
            return

        PlayHandler.change_hex_colour(play_obj, flag, matching)


    @staticmethod
    def reinforcement_left_click(play_obj, unit, mouse_position):
        if gamelogic.GameLogic.check_right_player(play_obj.game_controller.get_akt_player(), play_obj.game_controller.get_choosed_site()):
            if gamelogic.GameLogic.check_right_player(unit.get_site(), play_obj.game_controller.get_choosed_site()):
                id = unit.get_id()

                if play_obj.game_controller.get_unit_id() == id:
                    play_obj.game_controller.set_unit_id(None)
                    play_obj.game_controller.set_unit_to_move(None)
                    if not unit.get_distracted():
                        PlayHandler.change_unit_outline_colour(play_obj, 'R', kolor.BLACK, id)
                    else:
                        PlayHandler.change_unit_outline_colour(play_obj, 'R', kolor.PURPLE, id)
                else:
                    if play_obj.game_controller.get_unit_id() == None:
                        play_obj.game_controller.set_unit_id(id)

                        PlayHandler.change_unit_outline_colour(play_obj, 'R', kolor.GOLD, id)
                    else:
                        PlayHandler.change_unit_outline_colour(play_obj, 'R', kolor.BLACK, play_obj.game_controller.get_unit_id())
                        play_obj.game_controller.set_unit_id(id)
                        PlayHandler.change_unit_outline_colour(play_obj, 'R', kolor.GOLD, id)
                        play_obj.tooltip.set_dirty()


    @staticmethod
    def change_unit_outline_colour(play_obj, flag, colour, id):
        if flag == 'R':
            play_obj.reinforcement[id].set_board_colour(colour)
            play_obj.reinforcement[id].set_dirty()
        elif flag == 'U':
            play_obj.unit[id].set_board_colour(colour)
            play_obj.unit[id].set_dirty()

    
    @staticmethod
    def hex_left_click(play_obj, hex_obj, mouse_position):
        site = play_obj.game_controller.get_choosed_site()
        if gamelogic.GameLogic.check_right_player(site, play_obj.game_controller.get_akt_player()):
            stage = play_obj.game_controller.get_akt_stage()
            phaze = play_obj.game_controller.get_akt_phaze()
          #  flag = play_obj.game_controller.get_unit_flag()
            unit_id = play_obj.game_controller.get_unit_id()
            qrs = tuple(hex_obj.get_qrs())
            terrain = hex_obj.get_terrain_sign()
            board = play_obj.get_game().get_board()

            if phaze == 0:
                if gamelogic.GameLogic.base_deploy(unit_id, site, qrs, terrain, phaze, board, 'c', play_obj.get_game()):
                    play_obj.connection.msg_t_server.deploy(play_obj.game_controller.get_session_id(), play_obj.connection.get_socket(), site, stage, phaze, unit_id, qrs)
                    PlayHandler.change_unit_outline_colour(play_obj, 'R', kolor.BLACK, unit_id)
                    play_obj.game_controller.set_unit_id(None)
                    play_obj.game_controller.set_unit_to_move(None)
                    play_obj.game_controller.set_unit_flag(None)

    