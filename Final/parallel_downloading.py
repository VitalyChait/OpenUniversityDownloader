from math import ceil
from multiprocessing.pool import ThreadPool
from time import time, sleep
from os import chdir, getcwd
from collections import OrderedDict
from requests import get, exceptions, HTTPError
from sys import exc_info
from yaml import safe_load
import path_finder


URL = path_finder.run_script()

# INIT
config_file_load = True
try:
    confb = safe_load(open('configurations.yml'))
except:
    config_file_load = False

if config_file_load is True:
    file_name   =  confb['saving_config']["file_name"]
    extension   =  confb['saving_config']["extension"]
    start_index =  confb['saving_config']["start_index"]
    save_dir    =  confb['saving_config']["save_dir"]

    video_start           = confb['video_config']["video_start"]
    video_end             = confb['video_config']["video_end"]
    video_size            = confb['video_config']["video_size"]
    num_of_retry_attempts = confb['video_config']["num_of_retry_attempts"]
    pool                  = confb['video_config']["pool"]

    split_text_a = confb['filter_config']["split_text_a"]  # 00000_
    split_text_b = confb['filter_config']["split_text_b"]

else:
    file_name = "DEV_"
    extension = ".mp4"
    start_index = 27
    save_dir = r"C:\Users\vital\Desktop\uni\dev"
    video_start = 0  # Video part start (Default = 0)
    video_end = 1350 + 1  # Video part end, +1 for looping (Default = 1150)
    video_size = 150  # Around 2MB * Size
    # Number of attempts to reconnect
    num_of_retry_attempts = 30
    split_text_a = "00000_"
    split_text_b = ".ts"
    pool = 50

try:
    chdir(save_dir)
except:
    print("Changing dir failed")

print("Working dir:  ", getcwd())

if isinstance(URL, list):
    looping = len(URL)
    URL = list(OrderedDict.fromkeys(URL))
    if looping != len(URL):
        print("---Warning---\tYou have path duplicates, see variable{URL}")
        looping = len(URL)
else:
    looping = 1
final = None
r = None
error_list = []


if video_start > 0:
    print("---Warning---\tNot starting from beginning, see variable{video_start}")
if video_end < 1201:
    print("---Warning---\tNot ending from default, see variable{video_end}")
if video_size > video_end-video_start:
    print("---Warning---\tVideo size is not correct, see variable{video_size}")


def url_handler(work_url, url_j=0):
    temp_url_succeed = True
    if len(work_url.split(split_text_a)) < 2:
        url_error_text = "---ERROR---, {} could not split {}\t".format(split_text_a, work_url)
        url_param = "start_index={} | j={} | i={} | video_size={}".format(start_index, url_j, 0, video_size)
        print("\n", url_error_text, url_param, "\n")
        error_list.append(url_error_text + url_param)
        temp_url_succeed = False
    if len(work_url.split(split_text_b)) < 2:
        url_error_text = "---ERROR---, {} could not split {}\t".format(split_text_b, work_url)
        url_param = "start_index={} | j={} | i={} | video_size={}".format(start_index, url_j, 0, video_size)
        print("\n", url_error_text, url_param, "\n")
        error_list.append(url_error_text + url_param)
        temp_url_succeed = False
    if temp_url_succeed is False:
        if url_j == 0:
            print("\n\n Exiting the program \n\n")
            exit()
        print("Skipping the video")
        return "", "", False
    # URL handling
    url_start = work_url.split(split_text_a)[0] + split_text_a
    url_end = split_text_b + work_url.split(split_text_b)[1]
    return url_start, url_end, True


def working(w_start='', w_i='', w_end=''):
    w_failed = False
    current_r = None
    failure = None
    try:
        current_r = get(w_start + w_i + w_end, allow_redirects=True, timeout=600)
    except exceptions.Timeout:
        failure = "Exception timeout"
        w_failed = True
    except exceptions.TooManyRedirects:
        failure = "Exception TooManyRedirects"
        w_failed = True
    except exceptions.RequestException as exception:
        failure = exception
        w_failed = True
    if not w_failed:
        try:
            current_r.raise_for_status()
        except HTTPError:
            failure = "Exception HTTPError"
            w_failed = True
    if w_failed:
        failure = "---Warning---\tFailure during the {0} chunk \n {1}\n".format(w_i, failure)
        current_r = None
    return current_r, w_i, failure


def parallel_worker(work_two_path):
    w_failed = False
    current_r = None
    try:
        current_r = get(work_two_path, allow_redirects=True, timeout=600)
    except exceptions.Timeout:
        failure_two = "Exception timeout"
        w_failed = True
    except exceptions.TooManyRedirects:
        failure_two = "Exception TooManyRedirects"
        w_failed = True
    except exceptions.RequestException as exception:
        failure_two = exception
        w_failed = True
    if not w_failed:
        try:
            current_r.raise_for_status()
        except HTTPError:
            failure_two = "Exception HTTPError"
            w_failed = True
    if w_failed:
        failure_two = "---Warning---\tFailure during the {0} chunk \n {1}\n".format(work_two_path, failure_two)
        print("not working")
        return None, work_two_path, failure_two
    return current_r.content, work_two_path, None


