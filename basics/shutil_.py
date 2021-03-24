from shutil import disk_usage

total_b, used_b, free_b = disk_usage('.')
gb = 10 ** 9

print("Total: {:6.2f} Gb".format(total_b / gb))
print("Used: {:6.2f} Gb".format(used_b / gb))
print("Free: {:6.2f} Gb".format(free_b / gb))