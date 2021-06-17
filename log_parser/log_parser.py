# --------------------------------------
# Script for parsing the nginx log file.
# Author: Somesh Kumar Prajapati
# --------------------------------------

"""
Example log lines:
13.66.139.0 - - [19/Dec/2020:13:57:26 +0100] "GET /index.php?option=com_phocagallery&view=category&id=1:almhuette-raith&Itemid=53 HTTP/1.1" 200 32653 "-" "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)" "-"
157.48.153.185 - - [19/Dec/2020:14:08:08 +0100] "GET /favicon.ico HTTP/1.1" 404 217 "http://www.almhuette-raith.at/apache-log/access.log" "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36" "-"

Perform the below tasks using the input sample log file:
----------------------------------------------------------------------------
1. Top 10 requested pages and the number of requests made for each
2. Percentage of successful requests (anything in the 200s and 300s range)
3. Percentage of unsuccessful requests (anything that is not in the 200s or 300s range)
4. Top 10 unsuccessful page requests
5. The top 10 hosts making the most requests, displaying the IP address and number of requests made.
6. Option parsing to produce only the report for one of the previous points (e.g. only the top 10 urls, only the percentage of successful requests and so on)
7. For each of the top 10 hosts, show the top 5 pages requested and the number of requests for each
"""

import argparse
from utils import exec_cmd_return_output, print_msg

dry_run = False

class BaseAction(object):
    """
    Base class for Log parser.
    """

    def __init__(self, args):
        global dry_run
        dry_run = args.dry_run_flag

        self._args = args
        self.input_file = args.input_file
        dry_run = args.dry_run_flag if args.dry_run_flag else ""

    @classmethod
    def add_args(cls, parser):
        parser.add_argument(
            "-f",
            "--input_file",
            help="Provide the input log file to parse the logs",
            type=str,
            dest="input_file",
            required=True)
        parser.add_argument(
            "-d",
            "--dry-run",
            help="Dry Run of all commands (do not execute)  (default: False)",
            dest="dry_run_flag",
            default=False,
            action="store_true")


class TopRequestedPagesCount(BaseAction):
    """
    Top [N] requested pages and the number of requests made for each page
    """

    def __init__(self, args):
        BaseAction.__init__(self, args)
        self.count_of_top_request = args.count_of_top_request

    @classmethod
    def process_cmd(cls, args):
        action = TopRequestedPagesCount(args)
        action.top_requested_pages_count()

    @classmethod
    def add_parser(cls, sp):
        parser = sp.add_parser("top-requested-pages-count", help="Top [N] requested pages and the number of requests made for each page")
        parser.set_defaults(func=cls.process_cmd)
        BaseAction.add_args(parser)
        parser.add_argument(
            "-n",
            "--count-of-top-request",
            help="Provide the count value N",
            type=int,
            dest="count_of_top_request",
            required=True)

    def top_requested_pages_count(self):
        print_msg("Top [N] requested pages and the number of requests made for each page")
        
        cmd = "awk -F' ' '{}' {} | sort | uniq -c | sort -nr | head -{}".format('{if ($11 !~ /""/ && $11 !~ /"-"/) {print $1, $9, $11}}', self.input_file, self.count_of_top_request)
        print(exec_cmd_return_output(cmd, dry_run))

    
class SuccessfulRequests(BaseAction):
    """
    Calculate percentage of successful requests (anything in the 200s and 300s range)
    """

    def __init__(self, args):
        BaseAction.__init__(self, args)

    @classmethod
    def process_cmd(cls, args):
        action = SuccessfulRequests(args)
        action.successful_requests()

    @classmethod
    def add_parser(cls, sp):
        parser = sp.add_parser("successful-requests", help="Calculate percentage of successful requests")
        parser.set_defaults(func=cls.process_cmd)
        BaseAction.add_args(parser)

    def successful_requests(self):
        print_msg("Percentage of successful requests")

        cmd="cat {} | wc -l".format(self.input_file)
        total_req = exec_cmd_return_output(cmd, dry_run)

        cmd="awk -F' ' '{}' {} | wc -l".format("{if ($9 == 200 || $9 == 300) {print $9}}", self.input_file)
        success = exec_cmd_return_output(cmd, dry_run)

        if not dry_run:
            success_percentage = 100 * float(success)/float(total_req)
            print("Success Percentage: {} %".format(str(success_percentage)))
            print("")


class UnSuccessfulRequests(BaseAction):
    """
    Calculate percentage of unsuccessful requests (anything other than 200s and 300s range)
    """

    def __init__(self, args):
        BaseAction.__init__(self, args)

    @classmethod
    def process_cmd(cls, args):
        action = UnSuccessfulRequests(args)
        action.unsuccessful_requests()

    @classmethod
    def add_parser(cls, sp):
        parser = sp.add_parser("unsuccessful-requests", help="Calculate percentage of unsuccessful requests")
        parser.set_defaults(func=cls.process_cmd)

        BaseAction.add_args(parser)

    def unsuccessful_requests(self):
        print_msg("Percentage of unsuccessful requests")

        cmd="cat {} | wc -l".format(self.input_file)
        total_req = exec_cmd_return_output(cmd, dry_run)

        cmd="awk -F' ' '{}' {} | wc -l".format("{if ($9 != 200 && $9 != 300) {print $9}}", self.input_file)
        unsuccess = exec_cmd_return_output(cmd, dry_run)

        if not dry_run:
            unsuccess_percentage = 100 * float(unsuccess)/float(total_req)
            print("UnSuccess Percentage: {} %".format(str(unsuccess_percentage)))
            print("")


