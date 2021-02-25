# fhmediacollector

import argparse
from argparse import RawTextHelpFormatter
from datetime import timezone
import datetime
from dotenv import load_dotenv
import json
import os
from pathlib import Path
import requests
from requests.auth import HTTPBasicAuth
import sys
from time import sleep
import uuid

CLI_ART = r"""   __ _               _ _           _             
  / _| |__   ___ ___ | | | ___  ___| |_ ___  _ __ 
 | |_| '_ \ / __/ _ \| | |/ _ \/ __| __/ _ \| '__|
 |  _| | | | (_| (_) | | |  __/ (__| || (_) | |   
 |_| |_| |_|\___\___/|_|_|\___|\___|\__\___/|_|   

"""

CLI_INTRO_TEXT = "\n".join([
    # "=" * 50,
    CLI_ART,
    "\tAuthor: \tOddPawsX",
    "\tDiscord: \tOddPawsX#6969",
    "\tVersion: \tv1.1.4",
    "\n",
    "=" * 50
])

USER_AGENT = "fhmediacollector/1.1.4"

DEFAULT_ENV_FILE_CONTENT = """# DEFAULT fhcollector env file
E621_USERNAME=
E621_API_KEY=
"""

# Define e621 class
class E621:
    posts_per_page = 50
    posts_api = "https://e621.net/posts.json?limit={}".format(posts_per_page)
    headers = {
        "User-Agent": USER_AGENT
    }
    def __init__(self,
                 username,
                 api_key,
                 allowed_ratings=["s", "q", "e"],
                 avoid_list=[]
                ):
        self.username = username
        self.api_key = api_key
        self.allowed_ratings = allowed_ratings
        self.runid = str(uuid.uuid4())
        self.avoid_list = avoid_list
    def download_post(self, post, dest):
        d = Path(dest)
        rating = post["rating"]
        fname = "[{score}][{artist}][{id}][{c}][{a}] {oname}"
        artist = ""
        c_flag = "C" if "cum" in post["tags"]["general"] else "D"
        a_flag = "A" if "animated" in post["tags"]["meta"] else "S"
        if type(post["tags"]["artist"]) is str:
            artist = post["tags"]["artist"]
        else:
            artist = "+".join(post["tags"]["artist"])
        oname = post["file"]["url"].split("/")[-1]
        fname = fname.format(
            score=post["score"]["total"],
            artist=artist,
            id=post["id"],
            oname=oname,
            c=c_flag,
            a=a_flag
        )
        if not Path.is_dir(d):
            Path.mkdir(d)
        d = Path(d / self.runid)
        if not Path.is_dir(d):
            Path.mkdir(d)
        rd = Path(d / rating)
        if not Path.is_dir(rd):
            Path.mkdir(rd)
        dest_img_path = Path(rd / fname)
        if dest_img_path.is_file():
            print("Skipping '{}', downloaded by another search"
                  "in this run already.".format(fname))
            return False
        else:
            with open(dest_img_path, "wb") as handle:
                if self.username is not None and self.api_key is not None:
                    response = requests.get(post["file"]["url"],
                                            stream=True,
                                            headers=self.headers,
                                            auth=HTTPBasicAuth(self.username, self.api_key))
                else:
                    response = requests.get(post["file"]["url"],
                                            stream=True,
                                            headers=self.headers)
                if not response.ok:
                    print(response)
                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)
            print("Downloaded '{}'.".format(fname))
            return True
    def get_posts(self, tags):
        if "s" not in self.allowed_ratings:
            tags += " -rating:s"
        if "q" not in self.allowed_ratings:
            tags += " -rating:q"
        if "e" not in self.allowed_ratings:
            tags += " -rating:e"
        if len(self.avoid_list) > 0:
            tags += " -" + " -".join(self.avoid_list)
        api_call_url = self.posts_api + "&tags=" + \
                       "+".join(tags.split()) + \
                       "{}"
        posts = []
        if self.username is not None and self.api_key is not None:
            r = requests.get(api_call_url.format(""),
                            headers=self.headers,
                            auth=HTTPBasicAuth(self.username, self.api_key))
        else:
            r = requests.get(api_call_url.format(""),
                            headers=self.headers)
        posts_tmp = r.json()["posts"]
        posts.extend(posts_tmp)
        page = 2
        while len(posts_tmp) >= 50:
            sleep(0.5)
            if self.username is not None and self.api_key is not None:
                r = requests.get(api_call_url.format(
                                "&page={}".format(page)),
                                 headers=self.headers,
                                 auth=HTTPBasicAuth(self.username,
                                                    self.api_key))
            else:
                r = requests.get(api_call_url.format(
                                "&page={}".format(page)),
                                 headers=self.headers)
            posts_tmp = r.json()["posts"]
            if len(posts_tmp) == 0:
                break
            for post in posts_tmp:
                if post not in posts:
                    posts.append(post)
            page += 1
        return posts


