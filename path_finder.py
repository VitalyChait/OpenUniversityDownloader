from selenium.webdriver import Chrome
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common import exceptions
from time import sleep
from csv import reader, writer
from json import loads
from collections import OrderedDict
from os import getcwd
# Local scripts
from parameters_define import login_credentials, path_finder_parameters


# INIT
OpenUniversityUsername, OpenUniversityPassword, OpenUniversityID = login_credentials(path='loginDetails.yml')
param_dict = path_finder_parameters(path='configurations.yml')
login_url         = param_dict["login_url"]
usernameId        = param_dict["usernameId"]
passwordId        = param_dict["passwordId"]
IDId              = param_dict["IDId"]
submit_xpath      = param_dict["submit_xpath"]
button_id         = param_dict["button_id"]
fid               = param_dict["fid"]
key_a             = param_dict["key_a"]
key_b             = param_dict["key_b"]
key_c             = param_dict["key_c"]
key_d             = param_dict["key_d"]
filter_a          = param_dict["filter_a"]
filter_b          = param_dict["filter_b"]
filter_c          = param_dict["filter_c"]
filter_d          = param_dict["filter_d"]
split_text_a      = param_dict["split_text_a"]
split_text_b      = param_dict["split_text_b"]
split_text_c      = param_dict["split_text_c"]
link_start        = param_dict["link_start"]
login_max_timeout = param_dict["login_max_timeout"]
video_max_timeout = param_dict["video_max_timeout"]
start_timeout     = param_dict["start_timeout"]
step              = param_dict["step"]
writeOutput       = param_dict["writeOutput"]
full_collection   = param_dict["full_collection"]
start_index       = param_dict["start_index"]
end_index         = param_dict["end_index"]


def work_urls(csv_path='url_list.csv'):
    print("--NOTE---\tLoading urls from {}".format(csv_path))
    url_found = []
    try:
        with open(csv_path, mode='r', newline='') as csv_file:
            csv_reader = reader(csv_file, delimiter=',', quotechar='|')
            file_print = False
            for row in csv_reader:
                if not file_print:
                    file_print = True
                    continue
                elif row[1] != "":
                    url_found.append(row[1])
                else:
                    break
    except OSError as err:
        print("---Warning---\tOS error: {0}".format(err))
        exit("Could not open this file: {0}".format(csv_path))

    if not url_found:
        exit("Empty URL list")
        exit()

    url_final = list(OrderedDict.fromkeys(url_found))
    if len(url_found) != len(url_final):
        print("---Warning---\tYou have {0} duplicated urls".format(len(url_found) - len(url_final)))

    return url_final


def save_url_file(link_list, video_list, save_video_names=None, csv_path='url_list_out.csv'):
    if save_video_names is not None:
        work_link_list = [[save_video_names[i][0], save_video_names[i][1], save_video_names[i][2], video_list[i], link_list[i]] for i in range(len(video_list))]
        work_link_list = [["Subject", "Sub Subject", "Video Index", "Video URL", "Download URL", "NOTE--Encoding in Hebrew"]] + work_link_list
    else:
        work_link_list = [[video_list[i], link_list[i]] for i in range(len(video_list))]
        work_link_list = [["Video URL", "Download URL"]] + work_link_list

    try:
        with open(csv_path, 'w', newline='', encoding="iso8859-8") as csv_out_file:
            writing_file = writer(csv_out_file)
            writing_file.writerows(work_link_list)
        print("\n---OK---\tWriting CSV file completed")
        print("--NOTE---\tCSV saving dir:  ", getcwd())
    except OSError as err:
        print("---Warning---\tOS error: {0}".format(err))
        print("\n---ERROR---\tCould not save the file")


def login(driver=None, username=OpenUniversityUsername, password=OpenUniversityPassword, ID=OpenUniversityID,
          login_timeout=start_timeout):
    button_xpath = '//*[@id="{0}"]'.format(button_id)
    frame_xpath = '//*[@id="{0}"]'.format(fid)
    user_xpath = '//*[@id="{0}"]'.format(usernameId)
    password_xpath = '//*[@id="{0}"]'.format(passwordId)
    id_xpath = '//*[@id="{0}"]'.format(IDId)
    button_element, frame_element, user_element, password_element, id_element, submit_element, filtered_url_list \
        = [None]*7

    print("---OK---\tStarting login stage")
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
        exit("Exceeded timeout, failed to find {0}".format("button_element"))
    driver.execute_script("arguments[0].click();", button_element)
    login_timeout += step
    sleep(step)
    print(" --> {}".format(login_timeout), end='')

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
        exit("Exceeded timeout, failed to find {0}".format("frame_element"))
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
        exit("Exceeded timeout, failed to find {0}".format("user_element"))
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
        exit("Exceeded timeout, failed to find {0}".format("password_element"))
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
        exit("Exceeded timeout, failed to find {0}".format("id_element"))
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
        exit("Exceeded timeout, failed to find {0}".format("submit_element"))
    driver.execute_script("arguments[0].click();", submit_element)

    sleep(step)
    print("\n---OK---\tLogin stage is successful\n")
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


def process_browser_logs_for_network_events_step_c(possible_urls, quick=True):
    filtered_url_list = None
    if not quick:
        filtered_url_list = []
    for mapped_w_url in possible_urls:
        if not len(mapped_w_url.split(split_text_c)) < 2:
            if not (len(mapped_w_url.split(split_text_a)) < 2 or len(mapped_w_url.split(split_text_b)) < 2):
                if quick:
                    return mapped_w_url
                else:
                    filtered_url_list.append(mapped_w_url)
    if not quick:
        return process_browser_logs_for_network_events_step_d(filtered_url_list)
    else:
        return None


