#-*-coding:utf-8;-*-
from ctypes import cast,c_void_p,POINTER
from typing import Tuple,Union
from .core import LIBRARY,hackrf_device_list_t
from .const import hackrf_error,hackrf_board_id,hackrf_board_rev,hackrf_usb_board_id,rf_path_filter
hackrf_init=LIBRARY.hackrf_init
hackrf_exit=LIBRARY.hackrf_exit
hackrf_library_version=LIBRARY.hackrf_library_version
hackrf_library_release=LIBRARY.hackrf_library_release
def hackrf_device_list()->Tuple[Union[int,None],dict]:
    real_hackrf_device_list=LIBRARY.hackrf_device_list()
    return cast(real_hackrf_device_list,c_void_p).value,{
        "serial_numbers":(*real_hackrf_device_list.contents.serial_numbers[:real_hackrf_device_list.contents.devicecount],),
        "usb_board_ids":(*(hackrf_usb_board_id(i) for i in real_hackrf_device_list.contents.usb_board_ids[:real_hackrf_device_list.contents.devicecount]),),
        "usb_device_index":(*real_hackrf_device_list.contents.usb_device_index[:real_hackrf_device_list.contents.devicecount],)
    }
def hackrf_device_list_free(list:Union[int,None])->None:
    LIBRARY.hackrf_device_list_free(cast(c_void_p(list),POINTER(hackrf_device_list_t)))
def hackrf_error_name(errcode:hackrf_error)->bytes:
    return LIBRARY.hackrf_error_name(errcode.value)
def hackrf_board_id_name(board_id:hackrf_board_id)->bytes:
    return LIBRARY.hackrf_board_id_name(board_id.value)
def hackrf_board_id_platform(board_id:hackrf_board_id)->int:
    return LIBRARY.hackrf_board_id_platform(board_id.value)
def hackrf_usb_board_id_name(usb_board_id:hackrf_usb_board_id)->bytes:
    return LIBRARY.hackrf_usb_board_id_name(usb_board_id.value)
def hackrf_filter_path_name(path:rf_path_filter)->bytes:
    return LIBRARY.hackrf_filter_path_name(path.value)
hackrf_compute_baseband_filter_bw_round_down_lt=LIBRARY.hackrf_compute_baseband_filter_bw_round_down_lt
hackrf_compute_baseband_filter_bw=LIBRARY.hackrf_compute_baseband_filter_bw
def hackrf_board_rev_name(board_rev:hackrf_board_rev)->bytes:
    return LIBRARY.hackrf_board_rev_name(board_rev.value)