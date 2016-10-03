"""
Copyright (c) 2016, Neeraj Prasad
 All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
- Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
- Neither the name of the 'incremental' nor the names of its contributors may
  be used to endorse or promote products derived from this software without
  specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
THE POSSIBILITY OF SUCH DAMAGE."""

import os
import sys
import subprocess
import shlex
import time
import datetime 
import select

class ProcessUnderMonitor:
    def __init__(self):
        pass

    def read_stdout_logs(self, proc, retVal=''): 
        retVal=[]
        while (select.select([proc.stdout],[],[],0)[0]!=[]):   
            retVal+=proc.stdout.read(1)
        return retVal

    def monitor_command(self, command, timeout):
        process=subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
        count=0
        max_count=timeout
        status=0
        while True:
            n=process.poll()
            if n is not None:
                print "Closing monitoring"
                return status

            logs = self.read_stdout_logs(process)
            if logs:
                print ''.join(logs)
            time.sleep(1)
            count +=1
            if (count >= max_count):
                status=1
                process.kill()
                print "process killed"
                time.sleep(1)
                return status

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print len(sys.argv)
        print "Correct Usage: process_under_monitor.py <command> <timedout> <max_retry>"
        exit(0)
        
    monitor = ProcessUnderMonitor()
    max_retry = int(sys.argv[3])
    retry_count = 0
    while (retry_count <= max_retry):
        status = monitor.monitor_command(sys.argv[1], int(sys.argv[2]))
        if (status == 0):
            break
        retry_count += 1
        if (retry_count >= max_retry):
            print "Max retry done, exiting now"
            exit(0)
        time.sleep(1)        
