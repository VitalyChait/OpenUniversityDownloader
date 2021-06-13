from selenium.webdriver import Chrome
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common import exceptions
from time import sleep
from yaml import safe_load
from csv import reader
from json import loads


# INIT - Loading from parent directory
confa_fail = False
try:
    confa = safe_load(open('loginDetails.yml'))
except:
    print("Loading error, loginDetails failed")
    confa_fail = True

if confa_fail is False:
    OpenUniversityUsername = confa['openU_user']['OpenUniversityUsername']
    OpenUniversityPassword = confa['openU_user']['OpenUniversityPassword']
    OpenUniversityID       = confa['openU_user']['OpenUniversityID']
else:
    OpenUniversityUsername = "username"
    OpenUniversityPassword = "password"
    OpenUniversityID = "idnumber"


confb_fail = False
try:
    confb = safe_load(open('configurations.yml'))
except:
    print("Loading error, configurations failed")
    confb_fail = True
    exit()

if confb_fail is False:
    login_url              = confb['login_config']["login_url"]
    usernameId             = confb['login_config']["usernameId"]
    passwordId             = confb['login_config']["passwordId"]
    IDId                   = confb['login_config']["IDId"]
    submit_xpath           = confb['login_config']["submit_xpath"]
    button_id              = confb['login_config']["button_id"]
    fid                    = confb['login_config']["fid"]

    key_a                  = confb['filter_config']["key_a"]
    key_b                  = confb['filter_config']["key_b"]
    key_c                  = confb['filter_config']["key_c"]
    key_d                  = confb['filter_config']["key_d"]

    filter_a               = confb['filter_config']["filter_a"]
    filter_b               = confb['filter_config']["filter_b"]
    filter_c               = confb['filter_config']["filter_c"]
    filter_d               = confb['filter_config']["filter_d"]

    split_text_a           = confb['filter_config']["split_text_a"]  # 00000_
    split_text_b           = confb['filter_config']["split_text_b"]

    login_max_timeout      = confb['timeout_config']["login_max_timeout"]
    video_max_timeout      = confb['timeout_config']["video_max_timeout"]
    start_timeout          = confb['timeout_config']["start_timeout"]
    step                   = confb['timeout_config']["step"]

else:
    login_url = "https://www.openu.ac.il/"
    usernameId = "p_user"
    passwordId = "p_sisma"
    IDId = "p_mis_student"
    submit_xpath = '//*[@id="login_sso"]/fieldset/input[1]'
    button_id = "openu_myop_plugin_MyOpAppsBtn"
    fid = "openu_myop_plugin_person_iframeId"
    key_a = "method"
    key_b = "params"
    key_c = "initia"
    key_d = "url"
    filter_a = "Network.requestWillBeSent"
    filter_b = "request"
    filter_c = "High"
    filter_d = "https://souvod.bynetcdn.com/vod"
    split_text_a = "00000_"
    split_text_b = ".ts"
    login_max_timeout = 100
    video_max_timeout = 400
    start_timeout = 5
    step = 5

IS_EMPTY = True
URLS = []
with open('url_list.csv', mode='r', newline='') as csv_file:
    csv_reader = reader(csv_file, delimiter=',', quotechar='|')
    file_print = False
    for row in csv_reader:
        if not file_print:
            file_print = True
            continue
        elif row[1] != "":
            URLS.append(row[1])
        else:
            break
if not URLS:
    exit("Empty URL list")
    exit()


