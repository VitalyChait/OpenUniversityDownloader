import time
import os
import requests
import sys

# Change these every time you run the script
file_name = "Complexity_"
extension = ".mp4"
start_index = 1
save_dir = r"C:\Users\vital\Desktop\uni\complexity"
URL = ["https://souvod.bynetcdn.com/vod/smil:vod/openu/PRV6/qfBJ7oIgYi/App/qfBJ7oIgYi_10.smil/media_b1800000_1.ts?md5=VWeTAL7PMR6i-G2aK9Yeyw&expires=1619825726",
       "https://souvod.bynetcdn.com/vod/smil:vod/openu/PRV6/In8ZkcRnGm/App/In8ZkcRnGm_10.smil/media_b1800000_1.ts?md5=hHD5rQa5ZgFqAOxjq0nrdg&expires=1619825747",
       "https://souvod.bynetcdn.com/vod/smil:vod/openu/PRV3/AjGudSpQI1/App/AjGudSpQI1_10.smil/media_b1800000_2.ts?md5=dIGaMSWo_xQ9jtAxG0-Mzg&expires=1619825766",
       "https://souvod.bynetcdn.com/vod/smil:vod/openu/PRV10/2Vop2rIxJR/App/2Vop2rIxJR_10.smil/media_b1800000_0.ts?md5=of_W2f7OC-5tpY1aNFqxmQ&expires=1619825785"]




# Save the output in the relevant directory
os.chdir(save_dir)

# Number of attempts to reconnect
max_num_of_reconnect_attempts = 3
split_text_a = "media_b1800000_"
split_text_b = ".ts"

if isinstance(URL, list):
    if len(URL[0].split(split_text_a)) < 2:
        print("ERROR with split_text_a variable")
        exit()
    if len(URL[0].split(split_text_b)) < 2:
        print("ERROR with split_text_a variable")
        exit()
    # URL handling
    start = URL[0].split(split_text_a)[0] + split_text_a
    end = ".ts" + URL[0].split(split_text_b)[1]
    looping = len(URL)

else:
    if len(URL.split(split_text_a)) < 2:
        print("ERROR with split_text_a variable")
        exit()
    if len(URL.split(split_text_b)) < 2:
        print("ERROR with split_text_a variable")
        exit()
    start = URL.split(split_text_a) + split_text_a
    end = ".ts" + URL.split(split_text_b)
    looping = 1


# First iteration
try:
    r = requests.get(start + '0' + end, allow_redirects=True)
    r.raise_for_status()
except requests.HTTPError as exception:
    print("Failed during the first attempt, please check the URL manually")
    print("exception: ", exception)
    exit()
final = r.content

for j in range(looping):
    print("start loop number {0}".format(j))
    if looping>1:
        current_url = URL[j]
        if len(current_url.split(split_text_a)) < 2:
            print("ERROR with split_text_a variable")
            exit()
        if len(current_url.split(split_text_b)) < 2:
            print("ERROR with split_text_a variable")
            exit()
        # URL handling
        start = current_url.split(split_text_a)[0] + split_text_a
        end = ".ts" + current_url.split(split_text_b)[1]

        try:
            r = requests.get(start + '0' + end, allow_redirects=True)
            r.raise_for_status()
        except requests.HTTPError as exception:
            print("Failed during the first attempt, please check the URL manually")
            print("exception: ", exception)
            exit()
        final = r.content

    # Based for OpenU video streaming
    # Collect all chunks of data, each chunk is ~1mb
    # 1100 chunks is a few min more than ~3hrs video
    # Adjust the range of the loop to extend your max video length
    for i in range(1, 1100):
        succeed = False
        current_attempts = 0
        # Try to collect data chunk
        while succeed is False and current_attempts < max_num_of_reconnect_attempts:
            memory = current_attempts
            try:
                r = requests.get(start + str(i) + end, allow_redirects=True)
                r.raise_for_status()
            except requests.HTTPError as exception:
                print("Failure during the {} chunk".format(i))
                print("Exception:\t", exception)
                current_attempts = current_attempts+1
            if memory == current_attempts:
                succeed = True
            elif current_attempts<max_num_of_reconnect_attempts:
                print("Retrying attempt, {} out of {}".format(current_attempts+1, max_num_of_reconnect_attempts))
                time.sleep(0.5)
        if current_attempts >= max_num_of_reconnect_attempts:
            break
        final = final+r.content
        print("loop number " + str(i) + " is done")

    print("Collecting the data is done, processing the information")
    try:
        open(file_name+"_{0}".format(str(start_index+j))+extension, 'wb').write(final)
    except OSError as err:
        print("OS error: {0}".format(err))
    except ValueError:
        print("ValueError")
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    print("Done, Remaning loops: {0}".format(looping-j-1))