def process_browser_logs_for_network_events_step_d(w_filtered_urls):
    final = None
    final_a = None
    final_b = None
    if w_filtered_urls is None:
        return None
    if len(w_filtered_urls) < 1:
        return None
    else:
        for url in w_filtered_urls:
            a = url.split(split_text_c)
            b = url.split(split_text_b)
            if final is None:
                final = url
                final_a = a[0]
                final_b = b[1]
            elif final_a != a[0] or final_b != b[1]:
                print("\n---ERROR---\tToo many links were found")
                print(w_filtered_urls)
                return None
    return final


def collect_urls(work_url, url_start_login_time=start_timeout, driver=None):
    final_url = None
    print("\n--NOTE---\tExtracting information from:\t{}".format(work_url), end='')
    driver.get(work_url)
    sleep(url_start_login_time)
    size = driver.get_window_size()
    print("\t", size, " page loaded - analyzing")

    retry = False
    while url_start_login_time <= video_max_timeout:
        logs_raw = driver.get_log("performance")
        sleep(3)
        if retry is False:
            print("Time pass: ", url_start_login_time, end='')
            retry = True
        else:
            print(" --> ", url_start_login_time, end='')

        events = process_browser_logs_for_network_events_step_a(logs_raw)
        possible_urls = process_browser_logs_for_network_events_step_b(events)
        final_url = process_browser_logs_for_network_events_step_c(possible_urls)
        if final_url is not None:
            break
        url_start_login_time += step
        sleep(step)

    if final_url is None:
        print("\n---ERROR---\tFailed\t{}".format(final_url))
        return None
    print("\n---OK---\tDone\t{}".format(final_url))
    return final_url


def auto_collect_url(list_work_url, url_start_login_time=start_timeout, driver=None):
    video_topic_xpath = '/html/head/title'
    video_sub_topic_xpath = '//*[@id="{0}"]'.format("ovc_selected_collection")
    path_id = []
    name_id = []
    strings_list = "'\","

    for work_url in list_work_url:
        print("\n--NOTE---\tFinding relevant URLS with minimum index of - {} from collection:\t{}".format(start_index, work_url), end='')
        if end_index > 0:
            print("\n--NOTE---\tFinding relevant URLS with maximum index of - {}".format(end_index), end='')
        driver.get(work_url)
        sleep(url_start_login_time)

        try:
            topic_element = driver.find_element_by_xpath(video_topic_xpath)
            subject_name = topic_element.get_attribute('innerHTML').split("אוסף וידאו : ")[1]
        except NoSuchElementException:
            print("---ERROR---\tCould not find subject_name")
            subject_name = 'NA'
        try:
            sub_topic_element = driver.find_element_by_xpath(video_sub_topic_xpath)
            sub_subject_name = sub_topic_element.text
        except NoSuchElementException:
            print("---ERROR---\tCould not find sub_subject_name")
            sub_subject_name = 'NA'

        subject_name = ''.join(c for c in subject_name if c not in strings_list)
        sub_subject_name = ''.join(c for c in sub_subject_name if c not in strings_list)

        print("\n--NOTE---\t", subject_name, " ", sub_subject_name)

        try:
            elements = driver.find_elements_by_class_name("ovc_playlist")
            elements.reverse()
        except NoSuchElementException:
            print("---ERROR---\tCould not analyze URL")
            continue
        if end_index < 1:
            temp_end_index = len(elements)
        else:
            temp_end_index = int(end_index)
        for i in elements[start_index-1: temp_end_index]:
            try:
                name = ((i.get_attribute('innerHTML')).split("\" tabindex")[0]).split("title=\"")[1]
                print("---OK---\tFound: {}".format(name))
            except NoSuchElementException:
                print("---ERROR---\tCould not find video name")
                name = 'NA'
            name = ''.join(c for c in name if c not in strings_list)

            path_id.append(link_start + i.get_attribute("id").split("playlist")[1])
            name_id.append([subject_name, sub_subject_name, name])

    if len(path_id) == 0:
        return None, False, None

    final_path_id = []
    final_name_id = []
    [final_path_id.append(x) for x in path_id if x not in final_path_id]
    [final_name_id.append(x) for x in name_id if x not in final_name_id]

    if len(final_path_id) != len(final_name_id) or len(final_name_id) == 0:
        print("\n---ERROR---\tCould not remove duplicates")
    else:
        path_id = final_path_id
        name_id = final_name_id

    return path_id, True, name_id


def run_script(external_url=None):
    caps = DesiredCapabilities.CHROME
    caps["goog:loggingPrefs"] = {"performance": "ALL"}
    caps['pageLoadStrategy'] = 'none'
    run_driver = Chrome(desired_capabilities=caps)
    run_driver.maximize_window()
    sleep(0.2)

    login_time_took = login(driver=run_driver)
    if login_time_took > video_max_timeout:
        r_start_timeout = video_max_timeout
    else:
        r_start_timeout = login_time_took*2

    video_names = None
    if external_url is not None:
        working_urls = external_url
    else:
        if full_collection is True:
            full_collection_start_url = work_urls()
            working_urls, worked, video_names = auto_collect_url(full_collection_start_url, url_start_login_time=r_start_timeout, driver=run_driver)
            if worked is False:
                working_urls = work_urls()
        else:
            working_urls = work_urls()

    url_output = []
    for video in working_urls:
        url = collect_urls(video, url_start_login_time=r_start_timeout, driver=run_driver)
        url_output.append(url)

    if writeOutput:
        save_url_file(url_output, working_urls, save_video_names=video_names)
    else:
        print("\n--NOTE---\tFound:")
        for i in url_output:
            print(i)
        print("\n\n")

    print("\n--NOTE---\tCollection stage finished\n")
    run_driver.quit()

    return url_output
