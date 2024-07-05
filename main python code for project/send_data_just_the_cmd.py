# Send the MAV_CMD_NAVIGATION message to move forward
master.mav.send(
    mavutil.mavlink.MAVLink_msg_id_set_position_target_global_int_pack(
        master.target_system,
        master.target_component,
        0b0000111111111000,  # Mask for the target coordinates
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
        0b0000000000001000,  # POSITION_TARGET_TYPEMASK_X_IGNORE | POSITION_TARGET_TYPEMASK_Y_IGNORE | POSITION_TARGET_TYPEMASK_VX_IGNORE | POSITION_TARGET_TYPEMASK_VY_IGNORE
        target_lat,  # x
        target_lon,  # y
        msg.alt,  # z
        0, 0, 0, 0, 0  # vx, vy, vz, afx, afy, afz (not used)
    )
)