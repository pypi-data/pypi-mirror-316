#-*-coding:utf-8;-*-
from ctypes import byref,cast,c_char_p,c_int,c_ubyte,c_uint16,c_uint32,c_uint8,c_void_p,POINTER
from math import floor
from typing import Callable,Tuple,Union
from numpy import uint8
from numpy.ctypeslib import as_array
from numpy.typing import NDArray
from .core import LIBRARY,read_partid_serialno_t,hackrf_operacake_dwell_time,hackrf_operacake_freq_range,hackrf_bias_t_user_settting_req,hackrf_m0_state,hackrf_device_list_t,hackrf_sample_block_cb_fn,hackrf_tx_block_complete_cb_fn,hackrf_flush_cb_fn
from .const import hackrf_error,hackrf_board_rev,rf_path_filter,operacake_switching_mode,sweep_style,HACKRF_OPERACAKE_ADDRESS_INVALID,HACKRF_OPERACAKE_MAX_BOARDS
def hackrf_device_list_open(list:Union[int,None],idx:int)->Tuple[int,Union[int,None]]:
    device=c_void_p()
    returnCode=LIBRARY.hackrf_device_list_open(cast(c_void_p(list),POINTER(hackrf_device_list_t)),idx,byref(device))
    if returnCode==hackrf_error.HACKRF_SUCCESS.value:
        return returnCode,device.value
    else:
        return returnCode,None
def hackrf_open()->Tuple[int,Union[int,None]]:
    device=c_void_p()
    returnCode=LIBRARY.hackrf_open(byref(device))
    if returnCode==hackrf_error.HACKRF_SUCCESS.value:
        return returnCode,device.value
    else:
        return returnCode,None
def hackrf_open_by_serial(desired_serial_number:bytes)->Tuple[int,Union[int,None]]:
    device=c_void_p()
    returnCode=LIBRARY.hackrf_open_by_serial(desired_serial_number,byref(device))
    if returnCode==hackrf_error.HACKRF_SUCCESS.value:
        return returnCode,device.value
    else:
        return returnCode,None
hackrf_close=LIBRARY.hackrf_close
def hackrf_start_rx(device:Union[int,None],rx_ctx:Union[int,None])->Callable[[Callable[[Union[int,None],NDArray[uint8],Union[int,None]],int]],Union[hackrf_sample_block_cb_fn,None]]:
    def real_hackrf_start_rx(callback:Callable[[Union[int,None],NDArray[uint8],Union[int,None]],int])->Union[hackrf_sample_block_cb_fn,None]:
        real_callback=hackrf_sample_block_cb_fn(lambda transfer:callback(transfer.contents.device,as_array(transfer.contents.buffer,(transfer.contents.valid_length,)),transfer.contents.rx_ctx))
        if LIBRARY.hackrf_start_rx(device,real_callback,rx_ctx)==hackrf_error.HACKRF_SUCCESS.value:
            return real_callback
    return real_hackrf_start_rx
hackrf_stop_rx=LIBRARY.hackrf_stop_rx
def hackrf_start_tx(device:Union[int,None],tx_ctx:Union[int,None])->Callable[[Callable[[Union[int,None],NDArray[uint8],Union[int,None]],Tuple[int,int]]],Union[hackrf_sample_block_cb_fn,None]]:
    def real_hackrf_start_tx(callback:Callable[[Union[int,None],NDArray[uint8],Union[int,None]],Tuple[int,int]])->Union[hackrf_sample_block_cb_fn,None]:
        @hackrf_sample_block_cb_fn
        def real_callback(transfer):
            real_hackrf_sample_block_cb_fn,valid_length=callback(transfer.contents.device,as_array(transfer.contents.buffer,(transfer.contents.buffer_length,)),transfer.contents.tx_ctx)
            transfer.contents.valid_length=valid_length
            return real_hackrf_sample_block_cb_fn
        if LIBRARY.hackrf_start_tx(device,real_callback,tx_ctx)==hackrf_error.HACKRF_SUCCESS.value:
            return real_callback
    return real_hackrf_start_tx
def hackrf_set_tx_block_complete_callback(device:Union[int,None])->Callable[[Callable[[Union[int,None],NDArray[uint8],int,Union[int,None],int],None]],Union[hackrf_tx_block_complete_cb_fn,None]]:
    def real_hackrf_set_tx_block_complete_callback(callback:Callable[[Union[int,None],NDArray[uint8],int,Union[int,None],int],None])->Union[hackrf_tx_block_complete_cb_fn,None]:
        real_callback=hackrf_tx_block_complete_cb_fn(lambda transfer,success:callback(transfer.contents.device,as_array(transfer.contents.buffer,(transfer.contents.buffer_length,)),transfer.contents.valid_length,transfer.contents.tx_ctx,success))
        if LIBRARY.hackrf_set_tx_block_complete_callback(device,real_callback)==hackrf_error.HACKRF_SUCCESS.value:
            return real_callback
    return real_hackrf_set_tx_block_complete_callback
