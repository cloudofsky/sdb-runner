#!/usr/bin/env python
import os
import sys
import csv

# After collecting target binaries
LOCAL_HOME = "."
LOCAL_BINARY = os.path.join(LOCAL_HOME, "BINARY")
LOCAL_OUTPUT = os.path.join(LOCAL_HOME, "OUTPUT")
LOCAL_INPUT = os.path.join(LOCAL_HOME, "INPUT")
LOCAL_CSV = os.path.join(LOCAL_HOME, "binarylist.csv")
DEVICE_HOME = "/opt/usr/armtracer_test"
DEVICE_BINARY = os.path.join(DEVICE_HOME, "BINARY")
DEVICE_INPUT = os.path.join(DEVICE_HOME, "INPUT")
DEVICE_OUTPUT = os.path.join (DEVICE_HOME, "OUTPUT")

def execute_cmd(cmd):
  print cmd
  os.system(cmd)

def dir_init():
  sdb_cmd = "sdb shell "
  cmd = sdb_cmd + "mkdir -p " + DEVICE_BINARY
  execute_cmd(cmd)
  cmd = sdb_cmd + "mkdir -p " + DEVICE_OUTPUT
  execute_cmd(cmd)
  cmd = "mkdir -p " + LOCAL_BINARY
  execute_cmd(cmd)
  cmd = "mkdir -p " + LOCAL_OUTPUT
  execute_cmd(cmd)

def get_binary_from_tizen_dir():
  pass

def create_input():
  #tmp_file = "INPUT"
  #f = (tmp_file, 'w')
  # input contents
  #f.close()
  #cmd = "sdb push " + tmp_file + " " + DEVICE_INPUT
  cmd = "sdb shell touch " + DEVICE_INPUT
  execute_cmd(cmd)
  pass
  
def push_binary(binary):
  local_binary = os.path.join(LOCAL_BINARY, binary)
  cmd = "sdb push " + local_binary + " " + DEVICE_BINARY
  execute_cmd(cmd)
  pass

def push_input():
  cmd = "sdb push " + LOCAL_INPUT + " " + DEVICE_INPUT
  execute_cmd(cmd)
  pass

def run_armtracer(armtracer, target_name, target_arg):
  dev_binary = os.path.join(DEVICE_BINARY, target_name)
  dev_output = os.path.join(DEVICE_OUTPUT, target_name + ".trace")
  cmd = "sdb shell " + armtracer + " -tf " + dev_output + ' ' + dev_binary + ' ' + target_arg
  execute_cmd(cmd)
  pass

def pull_output(binary):
  dev_output = os.path.join(DEVICE_OUTPUT, binary + ".trace")
  cmd = "sdb pull " + dev_output + " " + LOCAL_OUTPUT 
  execute_cmd(cmd)
  pass

def rm_output(output_path):
  cmd = "sdb shell rm " + output_path
  execute_cmd(cmd)
  pass

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print "argv[1] : armtracer path on device\n"
    exit(1)
  armtracer = sys.argv[1]  
  dir_init()
  push_input()
  f = open(LOCAL_CSV, 'r')
  rdr = csv.reader(f)
  for line in rdr:
    binary = line[0]
    arg = line[1].replace("@@", os.path.join(DEVICE_INPUT, "input"))
    print "[", binary, "]"
    push_binary(binary)
    run_armtracer(armtracer, binary, arg)
    # pull_output(binary)
    # rm_output(binary)
  f.close()
  base_path = os.path.dirname(armtracer)
  cmd = "sdb shell rm " + base_path + "/*.core"
  execute_cmd(cmd)

