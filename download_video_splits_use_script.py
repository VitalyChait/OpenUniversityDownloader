import time
import os
import requests
import sys

# Change these every time you run the script
file_name = "DEV_"
extension = ".mp4"
start_index = 6
save_dir = r"C:\Users\vital\Desktop\uni\dev"
URL = ["https://souvod.bynetcdn.com/vod/smil:vod/openu/PRV10/ZvvDvCP0M5/App/ZvvDvCP0M5_10.smil/media_b1800000_299.ts?md5=Q1VIf_bF6NkF6t_L8o4PKA&expires=1619918193",
       "https://souvod.bynetcdn.com/vod/smil:vod/openu/PRV6/qmgKd6Q0C6/App/qmgKd6Q0C6_10.smil/media_b1800000_53.ts?md5=Q6O0kBRKy2uFH2XHvp0gwg&expires=1619918269",
       "https://souvod.bynetcdn.com/vod/smil:vod/openu/PRV3/PIW3JpOXkC/App/PIW3JpOXkC_10.smil/media_b1800000_65.ts?md5=eeMxEMMhj2D-RAIS-ENI3A&expires=1619918316"]




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

split_vid = False
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
        if i>149 and i%150 == 0:
            try:
                open(file_name + "_{0}_part{1}".format(str(start_index + j), str(int(i/150))) + extension, 'wb').write(final)
            except OSError as err:
                print("OS error: {0}".format(err))
            except ValueError:
                print("ValueError")
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
            split_vid = True

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
            if i>100:
                print("Did not finish the entire video download")
                try:
                    open(file_name + "_{0}_part{1}".format(str(start_index + j), str(int(i / 150))) + extension, 'wb').write(final)
                except OSError as err:
                    print("OS error: {0}".format(err))
                except ValueError:
                    print("ValueError")
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    raise
            break
        if split_vid == True:
            final = r.content
            split_vid = False
        else:
            final = final+r.content
        print("loop number " + str(i) + " is done")

    # print("Collecting the data is done, processing the information")
    # try:
    #     open(file_name+"_{0}".format(str(start_index+j))+extension, 'wb').write(final)
    # except OSError as err:
    #     print("OS error: {0}".format(err))
    # except ValueError:
    #     print("ValueError")
    # except:
    #     print("Unexpected error:", sys.exc_info()[0])
    #     raise

    print("Done, Remaning loops: {0}".format(looping-j-1))