def login(driver=None, username=OpenUniversityUsername, password=OpenUniversityPassword, ID=OpenUniversityID, login_timeout=start_timeout):

    button_xpath = '//*[@id="{0}"]'.format(button_id)
    frame_xpath = '//*[@id="{0}"]'.format(fid)
    user_xpath = '//*[@id="{0}"]'.format(usernameId)
    password_xpath = '//*[@id="{0}"]'.format(passwordId)
    id_xpath = '//*[@id="{0}"]'.format(IDId)

    print("Starting login stage")
    driver.get(login_url)
    sleep(login_timeout)

    print("Time pass:  ", end='')
    while login_max_timeout >= login_timeout:
        print("{}".format(login_timeout), end='')
        try:
            button_element = driver.find_element_by_xpath(button_xpath)
        except exceptions.NoSuchElementException:
            login_timeout += step
            sleep(step)
            print(" --> ", end='')
            continue
        break
    if login_max_timeout < login_timeout:
        exit("Exceeded timeout, failed")
    driver.execute_script("arguments[0].click();", button_element)
    login_timeout += step
    sleep(step)

    while login_max_timeout >= login_timeout:
        try:
            frame_element = driver.find_element_by_xpath(frame_xpath)
        except exceptions.NoSuchElementException:
            login_timeout += step
            sleep(step)
            print(" --> {}".format(login_timeout), end='')
            continue
        break
    if login_max_timeout < login_timeout:
        exit("Exceeded timeout, failed")
    driver.switch_to.frame(frame_element)

    while login_max_timeout >= login_timeout:
        try:
            user_element = driver.find_element_by_xpath(user_xpath)
        except exceptions.NoSuchElementException:
            login_timeout += step
            sleep(step)
            print(" --> {}".format(login_timeout), end='')
            continue
        break
    if login_max_timeout < login_timeout:
        exit("Exceeded timeout, failed")
    driver.execute_script("arguments[0].value = '{}';".format(username), user_element)

    while login_max_timeout >= login_timeout:
        try:
            password_element = driver.find_element_by_xpath(password_xpath)
        except exceptions.NoSuchElementException:
            login_timeout += step
            sleep(step)
            print(" --> {}".format(login_timeout), end='')
            continue
        break
    if login_max_timeout < login_timeout:
        exit("Exceeded timeout, failed")
    driver.execute_script("arguments[0].value = '{}';".format(password), password_element)

    while login_max_timeout >= login_timeout:
        try:
            id_element = driver.find_element_by_xpath(id_xpath)
        except exceptions.NoSuchElementException:
            login_timeout += step
            sleep(step)
            print(" --> {}".format(login_timeout), end='')
            continue
        break
    if login_max_timeout < login_timeout:
        exit("Exceeded timeout, failed")
    driver.execute_script("arguments[0].value = '{}';".format(ID), id_element)

    while login_max_timeout >= login_timeout:
        try:
            submit_element = driver.find_element_by_xpath(submit_xpath)
        except exceptions.NoSuchElementException:
            login_timeout += step
            sleep(step)
            print(" --> {}".format(login_timeout), end='')
            continue
        break
    if login_max_timeout < login_timeout:
        exit("Exceeded timeout, failed")
    driver.execute_script("arguments[0].click();", submit_element)

    sleep(step)
    print("\nLogin stage is successful\n")
    return login_timeout


def process_browser_logs_for_network_events_step_a(logs):
    for entry in logs:
        log = loads(entry["message"])["message"]
        if filter_a in log[key_a]:
            if filter_b in log[key_b]:
                yield log["params"]["request"]


def process_browser_logs_for_network_events_step_b(events):
    for event in events:
        if filter_c in event[key_c]:
            if filter_d == event[key_d][:31]:
                yield event[key_d]


def process_browser_logs_for_network_events_step_c(possible_urls):
    filtered_url_list = []
    for mapped_w_url in possible_urls:
        if not (len(mapped_w_url.split(split_text_a)) < 2 or len(mapped_w_url.split(split_text_b)) < 2):
            filtered_url_list.append(mapped_w_url)
    return filtered_url_list


def process_browser_logs_for_network_events_step_d(w_filtered_urls):
    final = None
    finala = None
    finalb = None
    if w_filtered_urls is None:
        return None
    if len(w_filtered_urls) < 1:
        return None
    else:
        for url in w_filtered_urls:
            a = url.split(split_text_a)
            b = url.split(split_text_b)
            if final is None:
                final = url
                finala = a[0]
                finalb = b[1]
            elif finala != a[0] or finalb != b[1]:
                print("Too many links were found")
                return None
    return final


def collect_urls(work_url, url_start_login_time=start_timeout, driver=None):
    final_url = None
    print("\nExtracting information from:\t{}".format(work_url), end='')
    driver.get(work_url)
    sleep(url_start_login_time)
    size = driver.get_window_size()
    print("\t", size, "  page loaded")

    retry = False
    while url_start_login_time <= video_max_timeout:
        logs_raw = driver.get_log("performance")
        sleep(3)
        if retry is False:
            print("Analyzing")
            print("Time pass: ", url_start_login_time, end='')
            retry = True
        else:
            print(" --> ", url_start_login_time, end='')

        events = process_browser_logs_for_network_events_step_a(logs_raw)
        possible_urls = process_browser_logs_for_network_events_step_b(events)
        filtered_urls = process_browser_logs_for_network_events_step_c(possible_urls)
        final_url = process_browser_logs_for_network_events_step_d(filtered_urls)
        if final_url is not None:
            break
        url_start_login_time += step
        sleep(step)

    if final_url is None:
        print("\nFailed\t{}".format(final_url))
        return None
    print("\nDone\t{}".format(final_url))
    return final_url


def run_script(external_url=None):
    if external_url is not None:
        woking_urls = external_url
    else:
        woking_urls = URLS
    caps = DesiredCapabilities.CHROME
    caps["goog:loggingPrefs"] = {"performance": "ALL"}
    caps['pageLoadStrategy'] = 'none'
    sdriver = Chrome(desired_capabilities=caps)
    sdriver.maximize_window()
    sleep(0.2)

    login_time_took = login(driver=sdriver)
    if login_time_took > video_max_timeout:
        r_start_timeout = video_max_timeout
    else:
        r_start_timeout = login_time_took
    url_output = []
    for video in woking_urls:
        url = collect_urls(video, url_start_login_time=r_start_timeout, driver=sdriver)
        url_output.append(url)
    print("\n\n")
    return url_output