def hackrf_enable_tx_flush(device:Union[int,None],flush_ctx:Union[int,None])->Callable[[Callable[[Union[int,None],int],None]],Tuple[hackrf_flush_cb_fn,None]]:
    def real_hackrf_enable_tx_flush(callback:Callable[[Union[int,None],int],None])->Tuple[hackrf_flush_cb_fn,None]:
        real_callback=hackrf_flush_cb_fn(callback)
        if LIBRARY.hackrf_enable_tx_flush(device,real_callback,flush_ctx)==hackrf_error.HACKRF_SUCCESS.value:
            return real_callback
    return real_hackrf_enable_tx_flush
hackrf_stop_tx=LIBRARY.hackrf_stop_tx
def hackrf_get_m0_state(device:Union[int,None])->Tuple[int,dict]:
    value=hackrf_m0_state()
    returnCode=LIBRARY.hackrf_get_m0_state(device,byref(value))
    if returnCode==hackrf_error.HACKRF_SUCCESS.value:
        return returnCode,{
            "requested_mode":value.requested_mode,
            "request_flag":value.request_flag,
            "active_mode":value.active_mode,
            "m0_count":value.m0_count,
            "m4_count":value.m4_count,
            "num_shortfalls":value.num_shortfalls,
            "longest_shortfall":value.longest_shortfall,
            "shortfall_limit":value.shortfall_limit,
            "threshold":value.threshold,
            "next_mode":value.next_mode,
            "error":value.error
        }
    else:
        return returnCode,{}
hackrf_set_tx_underrun_limit=LIBRARY.hackrf_set_tx_underrun_limit
hackrf_set_rx_overrun_limit=LIBRARY.hackrf_set_rx_overrun_limit
hackrf_is_streaming=LIBRARY.hackrf_is_streaming
def hackrf_max2837_read(device:Union[int,None],register_number:int)->Tuple[int,int]:
    value=c_uint16()
    returnCode=LIBRARY.hackrf_max2837_read(device,register_number,byref(value))
    if returnCode==hackrf_error.HACKRF_SUCCESS.value:
        return returnCode,value.value
    else:
        return returnCode,-1
hackrf_max2837_write=LIBRARY.hackrf_max2837_write
def hackrf_si5351c_read(device:Union[int,None],register_number:int)->Tuple[int,int]:
    value=c_uint16()
    returnCode=LIBRARY.hackrf_si5351c_read(device,register_number,byref(value))
    if returnCode==hackrf_error.HACKRF_SUCCESS.value:
        return returnCode,value.value
    else:
        return returnCode,-1
hackrf_si5351c_write=LIBRARY.hackrf_si5351c_write
hackrf_set_baseband_filter_bandwidth=LIBRARY.hackrf_set_baseband_filter_bandwidth
def hackrf_rffc5071_read(device:Union[int,None],register_number:int)->Tuple[int,int]:
    value=c_uint16()
    returnCode=LIBRARY.hackrf_rffc5071_read(device,register_number,byref(value))
    if returnCode==hackrf_error.HACKRF_SUCCESS.value:
        return returnCode,value.value
    else:
        return returnCode,-1
hackrf_rffc5071_write=LIBRARY.hackrf_rffc5071_write
hackrf_spiflash_erase=LIBRARY.hackrf_spiflash_erase
def hackrf_spiflash_write(device:Union[int,None],address:int,data:bytes)->int:
    return LIBRARY.hackrf_spiflash_write(device,address,len(data),cast((c_ubyte*len(data))(*data),POINTER(c_ubyte)))
def hackrf_spiflash_read(device:Union[int,None],address:int,length:int)->Tuple[int,bytes]:
    data=(c_ubyte*length)()
    returnCode=LIBRARY.hackrf_spiflash_read(device,address,length,cast(data,POINTER(c_ubyte)))
    if returnCode==hackrf_error.HACKRF_SUCCESS.value:
        return returnCode,bytes(data[:])
    else:
        return returnCode,b""
def hackrf_spiflash_status(device:Union[int,None])->Tuple[int,Tuple[int,...]]:
    data=(c_uint8*2)()
    returnCode=LIBRARY.hackrf_spiflash_status(device,cast(data,POINTER(c_uint8)))
    if returnCode==hackrf_error.HACKRF_SUCCESS.value:
        return returnCode,(*data[:],)
    else:
        return returnCode,()
