#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

#ifdef _WIN32
#include <windows.h>
#include <conio.h>
#include <io.h>

HANDLE hChildProcess = NULL;
HANDLE hPipeIn = NULL;
HANDLE hPipeOut = NULL;

void setup_windows_terminal() {
    // Create pipes for communication with the child process
    SECURITY_ATTRIBUTES sa;
    sa.nLength = sizeof(SECURITY_ATTRIBUTES);
    sa.bInheritHandle = TRUE;
    sa.lpSecurityDescriptor = NULL;

    CreatePipe(&hPipeOut, &hPipeIn, &sa, 0);
    SetHandleInformation(hPipeOut, HANDLE_FLAG_INHERIT, 0);

    // Create a child process to run the shell
    PROCESS_INFORMATION pi;
    STARTUPINFO si;
    ZeroMemory(&si, sizeof(STARTUPINFO));
    si.cb = sizeof(STARTUPINFO);
    si.hStdInput = hPipeIn;
    si.hStdOutput = GetStdHandle(STD_OUTPUT_HANDLE);
    si.hStdError = GetStdHandle(STD_ERROR_HANDLE);
    si.dwFlags |= STARTF_USESTDHANDLES;

    char cmd[] = "cmd.exe";
    if (!CreateProcess(NULL, cmd, NULL, NULL, TRUE, 0, NULL, NULL, &si, &pi)) {
        fprintf(stderr, "CreateProcess failed (%d)\n", GetLastError());
        exit(EXIT_FAILURE);
    }
    hChildProcess = pi.hProcess;
    CloseHandle(pi.hThread);
}

void cleanup_windows_terminal() {
    CloseHandle(hPipeIn);
    CloseHandle(hPipeOut);
    TerminateProcess(hChildProcess, 0);
    CloseHandle(hChildProcess);
}

#else // Unix-like systems
#include <pty.h>
#include <ncurses.h>
#include <signal.h>
#include <sys/wait.h>

int master_fd;

void setup_unix_terminal(pid_t *child_pid) {
    struct winsize ws = {24, 80, 0, 0}; // Set window size
    *child_pid = forkpty(&master_fd, NULL, NULL, &ws);
    if (*child_pid == -1) {
        perror("forkpty");
        exit(EXIT_FAILURE);
    } else if (*child_pid == 0) {
        execlp("/bin/bash", "/bin/bash", NULL); // Start a shell
        perror("execlp");
        exit(EXIT_FAILURE);
    }
}

void handle_resize(int signo) {
    if (signo == SIGWINCH) {
        // Handle window resize
        struct winsize ws;
        ioctl(STDOUT_FILENO, TIOCGWINSZ, &ws);
        // Resize terminal
    }
}
#endif

void init_colors() {
    if (has_colors() == FALSE) {
        endwin();
        fprintf(stderr, "Your terminal does not support color\n");
        exit(1);
    }
    start_color();
    init_pair(1, COLOR_GREEN, COLOR_BLACK); // Define a color pair
}

int main() {
#ifdef _WIN32
    setup_windows_terminal();
#else
    pid_t child_pid;
    setup_unix_terminal(&child_pid);
    signal(SIGWINCH, handle_resize); // Handle window resize
#endif

    initscr();            // Initialize ncurses
    raw();                // Line buffering disabled
    keypad(stdscr, TRUE); // Enable special keys
    noecho();             // Don't echo input characters

    init_colors();
    attron(COLOR_PAIR(1)); // Use the color pair

    char buffer[256];
    int nbytes;

    while (1) {
        fd_set rfds;
        FD_ZERO(&rfds);

#ifdef _WIN32
        HANDLE handles[2] = {hPipeOut, GetStdHandle(STD_INPUT_HANDLE)};
        DWORD waitResult = WaitForMultipleObjects(2, handles, FALSE, INFINITE);

        if (waitResult == WAIT_OBJECT_0) {
            // Read from child process output
            DWORD bytesRead;
            ReadFile(hPipeOut, buffer, sizeof(buffer) - 1, &bytesRead, NULL);
            if (bytesRead > 0) {
                buffer[bytesRead] = '\0';
                printw("%s", buffer);
                refresh();
            }
        } else if (waitResult == WAIT_OBJECT_0 + 1) {
            // Read from standard input
            if (_kbhit()) {
                int ch = _getch();
                buffer[0] = ch;
                DWORD bytesWritten;
                WriteFile(hPipeIn, buffer, 1, &bytesWritten, NULL);
            }
        }
#else
        FD_SET(master_fd, &rfds);
        FD_SET(STDIN_FILENO, &rfds);
        int nfds = (master_fd > STDIN_FILENO ? master_fd : STDIN_FILENO) + 1;

        if (select(nfds, &rfds, NULL, NULL, NULL) > 0) {
            if (FD_ISSET(master_fd, &rfds)) {
                nbytes = read(master_fd, buffer, sizeof(buffer) - 1);
                if (nbytes > 0) {
                    buffer[nbytes] = '\0';
                    printw("%s", buffer);
                    refresh();
                }
            }

            if (FD_ISSET(STDIN_FILENO, &rfds)) {
                nbytes = read(STDIN_FILENO, buffer, sizeof(buffer) - 1);
                if (nbytes > 0) {
                    buffer[nbytes] = '\0';
                    write(master_fd, buffer, nbytes);
                }
            }
        }
#endif
    }

    attroff(COLOR_PAIR(1)); // Turn off the color pair
    endwin(); // End ncurses mode

#ifdef _WIN32
    cleanup_windows_terminal();
#endif

    return 0;
}



