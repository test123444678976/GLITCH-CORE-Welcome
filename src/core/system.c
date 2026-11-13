#include "system.h"
#include <sys/utsname.h>
#include <sys/sysinfo.h>

const char *glitch_kernel_release(void) {
    static struct utsname info;
    return uname(&info) == 0 ? info.release : "Unknown";
}

const char *glitch_machine(void) {
    static struct utsname info;
    return uname(&info) == 0 ? info.machine : "Unknown";
}

long glitch_total_memory_mb(void) {
    struct sysinfo info;
    if (sysinfo(&info) != 0) return -1;
    return (long)((unsigned long long)info.totalram * info.mem_unit / (1024ULL * 1024ULL));
}
