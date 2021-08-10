from math import ceil
from multiprocessing.pool import ThreadPool
from time import sleep
from os import chdir, getcwd
from requests import get, exceptions, HTTPError
# Local scripts
from path_finder import work_urls, run_script
from parameters_define import parallel_downloading_parameters


# INIT
config_file_load = True
param_dict = parallel_downloading_parameters(config_file_load, path='configurations.yml')

file_name             = param_dict["file_name"]
extension             = param_dict["extension"]
start_index           = param_dict["start_index"]
save_dir              = param_dict["save_dir"]
partial_work          = param_dict["partial_work"]
load_file_name        = param_dict["load_file_name"]
video_start           = param_dict["video_start"]
video_end             = param_dict["video_end"]
video_size            = param_dict["video_size"]
num_of_retry_attempts = param_dict["num_of_retry_attempts"]
pool                  = param_dict["pool"]
vid_quality           = param_dict["vid_quality"]
quality_low           = param_dict["quality_low"]
quality_medium        = param_dict["quality_medium"]
quality_high          = param_dict["quality_high"]
quality_very_high     = param_dict["quality_very_high"]
split_text_a          = param_dict["split_text_a"]
split_text_b          = param_dict["split_text_b"]
split_text_c          = param_dict["split_text_c"]
final = None
r = None
error_list = []
last_index = video_end


if partial_work:
    URL = work_urls(load_file_name)
else:
    URL = run_script()

if isinstance(URL, list):
    looping = len(URL)
else:
    looping = 1

if video_start > 0:
    print("---Warning---\tNot starting from beginning, see variable{video_start}")
if video_end < 1300:
    print("---Warning---\tNot ending from default, see variable{video_end}")
try:
    chdir(save_dir)
except OSError:
    print("---ERROR---\tChanging dir failed")
print("--NOTE---\tVideo saving dir:  ", getcwd())


def url_handler(work_url, url_j=0):
    test_a = work_url.split(split_text_a)
    test_b = work_url.split(split_text_b)
    test_c = work_url.split(split_text_c)
    if len(test_a) < 2 or len(test_b) < 2 or len(test_c) < 2 or len(test_c[0])  < len(test_a[0]) + len(split_text_a):
        error = work_url + "\t"
        if len(test_a) < 2:
            error += " split_text_a  "
        if len(test_b) < 2:
            error += " split_text_b  "
        if len(test_c) < 2:
            error += " split_text_c  "
        if len(test_c[0])  < len(test_a[0]) + len(split_text_a):
            error += " len(test_c)[0]"
        url_error_text = "---ERROR---\tcould not split: " + error
        print("\n", url_error_text, "\n")
        if url_j == 0:
            print("\n\n Exiting the program \n\n")
            exit()
        print("---ERROR---\tSkipping the video")
        return "", "", "", False

    # URL handling
    url_start = test_a[0] + split_text_a
    url_end = split_text_b + test_b[1]

    current_found_quality = test_c[0]
    current_found_quality = current_found_quality[len(url_start):]

    return url_start, url_end, current_found_quality, True


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
    failure_two = None
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
        return None, work_two_path, failure_two
    return current_r.content, work_two_path, None


def find_quality(path_start='', path_end='', last_start=video_start,
                 last_num_of_retry_attempts=num_of_retry_attempts, max_vid_quality=vid_quality):

    function_worked = False
    max_vid_quality = int(max_vid_quality)
    last_num_of_retry_attempts = int(last_num_of_retry_attempts / 4)
    if last_num_of_retry_attempts < 1:
        last_num_of_retry_attempts = 1

    for m in range(min(4, max_vid_quality)):
        if max_vid_quality-m == 4:
            current_quality = quality_very_high
        elif max_vid_quality-m == 3:
            current_quality = quality_high
        elif max_vid_quality-m == 2:
            current_quality = quality_medium
        else:
            current_quality = quality_low
        i = current_quality + split_text_c + str(last_start)

        current_attempts = 0
        while current_attempts < last_num_of_retry_attempts:
            err = working(path_start, i, path_end)[2]
            if err is None:
                function_worked = True
                print("---OK---\tQuality found: ", max_vid_quality-m, "  symbol: ", current_quality)
                break
            else:
                current_attempts += 1
                sleep(0.05)

        if function_worked:
            return current_quality, function_worked
        print("--NOTE---\tSearching for a lower quality video")

    return None, False


def find_last_index(path_start='', path_end='', ll=video_start, last_i=video_end,
                    rl=video_end, last_num_of_retry_attempts=num_of_retry_attempts):
    last_num_of_retry_attempts = int(last_num_of_retry_attempts / 4)
    if last_num_of_retry_attempts < 1:
        last_num_of_retry_attempts = 1

    print("--NOTE---\tWorking to find the video last index, starting from {}".format(last_i))

    # Narrowing the search if history exists [2^(5.5)]
    if last_i != rl:
        print(" --> ", last_i, end='')
        current_attempts = 0
        # Try to collect data chunk
        while current_attempts < last_num_of_retry_attempts:
            err = working(path_start, str(last_i), path_end)[2]
            if err is None:
                ll = last_i
                last_i = int(min(((ll + rl)/2), last_i+45))
                break
            else:
                current_attempts += 1
                sleep(0.05)
        if current_attempts >= last_num_of_retry_attempts:
            rl = last_i
            last_i = int(max(((ll + rl) / 2), last_i - 45))

    # Binary search
    while rl > ll+1:
        print(" --> ", last_i, end='')
        current_attempts = 0
        # Try to collect data chunk
        while current_attempts < last_num_of_retry_attempts:
            err = working(path_start, str(last_i), path_end)[2]
            if err is None:
                ll = last_i
                break
            else:
                current_attempts += 1
                sleep(0.05)
        if current_attempts >= last_num_of_retry_attempts:
            rl = last_i
        last_i = int((ll + rl) / 2)
    print("\n---OK---\tLast index found: ", ll)
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
                print("--NOTE---\tverify current_attempts: ", current_attempts, " \t i: ", i)
                print(err)
                print(path_start + i + path_end)
                current_attempts += 1
                sleep(0.1)
        if current_attempts >= verify_num_of_retry_attempts:
            return False
    return True


