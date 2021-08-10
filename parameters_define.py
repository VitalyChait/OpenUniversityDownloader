from yaml import safe_load, YAMLError


def login_credentials(path='loginDetails.yml'):
    # Optional - Manual putting the login credentials in the script
    manual_login = False
    if manual_login is True:
        username = "username"
        password = "password"
        identification = "id_num"
        return username, password, identification

    # INIT - Loading login credentials from parent directory
    username = None
    password = None
    identification = None
    login_details_config = None
    login_details_config_fail = False
    try:
        login_details_config = safe_load(open(path))
    except YAMLError as error:
        login_details_config_fail = True
        print("---ERROR---\nCould not load login file: {}".format(path))
        print(error)

    if login_details_config_fail is False:
        try:
            username = login_details_config['openU_user']['OpenUniversityUsername']
            password = login_details_config['openU_user']['OpenUniversityPassword']
            identification = login_details_config['openU_user']['OpenUniversityID']
        except KeyError:
            print("---ERROR---\tCould not find the correct login credentials in the file, loginDetails failed")
            login_details_config_fail = True

    if login_details_config_fail is True:
        exit("Check login_credentials function")

    return username, password, identification


def path_finder_parameters(path='configurations.yml'):
    config_file_load = True
    param_dict = {}
    script_parameters_config = None
    if config_file_load is True:
        try:
            script_parameters_config = safe_load(open(path))
        except YAMLError as error:
            config_file_load = False
            print("---ERROR---\nCould not load configuration file: {}".format(path))
            print(error)

    if config_file_load is True:
        try:
            param_dict["login_url"]         = script_parameters_config['login_config']["login_url"]
            param_dict["usernameId"]        = script_parameters_config['login_config']["usernameId"]
            param_dict["passwordId"]        = script_parameters_config['login_config']["passwordId"]
            param_dict["IDId"]              = script_parameters_config['login_config']["IDId"]
            param_dict["submit_xpath"]      = script_parameters_config['login_config']["submit_xpath"]
            param_dict["button_id"]         = script_parameters_config['login_config']["button_id"]
            param_dict["fid"]               = script_parameters_config['login_config']["fid"]
            param_dict["key_a"]             = script_parameters_config['filter_config']["key_a"]
            param_dict["key_b"]             = script_parameters_config['filter_config']["key_b"]
            param_dict["key_c"]             = script_parameters_config['filter_config']["key_c"]
            param_dict["key_d"]             = script_parameters_config['filter_config']["key_d"]
            param_dict["filter_a"]          = script_parameters_config['filter_config']["filter_a"]
            param_dict["filter_b"]          = script_parameters_config['filter_config']["filter_b"]
            param_dict["filter_c"]          = script_parameters_config['filter_config']["filter_c"]
            param_dict["filter_d"]          = script_parameters_config['filter_config']["filter_d"]
            param_dict["split_text_a"]      = script_parameters_config['filter_config']["split_text_a"]
            param_dict["split_text_b"]      = script_parameters_config['filter_config']["split_text_b"]
            param_dict["split_text_c"]      = script_parameters_config['filter_config']["split_text_c"]
            param_dict["link_start"]        = script_parameters_config['filter_config']["link_start"]
            param_dict["login_max_timeout"] = script_parameters_config['timeout_config']["login_max_timeout"]
            param_dict["video_max_timeout"] = script_parameters_config['timeout_config']["video_max_timeout"]
            param_dict["start_timeout"]     = script_parameters_config['timeout_config']["start_timeout"]
            param_dict["step"]              = script_parameters_config['timeout_config']["step"]
            param_dict["writeOutput"]       = bool(script_parameters_config['saving_config']["save_csv"])
            param_dict["full_collection"]   = bool(script_parameters_config['saving_config']["full_collection"])
            param_dict["start_index"]       = script_parameters_config['saving_config']["start_index"]
            param_dict["end_index"]         = script_parameters_config['saving_config']["end_index"]
        except KeyError:
            config_file_load = False
            print("---ERROR---\nCould not find the correct parameters in the file: {}".format(path))

    if config_file_load is False:
        param_dict["login_url"]         = "https://www.openu.ac.il/"
        param_dict["usernameId"]        = "p_user"
        param_dict["passwordId"]        = "p_sisma"
        param_dict["IDId"]              = "p_mis_student"
        param_dict["submit_xpath"]      = '//*[@id="login_sso"]/fieldset/input[1]'
        param_dict["button_id"]         = "openu_myop_plugin_MyOpAppsBtn"
        param_dict["fid"]               = "openu_myop_plugin_person_iframeId"
        param_dict["key_a"]             = "method"
        param_dict["key_b"]             = "params"
        param_dict["key_c"]             = "initialPriority"
        param_dict["key_d"]             = "url"
        param_dict["filter_a"]          = "Network.requestWillBeSent"
        param_dict["filter_b"]          = "request"
        param_dict["filter_c"]          = "High"
        param_dict["filter_d"]          = "https://souvod.bynetcdn.com/vod"
        param_dict["split_text_a"]      = "media_b"
        param_dict["split_text_b"]      = ".ts"
        param_dict["split_text_c"]      = "00000_"
        param_dict["link_start"]        = "https://opal.openu.ac.il/mod/ouilvideocollection/view.php?v="
        param_dict["login_max_timeout"] = 200
        param_dict["video_max_timeout"] = 400
        param_dict["start_timeout"]     = 5
        param_dict["step"]              = 5
        param_dict["writeOutput"]       = True
        param_dict["full_collection"]   = True
        param_dict["start_index"]       = 1
        param_dict["end_index"]         = -1
        print("Using default old parameters for path_finder script")

    if param_dict["start_index"] < 1:
        param_dict["start_index"] = 1

    return param_dict