def find_last_index(path_start='', path_end='', last_start=video_start, last_end=video_end, last_num_of_retry_attempts=num_of_retry_attempts):
    last_num_of_retry_attempts = int(last_num_of_retry_attempts / 4)
    if last_num_of_retry_attempts < 1:
        last_num_of_retry_attempts = 1

    i, ll, rl = last_end, last_start, last_end
    print("Working to find the video last index")
    while rl > ll+1:
        print(" --> ", i, end='')
        current_attempts = 0
        # Try to collect data chunk
        while current_attempts < last_num_of_retry_attempts:
            err = working(path_start, str(i), path_end)[2]
            if err is None:
                ll = i
                break
            else:
                current_attempts += 1
                sleep(0.05)
        if current_attempts >= last_num_of_retry_attempts:
            rl = i
        i = int((ll + rl) / 2)
    print("\nLast index found: ", ll)
    return ll


def verify_indices(path_start='', path_end='', verify_start=video_start, verify_end=video_end, verify_num_of_retry_attempts=num_of_retry_attempts):
    for i in [str(verify_start), str(verify_end)]:
        current_attempts = 0
        # Try to collect data chunk
        while current_attempts < verify_num_of_retry_attempts:
            err = working(path_start, i, path_end)[2]
            if err is None:
                break
            else:
                print("verify current_attempts: ", current_attempts, " \t i: ", i)
                print(err)
                print(path_start + i + path_end)
                current_attempts += 1
                sleep(0.1)
        if current_attempts >= verify_num_of_retry_attempts:
            return False
    return True


def saving(s_j=0, s_i=0, save_final=None, full_flag=True, save_start_index=start_index,
           save_video_size=video_size, save_file_name=file_name):
    if save_final is None:
        saving_error_text = "---ERROR---, debugging required final is None\t"
        saving_param = "start_index={} | j={} | i={} | video_size={}".format(start_index, s_j, s_i, save_video_size)
        print("\n", saving_error_text, saving_param, "\n")
        error_list.append(saving_error_text+saving_param)
        return True

    file = save_file_name + "_{0}_part{1}".format(str(save_start_index + s_j), str(int(s_i / save_video_size)))
    if not full_flag:
        file = file + '_' + str(int(s_i % save_video_size))

    saved = True
    try:
        open(file + extension, 'wb').write(save_final)
    except OSError as err:
        print("---Warning---\tOS error: {0}".format(err))
        saved = False
    except ValueError:
        print("---Warning---\tValueError")
        saved = False
    except:
        print("---Warning---\tUnexpected error:", exc_info()[0])
        saved = False

    if saved is True:
        print("---OK---\t Saved: ", file)
    return True


for j in range(looping):
    t_start = int(time())
    split_vid = True
    final = None
    print("---OK---\tStart loop video {0}, video index {1}".format(j, start_index+j))

    # Correct current URL
    if looping > 1:
        start, end, url_succeed = url_handler(URL[j], j)
        if url_succeed is False:
            continue
    elif isinstance(URL, list):
        URL = URL[0]
        start, end, url_succeed = url_handler(URL, j)
    else:
        start, end, url_succeed = url_handler(URL, j)
        if url_succeed is False:
            continue

    last_index = find_last_index(path_start=start, path_end=end)
    if not verify_indices(path_start=start, path_end=end, verify_end=last_index):
        print("---ERROR---\tCould not find video index start/end for video {0}".format(j))
        continue

    # Based for OpenU video streaming
    # Collect all chunks of data, each chunk is ~1mb
    # 1100 chunks is a few min more than ~3hrs video
    # Adjust the range of the loop to extend your max video length
    j_index_url_list = [start+str(i)+end for i in range(video_start, last_index+1)]
    total_len = len(j_index_url_list)
    completed = [None]*total_len
    j_index_retry_list = []
    last_o = 0
    retries = 1
    pool_size = pool

    for o in range(ceil(total_len/pool)):
        if last_o+pool_size > total_len - 1:
            pool_size = total_len-last_o-1
        results = ThreadPool(pool_size).imap_unordered(parallel_worker, j_index_url_list[last_o:last_o + pool_size])
        print(o)
        for r, w_path, failures in results:
            i_index = int(w_path[len(start): -len(end)])
            print(i_index)
            if failures is None:
                completed[i_index-video_start] = r
            else:
                j_index_retry_list.append(w_path)
                print("failure")

        last_o = last_o+pool_size

    while len(j_index_retry_list) > 0 and retries < num_of_retry_attempts:
        print("retries: ", retries)
        j_index_url_list = j_index_retry_list
        total_len = len(j_index_url_list)
        j_index_retry_list = []
        last_o = 0
        retries += 1
        pool_size = pool

        for o in range(ceil(total_len / pool)):
            if last_o + pool_size > total_len - 1:
                pool_size = total_len - last_o - 1

            results = ThreadPool(pool_size).imap_unordered(parallel_worker, j_index_url_list[last_o:last_o + pool_size])
            sleep(10)
            for r, w_path, failures in results:
                i_index = int(w_path[len(start): -len(end)])
                print(i_index)
                if failures is None:
                    completed[i_index-video_start] = r
                else:
                    j_index_retry_list.append(w_path)
                    print("failure")

            last_o = last_o + pool_size

    if len(j_index_retry_list) == 0:
        print("Download succeeded")
        total = len(completed) - 1
        while completed[total] is None:
            total -= 1
        final = completed[0]
        for t in range(1, total+1):
            final += completed[t]
        print("Saving")
        saving(j, 1, final, False, save_video_size=1)
    else:
        print("bug")
        break