# Define errors
class MultipleSearchMethodsException(Exception):
    """Exception raised when search is specified both inline and from file

    Attributes:
        fpath   -- file path specified
        search  -- inline search specified
        message -- explanation of the error
    """

    def __init__(self,
                 search,
                 fpath,
                 message="Cannot specify both inline search [-s]"
                         " \"{}\" and search file [-f] at {}."):
        self.fpath = fpath
        self.search = search
        self.message = message
        super().__init__(self.message.format(search, fpath))

class NoSearchMethodSpecifiedException(Exception):
    """Exception raised when no search is provided

    Attributes:
        message -- explanation of the error
    """

    def __init__(self,
                 message="No search method specified. Please use inline [-s]"
                         " or search file [-f]. Use [-h] for help. "):
        self.message = message
        super().__init__(self.message)

class ConfigFileDoesNotExistException(Exception):
    """Exception raised when config file does not exist at the path

    Attributes:
        fpath   -- file path specified
        message -- explanation of the error
    """

    def __init__(self,
                 fpath,
                 message="Config file [-c] \"{}\" does not exist on disk. "
                         "Please create the file or fill out the details in"
                         " ~/.fhcollector.env"):
        self.fpath = fpath
        self.message = message
        super().__init__(self.message.format(fpath))

class FileDoesNotExistException(Exception):
    """Exception raised when file does not exist at the path

    Attributes:
        fpath   -- file path specified
        message -- explanation of the error
    """

    def __init__(self,
                 fpath,
                 message="File [-c] \"{}\" does not exist on disk. "
                         "Please create the file or omit the option."):
        self.fpath = fpath
        self.message = message
        super().__init__(self.message.format(fpath))

class ConfigFileMissingValueException(Exception):
    """Exception raised when config file does not contain a required value

    Attributes:
        fpath   -- file path specified
        var     -- var not defined
        message -- explanation of the error
    """

    def __init__(self,
                 fpath,
                 var,
                 message="Config file [-c] \"{}\" is missing a required value."
                         " Please ensure config variable {} is set."):
        self.fpath = fpath
        self.var = var
        self.message = message
        super().__init__(self.message.format(fpath, var))

# Create default env file if it doesn't exist
def setup_env_file():
    default_env_file_path = Path.home() / ".fhcollector.env"
    if not (default_env_file_path).is_file():
        with open(default_env_file_path, "w") as f:
            f.write(DEFAULT_ENV_FILE_CONTENT)