hackrf_spiflash_clear_status=LIBRARY.hackrf_spiflash_clear_status
def hackrf_cpld_write(device:Union[int,None],data:bytes)->int:
    return LIBRARY.hackrf_cpld_write(device,cast((c_ubyte*len(data))(*data),POINTER(c_ubyte)),len(data))
def hackrf_board_id_read(device:Union[int,None])->Tuple[int,int]:
    value=c_uint8()
    returnCode=LIBRARY.hackrf_board_id_read(device,byref(value))
    if returnCode==hackrf_error.HACKRF_SUCCESS.value:
        return returnCode,value.value
    else:
        return returnCode,-1
def hackrf_version_string_read(device:Union[int,None],length:int)->Tuple[int,bytes]:
    version=c_char_p(b"\x00"*length)
    returnCode=LIBRARY.hackrf_version_string_read(device,version,length)
    if returnCode==hackrf_error.HACKRF_SUCCESS.value:
        return returnCode,version.value
    else:
        return returnCode,b""
def hackrf_usb_api_version_read(device:Union[int,None])->Tuple[int,int]:
    version=c_uint16()
    returnCode=LIBRARY.hackrf_usb_api_version_read(device,byref(version))
    if returnCode==hackrf_error.HACKRF_SUCCESS.value:
        return returnCode,version.value
    else:
        return returnCode,-1
hackrf_set_freq=LIBRARY.hackrf_set_freq
def hackrf_set_freq_explicit(device:Union[int,None],if_freq_hz:int,lo_freq_hz:int,path:rf_path_filter)->int:
    return LIBRARY.hackrf_set_freq_explicit(device,if_freq_hz,lo_freq_hz,path.value)
hackrf_set_sample_rate_manual=LIBRARY.hackrf_set_sample_rate_manual
hackrf_set_sample_rate=LIBRARY.hackrf_set_sample_rate
hackrf_set_amp_enable=LIBRARY.hackrf_set_amp_enable
def hackrf_board_partid_serialno_read(device:Union[int,None])->Tuple[int,dict]:
    read_partid_serialno=read_partid_serialno_t()
    returnCode=LIBRARY.hackrf_board_partid_serialno_read(device,byref(read_partid_serialno))
    if returnCode==hackrf_error.HACKRF_SUCCESS.value:
        return returnCode,{
            "part_id":(*read_partid_serialno.part_id[:],),
            "serial_no":(*read_partid_serialno.serial_no[:],)
        }
    else:
        return returnCode,{}
hackrf_set_lna_gain=LIBRARY.hackrf_set_lna_gain
hackrf_set_vga_gain=LIBRARY.hackrf_set_vga_gain
hackrf_set_txvga_gain=LIBRARY.hackrf_set_txvga_gain
hackrf_set_antenna_enable=LIBRARY.hackrf_set_antenna_enable
hackrf_set_hw_sync_mode=LIBRARY.hackrf_set_hw_sync_mode
def hackrf_init_sweep(device:Union[int,None],frequency_list:Tuple[int,...],num_bytes:int,step_width:int,offset:int,style:sweep_style)->int:
    num_ranges=floor(len(frequency_list)/2)
    real_num_ranges=num_ranges*2
    return LIBRARY.hackrf_init_sweep(device,cast((c_uint16*real_num_ranges)(*frequency_list[:real_num_ranges]),POINTER(c_uint16)),num_ranges,num_bytes,step_width,offset,style.value)
def hackrf_get_operacake_boards(device:Union[int,None])->Tuple[int,Tuple[int,...]]:
    boards=(c_uint8*HACKRF_OPERACAKE_MAX_BOARDS)()
    returnCode=LIBRARY.hackrf_get_operacake_boards(device,cast(boards,POINTER(c_uint8)))
    if returnCode==hackrf_error.HACKRF_SUCCESS.value:
        return returnCode,(*(i for i in boards[:] if i!=HACKRF_OPERACAKE_ADDRESS_INVALID),)
    else:
        return returnCode,()
def hackrf_set_operacake_mode(device:Union[int,None],address:int,mode:operacake_switching_mode)->int:
    return LIBRARY.hackrf_set_operacake_mode(device,address,mode.value)
def hackrf_get_operacake_mode(device:Union[int,None],address:int)->Tuple[int,operacake_switching_mode]:
    mode=c_int()
    returnCode=LIBRARY.hackrf_get_operacake_mode(device,address,byref(mode))
    if returnCode==hackrf_error.HACKRF_SUCCESS.value:
        return returnCode,operacake_switching_mode(mode.value)
    else:
        return returnCode,operacake_switching_mode.OPERACAKE_MODE_MANUAL
