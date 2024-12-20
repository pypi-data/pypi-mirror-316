import enum


class MapType(enum.IntEnum):
    ThreeDMap = 32
    RTABMap = 9
    KDVisual = 33
    TwoDMap = 2


class Capability(str, enum.Enum):
    # Command callbacks
    on_teleop = "on_teleop"
    on_stop = "on_stop"
    on_start_mapping = "on_start_mapping"
    on_start_mapping_3d = "on_start_mapping_3d"
    on_save_mapping = "on_save_mapping"
    on_save_mapping_3d = "on_save_mapping_3d"
    on_localize = "on_localize"
    on_load_navigation_map_pgm = "on_load_navigation_map_pgm"
    on_load_navigation_map_yaml = "on_load_navigation_map_yaml"
    on_load_localization_map_pgm = "on_load_localization_map_pgm"
    on_load_localization_map_yaml = "on_load_localization_map_yaml"
    on_load_map_3d = "on_load_map_3d"
    on_unload_map = "on_unload_map"
    on_execute_task = "on_execute_task"
    on_resume_task = "on_resume_task"
    on_pause_task = "on_pause_task"
    on_set_priority = "on_set_priority"
    on_robot_info = "on_robot_info"
    on_preview_map = "on_preview_map"
    on_acquire_lock_response = "on_acquire_lock_response"

    # Publisher
    set_camera_feed = "set_camera_feed"
    set_lidar = "set_lidar"
    set_lidar_3d = "set_lidar_3d"
    set_pose = "set_pose"
    set_map_data = "set_map_data"
    set_status = "set_status"
    set_battery_percentage = "set_battery_percentage"
    set_map_result = "set_map_result"
    set_map_result_3d = "set_map_result_3d"
    check_map_existance = "check_map_existance"
    set_map_preview_result = "set_map_preview_result"
    set_cpu_usage = "set_cpu_usage"
    set_memory_usage = "set_memory_usage"
    set_battery_usage = "set_battery_usage"
    set_robot_info = "set_robot_info"
    set_decimated_plan = "set_decimated_plan"
    set_result = "set_result"
    set_obstacle_notification = "set_obstacle_notification"
    set_notification_message = "set_notification_message"
    set_acquire_lock_request = "set_acquire_lock_request"