# CLI function
def cli():
    print(CLI_INTRO_TEXT)

    parser = argparse.ArgumentParser(
        description='Gathers posts from e621 matching the specified tags,\n'
                    ' then organizes for ease in video/slideshow creation.',
        formatter_class=RawTextHelpFormatter
    )
    parser.add_argument('--search',
                        '-s',
                        required=False,
                        type=str,
                        help="The e621 search string to use")
    parser.add_argument('--searchconf',
                        '-f',
                        required=False,
                        type=Path,
                        help="Path to a file containing multiple "
                             "e621 search strings")
    parser.add_argument('--config', '-c',
                        required=False,
                        type=Path,
                        default=Path.home() / ".fhcollector.env",
                        help="Path to env file with config variables. "
                             "Default: ~/.fhcollector.env")
    parser.add_argument('--avoid', '-a',
                        required=False,
                        type=Path,
                        help="Path to file with list of tags to avoid. "
                             "One per line. ")
    parser.add_argument('--no-safe',
                        dest='exclude_safe',
                        action='store_true',
                        help="If present, exclude posts with the "
                             "rating 'safe'")
    parser.add_argument('--no-questionable',
                        dest='exclude_questionable',
                        action='store_true',
                        help="If present, exclude posts with the "
                             "rating 'questionable'")
    parser.add_argument('--no-explicit',
                        dest='exclude_explicit',
                        action='store_true',
                        help="If present, exclude posts with the "
                             "rating 'explicit'")
    parser.add_argument('--no-api-key', '-l',
                        dest='no_api_key',
                        action='store_true',
                        help="If present, make requests to e621 "
                             "without API key")
    parser.set_defaults(exclude_safe=False,
                        exclude_questionable=False,
                        exclude_explicit=False, # include all by default
                        no_api_key=False) # use api with key by default
    parser.add_argument('--version', action='version', version='%(prog)s 1.1.4')
    args = parser.parse_args()

    if not args.no_api_key:
        setup_env_file()

    ratings = ["s", "q", "e"]
    if args.exclude_safe:
        ratings.pop(ratings.index("s"))
    if args.exclude_questionable:
        ratings.pop(ratings.index("q"))
    if args.exclude_explicit:
        ratings.pop(ratings.index("e"))
    try:
        if len(ratings) == 0:
            raise ValueError("You must let at least one rating through!")
    except Exception as e:
        print("ERROR: {}".format(e))
        sys.exit(1)

    searches = []
    avoid_list = []

    # check for conflicting input methods
    try:
        if not args.search and not args.searchconf:
            raise NoSearchMethodSpecifiedException()
        elif args.search and args.searchconf:
            raise MultipleSearchMethodsException(args.search, args.searchconf)
        elif args.searchconf:
            with open(args.searchconf, "r") as f:
                searches = f.read().splitlines()
        else:
            searches = [args.search]
    except Exception as e:
        print("ERROR: {}".format(e))
        sys.exit(1)

    # Print current configuration
    print("Current Configuration:")
    print("-" * 50)
    print("Allowed ratings: {}".format(ratings))
    credentialed = None
    if not args.no_api_key:
        credentialed = True
        print("CONF FILE: \t{}".format(args.config))
        env_path = Path(args.config)
        try:
            if not env_path.is_file():
                raise ConfigFileDoesNotExistException(env_path)
            if args.avoid and not args.avoid.is_file():
                raise FileDoesNotExistException(args.avoid)
        except Exception as e:
            print("ERROR: {}".format(e))
            sys.exit(1)
        load_dotenv(dotenv_path=env_path)

        try:
            for required_var in ["E621_USERNAME", "E621_API_KEY"]:
                if os.environ[required_var] == "":
                    raise ConfigFileMissingValueException(env_path, required_var)
        except Exception as e:
            print("ERROR: {}".format(e))
            sys.exit(1)

        # preview the creds
        print("Username: \t{}".format(os.environ["E621_USERNAME"]))
        print("API Key: \t{}".format(os.environ["E621_API_KEY"][:3] +
            ("*"*(len(os.environ["E621_API_KEY"])-3))))
        print("-" * 50)
    else:
        print("Not using API Key.")
        credentialed = False

    try:
        if args.avoid:
            with open(args.avoid, "r") as f:
                avoid_list.extend(f.read().splitlines())
        for item in avoid_list:
            if len(item) == 0:
                raise ValueError("Please remove blank line from "
                                 "{}: {}".format(args.avoid, avoid_list))
    except Exception as e:
        print("ERROR: {}".format(e))
        sys.exit(1)

    print("Tags to avoid: {}".format(avoid_list))
    print("-" * 50)

    # Create e621 object
    if credentialed:
        e621 = E621(os.environ["E621_USERNAME"],
                    os.environ["E621_API_KEY"],
                    allowed_ratings=ratings,
                    avoid_list=avoid_list)
    else:
        e621 = E621(None, None,
                    allowed_ratings=ratings,
                    avoid_list=avoid_list)

    print("Run ID: {}".format(e621.runid))
    print("-" * 50)

    start_time = datetime.datetime.now().isoformat()

    metadata_file_contents = "=== fhmediacollector ==="
    metadata_file_contents += "\n"
    metadata_file_contents += "RUN: {}".format(e621.runid)
    metadata_file_contents += "\n"
    metadata_file_contents += " at {}".format(start_time)
    metadata_file_contents += "\n"
    metadata_file_contents += "Ratings Enabled: {}".format(ratings)
    metadata_file_contents += "\n"
    metadata_file_contents += "Avoiding Tags: {}".format(avoid_list)
    metadata_file_contents += "\n"
    metadata_file_contents += "Searches performed: "
    metadata_file_contents += "\n"

    dst_dir = "fhcollected"
    downloaded_count = 0

    # Do search(es)
    for search in searches:
        print("Performing search \"{}\":".format(search))
        metadata_file_contents += " - {}\n".format(search)
        posts = e621.get_posts(search)
        if len(posts) == 0:
            print("No posts matched the search")
            continue
        metadata_file_contents += "   - {} posts\n".format(len(posts))
        for post in posts:
            try:
                dlresult = e621.download_post(post, dst_dir)
                if dlresult:
                    downloaded_count += 1
                sleep(0.5)
            except Exception as e:
                # print("ERROR: {}... caused by:".format(e))
                # print(post)
                print("Unable to download post {}. "
                      "You may need to be logged in to view. "
                      "Use API key to download.".format(post['id']))
    
    metadata_file_contents += "Total images downloaded: {}".format(downloaded_count)
    metadata_file_contents += "\n"

    try:
        with open(Path(dst_dir + "/" + e621.runid + "/" + 
                "{}_meta.txt".format(e621.runid)), "w") as f:
            f.write(metadata_file_contents)
    except FileNotFoundError as e:
        sys.exit(1)

    print("\n")
    print("-"*50)
    print("DONE. Downloaded {} pieces of media. Check the {} folder.".format(
        downloaded_count,
        dst_dir
    ))


if __name__ == "__main__":
    cli()