hackrf_set_operacake_ports=LIBRARY.hackrf_set_operacake_ports
def hackrf_set_operacake_dwell_times(device:Union[int,None],dwell_times:Tuple[Tuple[int,int],...])->int:
    real_dwell_times=(hackrf_operacake_dwell_time*len(dwell_times))(*dwell_times)
    return LIBRARY.hackrf_set_operacake_dwell_times(device,cast(real_dwell_times,POINTER(hackrf_operacake_dwell_time)),len(dwell_times))
def hackrf_set_operacake_freq_ranges(device:Union[int,None],freq_ranges:Tuple[Tuple[int,int,int],...])->int:
    real_freq_ranges=(hackrf_operacake_freq_range*len(freq_ranges))(*freq_ranges)
    return LIBRARY.hackrf_set_operacake_freq_ranges(device,cast(real_freq_ranges,POINTER(hackrf_operacake_freq_range)),len(freq_ranges))
hackrf_reset=LIBRARY.hackrf_reset
def hackrf_set_operacake_ranges(device:Union[int,None],ranges:Tuple[int,...])->int:
    num_ranges=floor(len(ranges)/5)*5
    return LIBRARY.hackrf_set_operacake_ranges(device,cast((c_uint8*num_ranges)(*ranges[:num_ranges]),POINTER(c_uint8)),num_ranges)
hackrf_set_clkout_enable=LIBRARY.hackrf_set_clkout_enable
def hackrf_get_clkin_status(device:Union[int,None])->Tuple[int,int]:
    status=c_uint8()
    returnCode=LIBRARY.hackrf_get_clkin_status(device,byref(status))
    if returnCode==hackrf_error.HACKRF_SUCCESS.value:
        return returnCode,status.value
    else:
        return returnCode,-1
def hackrf_operacake_gpio_test(device:Union[int,None],address:int)->Tuple[int,int]:
    test_result=c_uint16()
    returnCode=LIBRARY.hackrf_operacake_gpio_test(device,address,byref(test_result))
    if returnCode==hackrf_error.HACKRF_SUCCESS.value:
        return returnCode,test_result.value
    else:
        return returnCode,-1
hackrf_set_ui_enable=LIBRARY.hackrf_set_ui_enable
def hackrf_start_rx_sweep(device:Union[int,None],rx_ctx:Union[int,None])->Callable[[Callable[[Union[int,None],NDArray[uint8],Union[int,None]],int]],Union[hackrf_sample_block_cb_fn,None]]:
    def real_hackrf_start_rx_sweep(callback:Callable[[Union[int,None],NDArray[uint8],Union[int,None]],int])->Union[hackrf_sample_block_cb_fn,None]:
        real_callback=hackrf_sample_block_cb_fn(lambda transfer:callback(transfer.contents.device,as_array(transfer.contents.buffer,(transfer.contents.valid_length,)),transfer.contents.rx_ctx))
        if LIBRARY.hackrf_start_rx_sweep(device,real_callback,rx_ctx)==hackrf_error.HACKRF_SUCCESS.value:
            return real_callback
    return real_hackrf_start_rx_sweep
hackrf_get_transfer_buffer_size=LIBRARY.hackrf_get_transfer_buffer_size
hackrf_get_transfer_queue_depth=LIBRARY.hackrf_get_transfer_queue_depth
def hackrf_board_rev_read(device:Union[int,None])->Tuple[int,int]:
    value=c_uint8(hackrf_board_rev.BOARD_REV_UNDETECTED.value)
    returnCode=LIBRARY.hackrf_board_rev_read(device,byref(value))
    if returnCode==hackrf_error.HACKRF_SUCCESS.value:
        return returnCode,value.value
    else:
        return returnCode,-1
def hackrf_supported_platform_read(device:Union[int,None])->Tuple[int,int]:
    value=c_uint32()
    returnCode=LIBRARY.hackrf_supported_platform_read(device,byref(value))
    if returnCode==hackrf_error.HACKRF_SUCCESS.value:
        return returnCode,value.value
    else:
        return returnCode,-1
hackrf_set_leds=LIBRARY.hackrf_set_leds
def hackrf_set_user_bias_t_opts(device:Union[int,None],tx_do_update:bool,tx_change_on_mode_entry:bool,tx_enabled:bool,rx_do_update:bool,rx_change_on_mode_entry:bool,rx_enabled:bool,off_do_update:bool,off_change_on_mode_entry:bool,off_enabled:bool)->int:
    req=hackrf_bias_t_user_settting_req((tx_do_update,tx_change_on_mode_entry,tx_enabled),(rx_do_update,rx_change_on_mode_entry,rx_enabled),(off_do_update,off_change_on_mode_entry,off_enabled))
    return LIBRARY.hackrf_set_user_bias_t_opts(device,byref(req))