class TopUnsuccessfulPages(BaseAction):
    """
    Top N unsuccessful page requests
    """

    def __init__(self, args):
        BaseAction.__init__(self, args)
        self.count_of_top_unsuccessful = args.count_of_top_unsuccessful

    @classmethod
    def process_cmd(cls, args):
        action = TopUnsuccessfulPages(args)
        action.top_unsuccessful_pages()

    @classmethod
    def add_parser(cls, sp):
        parser = sp.add_parser("top-unsuccessful-pages-count", help="Top N unsuccessful page requests")
        parser.set_defaults(func=cls.process_cmd)

        BaseAction.add_args(parser)
        parser.add_argument(
            "-n",
            "--count-of-top-unsuccessful",
            help="Provide the count value N",
            type=int,
            dest="count_of_top_unsuccessful",
            required=True)

    def top_unsuccessful_pages(self):
        print_msg("Top N unsuccessful pages")
        
        cmd="awk -F' ' '{}' {} | sort | uniq -c | sort -nr | head -{}".format("{if ($9 != 200 && $9 != 300) {print $1, $9, $11}}", self.input_file, self.count_of_top_unsuccessful)
        print(exec_cmd_return_output(cmd, dry_run))


class TopRequestedHostCount(BaseAction):
    """
    Top [N] requested hosts and the number of requests made for each host
    """

    def __init__(self, args):
        BaseAction.__init__(self, args)
        self.count_of_top_request = args.count_of_top_request

    @classmethod
    def process_cmd(cls, args):
        action = TopRequestedHostCount(args)
        action.top_requested_host_count()

    @classmethod
    def add_parser(cls, sp):
        parser = sp.add_parser("top-requested-host-count", help="Top [N] requested pages and the number of requests made for each host")
        parser.set_defaults(func=cls.process_cmd)

        BaseAction.add_args(parser)
        parser.add_argument(
            "-n",
            "--count-of-top-request",
            help="Provide the top N count value",
            type=int,
            dest="count_of_top_request",
            required=True)

    def top_requested_host_count(self):
        print_msg("Top [N] requested hosts and the number of requests made for each host")
        cmd = "awk -F' ' '{}' {} | sort | uniq -c | sort -nr | head -{}".format("{print $1}", self.input_file, self.count_of_top_request)
        print(exec_cmd_return_output(cmd, dry_run))


class TopHostRequestedPage(BaseAction):
    """
    For each of the top [N] hosts, show the top [C] pages requested and the number of requests for each
    """

    def __init__(self, args):
        BaseAction.__init__(self, args)
        self.count_of_top_request = args.count_of_top_request
        self.count_of_page_request = args.count_of_page_request

    @classmethod
    def process_cmd(cls, args):
        action = TopHostRequestedPage(args)
        action.top_host_requested_page()

    @classmethod
    def add_parser(cls, sp):
        parser = sp.add_parser("top-host-requested-page", help="For each of the top [N] hosts, show the top [C] pages requested and the number of requests for each")
        parser.set_defaults(func=cls.process_cmd)

        BaseAction.add_args(parser)
        parser.add_argument(
            "-n",
            "--count-of-top-request",
            help="Provide the count value N",
            type=int,
            dest="count_of_top_request",
            required=True)
        parser.add_argument(
            "-c",
            "--count-of-page-request",
            help="Provide the count value C",
            type=int,
            dest="count_of_page_request",
            required=True)


    def top_host_requested_page(self):
        print_msg("For each of the top [N] hosts, show the top [C] pages requested and the number of requests for each")
        cmd = "awk -F' ' '{}' {} | sort | uniq -c | sort -nr | head -{}".format("{print $1}", self.input_file, self.count_of_top_request)
        print "No of Requests", "IP"
        print(exec_cmd_return_output(cmd, dry_run))

        cmd = "awk -F' ' '{}' {} | sort | uniq -c | sort -nr | awk -F' ' '{}' | head -{}".format("{print $1}", self.input_file, "{print $2}", self.count_of_top_request)
        output = exec_cmd_return_output(cmd, dry_run)

        if not dry_run:
            ips = list(output.split("\n"))
            ips = ips[:-1]

            for line in ips:
                cmd = "grep {} {} | head -{}".format(line, self.input_file, self.count_of_page_request)
                print(exec_cmd_return_output(cmd, dry_run))


def parse_args():
    """ Argument Parser """
    parser = argparse.ArgumentParser(description="Program to run the log parser")

    lp = parser.add_subparsers(title="Log Parser")
    TopRequestedPagesCount.add_parser(lp)
    SuccessfulRequests.add_parser(lp)
    UnSuccessfulRequests.add_parser(lp)
    TopUnsuccessfulPages.add_parser(lp)
    TopRequestedHostCount.add_parser(lp)
    TopHostRequestedPage.add_parser(lp)
    return parser.parse_args()


def main():
    args = parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
