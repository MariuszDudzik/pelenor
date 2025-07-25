
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
    def on_hover(button):
        button.colour = kolor.RGREY

    @staticmethod
    def un_hover(button):
        button.colour = kolor.GREY


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
    def action_left_click(play_obj, mouse_position=None):
        phaze = play_obj.game_controller.get_akt_phaze()
        stage = play_obj.game_controller.get_akt_stage()
        site = play_obj.game_controller.get_chosen_site()
        if gamelogic.GameLogic.check_right_player(site, play_obj.game_controller.get_akt_player()):
            if phaze == 0:
                PlayHandler.action_phaze_0(play_obj, site, stage, phaze)
                
        else:
            PlayHandler.show_message(play_obj, 20)


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
        unit_id = unit.get_id()

        gc = play_obj.game_controller
        side = gc.get_chosen_site()

        if not gamelogic.GameLogic.check_right_player(gc.get_akt_player(), side):
            return
        if not gamelogic.GameLogic.check_right_player(unit.get_site(), side):
            return

        chosen_unit_id = gc.get_unit_id()

        if chosen_unit_id == unit_id:
            PlayHandler.clear_unit_selection(play_obj, 'R', unit_id, side)
            return

        if chosen_unit_id is None:
            qrs = None
            PlayHandler.select_unit(play_obj, unit_id, side, qrs, 'R')
        else:
            if gc.get_unit_hex() is not None:
                return
            else:
                PlayHandler.change_unit_outline_colour(play_obj, 'R', kolor.BLACK, chosen_unit_id, side)
                gc.set_unit_id(unit_id, 'R', None)
                PlayHandler.change_unit_outline_colour(play_obj, 'R', kolor.GOLD, unit_id, side)
                play_obj.tooltip.set_dirty()


    @staticmethod
    def change_unit_outline_colour(play_obj, flag, colour, unit_id, side):
        if side == 'Z':
            play_obj.game.player_w.units[unit_id].set_board_colour(colour)
        elif side == 'C':
            play_obj.game.player_s.units[unit_id].set_board_colour(colour)
        
        if flag == 'R':
            play_obj.reinforcement[unit_id].set_board_colour(colour)
            play_obj.reinforcement[unit_id].set_dirty()
        elif flag == 'U':
            play_obj.units[unit_id].set_board_colour(colour)
            play_obj.units[unit_id].set_dirty()
  

    @staticmethod
    def show_message(play_obj, msg):
        play_obj.set_message(dictionary.message[msg])
        play_obj.message_field.set_dirty()


    @staticmethod
    def clear_unit_selection(play_obj, flag, unit_id, site):
        color = kolor.PURPLE if gamelogic.GameLogic.get_unit_distracted(unit_id, play_obj.get_game().get_player_w(), play_obj.get_game().get_player_s()) else kolor.BLACK
        PlayHandler.change_unit_outline_colour(play_obj, flag, color, unit_id, site)
        play_obj.game_controller.set_unit_id(None, None, None)
        play_obj.game_controller.set_unit_to_move(None)


    @staticmethod
    def select_unit(play_obj, unit_id, site, qrs, flag):
        play_obj.game_controller.set_unit_id(unit_id, flag, qrs)
        PlayHandler.change_unit_outline_colour(play_obj, flag, kolor.GOLD, unit_id, site)
        play_obj.tooltip.set_dirty()


    @staticmethod
    def hex_left_click(play_obj, hex_obj, mouse_position):
        if play_obj.game_controller.get_enabled():
            site = play_obj.game_controller.get_chosen_site()
            if gamelogic.GameLogic.check_right_player(site, play_obj.game_controller.get_akt_player()):
                stage = play_obj.game_controller.get_akt_stage()
                phaze = play_obj.game_controller.get_akt_phaze()
                unit_id = play_obj.game_controller.get_unit_id()
                flag = play_obj.game_controller.get_unit_flag()
                unit_qrs = play_obj.game_controller.get_unit_hex()
                qrs = tuple(hex_obj.get_qrs())
                board = play_obj.get_game().get_board()
                player_1 = play_obj.get_game().get_player_w()
                player_2 = play_obj.get_game().get_player_s()
            
                if phaze == 0:
                    PlayHandler.hex_phaze_0_left_click(play_obj, hex_obj, site, stage, phaze, unit_id, flag, qrs, unit_qrs, board, player_1, player_2)


    @staticmethod
    def hex_phaze_0_left_click(play_obj, hex_obj, site, stage, phaze, unit_id, flag, qrs, unit_qrs, board, player_1, player_2):
        try:
            if unit_id is not None:
                if flag in ['R', 'U']:
                    check, msg = gamelogic.GameLogic.base_deploy(unit_id, site, qrs, phaze, board, player_1, player_2)
                    if check and flag == 'U' and qrs != unit_qrs:
                        check, msg = gamelogic.GameLogic.check_commander_not_alone(unit_id, unit_qrs, board, player_1, player_2, msg)
                        if check and site == 'Z':
                            check, msg = gamelogic.GameLogic.check_palace_gward(unit_id, board, player_1, player_2, msg)
                    if check:
                        PlayHandler.show_message(play_obj, 10)
                        play_obj.connection.msg_t_server.deploy(
                            play_obj.game_controller.get_session_id(),
                            play_obj.connection.get_socket(),
                            site, stage, phaze, unit_id, qrs, flag
                        )
                        PlayHandler.clear_unit_selection(play_obj, flag, unit_id, site)
                    else:
                        PlayHandler.show_message(play_obj, msg)

            else:
                if hex_obj.get_pawn_list():
                    unit_hex = play_obj.game.board.hexes[qrs].pawn_graph_list[-1]
                    unit_site = gamelogic.GameLogic.get_unit_site(unit_hex, player_1, player_2)

                    if gamelogic.GameLogic.check_right_player(unit_site, site):
                        PlayHandler.select_unit(play_obj, unit_hex, site, qrs, 'U')

        except Exception as e:
            PlayHandler.clear_unit_selection(play_obj, flag, unit_id, site)
 

    @staticmethod
    def action_phaze_0(play_obj, site, stage, phaze):
        deployed = True
        if play_obj.game_controller.get_deploy():
            units = gamelogic.GameLogic.get_units_for_player(site, play_obj.game.get_player_w(), play_obj.game.get_player_s())
            for unit in units.values():
                if unit.get_stage_deploy() <= stage and unit.get_deploy() == False:
                    deployed = False
                    break
        if deployed:
            PlayHandler.show_message(play_obj, 10)
            play_obj.connection.msg_t_server.end_turn(play_obj.game_controller.get_session_id(), play_obj.connection.get_socket(), site, stage, phaze)
        else:
            PlayHandler.show_message(play_obj, 21)