def saving(save_final=None, s_j=0, save_start_index=start_index, save_file_name=file_name):
    saved = False
    if save_final is not None:
        file = save_file_name + "_" + str(save_start_index + s_j)
        saved = True
        try:
            open(file + extension, 'wb').write(save_final)
        except OSError as err:
            print("---Warning---\tOS error: {0}".format(err))
            saved = False
        except ValueError:
            print("---Warning---\tValueError")
            saved = False
        if saved is True:
            print("---OK---\tSaved: ", file)
    if saved is False:
        print("---ERROR---\tCould not save the video")


def run():
    global r, URL, final, last_index

    for j in range(looping):
        final = None
        print("---OK---\tStart loop video [{0} out of {1}], video index {2}, ".format(j+1, looping, start_index+j))

        # Correct current URL
        if looping > 1:
            start, end, found_quality, url_succeed = url_handler(URL[j], j)
            if url_succeed is False:
                continue
        elif isinstance(URL, list):
            URL = URL[0]
            start, end, found_quality, url_succeed = url_handler(URL, j)
        else:
            start, end, found_quality, url_succeed = url_handler(URL, j)
            if url_succeed is False:
                continue
        if found_quality not in [quality_low, quality_medium, quality_high, quality_very_high]:
            print("---Warning---\tYour video has different settings than default settings")

        auto_find_quality, quality_function_found = find_quality(path_start=start, path_end=end)
        if quality_function_found is True:
            found_quality = auto_find_quality
        start = start + found_quality + split_text_c

        last_index = find_last_index(path_start=start, path_end=end, last_i=last_index)
        if not verify_indices(path_start=start, path_end=end, verify_end=last_index):
            print("---ERROR---\tCould not find video index start/end for video {0}".format(j))
            continue

        # Based for OpenU video streaming
        # Collect all chunks of data, each chunk is ~2mb for high quality
        # 1100 chunks is a few min more than ~3hrs video
        # Adjust the range of the loop to extend your max video length
        j_index_url_list = [start+str(i)+end for i in range(video_start, last_index+1)]
        total_len = len(j_index_url_list)
        completed = [None]*total_len
        j_index_retry_list = []
        last_o = 0
        retries = 1
        pool_size = pool
        loop_iteration = ceil(total_len / pool)

        for o in range(loop_iteration):
            if last_o+pool_size > total_len - 1:
                pool_size = total_len-last_o-1
            results = ThreadPool(pool_size).imap_unordered(parallel_worker, j_index_url_list[last_o:last_o + pool_size])
            for r, w_path, failures in results:
                i_index = int(w_path[len(start): -len(end)])
                if failures is None:
                    completed[i_index-video_start] = r
                else:
                    j_index_retry_list.append(w_path)
                    print("\n--NOTE---\tFailed: ", i_index)

            last_o = last_o+pool_size
            percentage = round((100*(o+1))/loop_iteration, 1)
            if percentage > 100:
                percentage = 100
            print("--NOTE---\tFirst stage {} % completed".format(percentage))

        while len(j_index_retry_list) > 0 and retries < num_of_retry_attempts:
            print("--NOTE---\tRetries: ", retries)
            j_index_url_list = j_index_retry_list
            total_len = len(j_index_url_list)
            j_index_retry_list = []
            last_o = 0
            retries += 1
            pool_size = pool
            loop_iteration = ceil(total_len / pool)

            for o in range(loop_iteration):
                if last_o + pool_size > total_len - 1:
                    pool_size = total_len - last_o - 1

                results = ThreadPool(pool_size).imap_unordered(parallel_worker, j_index_url_list[last_o:last_o + pool_size])
                sleep(10)
                for r, w_path, failures in results:
                    i_index = int(w_path[len(start): -len(end)])
                    if failures is None:
                        completed[i_index-video_start] = r
                    else:
                        j_index_retry_list.append(w_path)
                        print("\n--NOTE---\tFailed: ", i_index)

                last_o = last_o + pool_size
        if retries >= num_of_retry_attempts:
            print("---ERROR---\tRetries >= num_of_retry_attempts")
            break
        if len(j_index_retry_list) == 0:
            print("---OK---\tDownload succeeded, appending parts")
            total = len(completed) - 1
            while completed[total] is None:
                total -= 1
            if any(x is None for x in completed[:total+1]):
                print("---ERROR---\tAuto correction for missing parts, before: {}".format(total), end='')
                completed = [x for x in completed if x is not None]
                total = len(completed) - 1
                print(" --> after: {}".format(total))

            final = completed[0]
            for t in range(1, total+1):
                final += completed[t]
            print("---OK---\tSaving")
            saving(save_final=final, s_j=j)
        else:
            print("---ERROR---\twith saving the video, check the following parts:\n")
            for i in j_index_retry_list:
                print(i, " ", end='')
            print("\n\n")