def parallel_downloading_parameters(config_file_load=True, path='configurations.yml'):
    param_dict = {}
    script_parameters_config = None
    if config_file_load is True:
        try:
            script_parameters_config = safe_load(open(path))
        except YAMLError as error:
            config_file_load = False
            print("---ERROR---\nCould not load configuration file: {}".format(path))
            print(error)

    if config_file_load is True:
        try:
            param_dict["file_name"]             = script_parameters_config['saving_config']["file_name"]
            param_dict["extension"]             = script_parameters_config['saving_config']["extension"]
            param_dict["start_index"]           = script_parameters_config['saving_config']["start_index"]
            param_dict["save_dir"]              = script_parameters_config['saving_config']["save_dir"]
            param_dict["partial_work"]          = script_parameters_config['saving_config']["partial_work"]
            param_dict["load_file_name"]        = script_parameters_config['saving_config']["load_file_name"]
            param_dict["video_start"]           = script_parameters_config['video_config']["video_start"]
            param_dict["video_end"]             = script_parameters_config['video_config']["video_end"]
            param_dict["video_size"]            = script_parameters_config['video_config']["video_size"]
            param_dict["num_of_retry_attempts"] = script_parameters_config['video_config']["num_of_retry_attempts"]
            param_dict["pool"]                  = script_parameters_config['video_config']["pool"]
            param_dict["vid_quality"]           = script_parameters_config['video_config']["vid_quality"]
            param_dict["quality_low"]           = script_parameters_config['filter_config']["quality_low"]
            param_dict["quality_medium"]        = script_parameters_config['filter_config']["quality_medium"]
            param_dict["quality_high"]          = script_parameters_config['filter_config']["quality_high"]
            param_dict["quality_very_high"]     = script_parameters_config['filter_config']["quality_very_high"]
            param_dict["split_text_a"]          = script_parameters_config['filter_config']["split_text_a"]
            param_dict["split_text_b"]          = script_parameters_config['filter_config']["split_text_b"]
            param_dict["split_text_c"]          = script_parameters_config['filter_config']["split_text_c"]
        except KeyError:
            config_file_load = False
            print("---ERROR---\nCould not find the correct parameters in the file: {}".format(path))

    if config_file_load is False:
        param_dict["file_name"] =                  "uni_"
        param_dict["extension"] =                  ".mp4"
        param_dict["start_index"] =                1
        param_dict["save_dir"] =                   "video_saved"
        param_dict["partial_work"] =               0
        param_dict["load_file_name"] =             "Book1.csv"
        param_dict["video_start"] =                0
        param_dict["video_end"] =                  1301
        param_dict["video_size"] =                 150
        param_dict["num_of_retry_attempts"] =      30
        param_dict["pool"] =                       50
        param_dict["vid_quality"] =                4
        param_dict["quality_low"] =               "4"
        param_dict["quality_medium"] =            "8"
        param_dict["quality_high"] =              "12"
        param_dict["quality_very_high"] =         "18"
        param_dict["split_text_a"] =              "media_b"
        param_dict["split_text_b"] =              ".ts"
        param_dict["split_text_c"] =              "00000_"
        print("Using default old parameters for parallel_downloading script")

    return param_dict
